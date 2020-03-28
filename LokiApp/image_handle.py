from __future__ import division 
from PIL import Image
import os
# directly importing from this folder
# If you put like "import db_handle",django says db_handle not found.
# If put like "from . import db_handle" ,this image_handle.py will thorw error (if you run separately(Ctrl+B).But we're not running it separately.So do like below)
from . import db_handle
import imagehash 
from io import BytesIO
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
image_storage_folder = os.path.join(BASE_DIR, 'image_storage')


def cropper(image,username):
		# Params
		width,height=image.size[0],image.size[1]
		cropStartX=0
		cropStartY=0
		cropEndX=0
		cropEndY=0
		cropHeight=height
		cropWidth=width
		# buff=BytesIO() do not remove.Useful for reference
	# Width adjustment
		if width<320:
			width=320
			image=image.resize((width,height))
	# Crop to keep the aspect ratio between 1.91:1 to 4:5
	#If aspect ratio less than 1.91:1
			# image.save(buff, 'JPEG', quality=100) do not remove.Useful for reference
		should_crop=False
		if height*1.91<width:
			should_crop=True
			cropWidth=height*1.91
			cropStartX=int((width/2)-(cropWidth/2))
			cropStartY=0
			cropEndX=int(cropStartX+cropWidth)
			cropEndY=height #Usually it's cropStartX+heightOfRequiredArea.Here cropStartX is 0 and we need full height.So..
		elif width*5<height*4:
			should_crop=True
			cropHeight=int((width*5)/4)
			cropStartX=0
			cropStartY=int((height/2)-(cropHeight/2))
			cropEndX=width #See comment of cropEndX
			cropEndY=int(cropStartY+cropHeight)
		if should_crop:
			print("[Information] Cropping file  "+username)
			image=image.crop((cropStartX,cropStartY,cropEndX,cropEndY))
		return image

def resizer(image,username):
		# If image is too big (rare case),resize it to 1080,1350 range, , without affecting aspect ratio
		width,height=image.size[0],image.size[1]
		if width>1080 or height>1350:
			print("[Warning] resizing "+username+" since it's too big")
			new_width=width
			new_height=height
			if width>height:
				new_width=1080
				new_height=int(new_width/(width/height))
			elif height>width:
				new_height=1350
				new_width=int(new_height/(height/width))
			else:#If it's a big square image
				new_width=1080
				new_height=1080
			image=image.resize((new_width,new_height))
		return image
			# print(image.size[0])
			# All image processing is done above ^

def add_to_db_disk(image,username,longitude,latitude):
	# temp_bytes=BytesIO()
	# image.save(temp_bytes,'JPEG',quality=50)
	isError,user_id,post_id=db_handle.add_post_to_db(username,longitude,latitude)
	if isError==None:
		image_path=''.join([image_storage_folder,"\\",str(user_id),"\\",str(post_id),".jpg"])
		# print(image_path)
		image.save(image_path,'JPEG',quality=50)
		# redis_handle.add_to_redis_feed(hash_of_image,temp_bytes.getvalue())
		return True,isError
	else:
		print("Error while DB")
		return False,isError

def clean_and_store(image_received,username,longitude,latitude):
	# **Loading the image and Checking 1.whether the image is valid file
	image="blah"
	isValidImage="xxx"
	try:
		image=Image.open(image_received)
	except Exception as e:
		print("[Failure] Corrupted file :username "+username)
		print(e)
		isValidImage=False
	if isValidImage==False:
		print("[Failure] Skipping the file  :user is ",username,"-->is_valid_image=",isValidImage)
		return False #DND 
	image=cropper(image,username)
	image=resizer(image,username)
	image=image.convert('RGB')
	status,error= add_to_db_disk(image,username,longitude,latitude)
	if(error!=None):
		print("[Fatal]",error)
	return status #DND Affects upload_done.html
