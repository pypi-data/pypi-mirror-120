import os
from dataclasses import dataclass
import yaml

import logging as log

@dataclass
class Auth:
    """Auth class.
        Github token configurations.
    """
    token: str = ""


@dataclass
class EmailConf:
    """EmailConf class.
        Email configurations.
    """
    to: str = "zinalacina@gmail.com"
    subject: str = "Pull request Test"
    sendGridApi: str = ""
    fromEmail: str = "zlacina@gmail.com"


@dataclass
class Repo:
    """Repo class.
        Public repo setting.
    """
    user: str = "kubernetes"
    repo: str = "kubernetes"


@dataclass
class GhTrackObject:
    """GhTrackObject class.
        Contents the configuration information coming from data/config.yml and also default value.
    """
    filename: str = None
    emailConf: EmailConf = EmailConf()
    repoConf: Repo = Repo()
    authToken: Auth = Auth()

    def __post_init__(self):
        self.emailConf, self.repoConf, self.authToken = self.getConf(self.filename)

    def getConf(self, file_name: str) -> (EmailConf, Repo, Auth):
        if not file_name:
            file_name = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data/config.yml")
        else:
            file_name = os.path.abspath(file_name)
        try:
            with open(file_name) as f:
                setting = yaml.safe_load(f)["settings"]
                token = Auth(setting["github"]["token"])
                email = EmailConf(to=setting["email"]["to"],
                                  subject=setting["email"]["subject"],
                                  sendGridApi=setting["email"]["sendGridApi"],
                                  fromEmail=setting["email"]["from"])
                repo = Repo(user=setting["repo"]["user"], repo=setting["repo"]["name"])
                return email, repo, token
        except Exception as ex:
            log.info(f"impossible to open file {file_name}, ex={ex}")
            return EmailConf(), Repo(), Auth()


