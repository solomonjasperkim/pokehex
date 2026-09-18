"""TCP client for the sys-botbase protocol.

sys-botbase (https://github.com/olliz0r/sys-botbase) is an open, documented
homebrew sysmodule that exposes a plain-text command protocol over TCP for
reading/writing a running Nintendo Switch's memory and simulating controller
input. This client speaks that existing protocol; it does not reverse-engineer
anything about a specific game.

Requires a Switch on Atmosphere CFW with sys-botbase installed and reachable
over the local network.
"""

from __future__ import annotations

import socket

DEFAULT_PORT = 6000
BUFFER_SIZE = 4096


class SysbotClient:
    def __init__(self, host: str, port: int = DEFAULT_PORT, timeout: float = 5.0) -> None:
        self.host = host
        self.port = port
        self.timeout = timeout
        self._sock: socket.socket | None = None

    def connect(self) -> None:
        self._sock = socket.create_connection((self.host, self.port), timeout=self.timeout)

    def close(self) -> None:
        if self._sock is not None:
            self._sock.close()
            self._sock = None

    def __enter__(self) -> "SysbotClient":
        self.connect()
        return self

    def __exit__(self, *exc_info: object) -> None:
        self.close()

    def _require_connection(self) -> socket.socket:
        if self._sock is None:
            raise RuntimeError("not connected; call connect() or use as a context manager")
        return self._sock

    def _send_command(self, command: str) -> str:
        sock = self._require_connection()
        sock.sendall((command + "\r\n").encode("ascii"))
        chunks: list[bytes] = []
        while True:
            chunk = sock.recv(BUFFER_SIZE)
            if not chunk:
                break
            chunks.append(chunk)
            if chunk.endswith(b"\r\n"):
                break
        return b"".join(chunks).decode("ascii").strip()

    def click(self, button: str) -> None:
        self._send_command(f"click {button}")

    def peek(self, offset: int, size: int) -> bytes:
        response = self._send_command(f"peek {offset:X} {size:X}")
        return bytes.fromhex(response)

    def peek_absolute(self, address: int, size: int) -> bytes:
        response = self._send_command(f"peekAbsolute {address:X} {size:X}")
        return bytes.fromhex(response)

    def poke(self, offset: int, data: bytes) -> None:
        self._send_command(f"poke {offset:X} {data.hex()}")

    def poke_absolute(self, address: int, data: bytes) -> None:
        self._send_command(f"pokeAbsolute {address:X} {data.hex()}")

    def get_title_id(self) -> str:
        return self._send_command("getTitleID")

    def detach_controller(self) -> None:
        self._send_command("detachController")
