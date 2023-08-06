"""Command-line interface to generate SCRU-160 identifiers"""
import argparse
import datetime
import re
import sys

from .. import scru160, scru160f, _base32hex160


def generate() -> None:
    parser = argparse.ArgumentParser(description="Generate SCRU-160 identifiers.")
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


def inspect() -> None:
    parser = argparse.ArgumentParser(
        description="Show components of SCRU-160 identifiers read from stdin. "
        + "Print a human-readable JSON object for each valid line read."
    )
    parser.add_argument(
        "file",
        nargs="?",
        default="-",
        type=argparse.FileType("r"),
        help="read identifiers from file",
    )

    pattern = re.compile(r"^[0-9A-V]{32}|[0-9a-f]{42}$", flags=re.I)

    args = parser.parse_args()
    try:
        for line in args.file:
            line = line.strip()
            if line == "":
                continue
            elif pattern.search(line):
                print(_inspect_id(line))
            else:
                print("warning: skipped invalid identifier:", line, file=sys.stderr)
    except KeyboardInterrupt:
        sys.exit(1)


def _inspect_id(src: str) -> str:
    bs = int(src, 32 if len(src) == 32 else 16).to_bytes(20, "big")
    fields = (bs[0:6], bs[6:8], bs[8:10], bs[10:20])
    fields_int = [int.from_bytes(e, "big") for e in fields]
    fields_hex = ['"{}"'.format(e.hex()) for e in fields]

    timestamputc = datetime.datetime.fromtimestamp(
        fields_int[0] / 1000, tz=datetime.timezone.utc
    ).isoformat(sep=" ", timespec="milliseconds")

    return "\n".join(
        [
            "{",
            f'  "input":        "{src}",',
            f'  "canonical":    "{_base32hex160(bs)}",',
            f'  "timestamputc": "{timestamputc}",',
            f'  "timestamp":    "{fields_int[0]}",',
            f'  "counter":      "{fields_int[1]}",',
            f'  "random16":     "{fields_int[2]}",',
            f'  "random80":     "{fields_int[3]}",',
            f'  "hexfields":    [{", ".join(fields_hex)}]',
            "}",
        ]
    )
