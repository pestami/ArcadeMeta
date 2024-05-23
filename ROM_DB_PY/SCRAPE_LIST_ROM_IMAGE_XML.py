#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
#
#
#
# Author:      SESA237770
#
# Created:     03.04.2019
# Copyright:   (c) SESA237770 2019
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#===============================================================================
from xml.dom.minidom import parse
import xml.dom.minidom
import glob
import csv, sqlite3, os , sys , re

from CAX_XML import  cax_xml_rom

#==============================================================================
#===============================================================================

def SetFlags(sFLAGS):
    
     FLAGS = {
    "PATHS": 1,
    "INITIALIZE_DB": 0,
    "LOADLISTGAMES": 0,
    "LOADROMS": 1,
    "LOADIMAGES": 0,
    "LOADMEDIA":0,
    "LOADIMAGESSCRAPED": 0,
    "LOADLISTGAMES_2_XML_DB": 0
     }      
 
     i=0
     for item in FLAGS:
          
           FLAGS[item]=int(sFLAGS[i])
           i+=1
           
     print('SetFags()=' + str(FLAGS) )    
     return FLAGS
#===============================================================================
def SetFagsConsole(sFLAGSConsole):
    
     FLAGSConsole = {
    "arcade":0,
    "atari2600":0,
    "atari5200":0,
    "atari7800":0,
    "c64":0,
    "dreamcast":0,
    "gba":0,
    "gc":0,
    "mame":0,
    "mame-advmame":0,
    "mame-libretro":0,
    "mame-mame4all":0,
    "mastersystems":0,
    "megadrive":0,
    "n64":0,
    "nds":0,
    "neogeo":0,
    "nes":0,
    "pc":0,
    "ports":0,
    "psp":0,
    "psx":0,
    "saturn":0,
    "sg-1000":0,
    "snes":0,
    "zxspectrum":0,
    "pcengine":0,
    "coleco":0,
    "msx":0,
    "gamegear":0,
    "fba":0,

     }      
 
     i=0
     for item in FLAGSConsole:
           
           FLAGSConsole[item]=int(sFLAGSConsole[i])
           i+=1
     print('SetFags()=' + str(FLAGSConsole) )
    
     return FLAGSConsole
###############################################################################
if __name__ == '__main__':
 ##############################################################################
    print ("======================================================")
    print ("Arguments List =======================================")
    print ("======================================================")
    print ('argument list:', sys.argv)
    print ("======================================================")
    
    if len(sys.argv)>1:
          print('ARG1=1 =' +sys.argv[1])
          FLAGS = SetFlags(sys.argv[1])
          
    else:
        #"1 1 PATHS 2 INITIALIZE_DB 3 LOADLISTGAMES 4 LOADROMS"
        #2  1 LOADIMAGES 2 LOADMEDIA 3 LOADIMAGESSCRAPED 4 LOADLISTGAMES_2_XML_DB
        sFLAGS='1001 1000 X'
        sFLAGS='1010 0001 X'  # use this to load gameslist.path and xml contents
        sFLAGS=sFLAGS.replace(" ", "")
        FLAGS = SetFlags(sFLAGS)         
         #################12345678
         
    print ("\n------------------------------------------------------")     
    if len(sys.argv)>2:
         print('ARG2=' +sys.argv[2])
         FLAGSConsole = SetFagsConsole(sys.argv[2])
          
    else:
         #1 arcade"atari2600"atari5200"atari7800"
         #2 c64"dreamcast"gba"gc"
         #3 mame"mame-advmame""mame-libretro""mame-mame4all",
         #4 "mastersystems"megadrive"n64"nds"
         #5 "neogeo"nes"pc"ports"
         #6 psp"psx"saturn"sg-1000"
         #7 snes"TurboGrafX"zxspectrum"pcengine
         sFLAGS='0000000000000000000000000001111X'
         sFLAGS='0000000000000000000000000000001X'
         sFLAGS=sFLAGS.replace(" ", "")
         sFLAGS=sFLAGS.replace("X", "")
         
         FLAGSConsole = SetFagsConsole(sFLAGS) 
         
         
    #print(FLAGS)
    print ("======================================================")
    print ("Directories List =====================================")
    print ("======================================================")
#    sCurrentDir =os.path.realpath(os.path.dirname(__file__))
#    sROOT= "\\".join(sCurrentDir.split("\\")[:-1])
#    sROOT= "/".join(sCurrentDir.split("/")[:-1])
    
    sROOT_DB='/home/pi/Documents/ArcadeMeta/ROM_DB_PY'
    sROOT_GAMES='/home/pi/ROMS_EXTRA/'    #'/media/pi/ROM_EXTRA'
    
    print ("Root GAMES Direcory=", sROOT_GAMES)
    
    #sROOT='/media/pi/ROM_EXTRA'


    sPathFileDB=sROOT_DB + '/DB/RetroRoms.db'
    sPathIMAGES=sROOT_GAMES + '/downloaded_images'
    sPathGamesXML=sROOT_GAMES + '/gameslists'
    sPathROMS=sROOT_GAMES + '/roms'

    print ("sPathFileDB=",sPathFileDB)
    print ("sPathIMAGES=",sPathIMAGES)
    print ("sPathGamesXML=",sPathGamesXML)
    print ("sPathROMS=",sPathROMS)

    print ("======================================================/n")

    #===============================================================================
    #!/usr/bin/python
    #----------------------------
    # redirect StdOut output to log file
    if 1==2:
        sPath_Log_File =sROOT_DB + '/RomsDB/log.txt'
        old_stdout = sys.stdout
        log_file = open(sPath_Log_File,'a')
        sys.stdout = log_file
    #----------------------------
    print ("======================================================")
    print ("1. BEGIN TEST XML ==================================")
    print ("======================================================")
    #/media/pi/ROM_EXTRA/gameslists/ps2
 
    sPathFileDB=sROOT_DB + '/DB/RetroRoms.db'
    sPathIMAGES=sROOT_GAMES + '/downloaded_images'
    sPathMEDIA=sROOT_GAMES + '/downloaded_media'
    sPathIMAGESSCRAPED=sROOT_GAMES + '/downloaded_images_scraped'
    sPathGamesXML=sROOT_GAMES + '/gameslists'
    sPathROMS=sROOT_GAMES + '/roms'
    
    CAX_ROM=cax_xml_rom(sROOT_GAMES)

    if FLAGS["INITIALIZE_DB"]==1 :
        print ("\n###INITIALIZE_DB#######################################################")
        print ("Clear All Tables-------------")
        CAX_ROM.ROM_DB_Initialize(sPathFileDB)

    if FLAGS["LOADLISTGAMES"]==1 :
        print ("\n###LOADLISTGAMES#######################################################")
        print ("Load Paths to GAMELISTS XML for each console into DB")
        CAX_ROM.ROM_DB_LoadListsGameXML(sPathFileDB,sPathGamesXML, flagDebug=1)  # Looks for XML files and loads file list into DB
   
    if FLAGS["LOADLISTGAMES"]==1 :
        print ("\n###LOADLISTGAMES#############################################")   # Total Game ROM Found and uploaded: 13938    
        print ("Load RETROPIE ROM file paths  into DB")
        print (sPathROMS)
        CAX_ROM.ROM_DB_LoadRoms(sPathFileDB,sPathROMS, flagDebug=1)   # Looks for XML files and loads file list into DB
        print ("======================================================")
    
    if FLAGS["LOADIMAGES"]==1 :
        print ("\n###LOADIMAGES################################################")
        print ("Load RETROPIE Images file paths  into DB")
        print (sPathIMAGES)
        CAX_ROM.ROM_DB_LoadImages(sPathFileDB,sPathIMAGES, flagDebug=1)   # Looks for XML files and loads file list into DB
        print ("======================================================")
    
    if FLAGS["LOADMEDIA"]==1 :
        print ("\n###LOADMEDIA#################################################")
        print ("Load RETROPIE Images file paths  into DB")
        print (sPathMEDIA)
        CAX_ROM.ROM_DB_LoadImages(sPathFileDB,sPathMEDIA, flagDebug=1)   # Looks for XML files and loads file list into DB
        print ("======================================================")
        
    if FLAGS["LOADIMAGESSCRAPED"]==1 :
        print ("\n###LOADIMAGESSCRAPED#########################################")
        print ("Load RETROPIE Images file paths  into DB")
        print (sPathIMAGESSCRAPED)
        CAX_ROM.ROM_DB_LoadImages(sPathFileDB,sPathIMAGESSCRAPED, flagDebug=1)   # Looks for XML files and loads file list into DB
        print ("======================================================")
        
    if FLAGS["LOADROMS"]==1 :
        print ("\n####LOADROMS#################################################")
        print ("Load RETROPIE ROMS file paths  into DB")
        print (sPathROMS)
        CAX_ROM.ROM_DB_LoadRoms(sPathFileDB,sPathROMS, flagDebug=1)   # Looks for XML files and loads file list into DB
        print ("======================================================")


    if FLAGS["LOADLISTGAMES_2_XML_DB"]==1:
        print ("\n####LOADLISTGAMES_2_XML_DB###################################")
        print ("2. BEGIN RESULTS show Game GAMES_2_XM [lCollection] =====")
        
        print (sROOT_GAMES)
        print (sPathFileDB)
        print ("\n------------------------------------------------------")
        for key in FLAGSConsole:
             console=key
             value=FLAGSConsole[key]        
             if value==1:
                  print('Loading XML contents for:' +console + " " + str(value))
             
        print ("\n------------------------------------------------------")       
           
        for key in FLAGSConsole:
             console=key
             value=FLAGSConsole[key]          
            
            
             if value==1:
                print('Loading XML contents for:' +console)
                CAX_ROM.Load_xml_gameslist(sROOT_GAMES,sPathFileDB,console)        
        print ("======================================================")

   # CAX_ROM.make_xml("c64","gamelist.xml")
    #===============================================================================

    print ("END TEST XML ==================================")
    print ("======================================================")
    input("Press Enter to continue...")
##    name = input('What is your name: ')

  #  exit(0)