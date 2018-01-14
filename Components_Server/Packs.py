import Utils.BlazeFuncs as BlazeFuncs
import Utils.Globals as Globals
import json

def grantPacks(self, data_e):
	packet = BlazeFuncs.BlazeDecoder(data_e)
	packList = packet.getVar("PKLS")
	userID = packet.getVar("UID ")
	
	reply = BlazeFuncs.BlazePacket("0802","0002",packet.packetID,"1000")
	reply.writeArray("PIDL")
	for i in range(len(packList)):
		reply.writeArray_TInt("ERR ", 0)
		reply.writeArray_TString("PKEY", packList[i])
		reply.writeArray_ValEnd()
	reply.writeBuildArray("Struct")
	self.transport.getHandle().sendall(reply.build().decode('Hex'))
	
	name = None
	for Client in Globals.Clients:
		if Client.UserID == userID:
			name = Client.Name
			
	if name == None:
		return
	
	itemFile = open('Users/'+name+'/items.txt', 'r+')
	items = itemFile.readlines()
	for x in range(len(packList)):
		if not (packList[x] in items):
			itemFile.write(packList[x]+"\n")
			
			battlepackItem = [packList[x], []]

			battlepackFile = open('Users/'+name+'/battlepacks.txt', 'r')
			packStr = battlepackFile.readline()
			battlepackFile.close()
			
			writeDta = []
			if len(packStr) <= 2:
				writeDta = [battlepackItem]
			else:
				battlepacks = json.loads(packStr)
				battlepacks.append(battlepackItem)
				writeDta = battlepacks
			
			battlepackFile = open('Users/'+name+'/battlepacks.txt', 'w')
			battlepackFile.write(json.dumps(writeDta))
			battlepackFile.close()
			
	itemFile.close()


def ReciveComponent(self,func,data_e):
	func = func.upper()
	if func == '0002':
		print("[PACKS] grant Packs")
		grantPacks(self,data_e)
	else:
		print("[INV] ERROR! UNKNOWN FUNC "+func)