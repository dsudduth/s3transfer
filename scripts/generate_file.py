"""Non-production script to copy large files to S3."""

import logging
import os

from pathlib import Path


# Setup Logging
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)
log.addHandler(ch)


def generate_large_file(filename: str, size: int) -> None:
    """Generates binary files with specificed size in bytes."""

    log.info(f'Generating large file of {size} bytes')
    with open(filename, 'wb') as f:
        f.write(os.urandom(size))


if __name__ == '__main__':
    size = 1073741824  # 1GB
    filename = Path('~/Desktop/large_file.zip').expanduser()
    generate_large_file(filename, size)
