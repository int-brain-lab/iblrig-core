import hashlib
import math
import os
import tempfile
import unittest
from io import BytesIO
from pathlib import Path

import iblrigcore.rsync as rsync


class RsyncTests(unittest.TestCase):
    TEST_BLOCK_SIZE = 4
    TEST_FILE = b'one really small file here'

    TEST_FILE_ADDITIONS = b'one really smaller file here :)'
    ADDITIONS_DELTA = [0, 1, 2, 3, b'er', 4, 5, b're', b' :)']

    TEST_FILE_DELETES = b'one really s file here'
    DELETES_DELTA = [0, 1, 2, 4, 5, 6]

    TEST_FILE_REORDERS = b'realone mallly s file here'
    REORDERS_DELTA = [1, 0, 3, 2, 4, 5, 6]

    def get_block(self, data, block):
        return data[block * self.TEST_BLOCK_SIZE:(block + 1) * self.TEST_BLOCK_SIZE]

    def get_delta(self, file):
        file_to = BytesIO(self.TEST_FILE)
        file_from = BytesIO(file)

        hashes = rsync.block_checksums(
            file_to,
            block_size=self.TEST_BLOCK_SIZE
        )

        delta = rsync.delta(
            file_from,
            hashes,
            block_size=self.TEST_BLOCK_SIZE
        )
        return list(delta)

    def test_block_checksums(self):
        with BytesIO(self.TEST_FILE) as file1:
            hashes = rsync.block_checksums(
                file1,
                block_size=self.TEST_BLOCK_SIZE
            )

            for block, block_hash in enumerate(hashes):
                block_data = self.get_block(self.TEST_FILE, block)

                weak_sum = rsync.weak_checksum(block_data)[0]
                strong_sum = hashlib.md5(block_data).digest()

                self.assertEqual(block_hash, (weak_sum, strong_sum))

    def test_delta_same_file(self):
        with BytesIO(self.TEST_FILE) as file_to:
            hashes = rsync.block_checksums(
                file_to,
                block_size=self.TEST_BLOCK_SIZE
            )
            with BytesIO(self.TEST_FILE) as file_from:
                delta = rsync.delta(
                    file_from, hashes,
                    block_size=self.TEST_BLOCK_SIZE
                )
                for index, block in enumerate(delta):
                    self.assertEqual(index, block)

    def test_delta_with_changes(self):
        changes_in_blocks = [
            (0, 0),
            (3, 2),
            (4, 0),
            (5, self.TEST_BLOCK_SIZE - 1),
            (math.ceil(len(self.TEST_FILE) / self.TEST_BLOCK_SIZE) - 1, 0)
        ]
        changed_blocks = [block for block, position in changes_in_blocks]

        with BytesIO(self.TEST_FILE) as changed_file:
            file_buffer = changed_file.getbuffer()

            for block, position in changes_in_blocks:
                file_buffer[block * self.TEST_BLOCK_SIZE + position] += 1

            changed_file_data = changed_file.getvalue()

            with BytesIO(self.TEST_FILE) as file_to:
                hashes = rsync.block_checksums(
                    file_to,
                    block_size=self.TEST_BLOCK_SIZE
                )

                delta = rsync.delta(
                    changed_file,
                    hashes,
                    block_size=self.TEST_BLOCK_SIZE,
                    max_buffer=self.TEST_BLOCK_SIZE
                )

                for block, data in enumerate(delta):
                    if block in changed_blocks:
                        self.assertEqual(
                            self.get_block(changed_file_data, block),
                            data
                        )
                    else:
                        self.assertEqual(block, data)

    def test_delta_with_additions(self):
        delta = self.get_delta(self.TEST_FILE_ADDITIONS)
        self.assertEqual(delta, self.ADDITIONS_DELTA)

    def test_rsync_delta_with_deletes(self):
        delta = self.get_delta(self.TEST_FILE_DELETES)
        self.assertEqual(delta, self.DELETES_DELTA)

    def test_rsync_delta_with_reorders(self):
        delta = self.get_delta(self.TEST_FILE_REORDERS)
        self.assertEqual(delta, self.REORDERS_DELTA)

    def test_patch_stream_with_additions(self):
        delta = self.get_delta(self.TEST_FILE_ADDITIONS)
        old_file = BytesIO(self.TEST_FILE)
        out_file = BytesIO()
        rsync.patch_stream(
            old_file,
            out_file,
            delta,
            block_size=self.TEST_BLOCK_SIZE
        )
        self.assertEqual(out_file.getvalue(), self.TEST_FILE_ADDITIONS)

    def test_patch_stream_with_deletes(self):
        delta = self.get_delta(self.TEST_FILE_DELETES)
        old_file = BytesIO(self.TEST_FILE)
        out_file = BytesIO()
        rsync.patch_stream(
            old_file,
            out_file,
            delta,
            block_size=self.TEST_BLOCK_SIZE
        )
        self.assertEqual(out_file.getvalue(), self.TEST_FILE_DELETES)

    def test_patch_stream_with_reorders(self):
        delta = self.get_delta(self.TEST_FILE_REORDERS)
        old_file = BytesIO(self.TEST_FILE)
        out_file = BytesIO()
        rsync.patch_stream(
            old_file,
            out_file,
            delta,
            block_size=self.TEST_BLOCK_SIZE
        )
        self.assertEqual(out_file.getvalue(), self.TEST_FILE_REORDERS)

    def test_file_transfer(self):
        # create temp dirs and files
        temp_dir = tempfile.TemporaryDirectory()
        src_dir = Path(temp_dir.name) / 'src'
        dst_dir = Path(temp_dir.name) / 'dst'
        os.mkdir(src_dir)
        os.mkdir(dst_dir)
        src_file = src_dir / 'file1'
        dst_file = dst_dir / 'file1'
        with open(src_file, 'wb') as f:
            f.write(self.TEST_FILE)
        with open(dst_file, 'wb') as f:
            f.write(self.TEST_FILE_DELETES)

        # On the system containing the file that needs to be patched
        unpatched = open(dst_file, 'rb')
        hashes = rsync.block_checksums(unpatched)
        # On the remote system after having received hashes
        patched_file = open(src_file, 'rb')
        delta = rsync.delta(patched_file, hashes)
        # System with the unpatched file after receiving delta
        unpatched.seek(0)
        save_to = open(dst_file, 'wb')
        rsync.patch_stream(unpatched, save_to, delta)

        pass


if __name__ == '__main__':
    unittest.main()