#!/usr/bin/env python

import json

from os.path import basename, join
from pathlib import Path
from typing import Any, cast, Dict, List, Optional, TypedDict, Union

import arrow
import click
import requests

from canvas_workflow_sdk.patient import Patient
from canvas_workflow_sdk.timeframe import Timeframe
from canvas_workflow_sdk.utils import parse_class_from_python_source

from stringcase import camelcase
from decouple import Config, RepositoryIni

mocks_path = 'TODO'


# Utility methods -----------
#
def green(string: str) -> str:
    return click.style(string, fg='green')


def red(string: str) -> str:
    return click.style(string, fg='red')


def get_settings_path() -> Path:
    return Path.home() / '.canvas' / 'config.ini'


# Settings ---------------
#
def read_settings(ctx) -> Dict[str, Any]:

    try:
        ini = RepositoryIni(get_settings_path())
    except FileNotFoundError:
        raise click.ClickException(
            f'Please add your configuration at "{get_settings_path()}"; you can set '
            'defaults using `canvas-cli create-default-settings`.')

    if not ini.parser.has_section(ctx.obj['config_section']):
        raise click.ClickException(
            f'Settings file "{get_settings_path()}" does not contain section "{ctx.obj["config_section"]}"; '
            'you can set defaults using `canvas-cli create-default-settings`.')

    ini.SECTION = ctx.obj['config_section']
    config = Config(ini)

    settings: Dict[str, Any] = {
        'url': config('url', cast=str),
        'api_key': config('api-key', cast=str)
    }

    return settings


class PatientData(TypedDict):
    billingLineItems: List
    conditions: List
    imagingReports: List
    immunizations: List
    instructions: List
    interviews: List
    labReports: List
    medications: List
    referralReports: List
    vitalSigns: List
    patient: Dict[str, Any]
    protocolOverrides: List
    changeTypes: List
    protocols: List


def load_patient(fixture_folder: Path) -> Patient:
    data: PatientData = {
        'billingLineItems': [],
        'conditions': [],
        'imagingReports': [],
        'immunizations': [],
        'instructions': [],
        'interviews': [],
        'labReports': [],
        'medications': [],
        'referralReports': [],
        'referrals': [],
        'vitalSigns': [],
        'patient': {},
        'protocolOverrides': [],
        'changeTypes': [],
        'protocols': [],
    }

    file_loaded = False

    for filepath in fixture_folder.glob('*.json'):
        file_loaded = True

        filename = str(basename(filepath))
        field = camelcase(filename.split('.')[0])

        with open(filepath, 'r') as file:
            if field not in data:
                raise click.ClickException(
                    f'Found file that does not match a known field: "{field}"')

            data[field] = json.load(file)  # type: ignore

    if not file_loaded:
        raise click.ClickException(f'No JSON files were found in "{fixture_folder}"')

    data['patient']['key'] = fixture_folder.name

    # click.echo(json.dumps(data, indent=2))

    return Patient(data)


# def load_patient_data(patient_key: str, field: str) -> List:
#     """
#     Load data from mock data JSON files dumped by the dump_patient command.
#     """
#     filename = f'{mocks_path}/{patient_key}/{field}.json'

#     if not exists(filename):
#         if field == 'patient':
#             raise Exception(f'Missing mock patient data for "{patient_key}"!')

#         return []

#     with open(filename, 'r') as file:
#         return json.load(file)  # type: ignore


# CLI Commands -----------------------------------

@click.group()
@click.pass_context
@click.option('--use-config', required=False)
def cli(ctx, use_config='canvas_cli'):

    ctx.ensure_object(dict)
    ctx.obj['config_section'] = use_config and use_config or 'canvas_cli'

    if ctx.invoked_subcommand != 'create-default-settings':
        ctx.obj['settings'] = read_settings(ctx)


@cli.command()
def create_default_settings():
    """
    Create a default settings file with placeholder text in `~/.canvas/config.ini`.
    File will only be created if it does not yet exist.
    """

    settings_path = get_settings_path()

    if settings_path.is_file():
        raise click.ClickException(f'Settings file already exists at {settings_path}')

    settings_path.parent.mkdir(parents=True, exist_ok=True)

    click.echo(f'Writing default settings to "{settings_path}"...')

    settings_path.write_text('''[canvas_cli]
url =
api-key =
''')


@cli.command()
@click.argument('patient-key')
@click.argument('output_directory', nargs=1, required=False, type=click.Path())
@click.pass_context
def fixture_from_patient(ctx, patient_key: str, output_directory: Path):
    """
    Export a fixture for a given patient.  Providing an
    output directory will create a json file for each key.
    Eg: billingLineItems.json, conditions.json, referralReports.json ...
    """
    click.echo(f'Getting fixture from patient "{patient_key}"...')

    response = requests.get(join(
        ctx.obj["settings"]["url"], f'api/PatientProtocolInput/{patient_key}'
    ), headers={'Authorization': ctx.obj['settings']['api_key']})
    response.raise_for_status()
    response_json = response.json()

    if not output_directory:
        click.echo(response_json)
    else:
        output_directory = Path(output_directory)
        output_directory.mkdir(parents=True, exist_ok=True)
        for key, values in response_json.items():
            (output_directory / f'{key}.json').write_text(json.dumps(values))
        click.echo(green(f'Successfully wrote patient fixture to {output_directory.absolute()}'))


@cli.command()
@click.argument('module-path')
@click.argument('fixture-folder')
@click.option('--date')
@click.option('--start-date')
@click.option('--end-date')
def test_fixture(module_path: str, fixture_folder: str, date: str = None, start_date: str = None, end_date: str = None):
    """
    Test a python file with a ClinicalQualityMeasure against a fixture folder.
    """

    Class = parse_class_from_python_source(Path(module_path).open('r').read())

    # 2. load JSON folder of fixture data
    patient = load_patient(Path(fixture_folder))

    if date:
        date = arrow.get(date)
    else:
        date = arrow.get('2018-08-23 13:24:56')

    if start_date:
        start_date = arrow.get(start_date)
    else:
        start_date = arrow.get('2017-10-23 13:24:56')

    if end_date:
        start_date = arrow.get(start_date)
    else:
        end_date = arrow.get('2018-08-23 13:24:56')

    timeframe = Timeframe(start=start_date, end=end_date)

    # 3. instantiate module
    protocol = Class(patient=patient, date=date, timeframe=timeframe)
    results = protocol.compute_results()

    # 4. return results
    results.recommendations = [vars(r) for r in results.recommendations]
    click.echo(json.dumps(vars(results), indent=2))


@cli.command()
@click.argument('filename', type=click.Path(exists=True))
@click.pass_context
def upload(ctx, filename: Path):
    """
    Upload a ClinicalQualityMeasure to the server
    """

    if not filename.endswith('.py'):
        raise click.ClickException(f'Only python files with a .py extension can be uploaded.')

    filename_path = Path(filename)

    click.echo(f'Uploading {filename_path.name}...')

    with filename_path.open() as f:
        contents = f.read()

    files = {'file': filename_path.open('rb')}

    response = requests.post(join(
        ctx.obj["settings"]["url"], f'api/PatientProtocol/upload/'
    ), files=files, headers={
        'Authorization': ctx.obj['settings']['api_key'],
        'Content-Length': str(len(contents)),
        'Content-Disposition': f'attachment; filename="{filename_path.name}"'
    })

    if response.status_code == 201 and response.json().get('status') == 'success':
        version = response.json().get('data', {}).get('version')
        version_str = ''
        if version:
            version_str = f'Version {version}'
        click.echo(green(f'Upload successful.  {version_str} set to latest version.'))
    else:
        raise click.ClickException(response.text)


@cli.command()
@click.argument('module-name')
def set_active(module_name: str):
    """
    Set a protocol to active on the server
    """
    click.echo(f'Setting {module_name} as active...')
    _set_active(True, module_name)


@cli.command()
@click.argument('module-name')
def set_inactive(module_name: str):
    """
    Set a protocol to inactive on the server
    """
    click.echo(f'Setting {module_name}" as inactive...')
    _set_active(False, module_name)


@click.pass_context
def _set_active(ctx, is_active: bool, module_name: str):
    response = requests.post(join(
        ctx.obj["settings"]["url"], f'api/PatientProtocol/set_active/'
    ), data={
        'is_active': is_active and 1 or 0,
        'module_name': module_name,
    }, headers={
        'Authorization': ctx.obj['settings']['api_key'],
    })
    if response.status_code == 200:
        click.echo(green(response.json().get('data', {}).get('detail')))
    else:
        raise click.ClickException(response.text)


@cli.command()
@click.argument('module-name')
@click.pass_context
def list_versions(ctx, module_name: str):
    """
    List the available versions on the server.
    """
    response = requests.get(join(
        ctx.obj["settings"]["url"], f'api/PatientProtocol/version/{module_name}/'
    ), headers={
        'Authorization': ctx.obj['settings']['api_key'],
    })

    if response.status_code == 200:
        is_active = response.json().get('is_active')
        active_version = response.json().get('active_version')

        color_method = green if is_active else red

        click.echo("Is Active: " + color_method(is_active))
        click.echo("Active version: " + green(active_version))
        click.echo("Versions: ")

        for version in response.json().get('versions', []):
            version_number = version.get('version')
            def color_method(x): return x
            if version_number == active_version:
                color_method = green

            click.echo(color_method(f' {version_number}: {version.get("changelog")}'))

    else:
        raise click.ClickException(response.text)


@cli.command()
@click.argument('module-name')
@click.argument('version')
@click.pass_context
def set_version(ctx, module_name: str, version: str):
    """
    Set a protocol's active version on the server.
    The protocol upload may still need to be made active after changing the version.
    """
    response = requests.post(join(
        ctx.obj["settings"]["url"], f'api/PatientProtocol/version/{module_name}/'
    ), data={
        'version': version,
    }, headers={
        'Authorization': ctx.obj['settings']['api_key'],
    })
    if response.status_code == 200:
        click.echo(green(response.json().get('data', {}).get('detail')))
    else:
        raise click.ClickException(response.text)


if __name__ == '__main__':
    cli()
