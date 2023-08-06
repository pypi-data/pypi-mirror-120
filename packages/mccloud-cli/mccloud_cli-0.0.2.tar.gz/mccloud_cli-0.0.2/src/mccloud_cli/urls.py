from typing import Tuple, Union
import traceback

import click
import boto3
from botocore.exceptions import ClientError, NoCredentialsError, ProfileNotFound
import humanfriendly

"""
McCloud CLI sub-command to generate AWS S3 presigned URLs for use in a McCloud job.
"""
NEWLINE = "\n"
DEFAULT_EXPIRES_IN = 8 * 3600  # in seconds


@click.command(context_settings=dict(max_content_width=512))
@click.option("--profile", help="Use a specific profile from your AWS credential file.")
@click.option(
    "--no-confirmation",
    default=False,
    help="Perform requested actions without user confirmation.",
)
@click.option(
    "--input-url",
    "-i",
    multiple=True,
    help="S3 URL which will be presigned to allow READ (input) access.",
)
@click.option(
    "--output-url",
    "-o",
    multiple=True,
    help="S3 URL which will be presigned to allow WRITE (output) access.",
)
@click.option(
    "--expires-in",
    type=int,
    default=DEFAULT_EXPIRES_IN,
    show_default=True,
    help="Number of seconds until the pre-signed URLs expire.",
)
def generate_S3_presigned_url(profile, no_confirmation, input_url, output_url, expires_in):
    try:
        aws = boto3.session.Session(profile_name=profile)
    except ProfileNotFound as e:
        raise click.ClickException(f"AWS profile: {str(e)}") from e

    validate_arguments(aws, input_url, output_url, expires_in)

    try:
        make_presign_urls(aws, input_url, output_url, expires_in, no_confirmation)
    except NoCredentialsError as e:
        raise click.ClickException("Unable to locate AWS credentials.") from e
    except click.Abort:
        raise
    except Exception as e:
        # should only happen on an internal error, so dump stack and re-raise
        traceback.print_exc()
        raise click.ClickException(f"Internal error: {str(e)}") from e


def validate_arguments(aws, input_urls, output_urls, expires_in):
    """
    Validate generate_S3_presigned_url parameters.

    Returns
    -------
    None

    Raises
    ------
    ClickException
        On invalid param.
    """
    if len(input_urls) == 0 and len(output_urls) == 0:
        raise click.ClickException("You must specify at least one S3 URL, using --input-url or --output-url.")

    for url in input_urls + output_urls:
        if not validate_S3_URI(url):
            raise click.ClickException(f"invalid URL format ({url}).")
        bucket_name, _ = split_S3_URI(url)
        if not bucket_exists(aws, bucket_name):
            raise click.ClickException(f"Bucket {bucket_name} doesn't exist or you don't have access to it.")

    if expires_in <= 0 or expires_in > 7 * 24 * 3600:
        raise click.ClickException(
            "--expires-in value must be greater than zero and less than 604800 seconds (one week)."
        )


def make_presign_urls(aws, input_urls, output_urls, expires_in, no_confirmation) -> None:
    print(
        """\n"""
        """This action will generate AWS S3 presigned URLs for the input and """
        f"""output URLs you have specified, with an expiration time {expires_in} seconds """
        f"""[{humanfriendly.format_timespan(expires_in)}] from now.""",
    )
    if len(input_urls) > 0:
        print(
            f"""
Read (input) URLs:
------------------
{NEWLINE.join(input_urls)}

Write (output) URLs:
--------------------
{NEWLINE.join(output_urls)}
        """
        )

    if not no_confirmation and not click.confirm("Do you wish to proceed?"):
        click.echo("Exiting, with no action taken.")
        return

    input_presigned_urls = []
    for url in input_urls:
        bucket_name, object_name = split_S3_URI(url)
        bucket_location = get_bucket_location(aws, bucket_name)
        if bucket_location != aws.region_name:
            aws = boto3.session.Session(profile_name=aws.profile_name, region_name=bucket_location)
            s3 = aws.client("s3")

        presigned_url = s3.generate_presigned_url(
            ClientMethod="get_object",
            Params={"Bucket": bucket_name, "Key": object_name},
            ExpiresIn=expires_in,
        )
        input_presigned_urls.append(presigned_url)

    output_presigned_urls = []
    for url in output_urls:
        bucket_name, object_name = split_S3_URI(url)
        bucket_location = get_bucket_location(aws, bucket_name)
        if bucket_location != aws.region_name:
            aws = boto3.session.Session(profile_name=aws.profile_name, region_name=bucket_location)
            s3 = aws.client("s3")

        presigned_url = s3.generate_presigned_url(
            ClientMethod="put_object",
            Params={
                "Bucket": bucket_name,
                "Key": object_name,
                "ContentType": "application/octet-stream",
            },
            ExpiresIn=expires_in,
            HttpMethod="PUT",
        )
        output_presigned_urls.append(presigned_url)

    print(
        f"""
Your presigned URLs will expire in {humanfriendly.format_timespan(expires_in)}.

Please launch the McCloud job with these URLs.

Presigned INPUT URLs:
---------------------
{(NEWLINE+NEWLINE).join(input_presigned_urls)}

Presigned OUTPUT URLs:
----------------------
{(NEWLINE+NEWLINE).join(output_presigned_urls)}
"""
    )


def split_S3_URI(path: str) -> Union[Tuple[str, str], None]:
    """
    Split and normalize an S3 URI into a bucket and key.
    Will strip trailing slash.

    There are four known HTTPS formats we have to support:
    * https://bucket.s3.amazonaws.com/key
    * https://bucket.s3-aws-region.amazonaws.com/key
    * https://s3.amazonaws.com/bucket/key
    * https://s3-aws-region.amazonaws.com/bucket/key

    and one S3 URI:
    * s3://bucket/key

    Returns False if the URI can't be parse or is not in a
    supported form.
    """

    if path.startswith("s3://"):
        path = path[5:]
    elif path.startswith("https://"):
        path = path[8:]
    else:
        return None

    path = path.lstrip("/")
    if "/" not in path:
        return path, ""
    else:
        return path.split("/", 1)


def validate_S3_URI(path) -> bool:
    return split_S3_URI(path) is not None


def bucket_exists(aws, bucket_name: str):
    """
    Determine whether a bucket with the specified name exists.

    :param bucket_name: The name of the bucket to check.
    :return: True when the bucket exists; otherwise, False.
    """
    s3 = aws.client("s3")
    try:
        s3.head_bucket(Bucket=bucket_name)
        exists = True
    except ClientError:
        exists = False
    return exists


def get_bucket_location(aws, bucket: str) -> str:
    """
    Lookup and return region (LocationConstraint) of the named bucket.

    NOTE: per https://docs.aws.amazon.com/AmazonS3/latest/API/API_GetBucketLocation.html,
    all buckets in us-east-1 have a LocationConstraint value set to None.
    """
    res = aws.client("s3").get_bucket_location(Bucket=bucket)
    bucket_location = res["LocationConstraint"]
    if bucket_location is None:
        bucket_location = "us-east-1"
    return bucket_location
