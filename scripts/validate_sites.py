"""
 TITLE: validate_sites.py
 AUTHOR: Amy DiPierro
 VERSION: 2020-09-08

 DESCRIPTION:

 Given a csv of potential Tyler Technologies Odyssey endpoints, find out if there is a valid
 search portal for each endpoint. Add each valid endpoint and associated metadata to a csv.

 NOTE: Avoid overwriting previous versions of the csv produced by this file, since it is
 necessary to hand-key some values after running this script.

 USAGE: From the command line,

     python validate_sites.py \
     "/Users/amydipierro/Downloads/court_sites_raw.csv" \
     "/Users/amydipierro/GitHub/court_sites.csv"

 """
import csv

import bs4
import requests


# Code
def read_csv(file_in):
    """
    :param file_in: csv with possible Tyler Technologies endpoints
    :return: list with possible Tyler Technologies endpoints
    """
    raw_list = []

    with open(file_in) as f:
        for line in f:
            raw_url = line.strip().strip(",")
            if raw_url not in raw_list:
                raw_list.append(raw_url)

    # Take out the header from the list
    raw_list.pop(0)

    return raw_list


def validate(raw_list):
    """
    Validates whether a url in raw_list is an endpoint we might want to scrape

    :param raw_list:
    :return: list of dictionaries containing valid endpoints to scrape with metadata
    """
    final_list = []

    for url in raw_list:
        print("base url: ", url)
        portal_one, valid = try_site(url, "https://{}/Portal", 1)
        if portal_one != {}:
            final_list.append(portal_one)
        if not valid:
            portal_two, valid = try_site(url, "https://{}/PublicAccess/default.aspx", 2)
            if portal_two != {}:
                final_list.append(portal_two)
            if not valid:
                portal_three, valid = try_site(url, "https://{}/default.aspx", 2)
                if portal_three != {}:
                    final_list.append(portal_three)
                if not valid:
                    if "odyprod" in url:
                        url = url.replace("odyprod", "portal")
                        portal_four, valid = try_site(url, "https://{}/Portal", 1)
                        if portal_four != {}:
                            final_list.append(portal_four)
                        if not valid:
                            print("Could not find valid url for ", url)

    return final_list


def try_site(url, url_format, site_type):
    """
    Helper function. Pings each potential endpoint and attempts to collect metadata.

    :param url: str. Base url to try to reach
    :param url_format: str. Reformated URL
    :param site_type: int. Type of Odyssey platform
    :return: site_dict: dict. Metadata associated with each endpoint
            valid: bool. Flag indicating whether this url_format was valid

    """

    # Initialize parameters
    valid = False
    response = None
    format_url = url_format.format(url)

    # Try to reach the site
    print("trying ", format_url)
    response = requests.get(format_url)

    # Try to extract metadata
    if response is not None and response.status_code == 200:
        print(format_url, " 200 response!")
        title, raw_text = get_metadata(format_url, response)
        site_dict = {
            "state": None,
            "county": None,
            "title": title,
            "site_type": "odyssey_site",
            "site_version": site_type,
            "captcha_service_required": None,
            "home_url": format_url,
            "raw_text": raw_text,
        }
        valid = True
    else:
        site_dict = {}

    # Return metadata, if any
    return site_dict, valid


def get_metadata(url, response):
    """
    Helper function. Grabs metadata for each potential endpoint, if possible.

    :param url: str. Potential endpoint to scrape.
    :param response: str. Parsed HTML.
    :return title: str. Title of page.
    :return raw_text: str. Notable text on page.
    """
    soup = bs4.BeautifulSoup(response.text, "html.parser")

    # Get page title
    if (
        "/default.aspx" in url
        and soup.table is not None
        and soup.table.td is not None
        and soup.table.td.td is not None
    ):
        title = soup.table.td.td.text.strip()
    else:
        if soup.title is not None:
            title = soup.title.text.strip()
        else:
            title = None

    # Get page description
    notifications = soup.find(text="Notifications")
    if notifications is not None:
        raw_text = notifications.find_next().text
    else:
        raw_text = title

    return title, raw_text


def write_csv(clean_dict, file_out):
    """

    :param clean_dict: List of dictionaries containing metadata for each validated
                        Tyler Technologies endpoint
            file_out: Path to csv of validated endpoints with metadata
    :return: None
    :output: csv of validated endpoints with metadata
    """
    fieldnames = [
        "state",
        "county",
        "title",
        "site_type",
        "site_version",
        "captcha_service_required",
        "home_url",
        "raw_text",
    ]

    with open(file_out, "w", newline="") as out_file:
        writer = csv.DictWriter(out_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(clean_dict)


if __name__ == "__main__":
    """
    Call generate_site_csv from the command line.
    """

    import argparse

    # Set up parser
    parser = argparse.ArgumentParser()
    parser.add_argument("file_in", type=str)
    parser.add_argument(
        "file_out",
        type=str,
    )

    args = parser.parse_args()

    # Call functions
    url_list = read_csv(file_in=args.file_in)
    checked = validate(url_list)
    print(checked)
    write_csv(checked, file_out=args.file_out)
