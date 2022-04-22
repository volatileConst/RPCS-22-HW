import boto3
import time
from boto3.dynamodb.conditions import Key, Attr
from decimal import Decimal
import json
import datetime

loc_client = boto3.client('location')
collectionName = 'dangerous_location'
BOUND_DIM = 0.1

def putGeofence(lat, long):
    
    response = loc_client.put_geofence(
        CollectionName = collectionName,
        GeofenceId     = str(long) + str(lat),
        Geometry = {
            'Polygon': [
                [
                    [
                        long, lat
                    ],
                    [
                        long-BOUND_DIM,lat
                    ],
                    [
                        long-BOUND_DIM,lat-BOUND_DIM
                    ],
                    [
                        long,lat-BOUND_DIM
                    ],
                    [
                        long, lat
                    ],
                ],
            ]
        }
    )

    return response

#TODO: write this code
def checkInGeofence(lat, long):
    
    response = loc_client.batch_evaluate_geofences(
    CollectionName=collectionName,
    DevicePositionUpdates=[
        {
            'Accuracy': {
                'Horizontal': 1
            },
            'DeviceId': 'testdevice',
            'Position': [
                long, lat
            ],
            'PositionProperties': {
                'string': 'string'
            },
            'SampleTime': datetime.datetime(2022, 1, 1)
        },
    ]
    )
    
    return 1