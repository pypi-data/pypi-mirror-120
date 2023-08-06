import logging

import requests


class JiraSite(object):
    def __init__(self, jira_url: str, jira_username: str, jira_password: str, jira_destination: list = None,
                 iterate: bool = False, additional_urls: list = None):
        self.additional_urls = additional_urls
        self.jira_destination: list = jira_destination
        self.jira_url = jira_url.rstrip('/')
        self.jira_username = jira_username
        self.jira_password = jira_password
        self.session = requests.session()

        # TODO: implement project iteration
        self.iterate_project = iterate

        try:
            self.login()
        except Exception as ex:
            logging.error(ex)


    def run(self):
        if self.jira_destination is not None:
            for d in self.jira_destination:
                self.session.request(method="GET", url=f'{self.jira_url}/{d}')
        if self.iterate_project:
            print("Not implemented yet.  Sorry!")
        if self.additional_urls is not None:
            for u in self.additional_urls:
                try:
                    logging.debug(f"starting request for additional url {u}")
                    response = self.session.request(method="GET",
                                                    url=u,
                                                    cookies=self.session.cookies)
                    logging.debug(response.text.encode('utf8'))
                except Exception as ex:
                    logging.exception(ex)

    def login(self):
        url = f"{self.jira_url}/login.jsp"
        logging.info(f"attempting login to Jira using url: {url} ")

        payload = f'atl_token=&login=Log%20In&os_destination={self.jira_destination}&os_password={self.jira_password}&os_username={self.jira_username}&user_role='
        headers = {
            'Origin': f'{self.jira_url}',
            'Upgrade-Insecure-Requests': '1',
            'DNT': '1',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
            'Sec-Fetch-User': '?1',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
        }

        response = self.session.request("POST", url, headers=headers, data=payload)
        logging.debug(response.text.encode('utf8'))

