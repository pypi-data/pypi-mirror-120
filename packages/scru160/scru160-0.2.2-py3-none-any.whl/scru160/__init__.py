"""SCRU-160: Sortable, Clock and Random number-based Unique identifier"""

__all__ = ["scru160", "scru160f"]


import datetime
import secrets
import threading
import typing


class Generator:
    """Represents SCRU-160 ID generator."""

    def scru160(self) -> str:
        """Generates a new SCRU-160 ID encoded in the base32hex format.

        Returns:
            32-character base32hexupper string (/^[0-9A-V]{32}$/).
        """
        return _base32hex160(self.generate())

    def scru160f(self) -> str:
        """Generates a new SCRU-160 ID encoded in the hexadecimal format.

        Returns:
            40-character hexadecimal string (/^[0-9a-f]{40}$/).
        """
        return self.generate().hex()

    def generate(self) -> bytes:
        """Generates a byte sequence that represents a new SCRU-160 ID.

        Returns:
            20-byte sequence.
        """
        ts, cnt = self._get_ts_and_cnt()
        return (
            ts.to_bytes(6, "big")
            + cnt.to_bytes(2, "big")
            + secrets.randbits(96).to_bytes(12, "big")
        )

    def __init__(self) -> None:
        self._ts: int = 0
        self._cnt: int = 0
        self._lock: threading.Lock = threading.Lock()

    def _get_ts_and_cnt(self) -> typing.Tuple[int, int]:
        """Updates the internal state and returns the latest values.

        Returns:
            The latest timestamp and counter.
        """

        def now() -> int:
            return int(datetime.datetime.now().timestamp() * 1000)

        with self._lock:
            new_ts = now()
            if new_ts <= self._ts:
                self._cnt += 1
                if self._cnt < 0x1_0000:
                    return (self._ts, self._cnt)

                # wait a moment until clock goes forward
                i = 0
                while new_ts <= self._ts:
                    new_ts = now()
                    i += 1
                    if i > 1_000_000:
                        import warnings

                        warnings.warn(
                            "scru160: reinitialized internal state as clock did not go forward; monotonicity may be broken",
                            RuntimeWarning,
                        )
                        break

            self._ts = new_ts
            self._cnt = secrets.randbits(15)
            return (self._ts, self._cnt)


_default_generator = Generator()


def scru160() -> str:
    """Generates a new SCRU-160 ID encoded in the base32hex format.

    Returns:
        32-character base32hexupper string (/^[0-9A-V]{32}$/).
    """
    return _default_generator.scru160()


def scru160f() -> str:
    """Generates a new SCRU-160 ID encoded in the hexadecimal format.

    Returns:
        40-character hexadecimal string (/^[0-9a-f]{40}$/).
    """
    return _default_generator.scru160f()


def _base32hex160(bs: bytes) -> str:
    """Encodes 20-byte sequence into base32hex."""
    cs = "0123456789ABCDEFGHIJKLMNOPQRSTUV"
    buffer = []
    for i in [0, 5, 10, 15]:
        buffer += [
            cs[31 & (bs[i + 0] >> 3)],
            cs[31 & (bs[i + 0] << 2) | (bs[i + 1] >> 6)],
            cs[31 & (bs[i + 1] >> 1)],
            cs[31 & (bs[i + 1] << 4) | (bs[i + 2] >> 4)],
            cs[31 & (bs[i + 2] << 1) | (bs[i + 3] >> 7)],
            cs[31 & (bs[i + 3] >> 2)],
            cs[31 & (bs[i + 3] << 3) | (bs[i + 4] >> 5)],
            cs[31 & (bs[i + 4] >> 0)],
        ]

    return "".join(buffer)
