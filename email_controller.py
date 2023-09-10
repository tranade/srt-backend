import os

import yagmail


class EmailController:
    def __init__(self):
        self.yag = yagmail.SMTP(os.getenv("EMAIL_ADDRESS"), os.getenv("EMAIL_PASSWORD"))
        self.email = os.getenv("EMAIL_ADDRESS")

    def send_error(self, contents=None):
        """
        Sends an email to myself
        """
        self.yag.send(subject='Error with SRT Backend Application', contents=contents)

    def send_results_to_user(self, file_paths: list[str], user_email: str, user_name: str):
        """
        Sends an email to the user with a bcc to myself

        :param file_paths: the paths of the files to attach to the email
        :param user_email: the email of the user to send the email to
        :param user_name: the name of the user to send the email to
        """
        text = f'Hello {user_name},\n\n' \
               f'Your SRT procedure has been completed. We have attached the ' \
               f'results of your procedure to this email.\n\n' \
               f'Best,\n' \
               f'The SRT Team @ JHU'

        contents = [text, *file_paths]

        self.yag.send(to=user_email, bcc=self.email, subject='Small Radio Telescope Results', contents=contents)
