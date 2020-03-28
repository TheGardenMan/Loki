create table post_details (user_id text,post_id integer,post_location geography,post_time timestamptz,CONSTRAINT same_user_same_post_id_This_will_not_happen PRIMARY KEY(user_id,post_id));
-- Trunc django table which stores user details,passwords,etc.
truncate auth_user restart identity cascade;
select user_id from auth_user where username=''