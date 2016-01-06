import requests
import os
import sys
import zipfile
import shutil
import pdb

#Globals

steamDir = 'C:\Program Files (x86)\Steam'
skinsDir = os.path.join(steamDir, 'skins')
logfile = os.path.join(skinsDir, 'auto-updater log.txt')
config = os.path.join(skinsDir, 'config.txt')
skinconfig = os.path.join(skinsDir, 'config.ini')

#Def--------------------------------------------------------------------------------------

def copytree(src, dst, symlinks=False, ignore=None):
    if not os.path.exists(dst):
        os.makedirs(dst)
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            copytree(s, d, symlinks, ignore)
        else:
            if not os.path.exists(d) or os.stat(s).st_mtime - os.stat(d).st_mtime > 1:
                shutil.copy2(s, d)

#Update check---------------------------------------------------------------------------

print "Checking for update..."
try:
	release = requests.get('https://api.github.com/repos/outsetini/Air-for-Steam/releases/latest')
except(Exception) as exception:
	print exception
	sys.exit(1)

#For log file write at EOF
updatetag = release.json()['tag_name']

if os.path.isfile(logfile):
	try:
		with open(logfile, 'r+') as updatelog:
			if updatelog.read() == updatetag:
				print 'No update found, quiting'
				sys.exit(0)
	except IOError:
		print 'An error occured trying to read the logfile. Please check write permission'
		sys.exit(1)

#Download and extraction ---------------------------------------------------------

#Zip request
print 'Update found, starting download...'
try:
	release = requests.get('https://api.github.com/repos/outsetini/Air-for-Steam/zipball/2015-1012a')
except(Exception) as exception:
	print exception
	sys.exit(1)

#Download zip
try:
	with open(os.path.join(skinsDir, 'temp.zip'), 'wb') as temp:
		temp.write(release.content)
except(Exception) as exception:
	print 'Error saving skin:', exception
	sys.exit(1)

#Extract and delete zip
with zipfile.ZipFile(os.path.join(skinsDir, 'temp.zip')) as temp:
	skin = temp.infolist()[0]
	temp.extractall(os.path.join(steamDir, 'skins'))
	temp.close()
	os.remove(os.path.join(skinsDir, 'temp.zip'))
	if os.path.exists(os.path.join(skinsDir, 'Air for steam (Auto-updated)')):
		shutil.rmtree(os.path.join(skinsDir, 'Air for steam (Auto-updated)')) #Remove old skin to force rename
	os.rename(os.path.join(skinsDir, skin.filename[:-1]), os.path.join(skinsDir, 'Air for steam (Auto-updated)'))

print 'Skin downloaded and extracted. Preparing configuration...'

#Configuration----------------------------------------------------------------------------

#Copy config file
if os.path.isfile(skinconfig):
	shutil.copy2(os.path.join(skinsDir, 'config.ini'), os.path.join(skinsDir, 'Air for steam (Auto-updated)'))
else:
	print 'No config file found (It should be named config.ini)'

#Copy extras
if os.path.isfile(config):
	with open(config, 'r') as config:
		if config.readline() == 'dark':
			copytree(os.path.join(skinsDir, 'Air for steam (Auto-updated)','+Extras', 'Themes', 'Dark'), os.path.join(skinsDir, 'Air for steam (Auto-updated)'))
			print 'Dark theme applied'
		if config.readline() == 'square':
			copytree(os.path.join(skinsDir, 'Air for steam (Auto-updated)','+Extras', 'Square Avatars'), os.path.join(skinsDir, 'Air for steam (Auto-updated)', 'Graphics'))
			print 'Square avatars applied'
else:
	print 'No extras applied'

#End------------------------------------------------------------------
with open(logfile, 'w') as updatelog:
	try:
		updatelog.write(updatetag)
		print 'Update successful'
	except(IOError):
		print 'An error occured writing to logfile, quiting...'
		sys.exit(1)
