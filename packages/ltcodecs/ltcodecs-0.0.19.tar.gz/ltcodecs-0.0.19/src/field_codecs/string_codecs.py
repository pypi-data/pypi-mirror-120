from sys import byteorder
from bitstring import BitArray, Bits, ConstBitStream
from .varint_codec import VarintCodec
from .field_codec import FieldCodec


def to_sixbit_ascii(character: str):
    upper_character = character.upper()
    ascii_code = int(upper_character.encode('ascii')[0])

    if ascii_code >= 0x40 and ascii_code <= 0x5f:
        sixbit_code = ascii_code - 0x40
    elif ascii_code >= 0x20 and ascii_code <= 0x3f:
        sixbit_code = ascii_code
    else:
        sixbit_code = 0x3f  # out of bounds values are encoded as '?'

    return sixbit_code


def from_sixbit_ascii(sixbit_code: int):
    if sixbit_code <= 0x1f:
        ascii_code = sixbit_code + 0x40
    # Other characters map directly
    else:
        ascii_code = sixbit_code

    return bytes([ascii_code]).decode('ascii')


class AsciiStringCodec(FieldCodec):
    def __init__(self, max_length: int = 128, bits_per_char: int = 7, tail=False, **kwargs):
        self.max_length = int(max_length)
        self.bits_per_char = bits_per_char
        self.tail = tail
        self.string_len_codec = VarintCodec(min_value=0, max_value=max_length)

    def encode(self, value: str):
        string_bytes = value.encode('ascii')
        compressed_bytes = bytearray()

        if self.bits_per_char == 7:
            for sb in string_bytes:
                if sb > 0x7f:
                    # Replace out of bounds values with "?"
                    sb = 0x3f
                compressed_bytes.append(sb)
        elif self.bits_per_char == 6:
            for sb in string_bytes:
                sixbit_value = to_sixbit_ascii(sb)
                compressed_byte = from_sixbit_ascii(sixbit_value).encode('ascii')
                compressed_bytes.extend(compressed_byte)
        else:
            compressed_bytes = string_bytes

    
        return BitArray(compressed_bytes)

    def decode(self, encoded_bits: ConstBitStream):
        encoded_bitArray = encoded_bits.tobytes()
        returnBytes = bytearray(encoded_bitArray)

        return returnBytes.decode('ascii')

    @property
    def max_length_bits(self):
        return self.string_len_codec.max_length_bits + (self.max_length * self.bits_per_char)

    @property
    def min_length_bits(self):
        return self.string_len_codec.max_length_bits