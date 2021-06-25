# 🔨 dospaces-telegraf

A small Python tool to fetch latest file from a Digital Ocean Spaces (S3) container and export it in influx compatible format. Useful for verifying backup exports working correctly via telegraf's `exec` input.

## Requirements

  * Python 3

## Installation

```
git clone https://github.com/foosel/dospaces-telegraf
cd dospaces-telegraf
virtualenv --python=python3 venv
venv/bin/pip install -r requirements.txt
```

## Configuration

  * `cp .env.sample .env`
  * Adjust `.env` as needed and save:
    * `SPACES_REGION`, `SPACES_BUCKET`: Can be read from your bucket URL, e.g. `https://<bucket>.<region>.digitaloceanspaces.com`
    * `SPACES_PREFIX`: Should be the sub dir in your bucket to check, without leading `/`
    * `SPACES_KEY`, `SPACES_SECRET`: See https://cloud.digitalocean.com/account/api/tokens

## Usage

Basic command line usage:

    venv/bin/python dospaces-telegraf.py

Example output:

    latest_dospaces_file,region=ams3,bucket=mybucket,prefix=some/prefix name="some/prefix/backup.tar.gz",lastmodified=1624610715.382,size=3103508917,hoursago=2.0207358125

Example telegraf configuration:

``` conf
[[inputs.exec]]
  commands = [
    "/dospaces-telegraf/venv/bin/python /dospaces-telegraf/dospaces-telegraf.py"
  ]
  timeout = "5s"
  interval = "10m"
  data_format="influx"
```

To monitor backup creation you might want to create alerts for `hoursago` and/or `size` in your alerting tool of choice.
