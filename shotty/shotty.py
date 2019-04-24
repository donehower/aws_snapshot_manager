import boto3
import click

session = boto3.Session(profile_name='shotty')
ec2 = session.resource('ec2')


def filter_instances(project):
    res_instances = []

    if project:
        filters = [{'Name':'tag:Project', 'Values':[project]}]
        res_instances = ec2.instances.filter(Filters=filters)
    else:
        res_instances = ec2.instances.all()

    return res_instances


@click.group()
def instances():
    '''
    Commands for instances
    '''


@instances.command('list')
@click.option('--project', default=None,
              help="Only instances for project (tag Project:<name>)")
def list_instances(project):
    '''
    Prints all EC2 instances to the console.
    For each instance prints: id, type, AZ, state, dns name.
    '''
    res_instances = filter_instances(project)

    for i in res_instances:
        tags = {t['Key']: t['Value'] for t in i.tags or []}
        print(', '.join((
            i.id,
            i.instance_type,
            i.placement['AvailabilityZone'],
            i.state['Name'],
            i.public_dns_name,
            tags.get('Project', '<no project name>')
        )))

    return


@instances.command('stop')
@click.option('--project', default=None,
              help="Only instances for the project")
def stop_instances(project):
    '''
    Stops all EC2 instances for a project.
    '''
    res_instances = filter_instances(project)

    for i in res_instances:
        print("Stopping instance {0}...".format(i.id))
        i.stop()

    return


@instances.command('start')
@click.option('--project', default=None,
              help="Only instances for the project")
def start_instances(project):
    '''
    Starts all EC2 instances for a project.
    '''
    res_instances = filter_instances(project)

    for i in res_instances:
        print("Starting instance {0}...".format(i.id))
        i.start()

    return


if __name__ == '__main__':
    instances()
