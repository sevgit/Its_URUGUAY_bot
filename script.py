import praw #reddit
#import pyowm #informaciono meteorologica
import random
import time
import datetime
import traceback #para logear los errores
import unicodedata
#import login #informacion personal para log in del bot

def update_log(id, log_path): #para los comentarios que ya respondi
	with open(log_path, 'a') as my_log:
		my_log.write(id + "\n")

def load_log(log_path): #para los comentarios que ya respondi
	with open(log_path) as my_log:
		log = my_log.readlines()
		log = [x.strip('\n') for x in log]
		return log

def output_log(text): #lo uso para ver el output del bot
	output_log_path = "output_log.txt"
	with open(output_log_path, 'a') as myLog:
		s = "[" +  datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "] "
		s = s + text +  "\n"
		myLog.write(s)

def check_condition(c): #llamaron al bot?
	text = c.body
	uruguay_misspells = ["urugay", 
			     "uraguay",
			     "urogway",
			     "uruguauy",
			     "uruguary",
			     "uruguary"]
	for version in uruguay_misspells:
		if version in text.lower():
			return True

def get_reply():
	replies = [	"Did you mean *Uruguay**?",
				"I'm pretty sure you meant *Uruguay**",
				]
	return random.choice(replies)


print("RUNNING")
if __name__ == "__main__":
	comment_log_path = "log.txt"
	while True:
		try:
			
			output_log("Comenzando el script")
			log = load_log(comment_log_path)
			reddit = praw.Reddit(	client_id = "client_id",
									client_secret = "client_secret",
									password = "bot-password",
									user_agent = "desription",
									username = "bot-username")
			print("Logged to reddit as " + reddit.user.me().name) 						
			output_log("Login to reddit as: " + reddit.user.me().name)
			

			for comment in reddit.subreddit('all').stream.comments():
				if check_condition(comment) and comment.id not in log:
					#output_log("{" + unicodedata.normalize('NFKD', comment.body).encode('ascii', 'ignore') + "}") #esto porque me daba pila de problemas los comentarios unicode
					reply = get_reply()
					
					s = "\n\n*****"
					s = s + "\n\n Script by /u/Sevg, hosting by /u/DirkGentle *^and ^yes, ^weed ^is ^legal ^here*"
					s = s + "\n\n [Source.](https://github.com/sevgit/Its_URUGUAY_bot)"
					s = s + "\n\n Visit us at /r/Uruguay"
					
					comment.reply(reply + s)
					output_log("{" +  reply + "}")
					log.append(comment.id)
					update_log(comment.id, comment_log_path) 
		except Exception as exception:
			
			output_log(str(exception))
			output_log(traceback.format_exc())
