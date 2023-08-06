import argparse
import datetime
import select
import sys
import time

from . import __version__
from . import data
from . import memory
from . import nmea
from . import util


def dump(segment=0):
    """Dump the current contents of the NTP shared memory segment"""
    with memory.NtpShm(segment) as shm:
        snap = shm.read()
        field_names = (fn for fn, _ in snap._fields_)

        for field_name in field_names:
            if field_name.startswith("_"):
                continue
            print("{}: {}".format(field_name, getattr(snap, field_name)))

        # Special properties
        print("{}: {}".format("clock_ns", snap.clock_ns))
        print("{}: {}".format("clock_dt", snap.clock_dt))
        print("{}: {}".format("receive_ns", snap.receive_ns))
        print("{}: {}".format("receive_dt", snap.receive_dt))


def bridge(path, segment=0, verbose=False):
    """Parse NMEA sentences from the given file path and write to NTP SHM
    """
    print("ntp_shm v{} bridging {} to segment {}".format(__version__, path, segment))

    shm = memory.NtpShm(segment)

    for clock_ns, recv_ns in nmea.nmea_time(path):
        if verbose:
            print("Updating segment {} with clock {} received at {}".format(
                shm.segment, clock_ns, recv_ns))

        shm.update(clock_ns, recv_ns)
        last_ns = clock_ns


def main(args=None):
    if args is None:
        args = sys.argv

    parser = argparse.ArgumentParser("ntp-shm")
    parser.add_argument(
        "--version", action="store_true", default=False,
        help="Print the current version and exit"
    )
    subparsers = parser.add_subparsers()

    # dump command
    p_dump = subparsers.add_parser(
        "dump",
        help="Dump the contents of the given shared memory segment."
    )
    p_dump.add_argument(
        "--segment", "-s", type=int, default=0,
        help="Shared memory segment index (0-??)."
    )
    p_dump.set_defaults(func=dump)

    # bridge command
    p_bridge = subparsers.add_parser(
        "bridge",
        help="Bridge a NMEA0183 stream to the NTP shared memory."
    )
    p_bridge.add_argument(
        "--segment", "-s", type=int, default=0,
        help="Shared memory segment index (0-??)."
    )
    p_bridge.add_argument(
        "--path", "-p", type=str, default="/dev/stdin",
        help="File to read NMEA stream from, defaulting to stdin"
    )
    p_bridge.add_argument(
        "--verbose", "-v", action="store_true", default=False,
        help="Verbose output"
    )
    p_bridge.set_defaults(func=bridge)

    # Parse and run
    args = parser.parse_args(args[1:])
    arg_dict = args.__dict__

    version_flag = arg_dict.pop("version", False)
    if version_flag:
        print("ntp-shm v{}".format(__version__))
        exit(0)

    func = arg_dict.pop("func", None)
    if func is None:
        parser.print_help()
        exit(2)

    func(**arg_dict)
