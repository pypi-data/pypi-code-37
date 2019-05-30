from contextlib import ContextDecorator
import os
import json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP_SSL
from datetime import datetime
import socket
import getpass
from typing import List, Dict, Callable, Tuple
import humanize
import time
import pandas as pd
from validate_email import validate_email
from validators import domain
from environments_utils import is_stdout_enabled
from tabulate import tabulate
import sys

class Notipy(ContextDecorator):
    _config_path = ".notipy.json"

    def __init__(self):
        """Create a new istance of Notipy."""
        super(Notipy, self).__init__()
        self._enabled = is_stdout_enabled()
        if self._enabled:
            self._load_cache()
            print("Let's setup your notipy!")
            print("Hit enter to use the default values.")
            self._config["email"] = self._get("email", self._validate_email)
            self._password = getpass.getpass("Password: ")
            self._config["task_name"] = self._get("task_name")
            if "recipients" not in self._config:
                self._config["recipients"] = self._config["email"]
            self._config["recipients"] = self._get(
                "recipients",
                validator=self._validate_emails,
                comment=", separated by a comma")
            if "report_timeout" not in self._config:
                self._config["report_timeout"] = 24
            self._config["report_timeout"] = int(self._get(
                "report_timeout",
                validator=self._positive_int,
                comment=", in hours"))
            if "port" not in self._config:
                self._config["port"] = 465
            self._config["port"] = int(self._get(
                "port",
                validator=self._positive_int))
            if "smtp_server" not in self._config:
                self._config["smtp_server"] = "smtp.{server}".format(server=".".join(
                    self._config["email"].split("@")[1].split(".")[-2:])
                )
            self._config["smtp_server"] = self._get(
                "smtp_server",
                validator=self._validate_server)
            self._store_cache()
            self._report = None

    def _get(self, parameter: str, validator: Callable = None, comment: str = "", default: str = ""):
        default = " [{parameter}]".format(
            parameter=self._config[parameter]
        ) if parameter in self._config else ""
        while True:
            user_input = input("Please insert {parameter}{comment}{default}: ".format(
                default=default,
                parameter=parameter,
                comment=comment)).strip()
            if not user_input and default and (validator is None or validator(self._config[parameter])):
                return self._config[parameter]
            if validator is None or validator(user_input):
                return user_input
            print("The given {parameter} '{user_input}' is not valid.".format(
                parameter=parameter, user_input=user_input))

    def _validate_email(self, email:str):
        return not email.endswith("gmail.com") and validate_email(email)        

    def _validate_emails(self, emails: str):
        return all([
            validate_email(email) for email in emails.split(",")
        ])

    def _validate_server(self, server: str):
        return domain(server) and self._is_server_reacheable(server)

    def _is_server_reacheable(self, server: str)->bool:
        try:
            socket.gethostbyname(server)
            return True
        except socket.gaierror:
            return False

    def _positive_int(self, value: str):
        return int(value) > 0

    def _load_cache(self):
        if os.path.exists(self._config_path):
            with open(self._config_path, "r") as f:
                self._config = json.load(f)
        else:
            self._config = {}

    def _store_cache(self):
        with open(self._config_path, "w") as f:
            json.dump(self._config, f, indent=4)

    def _notify(self, subject: str, txt: str, html: str):
        server_ssl = SMTP_SSL(
            self._config["smtp_server"], self._config["port"])
        server_ssl.login(self._config["email"], self._password)
        msg = MIMEMultipart('alternative')
        msg["Subject"] = subject
        msg["To"] = self._config["recipients"]
        msg["From"] = self._config["email"]
        msg.attach(MIMEText(txt, 'plain'))
        msg.attach(MIMEText(html, 'html'))
        server_ssl.sendmail(msg["From"], msg["To"], msg.as_string())
        server_ssl.close()

    @property
    def _pwd(self):
        return os.path.dirname(os.path.realpath(__file__))

    def _load_model(self, name: str, ext: str):
        with open("{pwd}/models/{name}.{ext}".format(pwd=self._pwd, name=name, ext=ext), "r") as f:
            return f.read()

    def _json(self, name: str, ext: str)->Dict:
        common = json.loads(self._load_model("common", "json"))
        generic = json.loads(self._load_model(name, "json"))
        extension = json.loads(self._load_model(ext, "json"))
        return {**common, **generic, **extension}

    def _start(self):
        subject, txt, html = self._build_models("start")
        self._notify(subject, txt, html)

    def _completed(self):
        subject, txt, html = self._build_models("completed")
        self._notify(subject, txt, html)

    def _send_report(self):
        subject, txt, html = self._build_models("report")
        self._notify(subject, txt, html)

    def _info(self)->Dict:
        return {
            "hostname": socket.gethostname(),
            "username": getpass.getuser(),
            "pwd": os.getcwd(),
            "elapsed": humanize.naturaldelta(time.time() - self._start_time),
            "now": datetime.now().date(),
            "report_html": "" if self._report is None else self._report.tail().to_html(),
            "report_txt": "" if self._report is None else tabulate(self._report.tail(), tablefmt="pipe", headers="keys"),
            **self._config
        }

    def _build_models(self, name: str)->Tuple[str, str, str]:
        info = self._info()
        models = []
        for ext in ("txt", "html"):
            data = self._json(name, ext)
            model = self._load_model("basic", ext)
            for k, v in data.items():
                if isinstance(v, list):
                    if ext == "txt":
                        v = "\n".join(v)
                    if ext == "html":
                        v = "<br>".join(v)
                model = model.replace(k, v.format(**info))
            models.append(model)
        return (data["model_title"], *models)

    def add_report(self, df: pd.DataFrame):
        if not self._enabled:
            return
        self._report = df if self._report is None else pd.concat([
            self._report, df
        ])
        if time.time() - self._last_report > self._config["report_timeout"]*60*60:
            self._send_report()

    def __enter__(self):
        if self._enabled:
            self._start_time = time.time()
            self._last_report = time.time()
            self._start()
        return self

    def __exit__(self, *exc):
        if not self._enabled:
            return
        self._completed()