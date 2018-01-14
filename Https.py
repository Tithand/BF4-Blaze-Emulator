from twisted.web import server, resource
from twisted.internet import reactor
import twisted.web.http
import os, Utils.Globals as Globals, Utils.DataClass as DataClass
from random import randint

class Simple(resource.Resource):
	isLeaf = True
	def render_GET(self, request):
	
		urlPath = request.path.split('/')
		#print request
		#print request.args
		#print request.content.read()
		#print request.content.getvalue()
		#print request.getAllHeaders()
		#print "===================="
		
		cwd = os.getcwd()
		path = cwd+"\\Data\\"
		
		if(urlPath[1] == "api"):
			if(urlPath[4] == "battledash"):
				if(urlPath[6] == "widgetdata"):
					return open(path+'battledash.json').read()
			if(urlPath[4] == "persona"):
				if(urlPath[7] == "ingame_metadata"):
					return '{"clubRank": "", "personaId": "'+urlPath[6]+'", "emblemUrl": "", "clubName": "", "countryCode": "US"}'
		elif(urlPath[1] == "bf4"):
			if(urlPath[2] == "battledash"):
				request.setHeader("Access-Control-Allow-Origin", "*")
				#request.setHeader("Origin", "http://battlelog.battlefield.com")
				return open(path+'battledash.html').read()
		
		
		serverXML = open(path+'server.xml')
		
		request.setHeader("content-type", "text/xml")
		return serverXML.read()
		
		
	def getFreePort(self):
		port = randint(50000,58000)
		for auth in Globals.authClients:
			if auth.Port == port:
				return getFreePort()
				
		return port
		
	def render_POST(self, request):
		urlPath = request.path.split('/')
		#print request
		#print request.args
		#print request.content.read()
		#print request.content.getvalue()
		#print list(request.headers)
		#print urlPath
		#print "===================="
		
		#Error ints
		# 1 = No User found
		# 2 = Password error, check password.txt file or make one
		
		if(urlPath[1] == "login"):
			args = request.content.getvalue().split("&")
			
			name = ""
			password = ""
			if (args[0].split("=")[0] == "username"):
				name = args[0].split("=")[1]
			
			if(len(args) > 1):
				if (args[1].split("=")[0] == "password"):
					password = args[1].split("=")[1]

			cwd = os.getcwd()
			path = cwd+"\\Users\\"+name+"\\"
			
			if name == "" or os.path.exists(path) == False:
				return str(1)
			
			if (Globals.userPasswords):
				if(len(args) < 2):
					return str(2)
					
				if os.path.isfile(path+"password.txt") == False:
					return str(2)
					
				passwordFile = open(path+"password.txt")
				userPassword = str(passwordFile.readline())
				passwordFile.close()
				
				if(userPassword != password):
					return str(2)
				
			for auth in Globals.authClients:
				if auth.Name == name:
					return str(auth.Port)

			port = self.getFreePort()

			authClient = DataClass.AuthClient()
			authClient.Name = name
			authClient.Port = port
			Globals.authClients.append(authClient)
			print "Added " + name + ":" + str(authClient.Port) + " To Authentication List"
			
			return str(authClient.Port)
		
		return '"528591967549a51344692b9e18294e4c8240b7b7"'