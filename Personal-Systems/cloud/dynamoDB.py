import boto3
import time
import csv
from datetime import datetime 
from datetime import timedelta  
from boto3.dynamodb.conditions import Key, Attr
from decimal import Decimal
import json

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
        'gps_valid':item[0],
        'Latitude':item[1],
        'Longitude':item[2],
        'accX':item[3],
        'accY':item[4],
        'accZ':item[5],
        'gX':item[6],
        'gY':item[7],
        'gZ':item[8],
        'dist':item[9],
        'bright':item[10],
    })

def scan():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(TABLE_NAME) 

    resp = table.scan(
        FilterExpression = Attr('TimeStamp').between("2022-03-07 16:28:52.333156", "2022-03-14 16:28:52.600901")
    )
    print(resp['Items'])

def checkInGeofence(lat, long):
    return 1

#create_table()

#ingestData('results.csv')

#putSingleItem()

#query()
#scan()
