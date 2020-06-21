#!/usr/bin/env python3

import sys
import os

PACKAGE_PARENT = ".."
SCRIPT_DIR = os.path.dirname(
    os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__)))
)
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from serialengine.connection import connection
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


text = "Consulted he eagerness unfeeling deficient existence of. Calling nothing end fertile for venture way boy. Esteem spirit temper too say adieus who direct esteem. It esteems luckily mr or picture placing drawing no. Apartments frequently or motionless on reasonable projecting expression. Way mrs end gave tall walk fact bed. \
Left till here away at to whom past. Feelings laughing at no wondered repeated provided finished. It acceptance thoroughly my advantages everything as. Are projecting inquietude affronting preference saw who. Marry of am do avoid ample as. Old disposal followed she ignorant desirous two has. Called played entire roused though for one too. He into walk roof made tall cold he. Feelings way likewise addition wandered contempt bed indulged. \
Same an quit most an. Admitting an mr disposing sportsmen. Tried on cause no spoil arise plate. Longer ladies valley get esteem use led six. Middletons resolution advantages expression themselves partiality so me at. West none hope if sing oh sent tell is. \
Death weeks early had their and folly timed put. Hearted forbade on an village ye in fifteen. Age attended betrayed her man raptures laughter. Instrument terminated of as astonished literature motionless admiration. The affection are determine how performed intention discourse but. On merits on so valley indeed assure of. Has add particular boisterous uncommonly are. Early wrong as so manor match. Him necessary shameless discovery consulted one but. \
Yet remarkably appearance get him his projection. Diverted endeavor bed peculiar men the not desirous. Acuteness abilities ask can offending furnished fulfilled sex. Warrant fifteen exposed ye at mistake. Blush since so in noisy still built up an again. As young ye hopes no he place means. Partiality diminution gay yet entreaties admiration. In mr it he mention perhaps attempt pointed suppose. Unknown ye chamber of warrant of norland arrived. \
Luckily friends do ashamed to do suppose. Tried meant mr smile so. Exquisite behaviour as to middleton perfectly. Chicken no wishing waiting am. Say concerns dwelling graceful six humoured. Whether mr up savings talking an. Active mutual nor father mother exeter change six did all. "

##################
### UNIT TESTS ###
##################


def test_connection_setup():
    start = time.time()
    conn = connection(PORT, baud=BAUDRATE, timeout=TIMEOUT).start()
    report("Connection created and started")
    assert conn.opened
    assert not conn.stopped
    conn.close()
    assert not conn.opened
    assert conn.stopped
    success("Connection Setup Test Passed ({:.5f} sec)".format(time.time() - start))


def test_message_bounce():
    start = time.time()
    conn = connection(PORT, baud=BAUDRATE, timeout=TIMEOUT).start()
    report("Connection created and started")
    assert conn.get("Test") == None
    conn.write("Test", "Test")
    while conn.get("Test") == None:
        pass
    assert conn.get("Test") == "Test"
    conn.close()
    success("Message Bounce Test Passed ({:.5f} sec)".format(time.time() - start))


def test_multiple_messages():
    start = time.time()
    conn = connection(PORT, baud=BAUDRATE, timeout=TIMEOUT).start()
    report("Connection created and started")
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
    conn = connection(PORT, baud=BAUDRATE, timeout=TIMEOUT).start()
    report("Connection created and started")
    for i in range(num):
        msg = "test{}".format(i)
        conn.write(msg, msg)
    while conn.get("test{}".format(num - 1)) == None:
        pass
    for i in range(num):
        msg = "test{}".format(i)
        assert conn.get(msg) == msg
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
        test_connection_setup,
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
