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

sPathFileDB='/home/pi/RetroPie/roms/ports/search2collection/SearchRetroRoms.db'

con = sqlite3.connect(sPathFileDB)
con.text_factory = str
cur = con.cursor()

from colors import colors
from s2c_search import s2c


print(chr(27) + "[2J")


print( colors.fg.red, "...")

sCMD=''
result_List=[]
collections_List=[]

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
    
    if sCOMMAND=='s':
           result_List=s2c.Makeplaylist(sPARAMETERS,'s')   
           
    elif sCOMMAND=='sd':
           result_List=s2c.Makeplaylist(sPARAMETERS,'sd')            
          
        
    elif  sCOMMAND=='w':   
          s2c.WriteToCollection(result_List)
          
    elif  sCOMMAND=='wr':   
          s2c. WriteToCollectionRename(result_List)          
         
          
    elif  sCOMMAND=='l':   
          s2c.Displaylist(result_List)
          
    elif  sCOMMAND=='lc':   
          collections_List= s2c.DisplayCollections()
          
    elif  sCOMMAND=='dc':   
          s2c.DeleteCollection(collections_List)
          
    elif  sCOMMAND=='h':   
          s2c.Help('')
          
    elif  sCOMMAND=='x':   
          print('Good Bye, enjoy your games.')
          print('Remember:')
          print('1. : restart emulationstation !')
          print('2. : Ensure collection is set visible !')
          
    elif  sCOMMAND=='?':   
          s2c.Help('')
          
    else:
        print('...........................................')
        print('Unkown command = ' + sCMD )
        print('With Parameters = ' + sPARAMETERS )
        
sDUMMY = input()   ##  final wait
#-------------------------------------------------------------------------------
#con.commit()
#con.close()
#print('=======================================')
#print('==CLOSED===============================')
#print('=======================================')
