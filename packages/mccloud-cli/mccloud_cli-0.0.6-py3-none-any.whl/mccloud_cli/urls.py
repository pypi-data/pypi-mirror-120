import traceback

import click
import boto3
from botocore.exceptions import NoCredentialsError, ProfileNotFound
import humanfriendly

from .s3_utils import split_S3_URI, validate_S3_URI, bucket_exists, get_bucket_location, get_s3_client

"""
McCloud CLI sub-command to generate AWS S3 presigned URLs for use in a McCloud job.
"""
NEWLINE = "\n"
DEFAULT_EXPIRES_IN = 2 * 24 * 3600  # in seconds


@click.command(name="generate-s3-presigned-url", context_settings=dict(max_content_width=512))
@click.option("--profile", help="Use a specific profile from your AWS credential file.")
@click.option(
    "--no-confirmation",
    is_flag=True,
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
def generate_S3_presigned_url_cli(profile, no_confirmation, input_url, output_url, expires_in):
    try:
        validate_arguments(profile, input_url, output_url, expires_in)
        make_presigned_urls(profile, input_url, output_url, expires_in, no_confirmation)
    except ProfileNotFound as e:
        raise click.ClickException(f"AWS profile: {str(e)}") from e
    except NoCredentialsError as e:
        raise click.ClickException("Unable to locate AWS credentials.") from e
    except (click.Abort, click.ClickException):
        raise
    except Exception as e:
        # should only happen on an internal error, so dump stack and re-raise
        traceback.print_exc()
        raise click.ClickException(f"Internal error: {str(e)}") from e


def validate_arguments(profile_name, input_urls, output_urls, expires_in):
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
            raise click.ClickException(f"Invalid URL format ({url}).")
        bucket_name, _ = split_S3_URI(url)
        if not bucket_exists(bucket_name, profile_name=profile_name):
            raise click.UsageError(f"Bucket {bucket_name} doesn't exist or you don't have access to it.")

    if expires_in <= 0 or expires_in > 7 * 24 * 3600:
        raise click.BadParameter(
            "--expires-in value must be greater than zero and less than 604800 seconds (one week)."
        )


def make_presigned_urls(profile_name, input_urls, output_urls, expires_in, no_confirmation) -> None:
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
"""
        )

    if len(output_urls) > 0:
        print(
            f"""
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
        input_presigned_urls.append(generate_presigned_input_url(url, expires_in, profile_name))

    output_presigned_urls = []
    for url in output_urls:
        output_presigned_urls.append(generate_presigned_output_url(url, expires_in, profile_name))

    print(
        f"""Your presigned URLs will expire in {humanfriendly.format_timespan(expires_in)}. """
        """Please launch the McCloud job with these URLs."""
    )
    if len(input_presigned_urls) > 0:
        print(
            f"""
Presigned INPUT URLs:
---------------------
{(NEWLINE+NEWLINE).join(input_presigned_urls)}
"""
        )

    if len(output_presigned_urls) > 0:
        print(
            f"""
Presigned OUTPUT URLs:
----------------------
{(NEWLINE+NEWLINE).join(output_presigned_urls)}
"""
        )


def generate_presigned_input_url(url: str, expires_in: int, profile_name=None) -> str:
    if not url.startswith("s3://"):
        # can't presign random URLs!
        return url

    bucket_name, object_name = split_S3_URI(url)
    bucket_location = get_bucket_location(bucket_name, profile_name=profile_name)
    s3 = get_s3_client(profile_name=profile_name, region_name=bucket_location)
    return s3.generate_presigned_url(
        ClientMethod="get_object",
        Params={"Bucket": bucket_name, "Key": object_name},
        ExpiresIn=expires_in,
    )


def generate_presigned_output_url(url: str, expires_in: int, profile_name=None) -> str:
    if not url.startswith("s3://"):
        # can't presign random URLs!
        return url

    bucket_name, object_name = split_S3_URI(url)
    bucket_location = get_bucket_location(bucket_name, profile_name=profile_name)
    s3 = get_s3_client(profile_name=profile_name, region_name=bucket_location)
    return s3.generate_presigned_url(
        ClientMethod="put_object",
        Params={
            "Bucket": bucket_name,
            "Key": object_name,
            "ContentType": "application/octet-stream",
        },
        ExpiresIn=expires_in,
        HttpMethod="PUT",
    )
