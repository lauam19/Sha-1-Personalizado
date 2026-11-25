"""Expansión personalizada de 16 a 80 palabras."""

from .operations import majority3, rotl32, u32


def expand_words(block: bytes) -> list[int]:
    """
    Recibe exactamente 64 bytes (512 bits).
    W[0..15] se leen en big-endian.
    Para t=16..79:
      W[t] = ROTL1(MAJ(W[t-3], W[t-8], W[t-14]) XOR W[t-16])
    """
    if len(block) != 64:
        raise ValueError("El bloque debe contener exactamente 64 bytes.")

    words = [
        int.from_bytes(block[i:i + 4], byteorder="big")
        for i in range(0, 64, 4)
    ]

    for t in range(16, 80):
        nonlinear_term = majority3(
            words[t - 3],
            words[t - 8],
            words[t - 14],
        )
        words.append(rotl32(nonlinear_term ^ words[t - 16], 1))

    assert len(words) == 80
    assert all(0 <= word <= 0xFFFFFFFF for word in words)
    return words
