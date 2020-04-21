import random
import socket
import time
from _thread import *
import threading
from datetime import datetime
import json
import urllib
import urllib.parse
import urllib.request
import random

playerInQueue=[]


def connectionLoop(sock):
   while True:
      data, addr = sock.recvfrom(1024)
      res=json.loads(data.decode())
      res['WaitTime']="0"
      res['Addr']=addr
      print("Got this: "+str(res)+" From: "+str(addr))
      playerInQueue.append(res)
      
      # print(playerInQueue)
      # print(len(playerInQueue))
      
      # if len(playerInQueue)>=3:
      #    simulateMatch(playerInQueue[0],playerInQueue[1],playerInQueue[2])
      #    playerInQueue=[]
      
      

         
def matchMakingServer(sock):
   playerInGame=[]
   while True:
      for player in playerInQueue:
         player['WaitTime']=int(player['WaitTime'])+1
      # print(playerInQueue[7]['WaitTime'])   

      if len(playerInQueue)>=3:
         if not playerInGame:
            playerInGame.append(playerInQueue[0])
            p1Max=int(playerInGame[0]['MMR'])+int(playerInGame[0]['WaitTime'])*30
            p1Min=int(playerInGame[0]['MMR'])-int(playerInGame[0]['WaitTime'])*30
            del playerInQueue[0]
         # playerInGame.append[playerInQueue[0]]
         # del playerInQueue[0]
         else:
            for i in range(0,len(playerInQueue)-1):
                  # print("len="+str(len(playerInQueue))+"i="+str(i))
                  p2Max=int(playerInQueue[i]['MMR'])+int(playerInQueue[i]['WaitTime'])*30
                  p2Min=int(playerInQueue[i]['MMR'])-int(playerInQueue[i]['WaitTime'])*30
                  # print(p1Max)
                  if p1Max>=p2Min or p1Min<=p2Max:
                     # print(playerInQueue[i])
                     if playerInQueue[i] not in playerInGame:
                        playerInGame.append(playerInQueue[i])
                        del playerInQueue[i]
                        # print(playerInGame)
                        if len(playerInGame)==3:
                           simulateMatch(playerInGame[0],playerInGame[1],playerInGame[2],sock)
                           playerInGame=[]
                           break
               
      # for i in range(1, len(playerInQueue)):
      #    print(i)
            
      time.sleep(1)

      
def simulateMatch(player1,player2,player3,sock):
   print("MatchFound!\n"+str(player1)+str(player2)+str(player3))
   player1['Win']
   temp=random.randint(1,3)
   if temp==1:
      player1['Win']=str(int(player1['Win'])+1)
      player2['Lose']=str(int(player2['Lose'])+1)
      player3['Lose']=str(int(player3['Lose'])+1)
   elif temp==2:
      player2['Win']=str(int(player2['Win'])+1)
      player1['Lose']=str(int(player1['Lose'])+1)
      player3['Lose']=str(int(player3['Lose'])+1)
   elif temp==3:
      player3['Win']=str(int(player3['Win'])+1)
      player2['Lose']=str(int(player2['Lose'])+1)
      player1['Lose']=str(int(player1['Lose'])+1)
      
      
   
   player1['Kill']=str(int(player1['Kill'])+random.randint(0,5))
   player1['Death']=str(int(player1['Death'])+random.randint(0,5))
   player1['Level']=str(int(player1['Level'])+1)
   player2['Kill']=str(int(player2['Kill'])+random.randint(0,5))
   player2['Death']=str(int(player2['Death'])+random.randint(0,5))
   player2['Level']=str(int(player2['Level'])+1)
   player3['Kill']=str(int(player3['Kill'])+random.randint(0,5))
   player3['Death']=str(int(player3['Death'])+random.randint(0,5))
   player3['Level']=str(int(player3['Level'])+1)
   
      
   sock.sendto(json.dumps(player1).encode(), player1['Addr'])
   sock.sendto(json.dumps(player2).encode(), player2['Addr'])
   sock.sendto(json.dumps(player3).encode(), player3['Addr'])
   GameResult={"GameID":}

def UpdatePlayer(player):
   UserName=player['UserName']
   Win=player['Win']
   Lose=player['Lose']
   MMR=player['MMR']
   Kill=player['Kill']
   Death=player['Death']
   Level=player['Level']
   item={
      "UserName":UserName,
      "Win":Win,
      "Lose":Lose,
      "MMR":MMR,
      "Kill":Kill,
      "Death":Death,
      "Level":Level
   }
   # data = str(item).encode('utf-8')
   data = bytes(json.dumps(item),'utf8')
   headers = {"Content-Type": "application/json"}
   req = urllib.request.Request("https://nxsy27mns5.execute-api.us-east-2.amazonaws.com/default/Test", data=data, headers=headers)
   res = urllib.request.urlopen(req)
   print(res.read().decode("utf-8")) 
   
   
def main():
   #post
   # data = urllib.parse.urlencode({"name":"qb", "age": 12}).encode("utf-8")
   # req = urllib.request.Request("https://nxsy27mns5.execute-api.us-east-2.amazonaws.com/default/Test", data=data)
   # res = urllib.request.urlopen(req)
   # print(res.read().decode("utf-8")) 
   #post1
   # myname="123"
   # data = str({"name":myname, "age": 12}).encode('utf-8')
   # headers = {"Content-Type": "application/json"}
   # req = urllib.request.Request("https://nxsy27mns5.execute-api.us-east-2.amazonaws.com/default/Test", data=data, headers=headers)
   # res = urllib.request.urlopen(req)
   # print(res.read().decode("utf-8")) 

   
   #get
   # res = urllib.request.urlopen("https://nxsy27mns5.execute-api.us-east-2.amazonaws.com/default/Test")
   # print(res.read().decode("utf-8"))


   port = 12345
   s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
   s.bind(('', port))
   start_new_thread(connectionLoop, (s,))
   start_new_thread(matchMakingServer, (s,))
   while True:
      time.sleep(1)

if __name__ == '__main__':
   main()
