from setuptools import setup

setup(
    name='aws-snapshot-manager',
    version='0.1',
    author='Sarah Donehower',
    description='A tool to manage AWS EC2 snapshots',
    license='GPLv3+',
    packages=['shotty'],
    url='https://github.com/donehower/aws_snapshot_manager',
    install_requires=[
        'click',
        'boto3'
    ],
    entry_points={
        'console_scripts': [
            'shotty=shotty.shotty:cli',
        ],
    },
)
