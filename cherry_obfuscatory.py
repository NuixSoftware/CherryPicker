# -*- coding: utf-8 -*-
"""This code is a rewrite of the code provided by Eric Merritt at Trustwave.

I have cleaned up, optimized, and rewritten it to make it easier to read so you
can more easily understand the algorithm. I’ve also added an obfuscator method
so you can obfuscate and un-obfuscate strings.
"""
import struct

__author__ = "Shawn Lee"
__email__ = "shawn.lee@nuix.com"

XOR_KEY = [0x000396e6, 0x32010384, 0x35d0364d, 0x0165625f]
uint = struct.Struct("I")


def unpack_at_offset(value, start):
    """Unpack an integer at an offset."""
    return uint.unpack(value[start:start + 4])[0]


def deobfuscate(working_bytes):
    """Deobfuscate a string using the key."""
    return obfuscate(working_bytes, reverse=True)


def obfuscate(working_bytes, reverse=False):
    """Obfuscate a string using the key."""
    chunk = [0] * 3
    if reverse:
        offset_range = xrange(len(working_bytes) - 16, -1, -1)
        mix_round_range = xrange(48, 0, -1)
    else:
        offset_range = xrange(len(working_bytes) - 15)
        mix_round_range = xrange(1, 49)
    for offset in offset_range:
        for mix_round in mix_round_range:
            xor_piece = XOR_KEY[mix_round % 4]
            byte_shift = mix_round % 4 * 4
            chunk[0] = unpack_at_offset(
                working_bytes, offset + 4 * ((mix_round - 1) % 4)) * 2
            chunk[1] = unpack_at_offset(
                working_bytes, offset + 4 * ((mix_round + 1) % 4))
            chunk[2] = unpack_at_offset(working_bytes, offset + byte_shift)
            result = (mix_round ^ xor_piece ^ chunk[0] ^ chunk[1]) & 0xffffffff
            result = ((result >> 8 | result << 24) * 9 ^ chunk[2]) ^ xor_piece
            working_bytes = "".join([
                working_bytes[:offset + byte_shift],
                uint.pack(result & 0xffffffff),
                working_bytes[offset + byte_shift + 4:]])
    return working_bytes
