import Utils.BlazeFuncs as BlazeFuncs, Utils.Globals as Globals
import json

def getItems(self, data_e):
	packet = BlazeFuncs.BlazeDecoder(data_e)
	reply = BlazeFuncs.BlazePacket("0803","0001",packet.packetID,"1000")
	
	userID = int(packet.getVar('UID '))
	
	name = None
	for Client in Globals.Clients:
		if Client.PersonaID == userID:
			name = Client.Name
			
	if (name == None):
		self.transport.getHandle().sendall(reply.build().decode('Hex'))
		return
			
	consumeableFile = open('Users/'+name+'/consumables.txt', 'r')
   	consumeables = json.loads(consumeableFile.readline())
	consumeableFile.close()
	
	itemsFile = open('Data/items.txt', 'r+')
   	items = itemsFile.readlines()
	itemsFile.close()
	
	itemsFile = open('Users/'+name+'/items.txt', 'r')
   	userItems = itemsFile.readlines()
	itemsFile.close()
	
	reply.writeSStruct("INVT")
	
	reply.writeArray("BLST")
	for i in range(len(items)):
		if items[i] in userItems:
			reply.writeArray_Bool(1)
		else:
			reply.writeArray_Bool(0)
	reply.writeBuildArray("Bool")
	#reply.writeEUnion()
	
	reply.writeArray("CLST")
	for i in range(len(consumeables)):
		reply.writeArray_TInt("ACTT", userID)
		reply.writeArray_TString("CKEY", consumeables[i][0])
		reply.writeArray_TInt("DURA", consumeables[i][2])
		reply.writeArray_TInt("QANT", consumeables[i][1])
		reply.writeArray_ValEnd()
	
	reply.writeBuildArray("Struct")
	
	
	self.transport.getHandle().sendall(reply.build().decode('Hex'))
	
def drainConsumeable(self, data_e):
	packet = BlazeFuncs.BlazeDecoder(data_e)
	reply = BlazeFuncs.BlazePacket("0803","0005",packet.packetID,"1000")
	
	userID = int(packet.getVar('UID '))
	drainAMT = int(packet.getVar('DSEC'))
	itemKey = str(packet.getVar('IKEY'))
	
	name = None
	left = 0
	for Client in Globals.Clients:
		if Client.PersonaID == userID:
			name = Client.Name
			
	if (name == None):
		self.transport.getHandle().sendall(reply.build().decode('Hex'))
		return
		
	consumeableFile = open('Users/'+name+'/consumables.txt', 'r')
   	consumeables = json.loads(consumeableFile.readline())
	consumeableFile.close()
	
	for i in range(len(consumeables)):
		if(consumeables[i][0] == itemKey):
			consumeables[i][2] = consumeables[i][2]-drainAMT
			if(consumeables[i][2] < 0):
				consumeables[i][2] = 0
				
			left = consumeables[i][2]
		
	
	consumeableFile = open('Users/'+name+'/consumables.txt', 'w')
	consumeableFile.write(json.dumps(consumeables))
	consumeableFile.close()
	
	reply.writeInt("LEFT", left)
	
	self.transport.getHandle().sendall(reply.build().decode('Hex'))

def getTemplate(self, data_e):
	packet = BlazeFuncs.BlazeDecoder(data_e)
	reply = BlazeFuncs.BlazePacket("0803","0006",packet.packetID,"1000")
	
	reply.writeArray("ILST")
	
	itemFile = open('Data/items.txt', 'r')
   	items = itemFile.readlines()
	itemFile.close()

	for i in range(len(items)):
		val = str(items[i])
		reply.writeArray_String(val.strip())
		
	reply.writeBuildArray("String")
	
	self.transport.getHandle().sendall(reply.build().decode('Hex'))

def ReciveComponent(self,func,data_e):
	func = func.upper()
	if func == '0005':
		print("[INV] drainConsumeable")
		drainConsumeable(self,data_e)
	elif func == '0006':
		print("[INV] getTemplate")
		getTemplate(self,data_e)
	else:
		print("[INV] getItems")
		getItems(self,data_e)