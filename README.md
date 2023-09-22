# S3 Transfer

`s3_transfer` is a command line tool for uploading files to Amazon S3. It serves as an example of how multi-part uploads can be implemented using the boto3 library.

## Installation

To install the package, run the following command:

```bash
pip install -r requirements.txt
```

## Usage

### Help

To get help, run `python s3_transfer.py --help`. This will display the help menu of the CLI.

### Uploading Files

The `transfer` command can be used to upload files to Amazon S3. The following command will upload the file `my-file.txt` to the bucket `my-bucket`:

```bash
# Example
python s3_transfer.py my-file.txt my-bucket
```

### Downloading Files

The `download-file` command can be used to download individual files from Amazon S3. The following command will download the file `my-file.txt` from the bucket `my-bucket` to the local directory:

```bash
python s3_transfer.py download-file 'my-bucket' 'my-file.txt' '~/my-local-path/my-file.txt'
```
