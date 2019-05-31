
from random import randint

import myhdl as hdl
from myhdl import Signal, ResetSignal, intbv, always_seq
from myhdl.conversion import verify


TERMINATE_VALUE = 12


@hdl.block
def case1(x, y, clock, reset):

    @always_seq(clock.posedge, reset=reset)
    def beh_decode():
        if x == 1:
            y.next = 3
        elif x == 2:
            y.next = 4
        elif x == 3:
            y.next = 1
        else:
            y.next = 0

    return beh_decode


@hdl.block
def case2(x, y, clock, reset):

    @always_seq(clock.posedge, reset=reset)
    def beh_decode():
        if x == 1:
            y.next = 4
        elif x == 2:
            y.next = 1
        elif x == 3:
            y.next = 2
        elif x == TERMINATE_VALUE-1:
            y.next = 3
        else:
            y.next = 0

    return beh_decode


@hdl.block
def bench_converts(rtable, case_block):
    clock = Signal(bool(0))
    reset = ResetSignal(0, active=0, async=True)
    num_rands = len(rtable)
    x = Signal(intbv(0)[8:0])
    y = Signal(intbv(0)[8:0])

    tbdut = case_block(x, y, clock, reset)

    @hdl.instance
    def tbclk():
        clock.next = 0
        while True:
            yield hdl.delay(5)
            clock.next = not clock

    @hdl.instance
    def tbstim():
        reset.next = reset.active
        yield hdl.delay(10)
        reset.next = not reset.active
        yield clock.posedge

        for ii in range(num_rands):
            x.next = rtable[ii]
            yield clock.posedge
            print("x: %d,  y: %d" % (x, y,))

        raise hdl.StopSimulation

    return tbdut, tbclk, tbstim


def test_cases():
    rtable = tuple(
        [1, 2, 3, 4, TERMINATE_VALUE-1] +
        [randint(0, TERMINATE_VALUE-1) for _ in range(13)]
    )

    inst = bench_converts(rtable, case1)
    assert inst.verify_convert() == 0

    inst = bench_converts(rtable, case2)
    assert inst.verify_convert() == 0
