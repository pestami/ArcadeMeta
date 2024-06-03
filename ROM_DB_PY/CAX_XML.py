#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
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
from xml.dom.minidom import *
from xml.dom.minidom import parse
import xml.dom.minidom


class cax_xml_rom:

    ##  Class variables: This variable is shared between all objects of a class
    sConsoleList=[]
    sROOT=""
    #------------------------------------------------------------------------
    # oDialog=cax_xml_rom(["workspace_1X2","workspace_1X2_ojs","workspace_2x2","workspace_2x2_Elastic","workspace_1X2_Perspective"])

    def __init__(self, sROOT):

        self.sROOT = sROOT
        print("sROOT:", sROOT)


    def ROM_DB_Initialize(self,sPathFileDB):
            #==============================================================================
            # All Required DB Tables are Created Her
            #==============================================================================
            # con = sqlite3.connect(":memory:")
            con = sqlite3.connect(sPathFileDB)
            con.text_factory = str
            #sqlite3.ProgrammingError: You must not use 8-bit bytestrings unless you use a text_factory that can interpret 8-bit

            cur = con.cursor()
            #-BEGIN-----Games Database TreeTop structure----------------------------------------------------
            cur.execute("DROP TABLE IF EXISTS LIST_ROMS")  # XML lists of games
            #cur.execute("CREATE TABLE LIST_ROMS (PATH,FILE,CONSOLE,PATHFILE,NAMEROM type UNIQUE);") # use your column names here
            cur.execute("CREATE TABLE LIST_ROMS (PATH,FILE,CONSOLE,PATHFILE  type UNIQUE ,NAMEROM);") # use your column names here
            #-END-------Games Database TreeTop structure----------------------------------------------------

            cur.execute("DROP TABLE IF EXISTS LIST_IMAGES")  # XML lists of games
            #cur.execute("CREATE TABLE LIST_IMAGES (PATH,FILE,CONSOLE,PATHFILE,NAMEROM type UNIQUE);") # use your column names here
            cur.execute("CREATE TABLE LIST_IMAGES (PATH,FILE,CONSOLE,PATHFILE type UNIQUE,NAMEROM);") # use your column names here
            
            cur.execute("DROP TABLE IF EXISTS LIST_XML_GAMESLISTS")  # XML lists of games
            cur.execute("CREATE TABLE LIST_XML_GAMESLISTS (PATH,FILE,CONSOLE,PATHFILE type UNIQUE,ITEMS);") # use your column names here



            #-END-------Table column names as in RETROPIE----------------------------------------------------
            cur.execute("DROP TABLE IF EXISTS LIST_GAMES_META_XML")  # XML lists of games
            cur.execute("CREATE TABLE LIST_GAMES_META_XML (PATH,NAME type UNIQUE,DES CHAR(500),IMAGE,RATING,RELEASE,DEVELOPER,PUBLISHER,GENERE,PLAYERS,PLAYCOUNT,LASTPLAYED,CONSOLE);") # use your column names here


            con.commit()
            con.close()
            #-------------------------------------------------------------------------------
            #==============================================================================
            # All DATA is loaded
            #==============================================================================
    def ROM_DB_LoadListsGameXML(self,sPathFileDB,sPathGamesXML, **kwargs):
            print()
            lLIST_Roms=[]
            flagDebug=kwargs.get('flagDebug', None)
            flagDebugVerbose=kwargs.get('flagDebugVerbose', None)

            nGameCounter=0


            sSearchPath1='D:/gameslists/atari7800/*'
            sSearchPath2=sPathGamesXML +'/*/*'
            sSearchPath=sSearchPath2

            if flagDebug :
                    print('========================================')
                    print('Found XML Game Lists as Follows:')
                    print('........................................')
                    print('Search Path :' + sSearchPath)



    ##        for sfilename in glob.iglob(sSearchPath):
            for sfilename in glob.iglob(sSearchPath):


                if flagDebugVerbose : print('FileName:' + sfilename)

                #(PATH,FILE,CONSOLE,PATHFILE,ITEMS)
                tSplit=os.path.split(sfilename)
                sPath=tSplit[0]
                sFile=tSplit[1]
                sFolders=sPath.split('\\')
                sFolders=sPath.split('/')
                sCONSOLE=sFolders[-1]
                nGameCounter+=1
                
                sPath="/"+sFolders[-2]+"/"+sFolders[-1]
                

                lLIST_Roms.append([sPath,sFile,sCONSOLE,sfilename,''])

            con = sqlite3.connect(sPathFileDB)
            con.text_factory = str
            cur = con.cursor()
            cur.executemany("INSERT OR IGNORE INTO LIST_XML_GAMESLISTS (PATH,FILE,CONSOLE,PATHFILE,ITEMS) VALUES (?, ?, ?,? , ? );", lLIST_Roms)
            con.commit()
            con.close()
            if flagDebug :
                    print('Total Game Lists Found and uploaded:' , nGameCounter)
                    print('========================================')
            #==============================================================================
            # All DATA is loaded
            #==============================================================================
    def ROM_DB_LoadImages(self,sPathFileDB,sPathFileIMAGES, **kwargs):
    # **kwargs accept keyworded variable-length argument passed by the function call

            print()
            lLIST_Images=[]
            nGameCounter=0
            flagDebug=kwargs.get('flagDebug', None)
            flagDebugVerbose=kwargs.get('flagDebugVerbose', None)

            sPathFileSearchSpecImages=sPathFileIMAGES +'/**/*.[jp][pn][gg]'

            if flagDebug :
                    print('========================================')
                    print('Search Specification=' + sPathFileSearchSpecImages)

                    print('Found Image Files as Follows:')
                    print('........................................')
            for sfilename in glob.iglob(sPathFileSearchSpecImages):

                if flagDebugVerbose : print(sfilename)

                #(PATH,FILE,CONSOLE,PATHFILE,ITEMS)
                tSplit=os.path.split(sfilename)
                sPath=tSplit[0]
                sFile=tSplit[1]
                sFolders=sPath.split('\\')
                sFolders=sPath.split('/')
                
                sROM=sFolders[-1]
                sNAMEROM=sFile.replace("-image.jpg", "")
                sNAMEROM=sNAMEROM.replace("-image.png", "")
                sNAMEROM=sNAMEROM.replace(".jpg", "")
                sNAMEROM=sNAMEROM.replace(".png", "")
                
                
                nGameCounter+=1
                
                sPath="/"+sFolders[-2]+"/"+sFolders[-1]


                lLIST_Images.append([sPath,sFile,sROM,sfilename,sNAMEROM])

            con = sqlite3.connect(sPathFileDB)
            con.text_factory = str
            cur = con.cursor()
            cur.executemany("INSERT OR IGNORE INTO LIST_IMAGES (PATH,FILE,CONSOLE,PATHFILE,NAMEROM) VALUES (?, ?, ?, ? , ?);", lLIST_Images)
            con.commit()
            con.close()
            if flagDebug :
                    print('Total Game Image Files Found and uploaded:' , nGameCounter)
                    print('========================================')
                                #==============================================================================
            # All DATA is loaded
            #==============================================================================
    def ROM_DB_LoadRoms(self,sPathFileDB,sPathFileROMS, **kwargs):
    # **kwargs accept keyworded variable-length argument passed by the function call

            print()
            lLIST_ROMS=[]
            nGameCounter=0
            flagDebug=kwargs.get('flagDebug', None)
            flagDebugVerbose=kwargs.get('flagDebugVerbose', None)
            sPathFileSearchSpecImages=sPathFileROMS +'/**/*.[A-Za-z0-9]*'
           # sPathFileSearchSpecImages=sPathFileROMS +'/mame-mame4all/*.*'
           # sPathFileSearchSpecImages=sPathFileROMS +'/**/*'

            if flagDebug :
                    print('========================================')
                    print('Found ROM Files as Follows:')
                    print('........................................')
                    print(sPathFileSearchSpecImages)
                    
            for sfilename in glob.iglob(sPathFileSearchSpecImages):

                if flagDebugVerbose : print(sfilename)

                #(PATH,FILE,CONSOLE,PATHFILE,ITEMS)
                tSplit=os.path.split(sfilename)
                sPath=tSplit[0]
                sFile=tSplit[1]
                sFolders=sPath.split('\\')
                sFolders=sPath.split('/')
                sCONSOLE=sFolders[-1]
                
                sPath="/"+sFolders[-2]+"/"+sFolders[-1]
                
##                sNAMEGAME=sFile.replace(".[A-Za-z,0-9]*", "")
                sNAMEGAME=sFile[:-4]
                nGameCounter+=1

                lLIST_ROMS.append([sPath,sFile,sCONSOLE,sfilename,sNAMEGAME])

            con = sqlite3.connect(sPathFileDB)
            con.text_factory = str
            cur = con.cursor()
            cur.executemany("INSERT OR IGNORE INTO LIST_ROMS (PATH,FILE,CONSOLE,PATHFILE,NAMEROM) VALUES (?, ?, ?, ? , ?);", lLIST_ROMS)
            con.commit()
            con.close()
            if flagDebug :
                    print('Total Game ROM Found and uploaded:' , nGameCounter)
                    print('========================================')
            #==============================================================================
            # All DATA is loaded
            #==============================================================================
    def ROM_DB_LoadMultipleXmlContent(self,sPathFileDB,lLIST_XML_GAMESLISTS_Metadata,console):

            # LIST_GAMES_META
            #(PATH,NAME,DES,IMAGE,RATING,RELEASE,DEVELOPER,PUBLISHER,GENERE,PLAYERS,PLAYCOUNT,LASTPLAYED)
            con = sqlite3.connect(sPathFileDB)
            con.text_factory = str
            cur = con.cursor()
            cur.executemany("INSERT OR IGNORE INTO LIST_GAMES_META_XML (PATH,NAME,DES,IMAGE,RATING,RELEASE,DEVELOPER,PUBLISHER,GENERE,PLAYERS,PLAYCOUNT,LASTPLAYED,CONSOLE) VALUES (?, ?, ?, ? , ? , ? , ? , ? , ? , ? , ? , ?,'"+console+"');", lLIST_XML_GAMESLISTS_Metadata)

##            sSQL_01="UPDATE LIST_GAMES_META SET CONSOLE = '"+console+"'; "
##            cur.execute(sSQL_01)

            con.commit()
            con.close()
    ##        if flagDebug :
    ##                print('========================================')

            #==============================================================================
            # All DATA is loaded
            #==============================================================================
    #==============================================================================
    def GetElement(self,XMLElement,sTagName):
        try:
            Name = XMLElement.getElementsByTagName(sTagName)[0]
            sData=Name.childNodes[0].data
    ##        print(sTagName +" = " + sData)
            return sData
        except:
    ##        print(sTagName + " = Does Not Exist")
            return ''
    #==============================================================================
        ##<gameList system='raspberry'>
        ##  <game>
        ##    <path>./1943j.zip</path>
        ##    <name>1943j</name>
        ##  </game>
        ##  <game>
        ##    <path>./1943kai.zip</path>
        ##    <name>1943kai</name>
        ##  </game>

    #==============================================================================
    def ExtractMetadatefromGameXML(self,xmlfile, **kwargs):

    ##     xmlfile = 'G:\\roms\\mame\\gamelist.xml'
    ##    xmlfile = 'G:\\roms\\amstradcpc\\gamelist.xml'

        flagDebug=kwargs.get('flagDebug', None)
        print ('.......................................................')
        print ('...  ExtractMetadatefromGameXML ...')
        print (xmlfile)
        print ('...  lGamesListCollection...')
        print ('.......................................................')

##

        lGamesListCollection=[]
        lGamesList=[]

        # Open XML document using minidom parser
        DOMTree = xml.dom.minidom.parse(xmlfile)
        gameList = DOMTree.documentElement
        # Gamelist has no attributes typicaly
        print ('LINE 271')
        if gameList.hasAttribute("system"):
           print ("Root element : %s" % gameList.getAttribute("system"))

        # Get all the movies in the collection
        GAMES = gameList.getElementsByTagName("game")

        for game in GAMES:
            lGamesList=[]
            #(PATH,NAME,DES,IMAGE,RATING,RELEASE,DEVELOPER,PUBLISHER,GENERE,PLAYERS,PLAYCOUNT,LASTPLAYED)
            if flagDebug: print ('...<GAME>' , xmlfile)
            sValue = self.GetElement(game,'path')
            lGamesList.append(sValue)
            if flagDebug :print("path:"+sValue)

            sValue = self.GetElement(game,'name')
            lGamesList.append(sValue)
            if sValue and flagDebug: print("name:"+sValue)

            sValue = self.GetElement(game,'desc')
            lGamesList.append(sValue)
            if sValue and flagDebug: print("desc:"+sValue[:40])

            sValue = self.GetElement(game,'image')
            lGamesList.append(sValue)
            if sValue and flagDebug: print("image:"+sValue)

            sValue = self.GetElement(game,'rating')
            lGamesList.append(sValue)
            if sValue and flagDebug: print("rating:"+sValue)

            sValue = self.GetElement(game,'releasedate')
            lGamesList.append(sValue)
            if sValue and flagDebug: print("releasedate:"+sValue)

            sValue = self.GetElement(game,'developer')
            lGamesList.append(sValue)
            if sValue and flagDebug: print("developer:"+sValue)

            sValue = self.GetElement(game,'publisher')
            lGamesList.append(sValue)
            if sValue and flagDebug: print("publisher:"+sValue)

            sValue = self.GetElement(game,'genre')
            lGamesList.append(sValue)
            if sValue and flagDebug: print("genre:"+sValue)

            sValue = self.GetElement(game,'players')
            lGamesList.append(sValue)
            if sValue and flagDebug: print("players:"+sValue)

            sValue = self.GetElement(game,'playcount')
            lGamesList.append(sValue)
            if sValue and flagDebug: print("playcount:"+sValue)

            sValue = self.GetElement(game,'lastplayed')
            lGamesList.append(sValue)
            if sValue and flagDebug: print("lastplayed:"+sValue)
            if flagDebug: print ('...</GAME>')

            lGamesListCollection.append([lGamesList])
    ##        print (lGamesList)
        return lGamesListCollection
        print ("=============================================\n")
    #==============================================================================
    def SelectGamesListCollection(self,sPathFileDB, **kwargs):

            flagDebug=kwargs.get('flagDebug', None)
            GamesListCollection=[]

            con = sqlite3.connect(sPathFileDB)
            con.text_factory = str
            cur = con.cursor()

            SQL11='''select * from LIST_XML_GAMESLISTS
            '''
            cur.execute(SQL11)
            if flagDebug: print( SQL11)
            if flagDebug: print('Query result rows=',cur.rowcount)
            resultSQL11=cur.fetchall()
            con.commit()
            con.close()

            GamesListCollection=list(resultSQL11)

            if flagDebug: print(GamesListCollection)

            return GamesListCollection
    #==============================================================================



    def Load_xml_gameslist(self,sRoot,sPathFileDB,console):

        print ("-----------------------------------------------------")
        print ("2. BEGIN RESULTS show Game [lCollection] ------------")

        GamesListCollection = self.SelectGamesListCollection(sPathFileDB)

        for gamesList in GamesListCollection:
            xmlfile=gamesList[3]  #  '../gamelists/atari7800/gamelist.xml'
            consoleGameList=gamesList[2]
            print(xmlfile)

            if console in gamesList:

                lGameCollection =self.ExtractMetadatefromGameXML(xmlfile,flagDebug=1)

                for game in lGameCollection:
                    print(console , 'ITEM XML: ' , game[0][:1])
                    self.ROM_DB_LoadMultipleXmlContent(sPathFileDB,game,console)

            print ("END RESULTS ------------------------------------")
            #Test_GetGames()

        print ("")
        print ("======================================================")
    #==============================================================================
    def make_xml(self,sPathFileDB, sRoot,sConsole,sFileNameXML):

        sPathFilenameXML=sRoot + '/' + sConsole+ '/' + sFileNameXML
        
        con = sqlite3.connect(sPathFileDB)
        con.text_factory = str
        cur = con.cursor()
        SQL11='''select * from BBB_NEW_GAMESLISTS
        where console=''' + '\'' + sConsole + '\'' 
        
        cur.execute(SQL11)
        resultSQL11=cur.fetchall()
        con.commit()
        con.close()
        
        print(resultSQL11)

        import xml.etree.ElementTree as ET
# =============================================================================
# <gameList>
#	<game>
#		<path>./15-in-1 Mega Collection - Backtracking Ten Years (J).zip</path>
#		<name>15-in-1 Mega Collection - Backtracking Ten Years</name>
#		<desc> </desc>
#		<image>~/.emulationstation/downloaded_images/pcengine/xxxxx-image.png</image>
#		<releasedate>19920101T000000</releasedate>
#		<publisher>Image</publisher>
#		<genre>Compilation</genre>
#		<players></players>
#	</game>
# =============================================================================
        #ET.SubElement(doc, "field1", name="blah").text = "some value1"
        root = ET.Element("gameList")
        for GAME in resultSQL11:
            
            doc = ET.SubElement(root, "game")
            ET.SubElement(doc, "path").text = GAME[1]
            ET.SubElement(doc, "name").text = GAME[2]
            ET.SubElement(doc, "desc").text = GAME[3]
            ET.SubElement(doc, "image").text = GAME[4]
            ET.SubElement(doc, "releasedate").text =GAME[5]
            ET.SubElement(doc, "publisher").text = GAME[6]
            ET.SubElement(doc, "players").text = GAME[7]
 

        tree = ET.ElementTree(root)
        print ("\n---UNFORMATED PRINT-------------------------------------------")  
        print(ET.tostring(root, encoding='utf8').decode('utf8'))        
       # ET.indent(tree, space="\t", level=0)  # Python 3.8 upward        
        tree.write(sPathFilenameXML, encoding="utf-8")
        #------------------------------------------------------------------------
        from lxml import etree 
        
        temp = etree.parse(sPathFilenameXML) 
        new_xml = etree.tostring(temp, pretty_print = True, encoding = str) 
        print ("\n---PRETTY PRINT--------------------------------------------")  
        print(new_xml)
        #------------------------------------------------------------------------
        # Opening a file
        file1 = open(sPathFilenameXML, 'w')
        file1.writelines(new_xml)
        file1.close()

        print ("")
        print ("======================================================")

 #==============================================================================
#==============================================================================
#===============================================================================
################################################################################
if __name__ == '__main__':
################################################################################

    print ("======================================================")
    print ("1. BEGIN TEST XML ==================================")
    print ("======================================================")
##    name = input('What is your name: ')

  #  exit(0)


