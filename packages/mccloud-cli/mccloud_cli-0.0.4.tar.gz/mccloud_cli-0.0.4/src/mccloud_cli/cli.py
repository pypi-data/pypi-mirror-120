import click

from .urls import generate_S3_presigned_url_cli
from .jobs import submit_job_cli


@click.group(name="mccloud_cli")
@click.version_option()
def cli():
    pass


cli.add_command(generate_S3_presigned_url_cli)
cli.add_command(submit_job_cli)
