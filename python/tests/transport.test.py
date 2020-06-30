#!/usr/bin/env python3

import sys
import os

PACKAGE_PARENT = ".."
SCRIPT_DIR = os.path.dirname(
    os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__)))
)
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from serialengine import Transport
import time
import argparse

TIMEOUT = 1
DELAY = 0.5
DEBUG = False
PORT = "/dev/ttyACM0"
BAUDRATE = 2000000

########################
### HELPER FUNCTIONS ###
########################


def s(a=DELAY):
    time.sleep(a)


def report(text):
    global DEBUG
    if DEBUG:
        print("\033[93m[{}]\033[0m".format(text))


def success(text):
    print("\033[32m[{}]\033[0m".format(text))
    s(1)


##################
### UNIT TESTS ###
##################


def test_transport_setup():
    start = time.time()
    conn = Transport(PORT, baud=BAUDRATE, timeout=TIMEOUT).start()
    report("Transport created and started")
    assert conn.opened
    assert not conn.stopped
    conn.close()
    assert not conn.opened
    assert conn.stopped
    success("Transport Setup Test Passed ({:.5f} sec)".format(time.time() - start))


def test_message_bounce():
    start = time.time()
    conn = Transport(PORT, baud=BAUDRATE, timeout=TIMEOUT).start()
    report("Transport created and started")
    assert conn.get("Test") == None
    conn.write("Test", "Test")
    while conn.get("Test") == None:
        pass
    assert conn.get("Test") == "Test"
    conn.close()
    success("Message Bounce Test Passed ({:.5f} sec)".format(time.time() - start))


def test_multiple_messages():
    start = time.time()
    conn = Transport(PORT, baud=BAUDRATE, timeout=TIMEOUT).start()
    report("Transport created and started")
    assert conn.get("Test") == None
    conn.write("Test", "Test")
    while conn.get("Test") == None:
        pass
    assert conn.get("Test2") == None
    conn.write("Test2", "Test2")
    while conn.get("Test2") == None:
        pass
    assert conn.get("Test") == "Test"
    assert conn.get("Test2") == "Test2"
    conn.close()
    success(
        "Multiple Message Bounce Test Passed ({:.5f} sec)".format(time.time() - start)
    )


def test_multi_channel(num=10):
    start = time.time()
    conn = Transport(PORT, baud=BAUDRATE, timeout=TIMEOUT).start()
    report("Transport created and started")
    for i in range(num):
        msg = "test{}".format(i)
        conn.write(msg, msg)
        report("Writing test {}".format(i))
    while conn.get("test{}".format(num - 1)) == None:
        pass
    for i in range(num):
        msg = "test{}".format(i)
        assert conn.get(msg) == msg
        report("Reading test {}".format(i))
    conn.close()
    success("Multi-Channel Test Passed ({:.5f} sec)".format(time.time() - start))


###################
### TEST RUNNER ###
###################


def main(args):
    global DEBUG, DELAY
    if args.debug:
        DEBUG = True
    if args.sleep:
        DELAY = args.sleep
    if args.port:
        PORT = args.port
    routines = [
        test_transport_setup,
        test_message_bounce,
        test_multiple_messages,
        test_multi_channel,
    ]
    num = args.num or 1
    for i in range(num):
        for test in routines:
            test()
    print()
    success("All tests completed successfully")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Automated testing for the serial.engine library"
    )
    parser.add_argument(
        "-n", "--num", help="The number of times each test should run", type=int
    )
    parser.add_argument(
        "-d", "--debug", help="Turns on extra debugging messages", action="store_true"
    )
    parser.add_argument(
        "-p", "--port", help="Set the USB port to use for hardware tests"
    )
    parser.add_argument(
        "-s",
        "--sleep",
        help="Sleep timer between actions (default {})".format(DELAY),
        type=float,
    )
    args = parser.parse_args()
    main(args)
