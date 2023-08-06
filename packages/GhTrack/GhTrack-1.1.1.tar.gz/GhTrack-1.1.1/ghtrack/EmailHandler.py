import logging

from ghtrack.GhTrackObject import EmailConf, GhTrackObject
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


class EmailHandler(GhTrackObject):
    """EmailHandler is use to send email through twilio."""

    def __repr__(self):
        return f"to={self.emailConf.to}, from={self.emailConf.fromEmail}, subject={self.emailConf.subject}"

    """
    This method send email to an configurable email
    :param content: str
    :rtype: :tuple
    """
    def sendEmail(self, content: str) -> tuple:
        # try:
        message = Mail(
            from_email=self.emailConf.fromEmail,
            to_emails=self.emailConf.to,
            subject=self.emailConf.subject,
            html_content=content)

        sg = SendGridAPIClient(api_key=self.emailConf.sendGridApi)
        response = sg.send(message)
        return response.status_code, response.body, response.headers
        # except Exception as ex:
        #     logging.info(f"Api key = {self.sendGridApi}")
        #     logging.info(f"exception = {ex}")

