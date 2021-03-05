# Discovering court websites

 Author: Amy DiPierro
 Version: 2020-09-08

 This file describes further resources for finding other court websites, with an emphasis on Tyler Technologies' Odyssey sites.

 ## Finding Odyssey subdomains

 ### Strategy 1: nmmapper.com

 * This [subdomain finder](https://www.nmmapper.com/sys/tools/subdomainfinder/) is the best tool I've found to search for subdomains.
 * Since Odyssey websites don't always have a predictable subdomain, it will be good ot continue to search for new subdomains as we come across them.
 * Here are some searches to run:
   * tylerhost.net/
   * tylerhost.net/Portal/

 ### Strategy 2: Google Custom Search API

 * We can use Google's Custom Search API to run targetted searches that surface websites built with Odyssey. I've not run this yet but it might be worth it.
 * Some suggested searches that turn up promising results:
   * court portal "© 2020 Tyler Technologies, Inc." -site:tylertech.com -iTax -stock -taxes

 ## Existing efforts to scrape court data

 * The [**Police Data Accessibility Project**](https://www.wired.com/story/police-accountability-data-project-open-source-reddit/), an open data initiative started on Reddit this summer, has already compiled some basic databases of court websites upon which we can build:
   * The group's [Public Access to Court Records State Links.csv](https://docs.google.com/spreadsheets/d/1nD4LnjU1b1b9RgQNcn6op-Oj3ZQVcgz-2bUgEU5RVXA/edit#gid=0) GoogleSheet contains a partial list of court websites with the names of vendors sometimes noted.
   * It might be worth glancing at their [GitHub](https://github.com/Police-Data-Accessibility-Project/Police-Data-Accessibility-Project) and Slack channel from time to time to see if there are opportunities to learn from their research and code.

 * The [**Tubman Project**](https://www.tubmanproject.com), a nonprofit that is trying to build software to "make legal defense available to the masses", has also compiled some data on Tyler Technologies platforms [in this thread](https://github.com/TubmanProject/data_scraper/issues/10).
