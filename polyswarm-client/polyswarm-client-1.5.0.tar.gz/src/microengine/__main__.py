import click
import importlib.util
import logging
import sys

from polyswarmclient.config import init_logging, validate_apikey

logger = logging.getLogger(__name__)  # Initialize logger


def choose_backend(backend):
    """Resolves microengine name string to implementation

    Args:
        backend (str): Name of the backend to load, either one of the predefined
            implementations or the name of a module to load
            (module:ClassName syntax or default of module:Microengine)
    Returns:
        (Class): Microengine class of the selected implementation
    Raises:
        (Exception): If backend is not found
    """
    backend_list = backend.split(":")
    module_name_string = backend_list[0]

    # determine if this string is a module that can be imported as-is or as sub-module of the microengine package
    mod_spec = importlib.util.find_spec(module_name_string) or importlib.util.find_spec(
        "microengine.{0}".format(module_name_string))
    if mod_spec is None:
        raise Exception("Microengine backend `{0}` cannot be imported as a python module.".format(backend))

    # have valid module that can be imported, so import it.
    microengine_module = importlib.import_module(mod_spec.name)

    # find Microengine class in this module
    if hasattr(microengine_module, "Microengine"):
        microengine_class = microengine_module.Microengine
    elif len(backend_list) == 2 and hasattr(microengine_module, backend_list[1]):
        microengine_class = getattr(microengine_module, backend_list[1])
    else:
        raise Exception("No microengine backend found {0}".format(backend))

    return microengine_module.__name__, microengine_class


@click.command()
@click.option('--log', default='WARNING',
              help='App Log level')
@click.option('--client-log', default='WARNING',
              help='PolySwarm Client log level')
@click.option('--polyswarmd-addr', envvar='POLYSWARMD_ADDR', default='localhost:31337',
              help='Address (host:port) of polyswarmd instance')
@click.option('--keyfile', envvar='KEYFILE', type=click.Path(exists=True), default='keyfile',
              help='Keystore file containing the private key to use with this microengine')
@click.option('--password', envvar='PASSWORD', prompt=True, hide_input=True,
              help='Password to decrypt the keyfile with')
@click.option('--api-key', envvar='API_KEY', default='',
              callback=validate_apikey,
              help='API key to use with polyswarmd')
@click.option('--backend', envvar='BACKEND', required=True,
              help='Backend to use')
@click.option('--testing', default=0,
              help='Activate testing mode for integration testing, respond to N bounties and N offers then exit')
@click.option('--insecure-transport', is_flag=True,
              help='Connect to polyswarmd via http:// and ws://, mutually exclusive with --api-key')
@click.option('--chains', multiple=True, default=['side'],
              help='Chain(s) to operate on')
@click.option('--log-format', default='text',
              help='Log format. Can be `json` or `text` (default)')
# @click.option('--offers', envvar='OFFERS', default=False, is_flag=True,
#               help='Should the abassador send offers')
def main(log, client_log, polyswarmd_addr, keyfile, password, api_key, backend, testing, insecure_transport, chains, log_format):
    """Entrypoint for the microengine driver

    Args:
        log (str): Logging level for all app logs
        client_log (str): Logging level for all polyswarmclient logs
        polyswarmd_addr(str): Address of polyswarmd
        keyfile (str): Path to private key file to use to sign transactions
        password (str): Password to decrypt the encrypted private key
        backend (str): Backend implementation to use
        api_key(str): API key to use with polyswarmd
        testing (int): Mode to process N bounties then exit (optional)
        insecure_transport (bool): Connect to polyswarmd without TLS
        log_format (str): Format to output logs in. `text` or `json`
    """
    loglevel = getattr(logging, log.upper(), None)
    clientlevel = getattr(logging, client_log.upper(), None)
    if not isinstance(loglevel, int) or not isinstance(clientlevel, int):
        logging.error('invalid log level')
        sys.exit(-1)

    logger_name, microengine_class = choose_backend(backend)

    init_logging(['microengine', logger_name], log_format, loglevel)
    init_logging(['polyswarmclient'], log_format, clientlevel)
    microengine_class.connect(polyswarmd_addr, keyfile, password,
                              api_key=api_key, testing=testing,
                              insecure_transport=insecure_transport,
                              chains=set(chains)).run()


if __name__ == '__main__':
    main()
