# atl_cache_warmer
Little script to log in and warm up the cache of Jira or Confluence instances (just a basic http request)

## To Install
    pip install -U atl_cache_warmer
    
## To Use
### From the command line:
    > atlwarmer --help
    > usage: atlwarmer [-h] -u USERNAME -p PASSWORD [-j JIRA_URL] [-t JIRA_TARGET] [-c CONFLUENCE_URL] [-s SPACE] [-i]  [-v]

    >optional arguments:
      -h, --help         show this help message and exit
      -u USERNAME        username to use
      -p PASSWORD        password to use
      -j JIRA_URL        url for jira
      -t JIRA_TARGET     path in jira to make request to
      -c CONFLUENCE_URL  url for confluence
      -s SPACE           confluence space to make request to
      -i                 when used in combination with -s, will attempt to iterate through and request all pages in the target space. Jira support coming soon(TM)
      -v                 Increase verbosity level, can used up to 2 times
     
Note: to work from the command line you need to make sure that python-scripts is in your PATH 