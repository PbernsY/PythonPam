import os

def remove_folder():
	if os.path.exists("../images") == True:

		folders = [f for f in os.listdir("../images")] # list folders

		for f in folders:
			path = os.path.join("../images",f)		
			
		while len(os.listdir(path)) != 0:
			for f in os.listdir(path):
				delete = os.path.join(path,f)		
				os.remove(delete)
		os.rmdir(path)
		os.rmdir("../images")

	return False

