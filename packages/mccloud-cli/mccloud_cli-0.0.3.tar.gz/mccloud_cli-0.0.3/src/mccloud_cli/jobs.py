import time
import requests
import traceback

import click
from click_params import EMAIL

from botocore.exceptions import NoCredentialsError, ProfileNotFound

from .urls import generate_presigned_input_url, generate_presigned_output_url


class McCloudSubmitJobFailure(Exception):
    pass


@click.command(name="submit-job", context_settings=dict(max_content_width=512))
@click.option("--mcat", help="McCloud Access Token, ie, MCAT-****.", required=True)
@click.option("--email", help="Email address for job notifications.", type=EMAIL, required=True)
@click.option(
    "--input-url",
    "-i",
    multiple=True,
    help="S3 URL which will be presigned to allow READ (input) access.",
)
@click.option(
    "--output-url",
    "-o",
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
    help="After job is submittted, print out job log messages. NOTE: will not exit -- interrupt this program to exit.",
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
    domain,
    tail_job_log,
    profile,
    **kwargs,
):
    try:
        job_id = submit_job(mcat, email, input_url, output_url, shasta_version, shasta_config, shasta_cli_opts, domain)
        if tail_job_log:
            tail_job_log_(domain, job_id)
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


def submit_job(mcat, email, input_url, output_url, shasta_version, shasta_config, shasta_cli_opts, domain) -> str:
    validate_arguments(mcat, email, input_url, output_url, shasta_version, shasta_config, shasta_cli_opts, domain)

    mccloud_api = f"https://{domain}"
    inputs = {
        "mcat": mcat,
        "email": email,
        "input_urls": map(generate_presigned_input_url, input_url),
        "output_url": generate_presigned_output_url(output_url),
        "shasta_version": shasta_version,
        "shasta_ref": "",  # not currently supported in the CLI
        "shasta_config_options": shasta_cli_opts,
        "shasta_config_preset": shasta_config,
    }

    res = requests.post(f"{mccloud_api}/submit", json=inputs)
    if res.status_code != requests.codes.ok:
        raise McCloudSubmitJobFailure(res.json())

    job_id = res.json()["job_id"]
    return job_id


def get_job_log(domain: str, job_id: str) -> str:
    mccloud_api = f"https://{domain}"

    res = requests.get(f"{mccloud_api}/jobs/{job_id}/monitor")
    logs = res.text.split("\n")
    return logs


def tail_job_log_(domain: str, job_id: str) -> None:
    click.echo(f"Tailing job logs for {job_id}...")
    while True:
        logs = get_job_log(domain, job_id)
        click.echo(logs)
        time.sleep(1)


def validate_arguments(mcat, email, input_url, output_url, shasta_version, shasta_config, shasta_cli_opts, domain):
    raise click.ClickException("launch-job is not yet implemented.")


"""
    mccloud_api = f"https://{os.environ['DOMAIN_NAME']}"
    common_inputs = {
        "mcat": os.environ["MCCLOUD_ACCESS_TOKEN"],
        "email": "akislyuk+mccloud-system-test@chanzuckerberg.com",
        "input_urls": [
            "s3://mccloud-dev/r94_ec_rad2.181119.60x-10kb.fasta.gz"
        ],
        "output_url": "s3://mccloud-dev/system-test-output",
        "shasta_version": "0.7.0",
        "shasta_ref": "",
        "shasta_config_options": " ",
        "shasta_config_preset": "Nanopore-Jun2020"
    }

    def call_mccloud(self, inputs):
        res = requests.post(f"{self.mccloud_api}/submit", json=inputs)
        if res.status_code != requests.codes.ok:
            raise McCloudJobFailed(res.json())

        job_id = res.json()["job_id"]
        sys.stderr.write(f"Waiting for job {job_id}...")
        sys.stderr.flush()
        for iteration in range(0, 600):
            res = requests.get(f"{self.mccloud_api}/jobs/{job_id}/monitor")
            logs = res.text.split("\n")
            for i, line in enumerate(logs):
                if line == "status: SUCCEEDED":
                    return
                elif line == "status: FAILED":
                    raise McCloudJobFailed(logs[i + 1])
            sys.stderr.write(".")
            sys.stderr.flush()
            time.sleep(1)
"""
