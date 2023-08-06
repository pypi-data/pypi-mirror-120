"""Command-line interface to generate SCRU-160 identifiers"""
import argparse

from . import scru160, scru160f


def generate() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f", action="store_true", help="print identifiers in hex encoding"
    )
    parser.add_argument(
        "-n",
        default=1,
        type=int,
        help="generate given number of identifiers",
        metavar="count",
    )

    args = parser.parse_args()
    fn = scru160f if args.f else scru160
    for _ in range(args.n):
        print(fn())
