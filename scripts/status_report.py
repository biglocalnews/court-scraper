"""Generate a report on the project."""
from court_scraper import utils
from court_scraper.sites_meta import SitesMeta


def main():
    """Print a status report."""
    # Add all the sites
    meta = SitesMeta()
    state_list = []
    place_list = []
    site_list = []
    has_search_list = []
    for state, county in meta.data.keys():
        if state not in state_list:
            state_list.append(state)
        place_id = f"{state}_{county.replace(' ', '_')}"
        if place_id not in place_list:
            place_list.append(place_id)
        data = meta.data[(state, county)]
        site = utils.get_site_class(place_id, data["site_type"])
        site_list.append(site)
        has_date_search = hasattr(site, "search_by_date")
        if has_date_search:
            has_search_list.append(place_id)
    print(f"State count: {len(state_list)}")
    print(f"Place list: {len(place_list)}")
    print(f"{len(has_search_list)}/{len(site_list)} have a date search")


if __name__ == "__main__":
    main()
