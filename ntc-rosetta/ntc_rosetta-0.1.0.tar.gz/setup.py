# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['ntc_rosetta',
 'ntc_rosetta.cli',
 'ntc_rosetta.drivers',
 'ntc_rosetta.helpers',
 'ntc_rosetta.parsers',
 'ntc_rosetta.parsers.openconfig.ios',
 'ntc_rosetta.parsers.openconfig.ios.openconfig_if_ethernet',
 'ntc_rosetta.parsers.openconfig.ios.openconfig_interfaces',
 'ntc_rosetta.parsers.openconfig.ios.openconfig_network_instance',
 'ntc_rosetta.parsers.openconfig.ios.openconfig_vlan',
 'ntc_rosetta.parsers.openconfig.junos',
 'ntc_rosetta.parsers.openconfig.junos.openconfig_if_ethernet',
 'ntc_rosetta.parsers.openconfig.junos.openconfig_interfaces',
 'ntc_rosetta.parsers.openconfig.junos.openconfig_network_instance',
 'ntc_rosetta.parsers.openconfig.junos.openconfig_vlan',
 'ntc_rosetta.translators',
 'ntc_rosetta.translators.openconfig.ios',
 'ntc_rosetta.translators.openconfig.ios.openconfig_if_ethernet',
 'ntc_rosetta.translators.openconfig.ios.openconfig_interfaces',
 'ntc_rosetta.translators.openconfig.ios.openconfig_network_instance',
 'ntc_rosetta.translators.openconfig.ios.openconfig_vlan',
 'ntc_rosetta.translators.openconfig.junos',
 'ntc_rosetta.translators.openconfig.junos.openconfig_if_ethernet',
 'ntc_rosetta.translators.openconfig.junos.openconfig_interfaces',
 'ntc_rosetta.translators.openconfig.junos.openconfig_network_instance',
 'ntc_rosetta.translators.openconfig.junos.openconfig_vlan',
 'ntc_rosetta.yang']

package_data = \
{'': ['*'],
 'ntc_rosetta.yang': ['YangModels/standard/ietf/RFC/*',
                      'openconfig/*',
                      'openconfig/doc/*',
                      'openconfig/doc/examples/*',
                      'openconfig/doc/img/*',
                      'openconfig/release/*',
                      'openconfig/release/models/*',
                      'openconfig/release/models/acl/*',
                      'openconfig/release/models/aft/*',
                      'openconfig/release/models/bfd/*',
                      'openconfig/release/models/bgp/*',
                      'openconfig/release/models/catalog/*',
                      'openconfig/release/models/interfaces/*',
                      'openconfig/release/models/isis/*',
                      'openconfig/release/models/lacp/*',
                      'openconfig/release/models/lldp/*',
                      'openconfig/release/models/local-routing/*',
                      'openconfig/release/models/mpls/*',
                      'openconfig/release/models/multicast/*',
                      'openconfig/release/models/network-instance/*',
                      'openconfig/release/models/openflow/*',
                      'openconfig/release/models/optical-transport/*',
                      'openconfig/release/models/ospf/*',
                      'openconfig/release/models/platform/*',
                      'openconfig/release/models/policy-forwarding/*',
                      'openconfig/release/models/policy/*',
                      'openconfig/release/models/probes/*',
                      'openconfig/release/models/qos/*',
                      'openconfig/release/models/relay-agent/*',
                      'openconfig/release/models/rib/*',
                      'openconfig/release/models/segment-routing/*',
                      'openconfig/release/models/stp/*',
                      'openconfig/release/models/system/*',
                      'openconfig/release/models/telemetry/*',
                      'openconfig/release/models/types/*',
                      'openconfig/release/models/vlan/*',
                      'openconfig/release/models/wifi/*',
                      'openconfig/release/models/wifi/access-points/*',
                      'openconfig/release/models/wifi/ap-manager/*',
                      'openconfig/release/models/wifi/mac/*',
                      'openconfig/release/models/wifi/phy/*',
                      'openconfig/release/models/wifi/types/*']}

install_requires = \
['click>=7.0,<8.0',
 'jmespath>=0.9.3,<0.10.0',
 'lxml>=4.3,<5.0',
 'yangify>=0.1.1,<0.2.0']

entry_points = \
{'console_scripts': ['ntc_rosetta = ntc_rosetta.cli:run']}

setup_kwargs = {
    'name': 'ntc-rosetta',
    'version': '0.1.0',
    'description': 'The missing bridge between industry standard CLIs and YANG',
    'long_description': None,
    'author': 'David Barroso',
    'author_email': 'dbarrosop@dravetech.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
