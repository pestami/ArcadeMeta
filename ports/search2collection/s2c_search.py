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
        
        print('.........................................................')
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
                print('Displayed: ' +str(nTotal) +'/'+ sFound +'  Press key to continue..........')
                sCMD = str(input())   
            
        print('-----KEWORDS FOUND END-------------------')      
        print('.........................................................')
    
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
                    
        
        
        
#============================================================================
#============================================================================
    def Help(ID):
            
            print( colors.fg.green, "...")
            print('=====================================================')
            print('==Program to generate a playlist=======V20250527=====')
            print('=====================================================')
            print('type s keyword1+keyword2 to search for game in Name of ROM')
            print('type sd keyword1+keyword2 to search for games in description')
            print('type l  list last search results')
            print('type wr to write playlist to a collection list and rename')
            print('type w  to write playlist to collection list')
            print('....................................................')
            print('type lc to list collections')
            print('type dc to delete a collection')
            print('....................................................')
            print('type h  to help')
            print('type x  to quit')
            print('=====================================================')
#-------------------------------------------------------------------------------
#============================================================================
#============================================================================
