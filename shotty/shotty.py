import boto3
import click

session = boto3.Session(profile_name='shotty')
ec2 = session.resource('ec2')


# ---------- helper function to retrieve instance collection objects
def filter_instances(project):
    res_instances = []

    if project:
        filters = [{'Name':'tag:Project', 'Values':[project]}]
        res_instances = ec2.instances.filter(Filters=filters)
    else:
        res_instances = ec2.instances.all()

    return res_instances


@click.group()
def cli():
    ''' Shotty manages snapshots. '''


# ---------- SNAPSHOT COMMANDS ----------
@cli.group('snapshots')
def snapshots():
    ''' Commands for snapshots. '''


@snapshots.command('list')
@click.option('--project', default=None,
              help="Volumes attached to project's EC2 instance. ")
def list_snapshots(project):
    ''' Lists snapshots of volumes for the project. '''
    instances = filter_instances(project)

    for i in instances:
        for v in i.volumes.all():
            for s in v.snapshots.all():
                print(", ".join((
                    s.id,
                    v.id,
                    s.state,
                    s.progress,
                    s.start_time.strftime("%c")
                )))

    return


# ---------- VOLUMES COMMANDS ----------
@cli.group('volumes')
def volumes():
    ''' Commands for volumes. '''


@volumes.command('list')
@click.option('--project', default=None,
              help="Only volumes for project (tag Project:<name>)")
def list_volumes(project):
    ''' List volumes attached to EC2 instances for the given project. '''
    instances = filter_instances(project)

    for i in instances:
        for v in i.volumes.all():
            print(", ".join((
                v.id,
                i.id,
                v.state,
                str(v.size) + "GiB",
                v.encrypted and "Encypted" or "Not Encrypted"
            )))

    return


# ---------- INSTANCE COMMANDS ----------
@cli.group('instances')
def instances():
    ''' Commands for instances. '''


@instances.command('snapshot')
@click.option('--project', default=None,
              help="Create snapshots of all instances.")
def create_snapshots(project):
    ''' Create snapshots of all instances. '''
    instances = filter_instances(project)

    for i in instances:
        print("Stopping instance {0}...".format(i.id))
        i.stop()
        i.wait_until_stopped()

        for v in i.volumes.all():
            print("Creating snapshot of {0}".format(v.id))
            v.create_snapshot(Description="Created by snapshot-manager")

        print("Starting instance {0}...\n".format(i.id))
        i.start()
        i.wait_until_running()

    print("Snapshots completed.")

    return


@instances.command('list')
@click.option('--project', default=None,
              help="Only instances for project (tag Project:<name>)")
def list_instances(project):
    '''
    Prints all EC2 instances to the console.
    For each instance prints: id, type, AZ, state, dns name.
    '''
    instances = filter_instances(project)

    for i in instances:
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
    instances = filter_instances(project)

    for i in instances:
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
    instances = filter_instances(project)

    for i in instances:
        print("Starting instance {0}...".format(i.id))
        i.start()

    return


if __name__ == '__main__':
    cli()
