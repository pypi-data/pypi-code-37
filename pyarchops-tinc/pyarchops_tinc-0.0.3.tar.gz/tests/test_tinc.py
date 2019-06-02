#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `pyarchops_tinc` package."""

import textwrap
from suitable import Api
from pyarchops_helpers.helpers import ephemeral_docker_container
from pyarchops_tinc import tinc


def tinc_network_name():
    """ returns tinc network name """
    return 'core-vpn'


def public_key():
    """ returns public key """

    return textwrap.dedent('''
        -----BEGIN RSA PUBLIC KEY-----
        MIIBCgKCAQEAwBLTc+75h13ZyLWlvup0OmbhZWxohLMMFCUBClSMxZxZdMvyzBnW
        +JpOQuvnasAeTLLtEDWSID0AB/EG68Sesr58Js88ORUw3VrjObiG15/iLtAm6hiN
        BboTqd8jgWr1yC3LfNSKJk82qQzHJPlCO9Gc5HcqvWrIrqrJL2kwjOU66U/iRxJu
        dyOrz0sBkVgfwDBqNS96L0zFQCqk70w9KyOJqe4JNJUtBas6lbwgChDU4/B3BDW5
        PYJy2Pp8MSs2n1lhrUkXxRnj+Vl5wLQLdwog1XAGu2J8pIckPg/aB7mB/fSlFihU
        bnFlRlgHrlh8gyNYztbGWKMrQ4Bz2831PQIDAQAB
        -----END RSA PUBLIC KEY-----
    ''')


def private_key():
    """ returns private_key """

    return textwrap.dedent('''
        -----BEGIN RSA PRIVATE KEY-----
        MIIEpAIBAAKCAQEAwBLTc+75h13ZyLWlvup0OmbhZWxohLMMFCUBClSMxZxZdMvy
        zBnW+JpOQuvnasAeTLLtEDWSID0AB/EG68Sesr58Js88ORUw3VrjObiG15/iLtAm
        6hiNBboTqd8jgWr1yC3LfNSKJk82qQzHJPlCO9Gc5HcqvWrIrqrJL2kwjOU66U/i
        RxJudyOrz0sBkVgfwDBqNS96L0zFQCqk70w9KyOJqe4JNJUtBas6lbwgChDU4/B3
        BDW5PYJy2Pp8MSs2n1lhrUkXxRnj+Vl5wLQLdwog1XAGu2J8pIckPg/aB7mB/fSl
        FihUbnFlRlgHrlh8gyNYztbGWKMrQ4Bz2831PQIDAQABAoIBAQCU7UP1TWM/GX7m
        yCmGuYV7TxAPMxprYeTIrdR7rQklo9Ac5pIQvSxYwFRUQVPDCsmzkLyNZ+wwgPvI
        LJPANUkTsOzUrrS0UgD8cR9kPvaWtAqNX6n8syKNQTVD7pc6HrQKDbAMz0N65sqs
        ExNKUNaRSTsMTnXePrDx9cxerYIOi8duRVH/VEBIluVh5+m7ggiYzjWXOy1lExd3
        m5tqv0PicI6UTm6sUIar3pdypt0DitHBJN4apSIxv9yW+M+Uw4JEBlXL0Kq7o9M0
        NZRwdtL9q1xBC8/lu9K/nD55OvBo0cuHR6ZIqioBIsr5A0LJ6mc0xfwllEQjUD7E
        Z8pfW8blAoGBAP9iylxVvC3HWgXuTvDGPCbIdhw/AM4gR1Tz1eXGKCqyc9mTQR44
        MKCF8nrzVvQU+j5VVG1wQhZIMp7VyDLQMw0uZdj+mfSs2qwFPCLpbsa2hFco2xbs
        +Ejr3MQpbDYLodo9hAiFcg1AsRsI8MnlnigXFgEupMS+WSHQCMTZ5XcnAoGBAMCJ
        D9ofWgh1rMA1M5CSdukrcU26ScCq2b9WyhBTAd8v8SuOxLjVxsHjbhxZro9rEj0q
        Qb4AiDB88ksLGpiBg36UKHUwpiq5vlhkb27r+EwpCB5CFe1OBVIwMwwv+kyLHepl
        wdHEzndx9cWIbmlHwIaX7RM2qOGuA//3art7Ag77AoGAf4/54hsU7ozXw4SgO5XY
        78pLbJpvrYXj+2P8IFRVNdaDFVd/PDf22gdt8cngUfS0djQrAqsC55xSZJIF+JOU
        HG5jgvrRLay1YR0QR6PvqCP8gIiwvofJEKt3Tygdm/U9eAQoEhWNvV7l18okc8RU
        tlOpsxd4R6mIXeJKrwDjpBsCgYAp0FqB+5cZCT1oTOWS+0wZ3ZZw1Alab4B0vouJ
        ug1JBGdzF0GABuVwjE0ImS2A9jby06+NbR4msawJQjMXdeEx50lWEie0VbySA9Xz
        mAnHuI2LzLxoWi5rqA4eEnlgkEIB+vF59i0E4doHeVbJRIz6bhpNtuw8fwddWsVy
        TAepawKBgQDHOiiGIKsWR4Qrb0zTCQGLddRYE9/UG76ntTLA2ocOglLNZJtKFOGz
        0DbxS6Ow4enTcRMhvPf3Kn0AEdR9B1cnKgDZLZUqe0P1z11Q4LZ7BXjHJgypzEEF
        esViwAMKFer7C5GZwGMMaBVlzK/THREA1IPcOKwxopWgVvIbKus3VA==
        -----END RSA PRIVATE KEY-----
                           ''')


def tinc_up_file():
    """ returns tinc-up file """

    return textwrap.dedent(f'''
        #!/bin/sh
        # see: https://www.tinc-vpn.org/pipermail/tinc/2017-January/004729.html
        macfile=/etc/tinc/{tinc_network_name()}/address
        if [ -f $macfile ]; then
            ip link set tinc.{tinc_network_name()} address `cat $macfile`
        else
            cat /sys/class/net/tinc.{tinc_network_name()}/address >$macfile
        fi

        # https://bugs.launchpad.net/ubuntu/+source/isc-dhcp/+bug/1006937
        dhclient -4 -nw -v tinc.{tinc_network_name()} -cf /etc/tinc/{tinc_network_name()}/dhclient.conf -r
        dhclient -4 -nw -v tinc.{tinc_network_name()} -cf /etc/tinc/{tinc_network_name()}/dhclient.conf
    ''')  # noqa


def tinc_down_file():
    """ returns tinc-down file """

    return textwrap.dedent(f'''
      #!/bin/sh
      dhclient -4 -nw -v tinc.{tinc_network_name()} -cf /etc/tinc/{tinc_network_name()}/dhclient.conf -r
    ''')  # noqa


def fix_route_file():
    """ returns fix-route file """

    return textwrap.dedent(f'''
      #!/usr/bin/env bash

      sleep 15
      netstat -rnv | grep {tinc_network_name()} | grep 0.0.0.0 >/dev/null 2>&1

      if [ $? = 0 ]; then
    route del -net {tinc_network_name()} netmask 24 gateway 0.0.0.0
    route add -net {tinc_network_name()} netmask 24 gateway `ifconfig tinc.{tinc_network_name()}| grep inet | awk '{{ print $2 }}' `
      fi
    ''')  # noqa


def dhclient_conf_file():
    """ return dhclient.conf file  """

    return textwrap.dedent(f'''
        option rfc3442-classless-static-routes code 121 = array of unsigned integer 8;

        # https://bugs.launchpad.net/ubuntu/+source/isc-dhcp/+bug/1006937
        send host-name "my-host-name";
        #send dhcp-requested-address 10.16.254.23;

        request subnet-mask, broadcast-address, time-offset, routers,
            domain-name, domain-search, host-name,
            netbios-name-servers, netbios-scope, interface-mtu,
            rfc3442-classless-static-routes, ntp-servers;

        timeout 300;
    ''')  # noqa


def connect_to_hosts():
    """ returns connect_to_hosts """

    return {
        'core_network_01': textwrap.dedent('''
            Name=core_network_01
            Address=core01.example.com
            Port=655
            Compression=0
            Subnet=10.16.254.1/32

            -----BEGIN RSA PUBLIC KEY-----
            MIIBCgKCAQEAt9PKpazBuZMEH4mwX+yc0yq5sHT3D6fLJ+VHeJdSr6nsTWbthLGS
            ti+jt2bBniaUgkzbc1vRrWtM0sfRwhFbkBOXmXsSFQY19YfT7IqxG6nJ7JLiDMPL
            V1bK8xa9t2oXOdATNrTehq6oy8BeLls+BOKXJ9T6ZR6T4Hu4KN2tcf78ZMRCyrx1
            E1O/D3YAEErnZj1KN44Agf2GJXbCfayicywvojz3Otyiu/4VMtjubgUitbHS8ZiM
            yomH9ayDdAdqyFTEQopH4zQ7GYPH2syzIJsD9yRoc2CnMALb6q5rDGeLOfoCeIZq
            TAfi2ceSo0lGQwdiFehiogZ2ng5P9/Iq5QIDAQAB
            -----END RSA PUBLIC KEY-----
        '''),

        'core_network_02': textwrap.dedent('''
            Name=core_network_02
            Address=core02.example.com
            Port=655
            Compression=0
            Subnet=10.16.254.2/32

            -----BEGIN RSA PUBLIC KEY-----
            MIIBCgKCAQEApORHeJrFbe6H9Wqi25PEHpLMr1+scReE1BFNs9U5UME4PY+AGF92
            Qczpy70bH30quowy406zmglDQenIVWdpMpN2odm1V9OAz4vyk/AZzWK/wVDrIqqy
            OUFQnocdWwONGkfLShM5DHiyi5FcDS0oORWrh6LobxSQdBOZTKfgy2F6xJYUWAq7
            7jmqbJb40/Cd4BvyJekzkU71Y1TWfQnX7hvRD9S3pCpknwqtFnD8MYE+zv9p/uNC
            OsrCncN4Ur3/pcAqRRRfLuZqNvXTf1+HQk6jTPM0s1UCV5LtcEcbB4xzV8boDipm
            //8326DMTzUJntyqdhRxEYRjGuvI/Ri6uwIDAQAB
            -----END RSA PUBLIC KEY-----
        '''),

        'core_network_03': textwrap.dedent('''
            Name=core_network_03
            Address=core03.example.com
            Port=655
            Compression=0
            Subnet=10.16.254.3/32

            -----BEGIN RSA PUBLIC KEY-----
            MIIBCgKCAQEA81/Mkzf+qwxQ+Py8O5lyOWUmN84aAd5Z9d1XrCQ3iuHm7g5J0K4f
            U3JHMEOn0RU2RRUbUXiK0L8LeHCU7TiuBwz8+nOy/HCeZCiGUTuBkGKiIWSVVGY/
            SOHvAIUHhCCPMmgIuTBDywDthDGVPra++k1sRXsK5ODrPclqJzF5f5AKUaEfcfOw
            XdBn08fOu3S8SXSUoOepSS8mPQv2D0LB7hPXWlAV8tu3R9ibx2oR22c9zBWjgG5y
            tMhI3vLvnnzf2+0bNdY1ekc6G5wcCFuZb8qxt8+88Ls5Ek5jUc9Z1aqpe7x6MaYP
            KafbBTGK6BXmaAhyiQG4aALH5U2+Zl7BOwIDAQAB
            -----END RSA PUBLIC KEY-----
        '''),
    }


def tinc_conf_file():
    """ returns tinc.conf file """

    return textwrap.dedent(f'''
        Name = laptop
        DeviceType = tap

        Device = /dev/net/tun
        Interface = tinc.{tinc_network_name()}
        AddressFamily = ipv4
        LocalDiscovery = yes
        Mode=switch
        ConnectTo = core_network_01
        ConnectTo = core_network_02
        ConnectTo = core_network_03
        Cipher=aes-256-cbc
        ProcessPriority = high
    ''')


def test_tinc_apply():
    """Test the tinc apply function"""

    with ephemeral_docker_container(
            image='azulinho/pyarchops-base'
    ) as container:
        connection_string = "{}:{}".format(
            container['ip'], container['port']
        )
        api = Api(
            connection_string,
            connection='smart',
            remote_user=container['user'],
            private_key_file=container['pkey'],
            become=True,
            become_user='root',
            sudo=True,
            ssh_extra_args='-o StrictHostKeyChecking=no',
        )

        config = {
            'tinc_network_name': tinc_network_name(),
            'public_key': public_key(),
            'private_key': private_key(),
            'tinc_up_file': tinc_up_file(),
            'tinc_down_file': tinc_down_file(),
            'fix_route_file': fix_route_file(),
            'tinc_conf': tinc_conf_file(),
            'dhclient_conf': dhclient_conf_file(),
            'connect_to_hosts': connect_to_hosts(),
        }

        result, _ = tinc.apply(
            api,
            config=config
        )
        assert result

        result = api.shell(
            'systemctl is-active tinc'
        )['contacted'][connection_string]

        assert result['stdout'] == 'active'

        result = api.shell(
            'systemctl is-active tinc@core-vpn'
        )['contacted'][connection_string]

        assert result['stdout'] == 'active'
