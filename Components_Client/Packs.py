import Utils.BlazeFuncs as BlazeFuncs
import json
from random import randint
import time

def getPacks(self, data_e):
	packet = BlazeFuncs.BlazeDecoder(data_e)
	reply = BlazeFuncs.BlazePacket("0802","0001",packet.packetID,"1000")
	
	while (self.GAMEOBJ.Name == None):
		print "WAITING FOR NAME"
		continue
	
	battlepackFile = open('Users/'+self.GAMEOBJ.Name+'/battlepacks.txt', 'r')
   	battlepacks = json.loads(battlepackFile.readline())
	battlepackFile.close()
	
	#SCAT 0 = ALL
	#SCAT 1
	#SCAT 2
	#SCAT 3 = AWARDED
	
	if len(battlepacks) > 0:
		#No multi-array/list support yet!
		reply.append("c2ccf4040304")
		reply.writeArray("ITLI")
		for i in range(len(battlepacks)):
			if len(battlepacks[i][1]) == 0:
				reply.writeArray_String("")
			else:
				continue
			reply.writeBuildArray("String")
			reply.writeInt("PID ", (i+1))
			reply.writeString("PKEY", battlepacks[i][0])
			reply.writeInt("SCAT", 3)
			reply.writeInt("UID ", self.GAMEOBJ.UserID)
			reply.append("00")
	
	self.transport.getHandle().sendall(reply.build().decode('Hex'))
	
def openPack(self, data_e):
	packet = BlazeFuncs.BlazeDecoder(data_e)
	
	packID = (int(packet.getVar("PID "))-1)

	battlepackFile = open('Users/'+self.GAMEOBJ.Name+'/battlepacks.txt', 'r')
	battlepacks = json.loads(battlepackFile.readline())
	battlepackFile.close()
	
	itemFile = open('Data/items.txt', 'r')
   	itemDB = itemFile.readlines()
	itemFile.close()
	
	itemFile = open('Users/'+self.GAMEOBJ.Name+'/items.txt', 'a+')
	items = itemFile.readlines()
	
	#2223 (2224-1) = End of actual item list, the rest is battlepacks
	packItems = []
	
	#Select random item amount
	bpItemAmt = randint(2,5)
	for i in range(bpItemAmt):
		#XP Boosts
		if(i < bpItemAmt):
			xpChance = randint(1,100)
			if(xpChance >= 95):
				packItems.append("ulte_boost_200");
			elif(xpChance >= 90):
				packItems.append("ulte_boost_100");
			elif(xpChance >= 85):
				packItems.append("ulte_boost_50");
			elif(xpChance >= 75):
				packItems.append("ulte_boost_25");
				
			if(xpChance >= 75):
				bpItemAmt = bpItemAmt-1 #Take one item from the list.
				continue;
	
		# Check if item limit reached
		if (len(items) >= 2223):
			break
		
		#Add always new items
		itemID = None
		while (itemID == None):
			selectedItem = itemDB[randint(0,2223)].strip()
			if not (selectedItem in items):
				itemID = selectedItem
			
		packItems.append(itemID)
		
		if not (itemID in items):
			itemFile.write(itemID+"\n")
	itemFile.close()
	
	battlepacks[packID][1] = packItems;
	
	battlepackFile = open('Users/'+self.GAMEOBJ.Name+'/battlepacks.txt', 'w')
	battlepackFile.write(json.dumps(battlepacks))
	battlepackFile.close()
	
	consumeableFile = open('Users/'+self.GAMEOBJ.Name+'/consumables.txt', 'r')
	consumeables = json.loads(consumeableFile.readline())
	consumeableFile.close()
	
	for x in range(len(packItems)):
		if(packItems[x] == "ulte_boost_25"):
			consumeables[0][1] = consumeables[0][1] + 1
		elif(packItems[x] == "ulte_boost_50"):
			consumeables[1][1] = consumeables[1][1] + 1
		elif(packItems[x] == "ulte_boost_100"): 
			consumeables[2][1] = consumeables[2][1] + 1
		elif(packItems[x] == "ulte_boost_200"):
			consumeables[3][1] = consumeables[3][1] + 1
		
	
	consumeableFile = open('Users/'+self.GAMEOBJ.Name+'/consumables.txt', 'w')
	consumeableFile.write(json.dumps(consumeables))
	consumeableFile.close()
	
	reply = BlazeFuncs.BlazePacket("0802","0004",packet.packetID,"1000")
	reply.writeArray("ITLI")
	for x in range(len(packItems)):
		reply.writeArray_String(packItems[x])
	reply.writeBuildArray("String")
	
	reply.writeInt("PID ", (packID+1))
	reply.writeString("PKEY", battlepacks[packID][0])
	reply.writeInt("SCAT", 3)
	reply.writeInt("TGEN", int(time.time()))
	reply.writeInt("TVAL", int(time.time()))
	reply.writeInt("UID ", self.GAMEOBJ.UserID)
	
	self.transport.getHandle().sendall(reply.build().decode('Hex'))
	
	reply = BlazeFuncs.BlazePacket("0802","000a","0000","2000")
	reply.writeArray("ITLI")
	for x in range(len(packItems)):
		reply.writeArray_String(packItems[x])
	reply.writeBuildArray("String")
		
	reply.writeInt("PID ", (packID+1))
	reply.writeString("PKEY", battlepacks[packID][0])
	reply.writeInt("SCAT", 3)
	reply.writeInt("TGEN", int(time.time()))
	reply.writeInt("TVAL", int(time.time()))
	reply.writeInt("UID ", self.GAMEOBJ.UserID)
	pack1, pack2 = reply.build()
	self.transport.getHandle().sendall(pack1.decode('Hex'))
	self.transport.getHandle().sendall(pack2.decode('Hex'))
	
	if self.GAMEOBJ.CurServer != None:
		self.GAMEOBJ.CurServer.NetworkInt.getHandle().sendall(pack1.decode('Hex'))
		self.GAMEOBJ.CurServer.NetworkInt.getHandle().sendall(pack2.decode('Hex'))

def ReciveComponent(self,func,data_e):
	func = (str(func).upper()).strip()
	if func == '0001':
		print("[PACKS CLIENT] Get Packs")
		getPacks(self,data_e)
	elif func == '0004':
		print("[PACKS CLIENT] Open Pack")
		openPack(self,data_e)
	else:
		print("[INV CLIENT] ERROR! UNKNOWN FUNC "+func)