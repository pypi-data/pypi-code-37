'''
Small module for reading from a .ini configuration file at the command line
'''

import configparser

if __name__ == '__main__':
    def _cli():
        import optparse
        parser = optparse.OptionParser(usage='Usage: %prog SECTION KEY')
        parser.add_option('-c', '--config', dest='config',
                help='(REQUIRED) .ini configuration file to read from')
        (options, args) = parser.parse_args()

        def _bail(msg):
            print(msg)
            print('')
            parser.print_help()
            exit()

        if (not options.config):
            _bail('Must supply -c/--config')
        elif len(args) != 2:
            _bail('Must supply SECTION and KEY')

        return args, options
    (section, key), options = _cli()

    config = configparser.ConfigParser()
    config.read(options.config)

    if section in config:
        config_section = config[section]

        if key in config_section:
            config_value = config_section[key]
            print(config_value)
        else:
            raise KeyError('"%s" not found in section "%s"' % (
                key, section
            ))
    else:
        raise KeyError('No section named "%s" found in %s' % (
            section, options.config
        ))
