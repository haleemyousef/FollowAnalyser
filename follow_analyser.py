import os, time, sys, datetime
from io import StringIO

import instaloader
from pwinput import pwinput
from tqdm import tqdm

# import asyncio   \
# import aiohttp   ,`-> for future improvements on pfp download speed
# import aiofiles /

logo = """

	{OOO}   {OOO}           pua  					
	 I8I     I8I            :11  					
	 I8I     I8I   .oooo.    11   .ooooo.   .ooooo.  oooooooo.oooooo.	
	 I8I8I8I8I8I  `P  )88b   11  d88' `88b d88' `88b `88b' `88b' `88b	
	 I8I     I8I   .oP"888   11  888ooo888 888ooo888  888   888   888	
	 I8I.   .I8I  d8(  888   11. 888    .o 888    .o .888   888   888	
	dI8Ib   dI8Ib `Y888""8o  OOO `Y8bod8P' `Y8bod8P' 6888b  888  6888b	

				    Coded by haleemyousef			
	"""


intro = """
This script extracts the list of followers and followings on your Instagram account and creates HTML files containing:
non-follower followings / non-followed followers / followed followers (friends).\n
"""


# DEPRECATED
# Import packages, and if they don't exist it will install them then import them.
# Normal VSCODE made stuff irritating with its reportUndefinedVariable and disabled Intellisense, so I abandoned the function.
# If you want to use it with VSCODE and don't mind disabling Intellisense then you should include this comment in your file (remove '//' for it to work):
# pyright: reportUndefinedVariable=false //

# def install_and_import(packages):
# 	import importlib, sys, subprocess
# 	for package in packages:
# 		try:
# 			importlib.import_module(package)
# 		except ModuleNotFoundError:
# 			print(f"installing {package}:\n")
# 			subprocess.run([sys.executable, "-m", "pip", "install", package])
# 		finally:
# 			globals()[package] = importlib.import_module(package)

# DEPRECATED
# Looks up the directory named after the username entered and overwrites its contents after taking permission..
# Replaced by creating directory with datetime included in name (although the final result wasn't as clean as I would've liked it to be).

# def does_user_exist():
# 	if os.path.isdir(username):
# 		delete_prompt = input("User files already exist! Do you want to delete them? (Y/n): ").lower()
# 		if delete_prompt == "y":
# 			import shutil
# 			shutil.rmtree(username)
# 		elif delete_prompt == "n":
# 			print("Thank you for your time!")
# 			sys.exit()
# 		else:
# 			print("Invalid entry!")
# 			does_user_exist() # recursive if empty input


def t(para=None): # timing function. 
	if para == None: # start timing (Needs to be assigned to a variable (eg. t_ )).
		return time.perf_counter()
	else: # end timing and print value.
		print(f" Took {str(round(time.perf_counter() - para, 4))} seconds.", end='')


def write_html(profile_name, file_name, i):
	if not os.path.isfile(USER_FOLDER + file_name): # Check if HTML does not exist.
		with open(USER_FOLDER + file_name, "w") as file: # Start HTML document.
			file.write("""
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
* {
  box-sizing: border-box;
}

/* Container for flexboxes */
.row {
  display: flex;
  flex-wrap: wrap;
  border-style: solid;
  border-width: 1px;
}

/* Create four equal columns */
.column {
  flex: 25%;
  padding: 15px;
  border-style: solid;
  border-width: 1px;
  text-align: center;
  background-color: #eee;
}

h1 { font-family: Cambria, Georgia, serif; font-size: 24px; font-style: normal; font-variant: normal; font-weight: 700; line-height: 26.4px; }
h3 { font-family: Cambria, Georgia, serif; font-size: 14px; font-style: normal; font-variant: normal; font-weight: 700; line-height: 15.4px; }
p { font-family: Cambria, Georgia, serif; font-size: 15px; font-style: normal; font-variant: normal; font-weight: 400; line-height: 20px; }
blockquote { font-family: Cambria, Georgia, serif; font-size: 21px; font-style: normal; font-variant: normal; font-weight: 400; line-height: 30px; }
pre { font-family: Cambria, Georgia, serif; font-size: 13px; font-style: normal; font-variant: normal; font-weight: 400; line-height: 18.5714px; }

img {
  height: 200px;
  width: 200px
}

/* On screens that are 992px wide or less, go from four columns to two columns */
@media screen and (max-width: 992px) {
  .column {
    flex: 33%;
  }
}

@media screen and (max-width: 746px) {
  .column {
    flex: 50%;
  }
}

/* On screens that are 500px wide or less, make the columns stack on top of each other instead of next to each other */
@media screen and (max-width: 500px) {
  .row {
    flex-direction: column;
  }
}
</style>
</head>
<body>

<h2>InstaFollow</h2>
<p>
<strong>
Author : Haleem Yousef<br />
Email  : <a href='mailto: haleemyousef01@gmail.com' target='_blank'>haleemyousef01@gmail.com<a/><br />
Github : <a href='https://github.com/haleemyousef' target='_blank'>https://github.com/haleemyousef<a/><br />
</strong> 
This project is released under the MIT license. <br /><br />
<strong>Click the picture to be redirected to the corresponding account.</strong><br />
You need to login into your Instagram in this browser before you can view the accounts shown in this page. <br />
This project was built using InstaLoader module, please don't forget to support them (and me!) on GitHub. <br />
</p>

<div class="row">
			""")
	with open(USER_FOLDER + file_name, "a") as file: # List of profiles with clickable profile pics.
		file.write(f"""
	<div class="column">
	<p>{str(i)}. {profile_name}</p>
	<a href='https://www.instagram.com/{profile_name}/' target='_blank'><img src='pfps/{profile_name}.jpg'></a>
	</div>
		""")
def end_html(file_name):
	with open(USER_FOLDER + file_name, "a") as file:
		file.write("""
</div>
</body>
</html>
		""")


def fetch_pfps(all_profiles):
	for profile_name in tqdm(all_profiles):
		try:
			old_stdout = sys.stdout # basically, starting a 'function' that redirects the print output to a variable.
			get_pic_path = StringIO()
			sys.stdout = get_pic_path
			INSTA.download_profilepic(PROFILE(profile_name)) # prints a string, eg. 'example\2021-12-17_02-35-20_UTC_profile_pic.jpg \n'.
			sys.stdout = old_stdout # the end of that 'function', returning to the original state.
			pic_path = get_pic_path.getvalue()
			pic_path = pic_path.replace("\\", "/")
			if pic_path.split(' ')[0].startswith('\n'): # fixing '\nToo many queries' error.
				for item in pic_path.split(' '): 
					if '.jpg' in item: 
						pic_path = item.split('\n')[1]
						break
			os.rename(pic_path.split(' ')[0], f"{USER_FOLDER}/pfps/{profile_name}.jpg") # move pfp to a 'pfps' folder inside USER_FOLDER.
			os.rmdir(profile_name)
		except Exception as err:
			with open(f"{USER_FOLDER}/pfps/pfp_download.log", "a+") as log:
				log.write(f"Error occured for {profile_name}: {err}\n") # go through your logs in case something cheeky happened.
		except KeyboardInterrupt:
			sys.exit("\nSorry for the inconvenience.\nThis functionality can benefit from asynchronous processing.\nIf you would like to contribute please email me on haleemyousef01@gmail.com.\n")	


def main():
	
	global INSTA
	INSTA = instaloader.Instaloader() # Instaloader's main function. used for login, context, profile, and downloadpic.
	

	username = input("Enter your Instagram Username: ").lower()
	while not username: # No empty input
		username = input("Enter your Instagram Username: ").lower()
	
	# does_user_exist() DEPRECATED

	password = pwinput(prompt = "Enter your Instagram Password: ", mask = "*")
	while not password: # No empty input
		password = pwinput(prompt = "Enter your Instagram Password: ", mask = "*")
	

	# Downloading profiles pics is really slow, takes around 8s per pic. Requires upgrade using asyncio.
	pic_download_command = input("Do you want to download profile pics of your followers/followings(It may take a while)? (Y/n): ").lower()
	if pic_download_command == 'y': all_profiles = [] # A comprehensive list of all followers/followings without duplicates.


	print("\nSigning in:", end = '')
	t_ = t()

	try:
		INSTA.login(username, password)
	except instaloader.exceptions.TwoFactorAuthRequiredException:
		try:
			two_factor_code = input("Two factor indentification required!\nEnter the code your received on your phone messages: ")
			INSTA.two_factor_login(two_factor_code)
		except Exception:
			sys.exit("\nError occured!")
	except instaloader.exceptions.InvalidArgumentException:
		sys.exit("\nIncorrect username!")
	except instaloader.exceptions.BadCredentialsException:
		sys.exit("\nIncorrect password!")
	except instaloader.exceptions.ConnectionException:
		sys.exit("\nConnection failed!\nYou might have used the program a bit too much, give it a break & come back later (:")
	except Exception:
		sys.exit("\nError occured!")
	
	global PROFILE
	PROFILE = lambda user: instaloader.Profile.from_username(INSTA.context, user) # very useful for retrieving all sorts of data about any profile.

	t(t_)
	#-----------------------
	#-----------------------
	print("\nListing Followers:", end = '')
	t_ = t()
	followers_list = [follower.username for follower in PROFILE(username).get_followers()]
	t(t_)
	#-----------------------
	print("\nListing Followings:", end = '')
	t_ = t()
	followees_list = [followee.username for followee in PROFILE(username).get_followees()]
	t(t_)
	#-----------------------
	#-----------------------
	print("\nCreating Directory:", end='')
	t_ = t()

	try:
		now = datetime.datetime.utcnow()
		global USER_FOLDER
		USER_FOLDER = username + now.strftime("_%d-%m-%y_%H;%M_UTC") # I really don't like semicolons here, but couldn't find a better substitute.
		os.mkdir(USER_FOLDER)
		os.mkdir(USER_FOLDER + "/pfps") # Otherwise our fetch_pfps function would crash.
	except Exception:
		sys.exit("\nError occured while creating directory!")
		# does_user_exist() DEPRECATED
	t(t_)
	#-----------------------
	#-----------------------
	print("\nWriting HTML files:", end = '')
	t_ = t()

	i = 1 # an incremental variable is used here because of the conditional inside the loop.
	for followee in followees_list:
		if followee not in followers_list:
			write_html(followee, "/non-follower_followings.html", i)
			i += 1
	end_html("/non-follower_followings.html")

	i = 1
	for follower in followers_list:
		if follower in followees_list:
			write_html(follower, "/friends.html", i)
			i += 1
	end_html("/friends.html")

	i = 1
	for follower in followers_list:
		if follower not in followees_list:
			write_html(follower, "/non-followed_followers.html", i)
			i += 1
			if pic_download_command == 'y': all_profiles.append(follower)
	end_html("/non-followed_followers.html")
	i is None

	t(t_)
	#-----------------------
	#-----------------------
	if pic_download_command == 'y':
		all_profiles.extend(followees_list)
		print("\nDownloading profile pics (Ctrl ^C to quit):")
		fetch_pfps(all_profiles)
	#-----------------------
	print("\nTask completed!\nYou may find the information you need saved in a directory called {}".format(USER_FOLDER))


if __name__ == "__main__":

	print(logo)
	print(intro)
	# install_and_import(["instaloader", "pwinput", "tqdm"]) DEPRECATED
	main()
