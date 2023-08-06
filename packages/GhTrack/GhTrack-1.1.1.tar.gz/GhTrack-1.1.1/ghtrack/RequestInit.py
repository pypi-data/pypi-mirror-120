import json
import logging
from urllib import parse
import requests

from ghtrack.GhTrackException import UnknownApiQueryException
from ghtrack.Util import Util


class RequestInit:
    """This class initialize the requests object with default and required values"""

    def __init__(self, token, apiUrl="https://api.github.com/repos/"):
        """Constructor.
            token of github for unlimited queries if not provided you can not query more than 60 times
            apiUrl the base api url
            :param token: Personal github token .
            :param apiUrl: The base api url.
        """
        self.__tokenHeader = {
            "Accept": "application/vnd.github.v3+json"
        }
        if token:
            self.__tokenHeader["Authorization"] = f"token {token}"
        self.__apiUrl = apiUrl

    """
    This method return the api data in json format for all data not older than the provided param
    :param url: str the :owner/:repo_name
    :param parameters: str not recommended for now
    :param body: str not recommended for now
    :param old: int determines how old the data should be
    :rtype: :tuple:
    """
    def dataRequest(self, url, parameters=None, body="", old: int = 7):
        if parameters is None:
            parameters = dict()

        headers, output = self.__statusCheckedRequest(url, parameters, body)
        # output = [row for row in output if Util.oneWeekOld(row["created_at"], old)]
        # output = list(filter(lambda row: Util.oneWeekOld(row["created_at"], old), dict(output)))

        # page = 2
        # while "link" in headers and "next" in headers["link"]:
        #     parameters["page"] = page
        #     headers, newOutput = self.__statusCheckedRequest(url, parameters, body)
        #     output += newOutput
        #     page += 1

        return output

    """
    This method check the status of request, you can determine if the repo exists.
    :param url: str the :owner/:repo_name
    :param parameters: str not recommended for now
    :param input: str not recommended for now
    :rtype: :int:
    """
    def __statusCheckedRequest(self, url, parameters, input):
        status, headers, output = self.__jsonRequest(url, parameters, input)
        if status < 200 or status >= 300:
            raise UnknownApiQueryException(status, output, headers)
        return headers, output

    """
    This method check the status of request, you can determine if the repo exists.
    :param url: str the :owner/:repo_name
    :param parameters: str not recommended for now
    :param input: str not recommended for now
    :rtype: :int:
    """
    def statusRequest(self, url, parameters, input):
        status, headers, output = self.__jsonRequest(url, parameters, input)
        return status

    """
    This method return the api data in json format
    :param url: str the :owner/:repo_name
    :param parameters: str not recommended for now
    :param input: str not recommended for now
    :rtype: :tuple:
    """
    def __jsonRequest(self, url, parameters, input) -> tuple:
        fullUrl = self.getCompleteUrl(url, parameters)
        try:
            response = requests.get(
                url=fullUrl,
                headers=self.__tokenHeader
            )
            status = response.status_code
            headers = dict(response.headers)
            output = response.json()
            return status, headers, output
        except Exception as ex:
            logging.info(f"Exception during json conversion {ex}")
            return 200, dict(), []



    """
    This method give you the absolute url of the public repo you are querying on
    :param url: str the :owner/:repo_name
    :param parameters: str not recommended for now
    :rtype: :str:
    """
    def getCompleteUrl(self, url, parameters=None):
        if parameters is None or len(parameters) == 0:
            return f"{self.__apiUrl}{url}"
        else:
            return url + "?" + parse.urlencode(parameters)

    """
    In case if you have passed an github token, this method will return the value of the token
    :rtype: :class:`str`
    """
    def getToken(self):
        return self.__tokenHeader


