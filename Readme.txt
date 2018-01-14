Requirements:
Python 2.7
Twisted for Python (Inclusive of PyOpenSSL)
See Setup.txt

How to run:
Run Init.py
Profit!


!!!!!!!!!!!!!!!!!!!!!!!! DISCLAIMER !!!!!!!!!!!!!!!!!!!!!!!!
All care has been taken to allow people to play this emulator in
conjunction with the retail Battlefield 4 copy in online multiplayer.
Therefore in saying that; I WILL NOT BE HELD RESPONSIBLE IF YOUR 
ACCOUNT IS BANNED WHILE USING THIS!!!

This emulator does not allow for a pirated version of battlefield 4 to be used, only a legitimate copy will work!

Info:
To add users, go into "Users" then add their username as a file this is their authCode for the batch file
^ Works on the fly for adding users

This is just a beta, and has not been thoroughly tested!

Spaces/Special characters in users names have not been tested!

To change users stats go into "Users" find their username and edit the userstats.txt file.
The users directory also contains many other files now.
- battlepacks.txt; contains all the users battlepacks and their contents (if opened), JSON
- consumables.txt; contains data relating to the XP Boosts (not implemented, can't gain any yet), JSON
- items.txt; a list of all the users items that they've gained by opening battlepacks
- usersettings.txt; game settings (loadouts), don't touch
- userstats.txt; list of all the users stat values.


Inside the "Data" folder you'll find lots of files, 
- global_entitlements.json, don't touch this unless you understand what it is.
- server.xml; data relating to a servers operation, edit the ScoreMultiplier tag for more XP
- items.txt; the item list of the game, including all the Battlepacks line 2224 down are battlepacks, so don't add them.
- battledash.json; quick and dirty edit for battledash the in-game battelog system.
- batteldash.html; my quick attempts at making an in-game browser (need a way to change the games state)
- stats Folder; all the default stats and their categories, do not change!

The included dll has been changed from the previous conf.ini files. All config is done by launch commandline.

Client:
	-authCode username | defines the users name /account on the masterserver, must match with a directory in /Users/
	-password pass	   | defines the users password if the setting is enabled on the master server.

Client AND Server:
	-blazeIP masterserverip/name | IP address or hostname of the blaze server: eg 192.168.1.1 / myurlnotreal.com
	-patchSSL | The must do switch to allow the client or server to connect to the masterserver.
	
I've included examples for starting both the client and the server. - I use BF4WebHelper.exe as it loads faster :)
Please report all errors and findings so I can fix them!