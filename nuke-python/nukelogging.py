import nuke
import os, sys
sys.path.append("X:/apps/Scripts/FTRACK/python-lib")
from datetime import datetime
import getpass

def lognode2(node):

	now = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
	log_date = datetime.now().strftime("%Y-%m-%d")
	user = getpass.getuser() 
	log = "L:/HAL/LIVEAPPS/Log/Nuke/{user}/{log_date}.txt".format(user=user, log_date=log_date)
	if not os.path.isdir(os.path.dirname(log)):
		os.makedirs(os.path.dirname(log))
	with open(log, 'a') as log_file:
		log_line = '{now} {user}: {node}\n'.format(now=now, node=node, user=user)
		log_file.write(log_line)
	
	return 
	
def log_node(node):
	'''Logs the node creation for each shot'''

	user = getpass.getuser() 

	try:
		script_name = nuke.root().knob('name').value()
	except ValueError:
		script_name = ''
		return

	if script_name == '':
		log_name = 'untitled_script_log'
		script_path = 'Untitled'
		return

	else:
		log_name = os.path.basename(script_name).split('.')[0]
		script_path = os.path.dirname(script_name).split('/')[-1]

	log = "L:/HAL/LIVEAPPS/Log/Nuke/Nodes/{script_path}/{log_name}.txt".format(log_name=log_name, script_path=script_path)

	if not os.path.isdir(os.path.dirname(log)):
		os.makedirs(os.path.dirname(log))

	with open(log, 'a+') as log_file:
		nodelist = log_file.read()

		if nodelist == '':
			nodelist = {}

		else:
			nodelist = eval(nodelist)

		if user not in nodelist.keys():
			nodelist[user] = {}
		
		if node not in nodelist[user].keys():
			nodelist[user][node] = 1

		else:
			nodelist[user][node] = int(nodelist[user][node])+1

	with open(log, 'w+') as log_file:
		log_file.write(str(nodelist))

	return

def log_script():
	'''Logs the script open for each user'''

	user = getpass.getuser() 
	try:
		script_name = nuke.root().knob('name').value()

	except ValueError:
		script_name = ''
		return


	now = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
	log_date = datetime.now().strftime("%Y-%m-%d")

	log = "L:/HAL/LIVEAPPS/Log/Nuke/Scripts/{user}/{log_date}.txt".format(log_date=log_date, user=user)

	if not os.path.isdir(os.path.dirname(log)):
		os.makedirs(os.path.dirname(log))

	with open(log, 'a') as log_file:
		
		line = '{now} : {script_name}\n'.format(now=now, script_name=script_name)

		log_file.write(str(line))

	return

