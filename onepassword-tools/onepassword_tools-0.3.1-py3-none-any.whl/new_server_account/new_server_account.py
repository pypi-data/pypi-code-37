from onepassword_tools.lib.OnePasswordUtils import OnePasswordUtils
from onepassword_local_search.OnePassword import OnePassword
from onepassword_tools.lib.MiscUtils import generate_password
from onepassword_tools.lib.OnePasswordServerItem import OnePasswordServerItem
from onepassword_tools.lib.OnePasswordResult import OnePasswordResult
from onepassword_tools.lib.ClickUtils import ClickUtils
import click
import copy
import json
import sys


@click.command()
@click.option('--host', help='Host where the account is created', prompt=True, required=True)
@click.option('--username', help='Account username', prompt=True, required=True)
@click.option('--password', help='Password to use, default autogenerated')
@click.option('--password-length', help='Autogenerated password length, default 25', default=25, type=int)
@click.option('--vault', required=False, help='Vault uuid where to store the information')
@click.option('--account', required=False, help='Account to use (shorthand)')
@click.option('--return-field', required=False, help='Field value to return', default=None)
def new_server_account(host, username, password, password_length, vault, return_field, account):
    """Create a new Server item in 1Password with the given credentials."""
    NewServerAccount(**locals()).run()


class NewServerAccount:

    account: str = None
    entryTitleTemplate = 'USER %s ON %s'
    host: str = None
    onePassword: OnePassword
    onePasswordUtils: OnePasswordUtils
    password: str = None
    password_length: int = 25
    return_field: str = None
    title: str = None
    username: str = None
    vault: str = None

    def __init__(self, **kwargs):
        self.onePasswordUtils = OnePasswordUtils()
        self.onePassword = OnePassword()
        self._init(**kwargs)
        if self.password is None:
            self.password = generate_password(self.password_length)
        self.title = self.entryTitleTemplate % (self.username, self.host)

    def _init(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def run(self):

        if not self.onePasswordUtils.is_authenticated():
            self.onePasswordUtils.authenticate()

        item = self.save_on_1password()
        if 'uuid' in item.keys():
            result = ''
            if self.return_field is None:
                print(json.dumps(item))
            else:
                if self.return_field in item.keys():
                    result = item[self.return_field]
                else:
                    result = OnePasswordResult(dict(details=item['request_object'])).get(self.return_field)
            print(result)
            sys.exit(0)
        else:
            ClickUtils.error('Unable to save entry in 1Password')
            sys.exit(1)

    def save_on_1password(self):
        arguments = vars(copy.copy(self))
        del arguments['onePassword']
        del arguments['onePasswordUtils']
        server_item = OnePasswordServerItem(**arguments)
        request_object = server_item.get_request_object()
        return self.onePasswordUtils.create_item(
            account=self.account,
            request_object=request_object,
            template=server_item.item_type,
            title=server_item.get_title(),
            vault=self.vault
        )
