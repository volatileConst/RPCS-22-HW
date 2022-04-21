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

#TODO: implement this
def checkInGeofence(lat, long):
    return 1


# response = loc_client.create_geofence_collection(
#     CollectionName='test',
#     Description='testing right now',
#     # KmsKeyId='testid',
#     #PricingPlan='RequestBasedUsage',
#     #PricingPlanDataSource='string',
#     # Tags={
#     #     'string': 'string'
#     # }
# )

# print(response)

# response = loc_client.list_geofences(
#     CollectionName=collectionName,
#     #NextToken=''
# )

# print(response)


# response = loc_client.batch_evaluate_geofences(
#     CollectionName=collectionName,
#     DevicePositionUpdates=[
#         {
#             'Accuracy': {
#                 'Horizontal': 1
#             },
#             'DeviceId': 'testdevice',
#             'Position': [
#                 84.5, 84.5
#             ],
#             'PositionProperties': {
#                 'string': 'string'
#             },
#             'SampleTime': datetime.datetime(2015, 1, 1)
#         },
#     ]
# )

# print(response)