# aws_demo
Demo to manage EC2 instance snapshots

## About
This is a demo project that uses boto3 to manage EC2 instance snapshots.

## Configuring
shotty uses the configuration file created by the AWS cli.

`aws configure --profile shotty`

## Running
`pipenv run python shotty/shotty.py <command> <--project=PROJECT>`

*command* is list, start, or stop
*project* is optional
