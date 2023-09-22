"""Non-production script to copy large files to S3."""

import os

from pathlib import Path

import boto3
import typer
import tqdm

from typing import Union, List
from boto3.s3.transfer import TransferConfig
from botocore.exceptions import ClientError

app = typer.Typer()

S3_CLIENT = boto3.resource("s3")


@app.command()
def download_file(
    bucket_name: str = typer.Argument(
        ...,
        help='The name of the S3 bucket'
    ),
    src:  str = typer.Argument(
        ...,
        help='The files to download'
    ),
    dest: str = typer.Argument(
        ...,
        help='The destination directory'
    )
):
    """Download a file"""
    src = Path(src)
    dest = Path(dest).expanduser().resolve()

    bucket = S3_CLIENT.Bucket(bucket_name)

    if dest.is_dir():
        dest = dest / src.name

    typer.secho(f'Downloading {src} to {dest}', fg='green')

    with open(dest, 'wb') as f:
        try:
            bucket.download_fileobj(str(src), f)
        except ClientError as err:
            typer.secho(
                f'Error occurred while uploading file - {err}', err=True
            )
            raise typer.Exit(1)


@app.command()
def transfer(
    file_path: str = typer.Argument(..., help="The file to upload"),
    bucket_name: str = typer.Argument(..., help="The name of the S3 bucket"),  # NOQA
    prefix: str = typer.Option(
        None, help='The path in S3 to upload the file to'),
    object_name: str = typer.Option(
        None, help='Optional - rename the uploaded file')
):
    """Performs multi-part uploads of files to S3."""

    if not isinstance(file_path, Path):
        file_path = Path(file_path)

    if object_name is None:
        object_name = file_path.name

    config = TransferConfig(
        multipart_threshold=1024 * 25,
        max_concurrency=20,
        multipart_chunksize=1024 * 25,
        use_threads=True
    )

    if prefix:
        object_name = f'{prefix}/{object_name}'

    try:
        s3_object = S3_CLIENT.Object(
            bucket_name,
            object_name
        )

        file_size = os.stat(file_path).st_size
        with tqdm.tqdm(total=file_size, unit='B', unit_scale=True, desc=file_path.name) as pbar:
            s3_object.upload_file(
                Filename=str(file_path),
                Config=config,
                Callback=lambda bytes_transferred: pbar.update(
                    bytes_transferred
                )
            )

    except ClientError as err:
        typer.secho(f'Error occurred while uploading file - {err}', err=True)
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
