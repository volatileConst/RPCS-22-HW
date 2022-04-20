import boto3
import time
import csv
from datetime import datetime 
from datetime import timedelta  
from boto3.dynamodb.conditions import Key, Attr


def creat_table():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.create_table (
        TableName = 'Test_Phase2',
        KeySchema = [
            {
                'AttributeName': 'Name',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'TimeStamp',
                'KeyType': 'RANGE'
            }
            ],
        AttributeDefinitions = [
            {
                'AttributeName': 'Name',
                'AttributeType': 'S'
            },
            {
                'AttributeName':'TimeStamp',
                'AttributeType': 'S'
            }
            ],
        ProvisionedThroughput={
            'ReadCapacityUnits':10,
            'WriteCapacityUnits':10
        }
    )

def ingestData(path):
    dynamodb = boto3.resource('dynamodb')
    
    table = dynamodb.Table('Test_Phase2')

    with open(path,'r') as csvfile:
            csvf = csv.reader(csvfile,delimiter=',')
            next(csvf)
            for item in csvf:
                metadata_item={'Name':item[0],'TimeStamp':item[1],
                                'Email':item[2]}
                table.put_item(Item=metadata_item)

def putSingleItem():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Test_tickets') 
    for n in range(10):
        Name = datetime.now() + timedelta(days=n)
        timestamp = str(Name)
        table.put_item(Item={
            'Name': 'Michael{}'.format(n),
            'TimeStamp': timestamp
        })

def query():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Test_Phase2') 

    resp = table.query(

        KeyConditionExpression = 
        Key('Name').eq("Michael0")
    )
    print(resp['Items'])

def scan():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Test_Phase2') 

    resp = table.scan(
        FilterExpression = Attr('TimeStamp').between("2022-03-07 16:28:52.333156", "2022-03-14 16:28:52.600901")
    )
    print(resp['Items'])


# creat_table()

# ingestData('results.csv')
query()
# scan()
