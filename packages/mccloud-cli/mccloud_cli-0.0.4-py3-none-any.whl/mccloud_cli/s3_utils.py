from typing import Tuple, Union

from botocore.exceptions import ClientError


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
