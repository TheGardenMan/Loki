# import psycopg2
# isError=False
# cursor="blah"

# try:
# 	connection = psycopg2.connect(user = "postgres",
# 								  password = "jaxtek",
# 								  host = "127.0.0.1",
# 								  port = "5432",
# 								  database = "postgres")
# 	cursor = connection.cursor()

# except (Exception, psycopg2.Error) as error :
# 	print ("Error while connecting to PostgreSQL", error)
# 	isError=True

import psycopg2
import os
isError=False
cursor="blah"
DATABASE_URL = os.environ['DATABASE_URL']
try:
	connection = psycopg2.connect(DATABASE_URL,sslmode='require')
	cursor = connection.cursor()

except (Exception, psycopg2.Error) as error :
	print ("Error while connecting to PostgreSQL", error)
	isError=True

def get_nearby_posts(longitude,latitude,pageNo,user_id=0,post_id=0):
	# Offset is NOT used here.Remove it.
	offset=pageNo
	offset=int(offset)-1 #If pageNo is 2,we should skip first "10" images.And offset 0 doesn't produce an error
	offset=offset*10
	if pageNo==1: #if initial req.. user_id,post_id won't be passed .doesn't matter
		cursor.execute("select user_id,post_id from post_details where ST_DWithin(post_location,ST_MakePoint(%s,%s)::geography,100000) order by post_time desc limit 10 offset %s ",(longitude,latitude,offset,))
	else:
		print(user_id,post_id," up")
		# cursor.execute("select user_id,post_id from post_details where ST_DWithin					(post_location,ST_MakePoint(%s,%s)::geography,10000) and post_time<(select post_time from post_details where user_id=%s and post_id=%s)						order by post_time desc limit 10 offset %s ",(longitude,latitude,user_id,post_id,offset,))
		# Dont put offset here.Since we select NEXT n posts based on TIMESTAMP,we dont need offset at all.
		cursor.execute("select user_id,post_id from post_details where ST_DWithin					(post_location,ST_MakePoint(%s,%s)::geography,100000) and post_time<(select post_time from post_details where user_id=%s and post_id=%s)						order by post_time desc limit 10",(longitude,latitude,user_id,post_id,))

	x=cursor.fetchall()
	user_ids_and_post_ids=[]
	# user_ids_and_post_ids=[[user_id,post_id],[user_id,post_id],.......]
	# Don't need to do the below thing.Because tuples can be accessed in the same as way lists.Did it.So left it.
	# Converting to 2d list from a 2d list which contains tuples inside
	for n,e in enumerate(x):
		an_user_id_and_a_post_id=[]
		an_user_id_and_a_post_id.insert(0,e[0])
		# str 'coz we need strings for ''.join()
		an_user_id_and_a_post_id.insert(1,str(e[1]))
		user_ids_and_post_ids.insert(n,an_user_id_and_a_post_id)
	print(user_ids_and_post_ids)
	return user_ids_and_post_ids

# get_nearby_posts(80.2707184,13.082680199999999,1,2,2)


def add_post_to_db(username,longitude,latitude):
	try:
		cursor.execute("select id from auth_user where username=%s",(username,))
		user_id=cursor.fetchone()
		user_id=f"{user_id[0]}"
		print("User id",user_id)
		cursor.execute("select max(post_id) from post_details where user_id=%s",(user_id,))
		post_id=cursor.fetchone()
		post_id=f"{post_id[0]}"
		if post_id=="None":
			post_id=0
		post_id=int(post_id)+1
		print("post_id ",post_id)
		print(longitude)
		print(latitude)
		cursor.execute("insert into post_details(user_id,post_id,post_location,post_time) values(%s,%s,ST_MakePoint(%s,%s),current_timestamp )",(user_id,post_id,longitude,latitude,))
		connection.commit()
		return None,user_id,post_id
	except Exception as e:
		connection.rollback()
		return e,"no user_id due to error","no post_id due to error"
