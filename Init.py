#! python2.7
import sys
sys.dont_write_bytecode = True

import BlazeMain_Client
import BlazeMain_Server
import GosRedirector
import Https

from Utils import garbage
import Utils.Globals as Globals

from twisted.internet import ssl, reactor
from twisted.internet.protocol import Factory, Protocol
from twisted.web import server, resource

def Start():

	Globals.serverIP = "127.0.0.1"
	Globals.userPasswords = False

	SSLInfo = ssl.DefaultOpenSSLContextFactory('crt/privkey.pem', 'crt/cacert.pem')
	
	factory = Factory()
	factory.protocol = GosRedirector.GOSRedirector
	reactor.listenSSL(42127, factory, SSLInfo)
	print("[SSL REACTOR] GOSREDIRECTOR STARTED [42127]")
	
	factory = Factory()
	factory.protocol = BlazeMain_Client.BLAZEHUB
	reactor.listenTCP(10041, factory)
	print("[TCP REACTOR] BLAZE CLIENT [10041]")
	
	factory = Factory()
	factory.protocol = BlazeMain_Server.BLAZEHUB
	reactor.listenTCP(10071, factory)
	print("[TCP REACTOR] BLAZE SERVER [10071]")
	
	sites = server.Site(Https.Simple())
	reactor.listenSSL(443, sites, SSLInfo)
	print("[WEB REACTOR] Https [443]")
	
	reactor.run()
	
if __name__ == '__main__':
	Start()