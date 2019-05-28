from contextlib import ContextDecorator
import os
import json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP_SSL
from datetime import datetime
import socket
import getpass
from typing import List, Dict
import humanize
import time

class Notipy(ContextDecorator):
    def __init__(self, task:str, email:str, recipients:List[str]=None, port:int=465, server:str=None, send_start_mail:bool=False):
        """Create a new istance of Notipy.
            task:str, name of the current task you are tracking execution of.
            email:str, email from which to send the email.
            recipients:List[str]=None, list of mails to send it to. By default, only your own.
            port:int, the port through which send the email.
            server:str, the server of your email. By default extracted from the email.
            send_start_mail:bool, whetever to send a mail also when the script starts. By default False.
        """
        super(Notipy, self).__init__()
        self._task = task
        self._email = email
        self._recipients = [email] if recipients is None else recipients
        self._port = port
        self._server = "smtp.{server}".format(
            server=".".join(email.split("@")[1].split(".")[-2:])
        ) if server is None else server
        self._send_start_mail = send_start_mail
        self._password = getpass.getpass("Please insert your email password: ")
        
    def _notify(self, subject:str, txt_model:str, html_model:str):
        server_ssl = SMTP_SSL(self._server, self._port)
        server_ssl.login(self._email, self._password)
        msg = MIMEMultipart('alternative')
        msg["Subject"] = subject
        msg["To"] = ", ".join(self._recipients)
        msg["From"] = self._email
        msg.attach(MIMEText(self._build_model(txt_model), 'plain'))
        msg.attach(MIMEText(self._build_model(html_model), 'html'))
        server_ssl.sendmail(msg["From"], msg["To"], msg.as_string())
        server_ssl.close()

    @property
    def _pwd(self):
        return os.path.dirname(os.path.realpath(__file__))

    def _load_model(self, path:str):
        with open("{pwd}/models/{path}".format(pwd=self._pwd, path=path), "r") as f:
            return f.read()

    @property
    def _html_completion_model(self)->str:
        return self._load_model("completion.html")

    @property
    def _html_start_model(self)->str:
        return self._load_model("start.html")

    @property
    def _txt_completion_model(self)->str:
        return self._load_model("completion.txt")

    @property
    def _txt_start_model(self)->str:
        return self._load_model("start.txt")

    @property
    def _info(self)->Dict:
        return {
            "TASK_NAME":self._task,
            "SERVER_HOSTNAME":socket.gethostname(),
            "USERNAME":getpass.getuser(),
            "WORKING_PATH":os.getcwd(),
            "START_TIME":humanize.naturaldelta(time.time() - self._start),
            "COMPLETION_DATE":datetime.now().date(),
            "SENDER":self._email
        }

    def _build_model(self, model:str)->str:
        for key, value in self._info.items():
            model = model.replace(key, str(value))
        return model

    def __enter__(self):
        self._start = time.time()
        self._notify("Your task has started!", self._txt_start_model, self._html_start_model)
        return self

    def __exit__(self, *exc):
        self._notify("Your task has completed!", self._txt_completion_model, self._html_completion_model)
        return False