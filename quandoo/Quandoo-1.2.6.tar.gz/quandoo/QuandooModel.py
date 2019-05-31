import json
from datetime import datetime
from quandoo.Error import PoorType


class PrettyClass:
    useless_attrs = ["api_response", "agent"]

    def __str__(self):
        useful_attrs = ["{}: {}".format(key, val) for key, val in self.__dict__.items() if
                        key not in self.useless_attrs]

        return "{}(\n\t{}\n)".format(
            self.__class__.__name__,
            ",\n\t".join(useful_attrs)
        )

    def __repr__(self):
        return "\n" + indent(str(self))

    def to_tuple(self):
        return tuple([val for key, val in self.__dict__.items() if key not in self.useless_attrs])


class QuandooModel(PrettyClass):

    def __init__(self, data):
        self.api_response = data

    def get_api_response(self):
        return json.dumps(self.api_response, indent=2)


class QuandooDatetime(PrettyClass):

    def __init__(self, data):
        self.datetime = data
        self.datetime = self.get_datetime()

        if type(self.datetime) != datetime:
            raise PoorType("Not a datetime object, input must be either a datetime object or quandoo datetime in form: %Y-%m-%dT%H:%M:%S%z", str(data))

    def __str__(self):
        useful_attrs = ["{}: {}".format(key, val) for key, val in self.__dict__.items() if
                        key not in self.useless_attrs] + ["{}: {}".format("q_datetime", self.get_q_datetime()),
                                                          "{}: {}".format("pretty_date", self.longdate())]

        return "{}(\n\t{}\n)".format(
            self.__class__.__name__,
            ",\n\t".join(useful_attrs)
        )

    def get_q_datetime(self):
        if type(self.datetime) == datetime:
            return datetime.strftime(self.datetime, "%Y-%m-%dT%H:%M:%S%z") + "+10:00"
        return self.datetime

    def get_datetime(self):
        if type(self.datetime) == str:
            d = self.datetime.split("+")
            d[1] = d[1].replace(":", "")
            return datetime.strptime("+".join(d), "%Y-%m-%dT%H:%M:%S%z")
        return self.datetime

    def longdate(self):
        return self.datetime.strftime("%I:%M %p, %a %d %B, %Y")

    def shortdate(self):
        return self.datetime.strftime("%d/%m/%y")


def urljoin(*argv):
    return "/".join([str(arg) for arg in argv])


def indent(string, indent_amount=1):
    return "\n".join(["\t" * indent_amount + line for line in string.split("\n")])

