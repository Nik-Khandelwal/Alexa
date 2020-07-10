import speech_recognition as sr
import mute_alsa
from datetime import datetime
import pyttsx3
import smtplib
import time
import imaplib
import email
from googlesearch import search as ims
import pafy
import vlc
import feedparser
import webbrowser
import os,sys

def interpret_speech():
	with microphone as source:
		# recognizer.adjust_for_ambient_noise(source)
		print "..."
		audio = recognizer.listen(source,timeout=5, phrase_time_limit=5)

	try:
		instruction = recognizer.recognize_google(audio)
		return instruction
	except sr.UnknownValueError:
		pass
	except sr.RequestError as e:
		print "Could not request results from Google Speech Recognition service; {0}".format(e)
		exit() 


def speak(text):
	engine.setProperty('rate', 150)
	engine.say(text)
	engine.runAndWait()



def fetch_mail():
	FROM_EMAIL  = "###"
	FROM_PWD    = "###"
	try:
		mail = imaplib.IMAP4_SSL("imap.gmail.com")
		mail.login(FROM_EMAIL,FROM_PWD)
		mail.select('inbox')

		type, data = mail.search(None, 'ALL')
		mail_ids = data[0]

		id_list = mail_ids.split()   
		first_email_id = int(id_list[0])
		latest_email_id = int(id_list[-1])


		for i in range(latest_email_id,latest_email_id-7, -1):
			typ, data = mail.fetch(i, '(RFC822)' )

			for response_part in data:
				if isinstance(response_part, tuple):
					msg = email.message_from_string(response_part[1].decode('utf-8'))
					email_subject = msg['subject'].decode('utf-8')
					email_from = msg['from'].decode('utf-8').split('<')[0]

					if email_from[0] != '=' and email_subject[0] != '=':
					 	print 'From :' , email_from
					 	print 'Subject :' , email_subject , '\n'
					 	speak(email_from+' has sent '+email_subject)
					elif email_from[0] != '=':
						print 'From :' , email_from , ' has sent a new mail' , '\n'
						speak(email_from + ' has sent a new mail ')
					elif email_subject[0] != '=':
						print 'Subject :' , email_subject , '\n'
						speak('Someone has sent ' + email_subject )
					else:
						pass

	except Exception, e:
		print e


def get_sec(time_str):
    """Get Seconds from time."""
    h, m, s = time_str.split(':')
    return int(h) * 3600 + int(m) * 60 + int(s)

def play_music(song_name):

	for url in ims(song_name+'song youtube', stop=2):
		break

	video = pafy.new(url)
	best = video.getbest()
	media = vlc.MediaPlayer(best.url)
	media.set_fullscreen(True)
	media.play()
	# time.sleep(25)
	# media.stop()


def read_news():
	d = feedparser.parse('https://timesofindia.indiatimes.com/rssfeedstopstories.cms')

	for post in d.entries:
		print post.title
		print post.link , '\n'
		speak(post.title)
		tmp_instruction = interpret_speech()
		if tmp_instruction and tmp_instruction.lower() == "read":
			speak('Reading News    ' + post.description)



if __name__ == "__main__":

	recognizer = sr.Recognizer()
	microphone = sr.Microphone()
	engine = pyttsx3.init()

	
	while 1:
		instruction = interpret_speech()
		if instruction:
			print "You said: ", instruction , '\n'
			if "time" in instruction.lower():
				current_time = "The time is "+datetime.now().strftime("%I:%M")
				print "Current Time =", current_time
				speak(current_time)
			elif "mail" in instruction.lower():
				speak("Fetching your e mails")
				fetch_mail()
			elif "play" in instruction.lower():
				song_name = instruction.strip('play')
				speak('playing '+ song_name)
				play_music(song_name)
			elif "news" in instruction.lower():
				speak("Talking to Times of India")
				read_news()
			else:
				speak(instruction)



