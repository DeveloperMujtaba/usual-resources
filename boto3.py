#!/usr/bin/env python
from datetime import datetime, timedelta, timezone
import boto3
ec2 = boto3.resource('ec2')
cl = boto3.client('ec2')
count=0
def lambda_handler(event, context):
    ec2=boto3.client('ec2')
# List (ec2.Snaphot)
snapshots = ec2.snapshots.filter(OwnerIds=['self'])
def if_associated_to_ami(client, snapshot_id):
    img = client.describe_images(Filters=[{'Name': 'block-device-mapping.snapshot-id', 'Values': [snapshot_id]}])
    try:
        ami_id = img['Images'][0]['ImageId']
        #print("Snapshot(" + snapshot_id + ") is associated to image(" + ami_id + "). Return True")
        return True
    except IndexError:
        #print("Snapshot(" + snapshot_id + ") is not associated to any image. Return False")
        return False
for snapshot in snapshots:
    if if_associated_to_ami(cl, snapshot.snapshot_id):
        print('Unabble to delete Snapshot with Id = {}. Snapshot is in used! '. format(snapshot.snapshot_id))
    else:
        start_time = snapshot.start_time
        delete_time = datetime.now(tz=timezone.utc) - timedelta(days=90)
        if delete_time > start_time:
            #snapshot.delete()
            print('Snapshot with Id = {} is deleted '. format(snapshot.snapshot_id))
    count+=1
    if count == 1000:
        break

