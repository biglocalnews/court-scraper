"""Download the latest cases with scrapers that support `search_by_date`."""
from datetime import datetime, timedelta
from pathlib import Path

from court_scraper import utils
from court_scraper.configs import Configs


def main():
    """Run the routine."""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)

    configs = Configs()
    cache_dir = Path(configs.cache_dir)
    cache_dir.mkdir(parents=True, exist_ok=True)

    place_id = "ok_oklahoma"
    runner_klass = utils.get_runner(place_id)
    runner = runner_klass(configs.cache_dir, configs.config_file_path, place_id)

    print(f"Scraping {place_id}")
    results = runner.search_by_date(
        start_date=start_date.strftime("%Y-%m-%d"),
        end_date=end_date.strftime("%Y-%m-%d"),
    )
    print(f"- {len(results)} records found")


if __name__ == "__main__":
    main()
