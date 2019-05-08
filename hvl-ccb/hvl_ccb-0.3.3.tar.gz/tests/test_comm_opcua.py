"""
Tests for the OPC UA communication protocol.
"""

from time import sleep

import pytest

from hvl_ccb.comm import OpcUaCommunication, OpcUaSubHandler
from tests.opctools import DemoServer


@pytest.fixture(scope='module')
def testconfig():
    return {
        'host': 'localhost',
        'port': 14125,
        'endpoint_name': '',
        'sub_handler': MySubHandler(),
        'update_period': 100
    }


@pytest.fixture(scope='module')
def demo_opcua_server():
    opcua_server = DemoServer(100, 'x', 14125)
    opcua_server.start()

    yield opcua_server

    opcua_server.stop()


@pytest.fixture(scope='module')
def connected_comm_protocol(testconfig, demo_opcua_server):
    opc_comm = OpcUaCommunication(testconfig)
    opc_comm.open()
    yield opc_comm
    opc_comm.close()


class MySubHandler(OpcUaSubHandler):

    def __init__(self):
        self.change_counter = 0

    def datachange_notification(self, node, val, data):
        super().datachange_notification(node, val, data)
        print(node, val, data)
        self.change_counter += 1


def test_opcua(testconfig, demo_opcua_server):
    opc_comm = OpcUaCommunication(testconfig)
    assert opc_comm is not None

    opc_comm.open()

    opc_comm.close()


def test_read(connected_comm_protocol, demo_opcua_server):
    demo_opcua_server.add_var('testvar_read', 1.23, True)
    assert connected_comm_protocol.read('testvar_read', 100) == 1.23


def test_write(connected_comm_protocol, demo_opcua_server):
    demo_opcua_server.add_var('testvar_write', 1.23, True)
    connected_comm_protocol.write('testvar_write', 100, 2.04)
    assert connected_comm_protocol.read('testvar_write', 100) == 2.04


def test_init_monitored_nodes(connected_comm_protocol, demo_opcua_server):
    demo_opcua_server.add_var('mon1', 0, False)
    demo_opcua_server.add_var('mon2', 0, False)
    demo_opcua_server.add_var('mon3', 0, False)

    connected_comm_protocol.init_monitored_nodes('mon1', 100)
    connected_comm_protocol.init_monitored_nodes(['mon2', 'mon3'], 100)
    sleep(0.15)


def test_datachange(connected_comm_protocol, demo_opcua_server):
    demo_opcua_server.add_var('test_datachange', 0.1, True)
    connected_comm_protocol.init_monitored_nodes('test_datachange', 100)
    sleep(0.5)

    counter_before = connected_comm_protocol._sub_handler.change_counter
    demo_opcua_server.set_var('test_datachange', 0.2)
    assert demo_opcua_server.get_var('test_datachange') == 0.2
    sleep(0.15)
    counter_after = connected_comm_protocol._sub_handler.change_counter
    assert counter_after == counter_before + 1
