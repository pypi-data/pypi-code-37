#!/usr/bin/env python3

import singer
import json
import sys
from tap_pipedrive.tap import PipedriveTap


logger = singer.get_logger()


def main_impl():
    args = singer.utils.parse_args(['api_token', 'start_date'])

    pipedrive_tap = PipedriveTap(args.config, args.state)

    if args.discover:
        catalog = pipedrive_tap.do_discover()
        json.dump(catalog.to_dict(), sys.stdout, indent=2)
        logger.info('Finished discover')
    else:
        if args.catalog:
            catalog = args.catalog
        else:
            catalog = pipedrive_tap.do_discover()
        pipedrive_tap.do_sync(catalog)


def main():
    try:
        main_impl()
    except Exception as e:
        logger.critical(e)
        raise e


if __name__ == '__main__':
    main()
