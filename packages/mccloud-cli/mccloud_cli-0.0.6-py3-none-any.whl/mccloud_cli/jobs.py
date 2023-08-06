from typing import Tuple, Union

import time
from datetime import datetime, timezone
import requests
import traceback

import click
from click_params import EMAIL

import boto3
from botocore.exceptions import NoCredentialsError, ProfileNotFound

from .urls import generate_presigned_input_url, generate_presigned_output_url
from .s3_utils import split_S3_URI, validate_S3_URI, bucket_exists


DEFAULT_API_DOMAIN = "mccloud.czi.technology"
DEFAULT_EXPIRES_IN = 2 * 24 * 3600


class McCloudSubmitJobFailure(Exception):
    def __init__(self, message):
        super().__init__()
        self.message = message if message else ""

    def __str__(self):
        return f"McCloudSubmitJobFailure: {self.message}"


@click.command(name="submit-job", context_settings=dict(max_content_width=512))
@click.option("--mcat", help="McCloud Access Token, ie, MCAT-****.", required=True)
@click.option("--email", help="Email address for job notifications.", type=EMAIL, required=True)
@click.option(
    "--input-url",
    "-i",
    multiple=True,
    required=True,
    help="S3 URL which will be presigned to allow READ (input) access.",
)
@click.option(
    "--output-url",
    "-o",
    required=True,
    help="A single S3 URL which will be presigned to allow WRITE (output) access.",
)
@click.option("--shasta-version", required=True)
@click.option("--shasta-config", required=True)
@click.option("--shasta-cli-opts")
@click.option(
    "--I-have-read-and-agree-to-McCloud-terms-of-use",
    default=False,
    is_flag=True,
    help="Confirm that you have read, and agree to, the McCloud terms of use, "
    "available at https://mccloud.czi.technology/terms-of-use",
    prompt=True,
)
@click.option(
    "--domain",
    default="mccloud.czi.technology",
    hidden=True,
    help="Domain name to use as the McCloud API service. Primary use is for testing.",
)
@click.option(
    "--tail-job-log",
    default=False,
    is_flag=True,
    help="After job is submitted, print out job log messages.",
)
@click.option("--profile", help="Use a specific profile from your AWS credential file.")
def submit_job_cli(
    mcat,
    email,
    input_url,
    output_url,
    shasta_version,
    shasta_config,
    shasta_cli_opts,
    tail_job_log,
    **other_options,
):
    if not other_options.get("i_have_read_and_agree_to_mccloud_terms_of_use", False):
        click.echo("Exiting, no action taken.")
        return

    try:
        validate_arguments(
            mcat, email, input_url, output_url, shasta_version, shasta_config, shasta_cli_opts, **other_options
        )
        job_id, job_logs_url = submit_job(
            mcat, email, input_url, output_url, shasta_version, shasta_config, shasta_cli_opts, **other_options
        )
        click.echo(f"Starting McCloud job, id = {job_id}")
        click.echo(f"You can view logs at {job_logs_url}")
        if tail_job_log:
            tail_job_log_(job_id, **other_options)
    except ProfileNotFound as e:
        raise click.ClickException(f"AWS profile: {str(e)}") from e
    except NoCredentialsError as e:
        raise click.ClickException("Unable to locate AWS credentials.") from e
    except (click.Abort, click.ClickException):
        raise
    except McCloudSubmitJobFailure as e:
        click.echo(e.message)
        raise click.ClickException("Unable to start McCloud job - server returned error.")
    except Exception as e:
        # should only happen on an internal error, so dump stack and re-raise
        traceback.print_exc()
        raise click.ClickException(f"Internal error: {str(e)}") from e


def submit_job(
    mcat, email, input_url, output_url, shasta_version, shasta_config, shasta_cli_opts, **other_options
) -> Tuple[str, str]:
    domain = other_options.get("domain", DEFAULT_API_DOMAIN)
    profile_name = other_options.get("profile")

    mccloud_api = f"https://{domain}"
    expires_in = DEFAULT_EXPIRES_IN
    inputs = {
        "mcat": mcat,
        "email": email,
        "input_urls": list(map(lambda url: generate_presigned_input_url(url, expires_in, profile_name), input_url)),
        "output_url": generate_presigned_output_url(output_url, expires_in, profile_name),
        "shasta_version": shasta_version,
        "shasta_ref": "",  # not currently supported in the CLI
        "shasta_config_options": shasta_cli_opts or "",
        "shasta_config_preset": shasta_config,
    }

    res = requests.post(f"{mccloud_api}/submit", json=inputs)
    if res.status_code != requests.codes.ok:
        raise McCloudSubmitJobFailure(res.text)
    job_id = res.json()["job_id"]
    return (job_id, f"{mccloud_api}/jobs/{job_id}/monitor")


def get_job_log(job_id: str, domain: str = DEFAULT_API_DOMAIN) -> Union[str, dict]:
    """
    JSON log format for McCloud is:
    {
        "log": {
            "timestamp in ISO8601 format": str,
            ...
        },
        "jobName": str,
        "jobId": str,
        "status": "SUBMITTED" | "SUCCEEDED" | "FAILED" | "RUNNABLE" | "RUNNING" | ...,
        "statusReason": str,
        "createdAt": int # time since epoch in ms,
        "startedAt": int # time since epoch in ms,
        "stoppedAt": int # time since epoch in ms,
        "environment": [
            {
                "name": str,
                "value": str
            },
            ...
        ],
    }
    """
    mccloud_api = f"https://{domain}"
    res = requests.get(f"{mccloud_api}/jobs/{job_id}/monitor", headers={"accept": "application/json"})
    if res.headers["content-type"] == "application/json":
        return res.json()
    else:
        # not sure what we received, so treat as text
        return res.text.split("\n")


def tail_job_log_(job_id: str, **other_options) -> None:
    click.echo(f"Tailing job logs for {job_id}...")
    domain = other_options.get("domain", DEFAULT_API_DOMAIN)
    log_cursor = 0
    last = {}

    logs = get_job_log(job_id, domain)
    while True:
        if not isinstance(logs, dict):
            click.echo("Unable to tail logs. Current log contents follow.")
            click.echo(logs)
            raise click.Abort("Unable to tail logs due to server response.")

        if logs["status"] != last.get("status"):
            click.echo(f"*** Job status change: {logs['status']}")

        # convert all timestamps to datetime and sort by timestamp.
        sorted_log_messages = list(sorted(map(lambda kv: (datetime.fromisoformat(kv[0]), kv[1]), logs["log"].items())))

        # render only those lines which have not yet been rendered.
        if log_cursor < len(sorted_log_messages):
            for _, msg in sorted_log_messages[log_cursor:]:
                click.echo(msg)
            log_cursor = len(sorted_log_messages)

        if logs["status"] in ["SUCCEEDED", "FAILED"]:  # terminal state
            click.echo(f"*** Exit, job status {logs['status']}")
            return

        time.sleep(3)
        last = logs
        logs = get_job_log(job_id, domain)


def validate_arguments(
    mcat, email, input_url, output_url, shasta_version, shasta_config, shasta_cli_opts, **other_options
) -> None:
    if not isinstance(mcat, str) or len(mcat) == 0:
        raise click.BadParameter("--mcat must specify a McCloud access token.")
    if not isinstance(email, str) or len(email) == 0 or "@" not in email:
        raise click.BadParameter("--email - malformed email address specified.")
    if not isinstance(input_url, tuple) or len(input_url) == 0:
        raise click.UsageError("One or more input URLs must be specified with --input-url")
    if not isinstance(output_url, str) or len(output_url) == 0:
        raise click.UsageError("One output URL must be specified.")

    profile_name = other_options.get("profile")
    for url in list(input_url) + [output_url]:
        if not validate_S3_URI(url):
            raise click.BadParameter(f"Invalid URL format ({url}).")
        bucket_name, _ = split_S3_URI(url)
        if not bucket_exists(bucket_name, profile_name=profile_name):
            raise click.UsageError(f"Bucket {bucket_name} doesn't exist or you don't have access to it.")

    if not isinstance(shasta_version, str) or not shasta_version:
        raise click.BadParameter("Must specify --shasta-version.")
    if not isinstance(shasta_config, str) or not shasta_version:
        raise click.BadParameter("Must specify a config name using--shasta-config. For no pre-config, use 'None'.")
