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
from colors import colors
import os
import re
from xml.dom.minidom import parse
import xml.dom.minidom

class s2c:

#-------------------------------------------------------------------------------
    def Makeplaylist(skeywords,sCMD):
        
        sPathFileDB='/home/pi/RetroPie/roms/ports/search2collection/SearchRetroRoms.db'
    
        con = sqlite3.connect(sPathFileDB)
        con.text_factory = str
        cur = con.cursor()
        
        skeywordsDelimited=skeywords.replace('+','#OR#')
        skeywordsDelimited=skeywordsDelimited.replace(' ','#OR#')
        skeywordsDelimited=skeywordsDelimited.replace('*','#AND#')
        lKeywordsRAW = skeywordsDelimited.split('#')          
        
        lOperators =lKeywordsRAW[1::2]   #a[start:stop:step]    lKeywordsRAW=['sd' ,'space','+','invaders','*','new']                                
        lKeywords= lKeywordsRAW[0::2]     

        

        sSQLlike=''   
        
        i=0                                 
        for item in  lKeywords:
           
            if i==0:
               sSQLlike='like \'%' + item + '%\''  
            else:
                
                sSQLlike=sSQLlike + lOperators[i-1] + ' &COLUMN& like \'%' + item + '%\'' 
            i=i+1
                   
#----------------------------------------------------------                                        
        #NAMEROM like '%invader%' OR NAMEROM like '%asteroid%  
        if sCMD=='sd':   
                sCOLUMN='SEARCHTEXT'
        if sCMD=='s':     
                sCOLUMN='NAMEROM'   
                  
        sSQL='''
                        SELECT
                        COLLECTIONPATHFILE
                        FROM LIST_SEARCH_DB
                        WHERE 
                        &COLUMN& &LIKE&
                        ORDER BY
                        COLLECTIONPATHFILE ASC
                ''' 
         
  
#----------------------------------------------------------  
        sSQL=sSQL.replace('&LIKE&',sSQLlike)
        sSQL=sSQL.replace('&COLUMN&',sCOLUMN)

                                 
        cur.execute(sSQL)
        
        result_List=cur.fetchall()
        
        con.commit()
        con.close()
        
                
        print('=====================================================')
        print('==SQL================================================')
        print('=====================================================')
        print(lKeywords) 
        print(lOperators)                                  
        print('-----------------------------------------------------')   
        print(sSQL)    
        print('Found:' + str(len(result_List)) + ' games.')
        print('=====================================================')
    
        return result_List
#-------------------------------------------------------------------------------
#===========================================================================
#============================================================================
    def Displaylist(result_List):
        
        #print(chr(27) + "[2J")
        os.system('cls||clear')
        print('---------------------------------------------------------')
        print('-----KEWORDS FOUND LIST------------------')
        sFound=str(len(result_List))
        
        i=0
        nTotal=0
        for items in result_List:
            i=i+1
            nTotal=nTotal+1
            print(items)
            if i==25:
                i=0
                print('Displayed: ' +str(nTotal) +'/'+ sFound +'  Press key to continue, x to exit.........')
                sCMD = str(input())   
                if sCMD =='x' or sCMD =='X':
                    break
            
        print('-----KEWORDS FOUND END-------------------')      
        print('---------------------------------------------------------')
    
#-------------------------------------------------------------------------------
#============================================================================
#============================================================================
    def WriteToCollectionRename(result):
        
            print('.........................................................')
            print('Collection will be saved: custom-A-KEYWORD.cfg')
            print('Type the keyword KEYWORD you would like to use to write the collection: ')
            sName = str(input())
            sName=sName.replace(' ','')

            PathFile='/home/pi/.emulationstation/collections/custom-A-KEYWORD.cfg'
            PathFile=PathFile.replace('KEYWORD',sName)
            
            with open(PathFile, 'w') as writer:  
                
                 writer.write('/home/pi/RetroPie/roms/ports/search2collection.sh\n')
                 nCount=0
                 for items in result:
                   #  print(items)   
                     writer.write(items[0] + '\n')
                     nCount=nCount+1
            writer.close
            print('  ')
            print('Collection has been saved to: ')
            print( PathFile)            
            print('Found:' + str(nCount) + ' games.')
            print('.........................................................')
#-------------------------------------------------------------------------------
#============================================================================
#===========================================================================
    def WriteToCollection(result):

            
            PathFile='/home/pi/.emulationstation/collections/custom-A-search-KEYWORD.cfg'
            with open(PathFile, 'w') as writer:  
                
                 writer.write('/home/pi/RetroPie/roms/ports/search2collection.sh\n')
                 nCount=0
                 for items in result:
                   #  print(items)   
                     writer.write(items[0] + '\n')
                     nCount=nCount+1
            writer.close
            print('.........................................................')
            print('Collection has been saved: custom-A-search-KEYWORD.cfg')
            print('Found:' + str(nCount) + ' games.')
            print('.........................................................')
#-------------------------------------------------------------------------------
#============================================================================
#===========================================================================
    def DisplayCollections():
               
                pathcollections='/home/pi/.emulationstation/collections/'             

                dir_list = os.listdir(pathcollections)
                i=0
               
                # prints all files
                os.system('cls||clear')
                print('.........................................................')
                print('-----COLLECTIONS FOUND------------------')
                print("Directory= '", pathcollections, "' :")
                for sfiles in dir_list:                   
                    print(str(i) + ": " + sfiles)
                    i=i+1
                return dir_list
#-------------------------------------------------------------------------------
#============================================================================
#===========================================================================
    def DisplayGameLists():
               
                pathcollections='/home/pi/.emulationstation/gamelists/'             

                dir_list = os.listdir(pathcollections)
                i=0
               
                # prints all files
                os.system('cls||clear')
                print('.........................................................')
                print('-----GAME Lists FOUND------------------')
                print("Directory= '", pathcollections, "' :")
                for sfiles in dir_list:                   
                    print(str(i) + ": " + sfiles)
                    i=i+1
                return dir_list
#-------------------------------------------------------------------------------
#============================================================================
#===========================================================================
    def DeleteCollection(collections_List):
            print('.........................................................')
            print('Type collection index Number, it will be deleted: ')
            sIndex = str(input())
            sIndex=sIndex.replace(' ','')
            
            pathcollections='/home/pi/.emulationstation/collections/' 
            file_path = pathcollections + collections_List[int(sIndex)]
            
            if os.path.exists(file_path):
                    os.remove(file_path)
                    print("The collection has been removed.")
                    print(file_path)
            else:
                    print("The system cannot find the file specified.")
                    print(file_path)
                    
    def DeleteSystem(sPathFileDB,sSystemName):
            print('.........................................................')
            print('Type systems name(NES, SNES etc.), it will be deleted: ')     
            sSystemName = str(input())
            sSystemName=sSystemName.replace(' ','')
            
            con = sqlite3.connect(sPathFileDB)
            con.text_factory = str
            cur = con.cursor()
            sSQL="DELETE FROM LIST_SEARCH_DB WHERE CONSOLE='" + sSystemName + "';"
            print(sSQL)
            cur.execute(sSQL)

            print('Rows Deleted =' + str(cur.rowcount))
##            sSQL_01="UPDATE LIST_GAMES_META SET CONSOLE = '"+console+"'; "
##            cur.execute(sSQL_01)

            con.commit()
            con.close()
        
#============================================================================
#============================================================================
# ID='0123456789'0-clscr; 1-heading; 2-systems; 3-collections; 4-search keywrd; 5-save search; 6-admin
# Help(ID)     
    def Help(ID): 
            
            if ID=='':
                ID='0123456789'
            #print(chr(27) + "[2J")
            
            if '0' in ID:
                os.system('cls||clear')
            if '1' in ID:
                print( colors.fg.green, "...")
                print('==========================================================')
                print('==Program to generate a playlist=======V20250613==========')
                print('==========================================================')
           
            if '2' in ID:
                print( colors.fg.red, "...")
                print('\n..Update Search DataBase................................')
                print('type ls to list installed  game Systems')
                print('type ws to write index game Systems to DataBase')
                print('type ds to delete a Systems from the search DataBase')
           
            if '3' in ID:
                print( colors.fg.purple, "...")
                print('\n.............................................')
                print('type lc to list collections')
                print('type dc to delete a collection')
           
            if '4' in ID:
                print( colors.fg.lightblue, "...")
                print('\n..SEARCH for ROMS......................................')
                print('type s keyword1+keyword2 to search for game in Name of ROM')
                print('type sd keyword1+keyword2 to search for games in description')
            
            if '5' in ID:
                print( colors.fg.lightblue, "...")
                print('\n..SEARCH RESULTS.......................................')
                print('type l  list last plalists search results')
                print('type wr to write playlist to a collection list and rename')
                print('type w  to write playlist to collection list')
           
            if '6' in ID:
                print( colors.fg.green, "...")
                print('\n........................................................')
                print('type h  to help')
                print('type x  to quit')
                print('==========================================================')
#-------------------------------------------------------------------------------
#============================================================================
#============================================================================
    def ROM_DB_LoadGameListsContents(sPathFileDB,lLIST_XML_GAMESLISTS_Metadata,console):

            # LIST_GAMES_META
            #(PATH,NAME,DES,IMAGE,RATING,RELEASE,DEVELOPER,PUBLISHER,GENERE,PLAYERS,PLAYCOUNT,LASTPLAYED)
            #/home/pi/RetroPie/roms/c64/Ping Pong.tap
            lLIST_SEARCH_DB=[]
            
            #print(lLIST_XML_GAMESLISTS_Metadata[1])
            
            for items in  lLIST_XML_GAMESLISTS_Metadata:
                NAMEROM= items[1]
                CONSOLE= console  # not in gameslist.xml
                SEARCHTEXT= items[1] +': '+ items[2]
                COLLECTIONPATHFILE = items[0].replace('./','/home/pi/RetroPie/roms/'+CONSOLE +'/')
                
                lLIST_SEARCH_DB.append([NAMEROM,CONSOLE,SEARCHTEXT,COLLECTIONPATHFILE])
            
            con = sqlite3.connect(sPathFileDB)
            con.text_factory = str
            cur = con.cursor()
            cur.executemany("INSERT OR IGNORE INTO LIST_SEARCH_DB (NAMEROM,CONSOLE,SEARCHTEXT,COLLECTIONPATHFILE) VALUES (?, ?, ?, ? );", lLIST_SEARCH_DB)

            print('Rows uploaded into SEARCH DataBase =' + str(cur.rowcount))
##            sSQL_01="UPDATE LIST_GAMES_META SET CONSOLE = '"+console+"'; "
##            cur.execute(sSQL_01)

            con.commit()
            con.close()
#============================================================================
#============================================================================

#============================================================================
#============================================================================
    def ExtractMetadatefromGameXML(xmlfile,sPathROMS, **kwargs):
        
        def GetElement(XMLElement,sTagName):
                try:
                    Name = XMLElement.getElementsByTagName(sTagName)[0]
                    sData=Name.childNodes[0].data
            ##        print(sTagName +" = " + sData)
                    return sData
                except:
            ##        print(sTagName + " = Does Not Exist")
                    return ''

    ##     xmlfile = 'G:\\roms\\mame\\gamelist.xml'
    ##    xmlfile = 'G:\\roms\\amstradcpc\\gamelist.xml'

        flagDebug=kwargs.get('flagDebug', None)
        print ('.......................................................')
        print ('...  Extract Metadata from Game XML ...')
        print (xmlfile)
        #print ('...  lGamesListCollection...')
        print ('.......................................................')

        lGamesListCollection=[]
        lGamesList=[]
        lgames = os.listdir(sPathROMS)

        # Open XML document using minidom parser
        DOMTree = xml.dom.minidom.parse(xmlfile)
        gameList = DOMTree.documentElement
        # Gamelist has no attributes typicaly
        #print ('LINE 271')
        if gameList.hasAttribute("system"):
           print ("Root element : %s" % gameList.getAttribute("system"))

        # Get all the movies in the collection
        GAMES = gameList.getElementsByTagName("game")

        for game in GAMES:
            lGamesList=[]
            #(PATH,NAME,DES,IMAGE,RATING,RELEASE,DEVELOPER,PUBLISHER,GENERE,PLAYERS,PLAYCOUNT,LASTPLAYED)
            if flagDebug: print ('...<GAME>' , xmlfile)
            sValue = GetElement(game,'path')
            sGameRom_File= re.split('/', sValue)[-1]   #last value in list]
            lGamesList.append(sValue)
            if flagDebug :print("path:"+sValue)

            sValue = GetElement(game,'name')
            lGamesList.append(sValue)
            if sValue and flagDebug: print("name:"+sValue)

            sValue = GetElement(game,'desc')
            lGamesList.append(sValue)
            if sValue and flagDebug: print("desc:"+sValue[:40])

            sValue = GetElement(game,'image')
            lGamesList.append(sValue)
            if sValue and flagDebug: print("image:"+sValue)

            sValue = GetElement(game,'rating')
            lGamesList.append(sValue)
            if sValue and flagDebug: print("rating:"+sValue)

            sValue = GetElement(game,'releasedate')
            lGamesList.append(sValue)
            if sValue and flagDebug: print("releasedate:"+sValue)

            sValue = GetElement(game,'developer')
            lGamesList.append(sValue)
            if sValue and flagDebug: print("developer:"+sValue)

            sValue = GetElement(game,'publisher')
            lGamesList.append(sValue)
            if sValue and flagDebug: print("publisher:"+sValue)

            sValue = GetElement(game,'genre')
            lGamesList.append(sValue)
            if sValue and flagDebug: print("genre:"+sValue)

            sValue = GetElement(game,'players')
            lGamesList.append(sValue)
            if sValue and flagDebug: print("players:"+sValue)

            sValue = GetElement(game,'playcount')
            lGamesList.append(sValue)
            if sValue and flagDebug: print("playcount:"+sValue)

            sValue = GetElement(game,'lastplayed')
            lGamesList.append(sValue)
            if sValue and flagDebug: print("lastplayed:"+sValue)
            if flagDebug: print ('...</GAME>')
                
            
            if sGameRom_File in lgames:
                lGamesListCollection.append(lGamesList)
                
    ##        print (lGamesList)
        return lGamesListCollection, lgames
        print ("Number of ROMS Detected in folder=" + lgames.count)
        print ("Number of ROMS Listed in gamelist=" + lGamesListCollection.count)
        print ("=============================================\n")
        



#============================================================================
#============================================================================
        
###############################################################################
if __name__ == '__main__':
    
    print ("======================================================")
    print ("TEST CODE s2c_search.py===============================")
    print ("======================================================")