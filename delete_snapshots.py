import boto3
from datetime import datetime, timedelta

region = 'us-west-2'
retention_days = 90
delete_before_date = datetime.now() - timedelta(days=retention_days)
ec2_client = boto3.client('ec2', region_name=region)
response = ec2_client.describe_snapshots(OwnerIds=['self'])
count = 0
total_size=0
for snapshot in response['Snapshots']:
        snapshot_date = (snapshot['StartTime']).replace(tzinfo=None)
        snapshot_description = snapshot['Description']
        snapshot_size = snapshot['VolumeSize']
        if snapshot_date < delete_before_date:
            if 'Created' in snapshot_description or 'Copied' in snapshot_description:
                  print('Eliminando \t', snapshot['SnapshotId'], '\t', snapshot_date, '\t',snapshot_size, '\t',snapshot_description)
                  count = count + 1
                  total_size=total_size+snapshot_size
#            comment ec2_client.delete_snapshot(SnapshotId=snapshot['SnapshotId'])
print ('Se eliminaron ', count, 'snapshots y ', total_size, 'GB')   
#print('Proceso de eliminación de snapshots  completado.')
