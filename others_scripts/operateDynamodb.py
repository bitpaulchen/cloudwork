import json
import uuid
import boto3


def lambda_handler(event, context):
    # 1. get table name
    rawPath = event["rawPath"]
    if 'Comment' in rawPath:
        tableName = 'comments'
    elif 'Article' in rawPath:
        tableName = 'articles'
    else:
        return []
    dynamo_tb = boto3.resource('dynamodb').Table(tableName)

    print(tableName, rawPath)

    # 获取方法
    if rawPath in ("/getComment", "/getArticle"):
        ids = event["queryStringParameters"]["ids"]
        return getOnes(dynamo_tb, ids)
    if rawPath in ("/postComment", "/postArticle"):
        body = json.loads(event['body'])["body"]
        uid = createOne(dynamo_tb, body)
        return {"uid": uid}
    return []


def getOnes(dynamo, idstr):
    if not idstr:
        return []
    commentids = idstr.split(',')
    if len(commentids) <= 1:
        resp = dynamo.get_item(Key={'id': idstr})
        if "Item" in resp:
            return [resp["Item"]]
        else:
            return []

    resp = dynamo.scan(
        ScanFilter={'id': {
            'AttributeValueList': commentids,
            'ComparisonOperator': 'IN'}
        })

    return resp.get("Items", [])


def createOne(dynamo, body):
    uid = str(uuid.uuid1())
    dynamo.put_item(Item={
        'id': uid,
        'body': body
    })

    return uid



