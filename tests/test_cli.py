import json
import logging
from pathlib import Path
from unittest import mock
from unittest.mock import patch

import pytest
from click.testing import CliRunner

from .conftest import (
    court_scraper_dir,
    file_contents,
    sites_csv_text,
    update_test_configs
)

from court_scraper import cli
from court_scraper.cli import _get_runner
from court_scraper.platforms.odyssey.runner import Runner as OdysseyRunner
from court_scraper.case_info import CaseInfo


@pytest.mark.slow
@pytest.mark.webtest
@pytest.mark.usefixtures('set_env', 'create_scraper_dir', 'create_config')
def test_integration_wicourts(court_scraper_dir, config_path, headless):
    # Add captcha key to test config file
    from tests.conftest import CAPTCHA_API_KEY
    update_test_configs(config_path, {
        'captcha_service_api_key': CAPTCHA_API_KEY
    })
    # Run the test
    runner = CliRunner()
    args = [
        'search',
        '-p', 'wi_green_lake',
        '-c', '2021CV000055',
    ]
    if not headless:
        args.append('--with-browser')
    runner.invoke(cli.cli, args)
    cache_file = Path(court_scraper_dir)\
        .joinpath('cache/wi_green_lake/2021CV000055.json')
    with open(cache_file, 'r') as fh:
        data = json.load(fh)
    # Check for presence of some key data points
    assert data['caseNo'] == '2021CV000055'
    assert data['caseType'] == 'CV'
    assert data['countyName'] == "Green Lake"
    assert data['caption'] == "DISCOVER BANK c/o Discover Products Inc. vs. NOEL MCDOWELL"

@pytest.mark.vcr()
@pytest.mark.usefixtures('set_env', 'create_scraper_dir', 'create_config')
def test_integration_oscn(court_scraper_dir):
    # Using a non-login and non-Captcha site
    runner = CliRunner()
    runner.invoke(cli.cli, [
        'search',
        '-p', 'ok_tulsa',
        '-c', 'CJ-2021-2045'
    ])
    cache_file = Path(court_scraper_dir)\
        .joinpath('cache/ok_tulsa/CJ-2021-2045.html')
    contents = file_contents(cache_file)
    assert 'U S BANK NATIONAL ASSOCIATION' in contents

@pytest.mark.slow
@pytest.mark.webtest
@pytest.mark.usefixtures('set_env', 'create_scraper_dir', 'create_config')
def test_integration_odyssey(court_scraper_dir):
    # Using a non-login and non-Captcha site
    runner = CliRunner()
    runner.invoke(cli.cli, [
        'search',
        '-p', 'ca_napa',
        '-c', '20CV000402'
    ])
    cache_file = Path(court_scraper_dir)\
        .joinpath('cache/ca_napa/20CV000402.html')
    contents = file_contents(cache_file)
    assert 'Mary Faase et al' in contents

def test_list_scrapers(sites_csv_text):
    to_patch = 'court_scraper.cli.SitesMeta._get_sites_csv_text'
    with patch(to_patch) as mock_method:
        mock_method.return_value = sites_csv_text
        runner = CliRunner()
        response = runner.invoke(cli.cli, ['info'])
        expected = "\nAvailable scrapers:\n\n" +\
                " * CA - San Mateo (ca_san_mateo)\n" +\
                " * GA - Chatham (ga_chatham)\n" +\
                " * GA - Dekalb (ga_dekalb)\n" +\
                " * GA - Fulton (ga_fulton)\n\n" +\
                "NOTE: Scraper IDs (in parentheses) should be used with the " +\
                "search command's --place-id argument.\n"
        assert response.output == expected


def test_get_runner():
    runner_kls = _get_runner('ga_dekalb')
    expected = 'court_scraper.platforms.odyssey.runner'
    assert runner_kls.__module__ == expected
