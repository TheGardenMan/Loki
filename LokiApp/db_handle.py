import psycopg2
isError=False
cursor="blah"

try:
	connection = psycopg2.connect(user = "postgres",
								  password = "jaxtek",
								  host = "127.0.0.1",
								  port = "5432",
								  database = "postgres")
	cursor = connection.cursor()

except (Exception, psycopg2.Error) as error :
	print ("Error while connecting to PostgreSQL", error)
	isError=True


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
