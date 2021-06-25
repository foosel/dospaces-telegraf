import datetime
import os
import sys

import boto3
from dotenv import load_dotenv

load_dotenv()

SPACES_REGION=os.getenv("SPACES_REGION")
SPACES_BUCKET=os.getenv("SPACES_BUCKET")
SPACES_PREFIX=os.getenv("SPACES_PREFIX")
SPACES_KEY=os.getenv("SPACES_KEY")
SPACES_SECRET=os.getenv("SPACES_SECRET")

session = boto3.session.Session()
client = session.client(
    's3',
    region_name=SPACES_REGION,
    endpoint_url=f"https://{SPACES_REGION}.digitaloceanspaces.com",
    aws_access_key_id=SPACES_KEY,
    aws_secret_access_key=SPACES_SECRET
)

response = client.list_objects(Bucket=SPACES_BUCKET, Prefix=SPACES_PREFIX)
contents = sorted(response.get("Contents", []), key=lambda x: x["LastModified"], reverse=True)
if not len(contents):
    print("Got no results!", file=sys.stderr)
    sys.exit(-1)

latest = contents[0]

name = latest["Key"]
lastmodified = latest["LastModified"]
size = latest["Size"]

difference = datetime.datetime.now(datetime.timezone.utc) - lastmodified
hours = difference.total_seconds() / 3600

print(f"latest_s3_file s3=digitalocean,region={SPACES_REGION},bucket={SPACES_BUCKET},prefix={SPACES_PREFIX} name={name},lastmodified={lastmodified.timestamp()},size={size},hoursago={hours}")