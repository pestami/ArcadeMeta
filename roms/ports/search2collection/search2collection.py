# input#-------------------------------------------------------------------------------
# Name:      search2collection.py
# Purpose:
#
# Author:      MPA
#
# Created:     2024 05 03
#
#-------------------------------------------------------------------------------
import sqlite3
import os
import re

sPathFileDB='/home/pi/RetroPie/roms/ports/search2collection/SearchRetroRoms.db'

con = sqlite3.connect(sPathFileDB)
con.text_factory = str
cur = con.cursor()

from colors import colors
from s2c_search import s2c

def checkInteger(s):
    # our created pattern to check for the integer value
    if re.match('^[+-]?[0-9]+$', s):
        return True
    else:
        return False
 



print(chr(27) + "[2J")


print( colors.fg.red, "...")

sCMD=''
result_List=[]
collections_List=[]
game_lists_List=[]

#-------------------------------------------------------------------------------

s2c.Help('')
 
#-------------------------------------------------------------------------------
while(sCMD!='x'):

      
    print( colors.fg.yellow, colors.cursor.blinkon, ":")   
    sCMD = str(input())    ##   s space+invaders
    print( colors.cursor.blinkoff, "")
    if sCMD =='':
        sCMD='?'
        
    sCMD_LINE=sCMD.split(' ') 
    
    sCOMMAND=sCMD_LINE[0]
    sPARAMETERS=''
    sPARAMETERS=sCMD.replace(sCOMMAND+' ','')
    
#    print( 'Command='+ sCOMMAND)
#    print( 'Parameters='+ sPARAMETERS)
    print( colors.fg.pink, "")
###################################################################
###----search commands---------------------------------------------------       
    if sCOMMAND=='s':
           print( colors.fg.lightblue, "...")
           result_List=s2c.Makeplaylist(sPARAMETERS,'s')   
           
    elif sCOMMAND=='sd':
           print( colors.fg.lightblue, "...")
           result_List=s2c.Makeplaylist(sPARAMETERS,'sd')            
###-----Write Commands--------------------------------------------------  
    elif sCOMMAND=='ws':
            
            #--- parameters
            print( colors.fg.lightblue, "...")
            if checkInteger(sPARAMETERS):            
                sSystemName= game_lists_List[int(sPARAMETERS)]
           
            
                #--- Get ROMS in FOLDER
                #--require gameslisting to ensure games listed in gameslists realy exist
                sPathROMS="/home/pi/RetroPie/roms/"+sSystemName       
                sPathNameGamelist='/home/pi/.emulationstation/gamelists/' + sSystemName + '/gamelist.xml'
                
                print ("Your selection= " + sSystemName)
                
                lLIST_XML_GAMESLISTS_Metadata,lgames =s2c.ExtractMetadatefromGameXML(sPathNameGamelist,sPathROMS)   
               # print(lLIST_XML_GAMESLISTS_Metadata[0])
               
                print ("..................................................................\n")
                print ("Number of ROMS Detected in folder=" + str(len(lgames)))
                print ("Number of ROMS Listed in gamelist=" + str(len(lLIST_XML_GAMESLISTS_Metadata)))
                print ("..................................................................\n")
                
                console=sSystemName
                sPathFileDB="/home/pi/RetroPie/roms/ports/search2collection/SearchRetroRoms.db"             
                s2c.ROM_DB_LoadGameListsContents(sPathFileDB,lLIST_XML_GAMESLISTS_Metadata,console)
            else:
                print ("Argument is missing, example: ws 1")   
                
###-----Write Commands--------------------------------------------------  
        
    elif  sCOMMAND=='w':   
          print( colors.fg.lightblue, "...")
          s2c.WriteToCollection(result_List)          
          
    elif  sCOMMAND=='wr':  
          print( colors.fg.lightblue, "...")
          s2c. WriteToCollectionRename(result_List)      
    
###-----list Commands--------------------------------------------------          
          
    elif  sCOMMAND=='l':   
          print( colors.fg.lightblue, "...")
          s2c.Displaylist(result_List)
          s2c.Help('5')
          
    elif  sCOMMAND=='lc': 
          print( colors.fg.purple, "...")
          collections_List= s2c.DisplayCollections()
          s2c.Help('3')

    elif  sCOMMAND=='ls':  
          print( colors.fg.red, "...")
          game_lists_List= s2c.DisplayGameLists()
          print()
          s2c.Help('2')

###-----delete Commands-------------------------------------------------- 
          
    elif  sCOMMAND=='dc':  
          print( colors.fg.purple, "...")
          s2c.DeleteCollection(collections_List)
          s2c.Help('3')
          
    elif  sCOMMAND=='ds':   
          print( colors.fg.red, "...")
          s2c.DeleteSystem(sPathFileDB,sPARAMETERS)
          s2c.Help('5')

###-----System Commands--------------------------------------------------           
    elif  sCOMMAND=='h': 
          print( colors.fg.green, "...")
          s2c.Help('')
          
    elif  sCOMMAND=='x':   
          print( colors.fg.black, "...")
          print('Good Bye, enjoy your games.')
          print('Remember:')
          print('1. : restart emulationstation !')
          print('2. : Ensure collection is set visible !')
          sDUMMY = str(input())    

    elif  sCOMMAND=='?':   
          s2c.Help('')
          
    else:
        print('...........................................')
        print('Unkown command = ' + sCMD )
        print('With Parameters = ' + sPARAMETERS )
        
        
######################################################################        
sDUMMY = input()   ##  final wait
#-------------------------------------------------------------------------------
#con.commit()
#con.close()
#print('=======================================')
#print('==CLOSED===============================')
#print('=======================================')
