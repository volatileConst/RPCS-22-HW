import boto3
import time
import csv
from datetime import datetime 
from datetime import timedelta  
from boto3.dynamodb.conditions import Key, Attr
from decimal import Decimal
import json
#import pandas as pd

TABLE_NAME = 'Dangerous_GPS'

def create_table():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.create_table (
        TableName = TABLE_NAME,
        KeySchema = [
            {
                'AttributeName': 'Longitude',
                'KeyType': 'HASH'
            }
            ],
        AttributeDefinitions = [
            {
                'AttributeName':'Longitude',
                'AttributeType': 'N'
            }
            ],
        ProvisionedThroughput={
            'ReadCapacityUnits':10,
            'WriteCapacityUnits':10
        }
    )

def ingestData(path):
    dynamodb = boto3.resource('dynamodb')
    
    table = dynamodb.Table(TABLE_NAME)

    with open(path,'r') as csvfile:
            csvf = csv.reader(csvfile,delimiter=',')
            next(csvf)
            for item in csvf:
                metadata_item={'Index':item[0],'Latitude':item[1],
                                'Longitude':item[2]}
                table.put_item(Item=metadata_item)

def query():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(TABLE_NAME) 

    resp = table.query(

        KeyConditionExpression = 
        Key('Longitude').eq(1)
    )
    print(resp['Items'])

def putSingleItem(item):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(TABLE_NAME)
    item = json.loads(json.dumps(item), parse_float=Decimal)
    table.put_item(Item={
        'invalid1':item[0],
        'invalid2':item[1],
        'accX':item[2],
        'accY':item[3],
        'accZ':item[4],
        'gX':item[5],
        'gY':item[6],
        'gZ':item[7],
        'dist':item[8],
        'bright':item[9],
        'gps_valid':item[10],        
        'Latitude':item[11],
        'Longitude':item[12],
    })

def scan():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(TABLE_NAME) 

    resp = table.scan()
    return resp

def checkInGeofence(lat, long):
    return 1

# num = 1.2

# putSingleItem([-1.2, -1.2, -1.2, -1.2, -1.2, -1.2, -1.2, -1.2, -1.2, -1.2, -1.2, -1.2, -1.2])

# response = scan()['Items']

# print(response)

# response = response[1].values()

# print(response)

# table = list(map(float, response))

# print(table)

# df = pd.DataFrame(table)
# df.transpose()
# print(df)
# df.to_csv('test.csv', index=False, header=True)
