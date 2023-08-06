import json


class GhTrackException(Exception):
    """
    This class contains all the possible exceptions that you can encounter during the execution of this project.
    """

    def __init__(self, status, data, headers):
        super().__init__()
        self.__status = status
        self.__data = data
        self.__headers = headers
        self.args = (status, data, headers)

    @property
    def status(self):
        """
        The status returned by the Github API
        """
        return self.__status

    @property
    def data(self):
        """
        The data returned by the Github API
        """
        return self.__data

    @property
    def headers(self):
        """
        The headers returned by the Github API
        """
        return self.__headers

    def __str__(self):
        return "{status} {data}".format(status=self.status, data=json.dumps(self.data))


class NotFoundException(GhTrackException):
    """
    NotFoundException is raised when Github API return 404  status
    """


class BadUserException(GhTrackException):
    """
    BadUserException is raised when request the user which repos you try to pull does not exist.
    """


class RateLimitExceededException(GhTrackException):
    """
    RateLimitExceededException is  raised when the rate limit is exceeded github replies with 403
    """


class RepoNotFoundException(GhTrackException):
    """
    RepoNotFoundException is raised when Github can not find the public repo
    """


class UnknownApiQueryException(GhTrackException):
    """
    UnknownApiQueryException is raised when Github can not find the public repo
    """
