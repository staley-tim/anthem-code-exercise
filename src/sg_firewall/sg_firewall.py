import boto3
import iptc
import requests

def get_instance_id() -> str:
    response = requests.get('http://169.254.169.254/latest/meta-data/instance-id')
    instance_id = response.text
    return instance_id

def get_instance_security_groups(instance_id:str) -> dict:
    ec2 = boto3.client('ec2')
    response = ec2.describe_instances(InstanceIds=[instance_id])
    instances = response['Reservations'][0]['Instance']
    if len(instances) == 0:
        raise ValueError(f"Instance ID {instance_id} not found")
    security_groups = [sg['GroupId'] for sg in instances[0]['SecurityGroups']]
    return security_groups

def modify_firewall_rule(sg_id:str, port:int, cidr:str) -> None:
    ec2 = boto3.client('ec2')
    IpPermissions=[
        {
            'IpProtocol': 'tcp',
            'FromPort': port,
            'ToPort': port,
            'IpRanges': [{'CidrIp': cidr}]
        }
    ]
    response = ec2.authorize_security_group_ingress(GroupId=sg_id, IpPermissions=IpPermissions)
    return response