import logging
from pathlib import Path
from unittest.mock import patch

import pytest
from click.testing import CliRunner

from .conftest import (
    court_scraper_dir,
    file_contents
)

from court_scraper.case_info import CaseInfo
from court_scraper.cli import cli


@pytest.mark.usefixtures('create_scraper_dir', 'create_config')
def test_scraper_caching(court_scraper_dir):
    data = [
        CaseInfo({
            'number': '20A123',
            'status': 'Open',
            'page_source': '<html>foo</html>'
        })
    ]
    to_patch = 'court_scraper.runner.Runner.search'
    with patch(to_patch) as mock_method:
        mock_method.return_value = data
        runner = CliRunner()
        runner.invoke(cli, [
            '-p', 'ga_dekalb',
            '-s', '20A123'
        ])
        cache_file = Path(court_scraper_dir)\
            .joinpath('cache/ga_dekalb/20A123.html')
        expected = data[0].page_source
        actual = file_contents(cache_file)
        assert expected == actual

