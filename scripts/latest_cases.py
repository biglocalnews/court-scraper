"""Download the latest cases with scrapers that support `search_by_date`."""
import json
from datetime import datetime, timedelta
from pathlib import Path

from court_scraper import utils
from court_scraper.configs import Configs
from court_scraper.platforms.oscn.site import DAILY_FILING_COUNTIES
from court_scraper.sites_meta import SitesMeta


def main():
    """Download the latest cases with scrapers that support `search_by_date`."""
    # Get the date range we want to scrape
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)

    # Configure where we'll work
    configs = Configs()
    cache_dir = Path(configs.cache_dir)
    cache_dir.mkdir(parents=True, exist_ok=True)

    # Get a list of all the sites that qualify
    wi_list = [s["place_id"] for s in SitesMeta().get_state_list("wi")]
    ok_list = DAILY_FILING_COUNTIES
    qualified_sites = wi_list + ok_list

    # Create a master list for all cases
    case_list = []

    # Loop through all the qualified sites
    for place_id in qualified_sites:
        print(f"Scraping {place_id}")

        # Get the runner
        runner_klass = utils.get_runner(place_id)
        runner = runner_klass(configs.cache_dir, configs.config_file_path, place_id)

        # Run it
        results = runner.search_by_date(
            start_date=start_date.strftime("%Y-%m-%d"),
            end_date=end_date.strftime("%Y-%m-%d"),
        )
        print(f"- {len(results)} records found")

        # Tidy up the results
        for o in results:
            d = o.__dict__
            d["place_id"] = place_id
            # Adding them to the master list
            case_list.append(d)

    # Write out the results
    print(f"Writing out {len(case_list)} cases")
    with open("./cases.json", "w") as fp:
        json.dump(case_list, fp, indent=2)


if __name__ == "__main__":
    main()
