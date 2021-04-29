import logging
from pathlib import Path
from unittest.mock import patch

import pytest
from click.testing import CliRunner

from .conftest import (
    court_scraper_dir,
    file_contents,
    sites_csv_text
)

from court_scraper import cli
from court_scraper.case_info import CaseInfo


@pytest.mark.usefixtures('create_scraper_dir', 'create_config')
def test_scraper_caching(court_scraper_dir, monkeypatch):
    data = [
        CaseInfo({
            'number': '20A123',
            'status': 'Open',
            'page_source': '<html>foo</html>'
        })
    ]
    # Need to monkeypatch because Configs class is instantiated
    # in global scope of cli.py, and the import at top of this
    # test file executes cli.py before this test runs (therefore
    # standard patching doesn't work b/c it occurs too late)
    monkeypatch.setattr(cli.configs, 'cache_dir', court_scraper_dir)
    with patch('court_scraper.runner.Runner.search') as mock_method:
        mock_method.return_value = data
        runner = CliRunner()
        runner.invoke(cli.cli, [
            'search',
            '-p', 'ga_dekalb',
            '-s', '20A123'
        ])
        cache_file = Path(court_scraper_dir)\
            .joinpath('cache/ga_dekalb/20A123.html')
        expected = data[0].page_source
        actual = file_contents(cache_file)
        assert expected == actual


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
