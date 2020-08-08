import argparse
import json
import os
from pathlib import Path


DEFAULT_CACHE=str(Path(os.getcwd()).joinpath('data'))
DEFAULT_CONFIG=str(Path(os.getcwd()).joinpath('config.json'))


from court_scraper.platforms.odyssey import OdysseySite


def main():
    parser = argparse.ArgumentParser(description="Scrape data from various court systems.")
    parser.add_argument(
        '--config',
        default=DEFAULT_CONFIG,
        help='Path to configuration file.',
    )
    args = vars(parser.parse_args())
    with open(args['config'], 'r') as fh:
        configs = json.load(fh)
    username = configs['username']
    password = configs['password']
    download_dir = configs['download_dir']
    logfile_path = configs['logfile']
    #base_url = "https://publicrecordsaccess.fultoncountyga.gov/Portal/Home/Dashboard/29"
    url = "https://publicrecordsaccess.fultoncountyga.gov/Portal/Home/Dashboard/29"
    search_terms = ['Smith', 'foobar']
    scraper = OdysseySite(
        url,
        username,
        password,
        download_dir,
    )
    scraper.search(search_terms, headless=False)

def cases_to_scrape():
    #Fulton case numbers in 2019 range from 19ED105358 to 19ED150619 -- this includes Jan 1 2020
    #Fulton case numbers in 2020 range from 20ED150670 to 20ED163368 -- this starts at Jan 2 2020, ends June 23
    #final number in range is 1 higher than it should be ON PURPOSE
    case_numbers = []
    for num in range(150670, 163368):
        prefix = '20ed'
        suffix = str(num)
        #if num < 10:
            #extra = '000'
            #case_number = (prefix + extra + suffix)
        #elif num < 100:
            #extra = '00'
            #case_number = (prefix + extra + suffix)
        #elif num < 1000:
            #extra = '0'
            #case_number = (prefix + extra + suffix)
        #else:
        case_number = (prefix + suffix)
        case_numbers.append(case_number)
    return case_numbers

if __name__ == '__main__':
    main()


