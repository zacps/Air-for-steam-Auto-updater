# Air for steam Auto-updater

I've finished the updater, it's written in python (2.7) and currently only available as source though I'll compile binaries tomorrow. At the moment the script updates when you run it, I suggest running it when steam exits or on startup however I haven't yet tested it during steam startup as it tries to modify files that steam will be using to startup.

###Usage:
Run the script using python 2.7.x from any location, change the directory at the top of the file to your steam directory. It should work on Windows and Linux & (Maybe,) OSX. However I can't test on anything other that windows atm so get back to me if you have any problems.
To force the updater to run again to regonise config changes delete the logfile.txt that is created in the skins directory. This file contains the tag of the latest release and deleting it will make it think there's a new release.

###Config:
Copy your config to the steam skins directory and make sure it's named 'config.ini'
Create a file called 'config.txt' in the skins directory and put 'dark' on the first line if you want the dark skin. Put 'square' on the second line if you want square avatars. See above to get it to apply config changes

The script doesn't currently try to recover errors however I'll add that tomorrow (At lease retrying the get requests.)

##License
The license is the CC 3.0 NZ attribution-noncomercial license. A human readable version is available here: https://creativecommons.org/licenses/by-nc/3.0/nz/.
