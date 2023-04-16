import boto3

ec2 = boto3.resource('ec2')

instance = ec2.create_instances(
    ImageId='ami-00874d747dde814fa',
    MinCount=1,
    MaxCount=1,
    SecurityGroupIds=['sg-0f4ddeb30997d24f2'],
    InstanceType='t2.micro',
    TagSpecifications=[
        {
            'ResourceType': 'instance',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': 'project-2'
                },
            ]
        },
    ],
)