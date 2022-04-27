import pymysql.cursors
# Connect to the database
import uuid
import random
import time
import string

def randomword(length):
    letters = string.ascii_lowercase + "        "
    return ''.join(random.choice(letters) for i in range(length))



AWS_RDS_HOST = "flaskapp.cce4qvbm0cza.us-east-1.rds.amazonaws.com"
AWS_RDS_NAME = "root"
AWS_RDS_PWD = "12345678"
AWS_RDS_DATABASE = "cloudwork"

#
# AWS_RDS_HOST = "localhost"
# AWS_RDS_NAME = "root"
# AWS_RDS_PWD = "root"
# AWS_RDS_DATABASE = "cloudwork"


connection = pymysql.connect(host=AWS_RDS_HOST,
                             user=AWS_RDS_NAME,
                             password=AWS_RDS_PWD,
                             database=AWS_RDS_DATABASE,
                             cursorclass=pymysql.cursors.DictCursor)
cursor = connection.cursor()



import boto3
ACCESS_KEY = "ASIA2ZZJ23VSLSFCVKEK"
SECRET_KEY = "BquhbOF0uurQA51r/cIgS5AL3Y5U8QZtAGX1ljkx"
SESSION_TOKEN = "FwoGZXIvYXdzEPT//////////wEaDH0w2XloS8xfKW9hNiLNAW7/SfOpRlCDSi84XAiK4/uxTOxKrUW67W7r4Eu7L2efdyw1jhP0M4T6AF8UNYExsLa86vrhiy06KluVvERFs/d9mmSzP1tMe5ltKRTIwrG2l4El0Fye0k68ITV08M3+XX+GLrDQytDONMzCdv3SNsSIj0EUoRNK9cjGeqPGhojjXFmC4ZxW1skOY7i+a9vKKDozXZNEd9r5NinYLCFds/D6Zv/clRUPu4lU7t2b5CjX6coPKY4h3douIHxyzm0huQqqFCLnAC3xB45CSBQo4qidkwYyLVYPbhFFM0g3nuFrMH8lujGmZEAjjfMkpibc9q+E9cVEsZse9r5vX5X9Q8eEvw=="
REGION = "us-east-1"


dynamodb_resource = boto3.resource('dynamodb', aws_access_key_id=ACCESS_KEY,
aws_secret_access_key=SECRET_KEY,
aws_session_token=SESSION_TOKEN)
dynamodb_client = boto3.client('dynamodb', aws_access_key_id=ACCESS_KEY,
aws_secret_access_key=SECRET_KEY,
aws_session_token=SESSION_TOKEN)


# 1. create 50 users to user table
# default pass: 123456
DEFAULT_PASSWORD_HASH = "pbkdf2:sha256:260000$pv3SocLQh5HY4TDz$565accf960ec407b582d1bb494c22269cd56b88a4748d1b8179c196bfcd83742"
vals = [["user%s"%i, DEFAULT_PASSWORD_HASH] for i in range(50)]
user_insert = "INSERT INTO user (username,`password_hash`) VALUES "
user_insert+=",".join(["('%s','%s' )" % (i[0], i[1])for i in vals])

cursor.execute(user_insert)
connection.commit()

cursor.execute("select id from user")
userids = [item['id'] for item in  cursor] # get ids to insert to posts


articles_db_table.get_item(Key={'id': '67011d4a-c55e-11ec-9cfd-9801a7a5e02d'})

# 2. insert into post
articles_db_table  = dynamodb_resource.Table("articles")
# dynamodb_client.delete_table(TableName="articles")
res = articles_db_table.scan()
fake_posts = open('fakedata.csv').readlines()

fake_posts = [i.split("#") for i in fake_posts if len(i.split("#"))>1]
# insert_post_mysql = []
# for post in fake_posts:
#     title, body = post[0], post[1]
#     post_uid = str(uuid.uuid1())
#     # put dynamodb
#     articles_db_table.put_item(
#         Item={
#             'id': post_uid,
#             'body': body})
#     insert_post_mysql.append([title,post_uid, time.strftime('%Y-%m-%d %H:%M:%S'), random.choice(userids)])
#
# or

puids = [i["id"] for i in res["Items"]]
insert_post_mysql = [[post[0],random.choice(puids), time.strftime('%Y-%m-%d %H:%M:%S'), random.choice(userids) ]for post in fake_posts]
post_insert  = "INSERT INTO post (title,post_uuid,timestamp, user_id) VALUES "
post_insert+=",".join(["('%s','%s', '%s', %s )" % (i[0], i[1], i[2], i[3])for i in insert_post_mysql])
cursor.execute(post_insert)
connection.commit()

#
# cursor.execute("select post_uuid from post")
# puids = [item['post_uuid'] for item in  cursor]
#
# resp = articles_db_table.scan(
#         ScanFilter={'id': {
#             'AttributeValueList': puids,
#             'ComparisonOperator': 'IN'}
#         })
#
# updatesql = "update post set short_desc= case post_uuid"
# casewhen = []
# for item in resp["Items"]:
#     puid, body = item["id"], item["body"]
#     casewhen.append(" when '%s' then '%s' " % (puid, body[:20]))
#
#
# updatesql += " ".join(casewhen)
#
# updatesql+=" end "
#
# updatesql += "where post_uuid in (%s)" % (",".join("'%s'"%(i)for i in puids))
#



# 3. inisert into comment
cursor.execute("select id from user")
userids = [item['id'] for item in  cursor] # get ids to insert to posts


cursor.execute("select id from post")
postids = [item['id'] for item in  cursor]

insert_comment_mysql = [[random.choice(userids),randomword(30), time.strftime('%Y-%m-%d %H:%M:%S'), random.choice(postids)] for _ in range(1000)]
comment_insert  = "INSERT INTO comment (user_id,body,timestamp, post_id) VALUES "
comment_insert+=",".join(["(%s,'%s', '%s', %s )" % (i[0], i[1],i[2], i[3])for i in insert_comment_mysql])
cursor.execute(comment_insert)
connection.commit()



# 4. insert into follows
insert_follow_mysql = [[random.choice(userids),random.choice(userids)] for _ in range(1000)]
insert_follow  = "INSERT INTO followers (follower_id,followed_id) VALUES "
insert_follow +=",".join(["(%s,%s )" % (i[0], i[1])for i in insert_follow_mysql])
cursor.execute(insert_follow)
connection.commit()













