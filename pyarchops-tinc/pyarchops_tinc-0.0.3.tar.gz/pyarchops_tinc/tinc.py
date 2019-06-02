# -*- coding: utf-8 -*-

"""Main module."""

import typing
import suitable


def apply(
        api: suitable.api.Api,
        config: dict,
        quiet: bool = False
) -> typing.Tuple:
    """ installs tinc """

    results = dict()
    results['install_pkgs'] = install_pkgs(api, quiet=quiet)
    results['create_tinc_network_folder'] = create_tinc_network_folder(
        api, config=config
    )
    results['deploy_configuration'] = deploy_configuration(
        api, config=config, quiet=quiet)
    results['enable_service'] = enable_service(api, config=config, quiet=quiet)

    if not quiet:
        print(results)
    return (True, results)


def install_pkgs(api: suitable.api.Api, quiet: bool = False) -> dict:
    """ installs tinc requirements"""

    result = api.pacman(
        name=['tinc', 'inetutils', 'dhclient', 'net-tools'],
        state='present'
    )
    if not quiet:
        print(result['contacted'])
    return dict({'install_pkgs': result})


def create_tinc_network_folder(
        api: suitable.api.Api,
        config: dict,
) -> dict:
    """ creates /etc/tinc/<network> """

    result = api.file(
        name=f"/etc/tinc/{config['tinc_network_name']}",
        state='directory',
        mode="0755",
        owner='root',
        group='root'
    )
    return dict({'create_tinc_network_folder': result})


def deploy_hosts_files(
        api: suitable.api.Api,
        config: dict,
) -> dict:
    """ deploys tinc /hosts/* files """

    results = dict()
    results['create_hosts_dir'] = api.file(
        name=f"/etc/tinc/{config['tinc_network_name']}/hosts",
        state='directory',
        mode="0755",
        owner='root',
        group='root'
    )
    results['connect_to_hosts'] = dict()
    for node, node_hostfile in config['connect_to_hosts'].items():
        results['connect_to_hosts'][node] = api.copy(
            dest=f"/etc/tinc/{config['tinc_network_name']}/hosts/{node}",
            content=node_hostfile,
            owner='root',
            group='root',
            mode="0644",
        )
    return dict({'deploy_host_files': results})


def deploy_tinc_key_files(
        api: suitable.api.Api,
        config: dict,
) -> dict:
    """ deploys tinc id_rsa files """

    results = dict()
    results['deploy_public_key'] = api.copy(
        dest=f"/etc/tinc/{config['tinc_network_name']}/rsa_key.pub",
        content=config['public_key'],
        owner='root',
        group='root',
        mode="0640",
    )
    results['deploy_private_key'] = api.copy(
        dest=f"/etc/tinc/{config['tinc_network_name']}/rsa_key.priv",
        content=config['private_key'],
        owner='root',
        group='root',
        mode="0600",
    )
    return dict({'deploy_tinc_key_files': results})


def deploy_interface_files(
        api: suitable.api.Api,
        config: dict,
) -> dict:
    """ deploys tinc interface files """

    results = dict()
    results['tinc_up'] = api.copy(
        dest=f"/etc/tinc/{config['tinc_network_name']}/tinc-up",
        owner='root',
        group='root',
        mode="0750",
        content=config['tinc_up_file'],
    )
    results['tinc_down'] = api.copy(
        dest=f"/etc/tinc/{config['tinc_network_name']}/tinc-down",
        owner='root',
        group='root',
        mode="0750",
        content=config['tinc_down_file'],
    )
    results['fix_route'] = api.copy(
        dest=f"/etc/tinc/{config['tinc_network_name']}/fix-route",
        owner='root',
        group='root',
        mode="0750",
        content=config['fix_route_file'],
    )
    results['dhclient_conf'] = api.copy(
        dest=f"/etc/tinc/{config['tinc_network_name']}/dhclient.conf",
        content=config['dhclient_conf'],
        owner='root',
        group='root',
        mode="0640",
    )
    return dict({'deploy_interface_files': results})


def deploy_tinc_conf(
        api: suitable.api.Api,
        config: dict,
) -> dict:
    """ deploys tinc.conf """

    result = api.copy(
        dest=f"/etc/tinc/{config['tinc_network_name']}/tinc.conf",
        content=config['tinc_conf'],
        owner='root',
        group='root',
        mode="0640",
    )
    return dict({'deploy_tinc_conf': result})


def deploy_configuration(
        api: suitable.api.Api,
        config: dict,
        quiet: bool = False
) -> dict:
    """ deploys tinc configuration """

    results = dict()
    results['deploy_tinc_key_files'] = deploy_tinc_key_files(
        api, config=config
    )
    results['deploy_interface_files'] = deploy_interface_files(
        api, config=config
    )
    results['deploy_host_files'] = deploy_hosts_files(api, config=config)

    results['deploy_tinc_conf'] = deploy_tinc_conf(api, config=config)

    if not quiet:
        print(results)
    return dict({'deploy_configuration': results})


def enable_service(
        api: suitable.api.Api,
        config: dict,
        quiet: bool = False
) -> dict:
    """ enables tinc services """

    results = dict()
    results['tinc_service'] = api.service(
        name='tinc', enabled=True, state='started')
    results[f'tinc_service_{config["tinc_network_name"]}'] = api.service(
        name=f"tinc@{config['tinc_network_name']}",
        enabled=True, state='started'
    )
    if not quiet:
        print(results)
    return dict({'enable_service': results})
