# Python implementation of rsync - https://github.com/isislovecruft/pyrsync
import hashlib

__all__ = [
    "rolling_checksum",
    "weak_checksum",
    "patch_stream",
    "patch_stream_block",
    "delta",
    "block_checksums"
]


def delta(datastream, hashes, block_size=4096, max_buffer=4096):
    """
    A binary patch generator when supplied with a readable stream for the up-to-date data and the
    weak and strong hashes from an unpatched target. The block_size must be the same as the value
    used to generate the hashes.
    """
    hashdict = {}
    for index, (weak, strong) in enumerate(hashes):
        if weak not in hashdict:
            hashdict[weak] = {}
        hashdict[weak][strong] = index

    match = True
    current_block = bytearray()

    while True:
        if match:
            # Whenever there is a match or
            # the loop is running for the first time,
            # populate the window using weakchecksum instead of rolling
            # through every single byte which takes at least twice as long.
            window = bytearray(datastream.read(block_size))
            if window:
                window_offset = 0
                checksum, a, b = weak_checksum(window)
            else:
                break
        else:
            # Roll one byte forward if not already at the EOF
            if datastream is not None:
                newbytearray = bytearray(datastream.read(1))
                if newbytearray:
                    newbyte = newbytearray[0]
                    window.append(newbyte)
                else:
                    # EOF; the window will slowly shrink.
                    # newbyte needs to be zero from here on to keep
                    # the checksum correct.
                    newbyte = 0
                    tailsize = datastream.tell() % block_size
                    datastream = None

            # Add the old byte the file delta. This is data that was not found
            # inside of a matching block so it needs to be sent to the target.
            oldbyte = window[window_offset]
            current_block.append(oldbyte)
            window_offset += 1
            # Yank off the extra byte and calculate the new window checksum
            checksum, a, b = rolling_checksum(oldbyte, newbyte, a, b, block_size)

        strongkey = hashlib.md5(window[window_offset:]).digest() if (checksum in hashdict) else None
        if checksum in hashdict and strongkey in hashdict[checksum]:
            match = True

            if current_block:
                yield bytes(current_block)
                current_block = bytearray()
            yield hashdict[checksum][strongkey]

            if datastream is None:
                break

        else:
            match = False

            if len(current_block) == max_buffer:
                yield bytes(current_block)
                current_block = bytearray()

            if datastream is None and len(window) - window_offset <= tailsize:
                # The likelihood that any blocks will match after this is
                # nearly nil so flush the current block and call it quits.
                if current_block:
                    yield bytes(current_block)
                    current_block = bytearray()
                yield bytes(window[window_offset:])
                break


# def rsync_delta(datastream, remote_signatures, block_size=4096, max_buffer=4096):
#     """
#     Generates a binary patch when supplied with the weak and strong hashes from an unpatched target
#     and a readable stream for the up-to-date data. The block_size must be the same as the value
#     used to generate remote_signatures.
#     """
#     remote_signatures = {
#         weak: (index, strong) for index, (weak, strong)
#         in enumerate(remote_signatures)
#     }
#     match = True
#     match_block = -1
#     current_block = bytearray()
#     checksum = window = window_offset = tail_size = next_byte = None
#
#     while True:
#         if match and datastream is not None:
#             # Whenever there is a match or the loop is running for the first time, populate the
#             # window using weak_checksum instead of rolling through every single byte which takes
#             # at least twice as long.
#             window = bytearray(datastream.read(block_size))
#             window_offset = 0
#             checksum, a, b = weak_checksum(window)
#
#         if (checksum in remote_signatures and
#                 remote_signatures[checksum][1] ==
#                 hashlib.md5(window[window_offset:]).digest()):
#
#             match_block = remote_signatures[checksum][0]
#             match = True
#             if len(current_block) > 0:
#                 yield bytes(current_block)
#
#             yield match_block
#             current_block = bytearray()
#             if datastream.closed:
#                 break
#             continue
#         else:
#             # The weak_checksum (or the strong one) did not match
#             match = False
#             try:
#                 if datastream:
#                     # Get the next byte and affix to the window
#                     next_byte = ord(datastream.read(1))
#                     window.append(next_byte)
#             except TypeError:
#                 # No more data from the file; the window will slowly shrink, next_byte needs to be
#                 # zero from here on to keep the checksum correct
#                 next_byte = 0
#                 tail_size = datastream.tell() % block_size
#                 datastream = None
#
#             if datastream is None and len(window) - window_offset <= tail_size:
#                 # No blocks are likely to match after this
#                 # Flush the current block
#                 if len(current_block) > 0:
#                     yield bytes(current_block)
#                 current_block = window[window_offset:]
#                 break
#
#             # Yank off the extra byte and calculate the new window checksum
#             prev_byte = window[window_offset]
#             window_offset += 1
#             checksum, a, b = rolling_checksum(prev_byte, next_byte, a, b, block_size)
#             if len(current_block) >= max_buffer:
#                 yield bytes(current_block)
#                 current_block = bytearray()
#
#             # Add the previous byte the file delta. This is data that was not found inside a
#             # matching block, it needs to be sent to the target
#             current_block.append(prev_byte)
#
#     if len(current_block) > 0:
#         yield bytes(current_block)


def block_checksums(in_stream, block_size=4096):
    """
    A generator of (weak hash (int), strong hash(bytes)) tuples for each block of the defined size
    for the given data stream.
    """
    read = in_stream.read(block_size)
    while read:
        yield weak_checksum(read)[0], hashlib.md5(read).digest()
        read = in_stream.read(block_size)


def patch_stream(in_stream, out_stream, delta, block_size=4096):
    """
    Patches in_stream using the supplied delta and write the resultant data to out_stream.
    """
    for element in delta:
        if isinstance(element, int) and block_size:
            in_stream.seek(element * block_size)
            element = in_stream.read(block_size)
        out_stream.write(element)


def patch_stream_block(in_stream, out_stream, delta_block, block_size=4096):
    if isinstance(delta_block, int) and block_size:
        in_stream.seek(delta_block * block_size)
        delta_block = in_stream.read(block_size)
    out_stream.write(delta_block)


# def rolling_checksum(removed, new, a, b, block_size=4096):
#     """
#     Generates a new weak checksum when supplied with the internal state of the checksum calculation
#     for the previous window, the removed byte, and the added byte.
#     """
#     a -= removed - new
#     b -= removed * block_size - a
#     return (b << 16) | a, a, b


def rolling_checksum(old, new, a, b, blocksize=4096):
    """
    Generate a new weak checksum when supplied with
    the internal state of the checksum calculation for the previous window,
    the old byte, and the new byte.
    """
    a -= old - new
    b -= old * blocksize - a
    return (b << 16) | a, a, b

def weak_checksum(data):
    """
    Generate a weak checksum from an iterable set of bytes.
    """
    a = b = 0
    l = len(data)
    for i in range(l):
        a += data[i]
        b += (l - i) * data[i]
    return (b << 16) | a, a, b
