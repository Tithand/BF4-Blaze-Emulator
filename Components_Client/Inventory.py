import Utils.BlazeFuncs as BlazeFuncs
import json

def getItems(self, data_e):
	packet = BlazeFuncs.BlazeDecoder(data_e)
	reply = BlazeFuncs.BlazePacket("0803","0001",packet.packetID,"1000")
	
	cflg = int(packet.getVar('CFLG'))	
	rtype = int(packet.getVar('RTYP'))
	
	while (self.GAMEOBJ.Name == None):
		return
	
	reply.writeSStruct("INVT")
	if(cflg == 2):
		consumeableFile = open('Users/'+self.GAMEOBJ.Name+'/consumables.txt', 'r')
		consumeables = json.loads(consumeableFile.readline())
		consumeableFile.close()
	
		reply.writeArray("CLST")
		for i in range(len(consumeables)):
			reply.writeArray_TInt("ACTT", self.GAMEOBJ.UserID)
			reply.writeArray_TString("CKEY", consumeables[i][0])
			reply.writeArray_TInt("DURA", consumeables[i][2])
			reply.writeArray_TInt("QANT", consumeables[i][1])
			reply.writeArray_ValEnd()
		
		reply.writeBuildArray("Struct")
	else:
		itemFile = open('Users/'+self.GAMEOBJ.Name+'/items.txt', 'r')
		items = itemFile.readlines()
		itemFile.close()

		reply.writeArray("ULST")
		for i in range(len(items)):
			val = str(items[i])
			if val == "":
				continue
			reply.writeArray_String(val.strip())
			
		reply.writeBuildArray("String")
	
	self.transport.getHandle().sendall(reply.build().decode('Hex'))
	
def useConsumeable(self, data_e):
	packet = BlazeFuncs.BlazeDecoder(data_e)
	reply = BlazeFuncs.BlazePacket("0803","0003",packet.packetID,"1000")
	
	itemName = str(packet.getVar('IKEY'))
	
	consumeableFile = open('Users/'+self.GAMEOBJ.Name+'/consumables.txt', 'r')
	consumeables = json.loads(consumeableFile.readline())
	consumeableFile.close()
	
	cIndex = None
	for i in range(len(consumeables)):
		if consumeables[i][0] == itemName:
			cIndex = i
	
	if cIndex == None:
		print "cIdndex is none"
		return
	
	for x in range(len(consumeables)):
		if consumeables[x][2] > 0:
			consumeables[x][2] = 0
	
	#One hour activate!
	consumeables[cIndex][2] = 3600
	consumeables[cIndex][1] = (consumeables[cIndex][1] - 1)
	
	consumeableFile = open('Users/'+self.GAMEOBJ.Name+'/consumables.txt', 'w')
	consumeableFile.write(json.dumps(consumeables))
	consumeableFile.close()
	
	reply.writeSStruct("CNSU")
	reply.writeInt("ACTT", self.GAMEOBJ.UserID)
	reply.writeString("CKEY", consumeables[i][0])
	reply.writeInt("DURA", consumeables[i][2])
	reply.writeInt("QANT", consumeables[i][1])
	reply.writeEUnion() #END USER
	
	reply.writeInt("UID ", self.GAMEOBJ.UserID)
	self.transport.getHandle().sendall(reply.build().decode('Hex'))
	
	#######
	reply = BlazeFuncs.BlazePacket("0803","000a","0000","2000")
	reply.writeSStruct("CNSU")
	reply.writeInt("ACTT", self.GAMEOBJ.UserID)
	reply.writeString("CKEY", consumeables[i][0])
	reply.writeInt("DURA", consumeables[i][2])
	reply.writeInt("QANT", consumeables[i][1])
	reply.writeEUnion() #END USER
	
	reply.writeInt("UID ", self.GAMEOBJ.UserID)
	pack1, pack2 = reply.build()
	self.GAMEOBJ.CurServer.NetworkInt.getHandle().sendall(pack1.decode('Hex'))
	self.GAMEOBJ.CurServer.NetworkInt.getHandle().sendall(pack2.decode('Hex'))

def getTemplate(self, data_e):
	packet = BlazeFuncs.BlazeDecoder(data_e)
	reply = BlazeFuncs.BlazePacket("0803","0006",packet.packetID,"1000")
	
	reply.writeArray("ILST")
	
	itemFile = open('Data/items.txt', 'r')
   	items = itemFile.readlines()
	itemFile.close()

	for i in range(len(items)):
		val = str(items[i])
		reply.writeArray_String(val)
		
	reply.writeBuildArray("String")
	
	self.transport.getHandle().sendall(reply.build().decode('Hex'))

def ReciveComponent(self,func,data_e):
	func = (str(func).upper()).strip()
	if "01" in func:
		print("[INV CLIENT] getItems")
		getItems(self,data_e)
	if func == '0003':
		print("[INV CLIENT] useConsumeable")
		useConsumeable(self,data_e)
	elif func == '0006':
		print("[INV CLIENT] getTemplate")
		getTemplate(self,data_e)
	else:
		print("[INV CLIENT] ERROR! UNKNOWN FUNC "+func)
		getItems(self,data_e)