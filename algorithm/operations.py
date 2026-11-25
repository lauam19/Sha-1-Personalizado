"""Operaciones booleanas de 32 bits para SHA-1 NL."""

from .constants import MASK32


def u32(value: int) -> int:
    """Reduce un entero al rango de una palabra sin signo de 32 bits."""
    return value & MASK32


def rotl32(value: int, amount: int) -> int:
    """Rotación circular a la izquierda sobre exactamente 32 bits."""
    amount %= 32
    value &= MASK32
    if amount == 0:
        return value
    return u32((value << amount) | (value >> (32 - amount)))


def majority3(x: int, y: int, z: int) -> int:
    """
    Mayoría de tres palabras, bit a bit:
    Q(x,y,z) = (x AND y) XOR (x AND z) XOR (y AND z).
    """
    return u32((x & y) ^ (x & z) ^ (y & z))


def select3(x: int, y: int, z: int) -> int:
    """
    Selección booleana:
    S(x,y,z) = (x AND y) XOR ((NOT x) AND z).
    NOT se limita a 32 bits.
    """
    x, y, z = u32(x), u32(y), u32(z)
    return u32((x & y) ^ ((~x & MASK32) & z))


def nl1(b: int, c: int, d: int) -> int:
    return select3(c, b, d)


def nl2(b: int, c: int, d: int) -> int:
    return select3(d, c, b)


def nl3(b: int, c: int, d: int) -> int:
    return select3(b, d, c)


def nl4(b: int, c: int, d: int) -> int:
    return select3(c, d, b)


def block_function(round_index: int, b: int, c: int, d: int) -> int:
    """Selecciona la función personalizada correspondiente al bloque."""
    if 0 <= round_index <= 19:
        return nl1(b, c, d)
    if 20 <= round_index <= 39:
        return nl2(b, c, d)
    if 40 <= round_index <= 59:
        return nl3(b, c, d)
    if 60 <= round_index <= 79:
        return nl4(b, c, d)
    raise ValueError("La iteración debe estar entre 0 y 79.")
