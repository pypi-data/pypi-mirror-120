import click
from click_params import EMAIL


@click.command(context_settings=dict(max_content_width=512))
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
    multiple=True,
    help="S3 URL which will be presigned to allow WRITE (output) access.",
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
def submit_job(mcat, email, input_url, output_url, shasta_version, shasta_config, shasta_cli_opts):
    raise click.ClickException("launch-job is not yet implemented.")


"""
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
