# aws_demo
Demo to manage EC2 instance snapshots

## About
This is a demo project that uses boto3 to manage EC2 instance snapshots.

## Configuring
shotty uses the configuration file created by the AWS cli.

`aws configure --profile shotty`

## Running
`pipenv run python shotty/shotty.py <command> <subcommand> <--project=PROJECT>`

*command* is instances  
*subcommand* list, stop, start, snapshot  

*command* is volumes  
*subcommand* list  

*command* is snapshots  
*subcommand* list 

*project* is optional  
