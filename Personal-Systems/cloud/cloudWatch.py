import boto3

event_client = boto3.client('logs')
logGroup     = "/aws/events/danger_loc"
logStream    = "danger_loc"

def cur_inside_geofence(prevTime):

    response = client.get_log_events(
        logGroupName=logGroup,
        logStreamName=logStream,
        startTime=0,
        endTime=curTime,
        limit=1,
        startFromHEAD=False
    )

    return response["message"] == 'ENTER'