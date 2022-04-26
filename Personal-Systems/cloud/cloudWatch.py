import boto3
from datetime import datetime
import json

client       = boto3.client('logs')
logGroup     = "/aws/events/AmazonLocationMonitor-dangerous_location"
logStream    = "6951897a-83b2-3bdb-9a5b-80fcba8826b8"

def cur_inside_geofence():

    t0 = datetime(1, 1, 1)
    now = datetime.utcnow()
    seconds = (now - t0).total_seconds()
    ticks = seconds * 10**7
    ticks = int(ticks)

    response = client.get_log_events(
        logGroupName=logGroup,
        logStreamName=logStream,
        startTime=0,
        endTime=ticks,
        limit=1
    )

    response = response['events'][0]['message']
    response = response.split(",")
    return response[8].find('ENTER') != -1

print(cur_inside_geofence())