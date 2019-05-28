from os.path import normpath, isfile, join
import stat

import click
from halo import Halo

from spell.cli.exceptions import (
    api_client_exception_handler,
    ExitException,
    SPELL_INVALID_CONFIG,
)
from spell.cli.log import logger
from spell.cli.utils import prettify_size


@click.command(name="cp",
               short_help="Retrieve a file or directory")
@click.argument("source_path")
@click.argument("local_dir", type=click.Path(file_okay=False, dir_okay=True, writable=True, readable=True), default=".")
@click.option("-f", "--force", is_flag=True,
              help="Overwrite all existing files")
@click.pass_context
def cp(ctx, source_path, local_dir, force):
    """
    Copy a file or directory from a finished run, uploaded resource, or public dataset
    specified by SOURCE_PATH to a LOCAL_DIR.

    The contents of SOURCE_PATH will be downloaded from Spell and written to LOCAL_DIR.
    If LOCAL_DIR is not provided the current working directory will be used as a default.
    If SOURCE_PATH is a directory, the contents of the directory will be written to LOCAL_DIR.
    """
    source_path = normpath(source_path)

    client = ctx.obj["client"]

    if source_path.startswith('/'):
        msg = 'Invalid source specification "{}". Source path must be a relative path.'.format(source_path)
        raise ExitException(msg, SPELL_INVALID_CONFIG)

    with api_client_exception_handler():
        logger.info("Copying run files from Spell")
        with client.tar_of_path(source_path) as tar:
            count = 0
            skip_count = 0
            spinner_name = "arrow3" if ctx.obj["utf8"] else "simpleDots"
            spinner = Halo(text="Copying", spinner=spinner_name).start() if ctx.obj["interactive"] else None
            for file in tar:
                if file.isdir() and not (file.mode & stat.S_IXUSR):
                    # Workaround for early uploads missing execute bit on directories, which breaks `ls`
                    file.mode |= stat.S_IXUSR
                if file.isfile() and spinner:
                    if not force and isfile(join(local_dir, file.name)):
                        # Require reply from user for duplicate files
                        spinner.stop()
                        overwrite = click.confirm(("File [{}] already exists. "
                                                   "Are you sure you want to "
                                                   "overwrite?").format(file.name))
                        spinner.start()
                        if not overwrite:
                            skip_count += 1
                            continue
                    count += 1
                    name = file.name[2:] if file.name.startswith("./") else file.name
                    spinner.text = "Copying {} ({})".format(name, prettify_size(file.size))
                tar.extract(file, path=local_dir)
            if spinner:
                report_line = "Copied {} files. Skipped {} files".format(count, skip_count)
                if ctx.obj["utf8"]:
                    spinner.succeed(report_line)
                else:
                    spinner.stop()
                    click.echo(report_line)
