"""Implementación educativa de SHA-1 NL v1.0."""

from .constants import INITIAL_STATE, MASK32, ROUND_CONSTANTS
from .expansion import expand_words
from .operations import block_function, rotl32, u32


def pad_message(message: bytes) -> bytes:
    """
    Padding estándar de SHA-1:
    mensaje || 1 || ceros || longitud original de 64 bits big-endian.
    """
    bit_length = len(message) * 8
    padded = message + b"\x80"
    zero_count = (56 - (len(padded) % 64)) % 64
    padded += b"\x00" * zero_count
    padded += (bit_length & 0xFFFFFFFFFFFFFFFF).to_bytes(8, "big")
    if len(padded) % 64 != 0:
        raise AssertionError("El padding no produjo bloques de 512 bits.")
    return padded


def _constant_for_round(round_index: int) -> int:
    if round_index <= 19:
        return ROUND_CONSTANTS[0]
    if round_index <= 39:
        return ROUND_CONSTANTS[1]
    if round_index <= 59:
        return ROUND_CONSTANTS[2]
    return ROUND_CONSTANTS[3]


def sha1_nl_bytes(message: bytes) -> bytes:
    """Calcula el digest experimental SHA-1 NL de un mensaje en bytes."""
    return bytes.fromhex(sha1_nl_analysis(message)["digest"])


def sha1_nl_analysis(message: bytes) -> dict:
    """Calcula el digest y devuelve trazas reales del procesamiento."""
    padded = pad_message(message)
    initial_state = INITIAL_STATE
    h0, h1, h2, h3, h4 = initial_state
    blocks = []

    for block_number, offset in enumerate(range(0, len(padded), 64), start=1):
        block = padded[offset:offset + 64]
        words = expand_words(block)
        a, b, c, d, e = h0, h1, h2, h3, h4
        rounds = []

        for t in range(80):
            before = (a, b, c, d, e)
            f = block_function(t, b, c, d)
            temp = u32(
                rotl32(a, 5) + f + e + words[t] + _constant_for_round(t)
            )
            a, b, c, d, e = (temp, a, rotl32(b, 30), c, d)
            rounds.append({
                "iteration": t,
                "block": (t // 20) + 1,
                "function": f"NL-{(t // 20) + 1}",
                "word": f"{words[t]:08x}",
                "constant": f"{_constant_for_round(t):08x}",
                "before": [f"{v:08x}" for v in before],
                "after": [f"{v:08x}" for v in (a, b, c, d, e)],
                "temp": f"{temp:08x}",
            })

        working_state = (a, b, c, d, e)
        h0, h1, h2, h3, h4 = (
            u32(h0 + a), u32(h1 + b), u32(h2 + c),
            u32(h3 + d), u32(h4 + e)
        )
        blocks.append({
            "number": block_number,
            "hex": block.hex(),
            "words": [f"{w:08x}" for w in words],
            "rounds": rounds,
            "working_state": [f"{v:08x}" for v in working_state],
            "chaining_state": [f"{v:08x}" for v in (h0, h1, h2, h3, h4)],
        })

    digest = b"".join(x.to_bytes(4, "big") for x in (h0, h1, h2, h3, h4)).hex()
    return {
        "digest": digest,
        "message_bytes": len(message),
        "message_bits": len(message) * 8,
        "padded_bytes": len(padded),
        "block_count": len(padded) // 64,
        "padding_hex": padded.hex(),
        "blocks": blocks,
    }


def sha1_nl(message: str) -> str:
    """Recibe texto UTF-8 y devuelve 40 caracteres hexadecimales."""
    if not isinstance(message, str):
        raise TypeError("El mensaje debe ser una cadena de texto.")
    digest = sha1_nl_bytes(message.encode("utf-8"))
    return digest.hex()
