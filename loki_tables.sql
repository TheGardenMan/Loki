create table post_details (user_id text,post_id integer,post_location geography,post_time timestamptz,CONSTRAINT same_user_same_post_id_This_will_not_happen PRIMARY KEY(user_id,post_id));
-- Trunc django table which stores user details,passwords,etc.
truncate auth_user restart identity cascade;
select user_id from auth_user where username='';
-- To convert raw hex from sql into coordinates.
ST_X('0101000020E61000003B9B447353115440B00D260F552A2A40'::geometry) as lon, ST_Y('0101000020E61000003B9B447353115440B00D260F552A2A40'::geometry) as lat;

select * from post_details where post_time<(select post_time from post_details where user_id=%s and post_id=%s);