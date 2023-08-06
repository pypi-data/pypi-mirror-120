# Intro

`mccloud_cli` is a command line interface to the McCloud service. McCloud provides
a simple means to start a [Shasta](https://github.com/chanzuckerberg/shasta) assembly
in the cloud.

`mccloud_cli` currently provides an easy means to generate presigned URLs to use with the
McCloud. Eventually it will also provide a means to submit jobs directly from the command
line.

# Quick start

1. [optional] we highly suggest you run all python programs in a
   [virtual environment](https://docs.python.org/3/tutorial/venv.html).
2. `pip install mccloud-cli`
3. `mccloud_cli --help`

# Presigned URLs example

`mccloud_cli` will generate AWS presigned URLs.  This is useful when you want to store your
data in *your own* AWS S3 bucket (ie, privately), but want to temporarily grant McCloud 
access to read input data, and write results back to your bucket.

Usage:
```
$ mccloud_cli generate-s3-presigned-url --help
Usage: mccloud_cli generate-s3-presigned-url [OPTIONS]

Options:
  --profile TEXT             Use a specific profile from your AWS credential file.
  --no-confirmation BOOLEAN  Perform requested actions without user confirmation.
  -i, --input-url TEXT       S3 URL which will be presigned to allow READ (input) access.
  -o, --output-url TEXT      S3 URL which will be presigned to allow WRITE (output) access.
  --expires-in INTEGER       Number of seconds until the pre-signed URLs expire.  [default: 28800]
  --help                     Show this message and exit.
```

For example:
```
$ mccloud_cli generate-s3-presigned-url --profile my-aws-profile -i s3://my-bucket/reads.fasta.gz -o s3://my-bucket/results.tar.gz

This action will generate AWS S3 presigned URLs for the input and output URLs you have specified, with an expiration time 28800 seconds [8 hours] from now.

Read (input) URLs:
------------------
s3://my-bucket/reads.fasta.gz

Write (output) URLs:
--------------------
s3://my-bucket/results.tar.gz
        
Do you wish to proceed? [y/N]: Y

Your presigned URLs will expire in 8 hours.

Please launch the McCloud job with these URLs.

Presigned INPUT URLs:
---------------------
https://s3.amazonaws.com/my-bucket/reads.fasta.gz?AWSAccessKeyId=...

Presigned OUTPUT URLs:
----------------------
https://s3.amazonaws.com/my-bucket/results.tar.gz?AWSAccessKeyId=...
```
