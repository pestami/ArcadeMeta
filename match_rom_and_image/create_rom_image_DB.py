import os
import sqlite3
from pathlib import Path
import sys

#==============================================================================
def make_xml(sPathFileDB, sRoot,sConsole,sFileNameXML):

    print ("\n===BEGIN make_xml=============================================")
    print(f"Name of XLM FILE: {sFileNameXML}")
    print(f"Location Root: {sRoot}")
    
    sPathFilenameXML=sRoot + '/' + sConsole+ '/' + sFileNameXML
    sPathFilenameXML=sFileNameXML
   
    
    con = sqlite3.connect(sPathFileDB)
    con.text_factory = str
    cur = con.cursor()
    SQL11='''select path,name,image from JOIN_images_rom
    where game_system=''' 
    SQL11= SQL11+ "'" + sConsole + "'"
    cur.execute(SQL11)
    resultSQL11=cur.fetchall()
    con.commit()
    con.close()
    
    #print(resultSQL11)

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
    nCount_Roms_ok_images=0
    nCount_Roms_no_images=0
    
    for GAME in resultSQL11:
        
        doc = ET.SubElement(root, "game")
        ET.SubElement(doc, "path").text = './'+GAME[0]
        ET.SubElement(doc, "name").text = GAME[1]
        if GAME[2] :
                ET.SubElement(doc, "image").text = './'+sConsole + '/'+GAME[2]
                nCount_Roms_ok_images+=1
        else:
            #ET.SubElement(doc, "image").text = './'+sConsole + '/'+'1a_ghost.png'
            ET.SubElement(doc, "image").text = './1a_ghost.png'
            nCount_Roms_no_images+=1
        
       # ET.SubElement(doc, "path").text = GAME[1]
       # ET.SubElement(doc, "name").text = GAME[2]
       # ET.SubElement(doc, "desc").text = GAME[3]
       # ET.SubElement(doc, "image").text = GAME[4]
       # ET.SubElement(doc, "releasedate").text =GAME[5]
       # ET.SubElement(doc, "publisher").text = GAME[6]
       # ET.SubElement(doc, "players").text = GAME[7]
 

    tree = ET.ElementTree(root)
    #print ("\n---UNFORMATED PRINT-------------------------------------------")  
    #print(ET.tostring(root, encoding='utf8').decode('utf8'))        
   # ET.indent(tree, space="\t", level=0)  # Python 3.8 upward        
    tree.write(sPathFilenameXML, encoding="utf-8")
    #------------------------------------------------------------------------
    from lxml import etree 
    
    temp = etree.parse(sPathFilenameXML) 
    new_xml = etree.tostring(temp, pretty_print = True, encoding = str) 
    #print ("\n---PRETTY PRINT--------------------------------------------")  
    #print(new_xml)
    #------------------------------------------------------------------------
    # Opening a file
    file1 = open(sPathFilenameXML, 'w')
    file1.writelines(new_xml)
    file1.close()

    #print (sPathFilenameXML)
    
    
    print(f"ROMS with images=: {nCount_Roms_ok_images}")
    print(f"ROMS without images=: {nCount_Roms_no_images}")
    
    log="\n ROMS with images=:" + str(nCount_Roms_ok_images)
    log+="\n ROMS without images=:" + str(nCount_Roms_no_images)
    
    print ("===DONE XML===================================================")
    
    return log
#==============================================================================
        # sFileNameSH='/media/pi/EASYROMS/'+ sConsole+ '/game_images.sh' 
        # sFilePath='/media/pi/EASYROMS/'+ sConsole+     
        
def make_bash(sPathFileDB, sConsole,sFilePathDestination,sFileNameSH):

    print ("\n===BEGIN make .SH=============================================")
    print(f"Name of SH FILE: {sFileNameSH}")
    #print(f"Location Root: {sFilePath}")
    
    # sPathFilenameSH=sRoot + '/' + sConsole+ '/' + sFileNameSH
    sPathFilenameSH=sFileNameSH
   
    
    con = sqlite3.connect(sPathFileDB)
    con.text_factory = str
    cur = con.cursor()
    SQL11='''select file_path from JOIN_images_rom
    where file_path !='' and game_system=''' 
    
    SQL11= SQL11+ "'" + sConsole + "'"
    cur.execute(SQL11)
    resultSQL11=cur.fetchall()
    con.commit()
    con.close()
    
    count_images_copied=0

        
    sdestination=sFilePathDestination
    sTEXT='#!/bin/bash \n'
    sTEXT+='set -v' +'\n'
    sTEXT+='DESTINATION="'+ sFilePathDestination+'/"' +'\n'
   
    
    for items in resultSQL11:
        
        sSource= items[0]
        sTEXT+='SOURCE="'+ sSource+'"' +'\n'
        sTEXT+='cp -p "$SOURCE" "$DESTINATION"' + '\n'            
        count_images_copied+=1
    
    with open(sFileNameSH, 'w') as file:
            file.write(sTEXT) 
        
    
    print(f"Images Copied=: {count_images_copied}")
                    #         #!/bin/bash
                    
                    # # Define source and destination
                    # SOURCE="/source/path/filename"
                    # DESTINATION="/destination/path/"
                    
                    # # Copy the file
                    # cp -p "$SOURCE" "$DESTINATION"
                    
    import shutil

    # Copy a file
    shutil.copy('/media/pi/EASYROMS/1a_ghost.png', '/media/pi/EASYROMS/'+sConsole+'/1a_ghost.png')
    print('CREATED: /media/pi/EASYROMS/'+sConsole+'/1a_ghost.png')
#====================================================================================
def make_log(sConsole,root_dir,stextlog):

    logfile=root_dir+sConsole+'/scraping.log'
    print ("\n===BEGIN make .LOG=============================================")
    print(f"Name of LOGFILE: {logfile}")
    
    with open(logfile, 'w') as file:
            file.write(stextlog) 
    
  
#===================================================================================================================
#===================================================================================================================
def remove_file_extension(filename):
    return filename.rsplit('.', 1)[0]

def substring_until(text,str_until):
    index = text.find(str_until)
    if index != -1:
        return text[:index]
    else:
        return text
    #----------------------------
def scan_directory(directory):
    file_info_list = []
    count_files=0
    for entry in os.scandir(directory):
        if entry.is_file():
                file_path = entry.path
                file_name = entry.name
                file_size = entry.stat().st_size              
                     
                game_system=file_path.split('/')[-2]                
                game_name=remove_file_extension(file_name)
                
                
                game_name=substring_until(game_name,'(')
                game_name=substring_until(game_name,'[')
                game_name=substring_until(game_name,'-image')                            
                # ROMS with images=: 281
                # ROMS without images=: 595
                #atari2600
                game_name=game_name.rstrip()
                # ROMS with images=: 1002
                # ROMS without images=: 257
                            
                file_info_list.append((game_name,game_system,file_name, file_path, file_size))
                count_files+=1
                # print(f"Found file: {file_path}")
                
                
    print(f"Found files: {count_files}")
    return file_info_list
    #----------------------------
    #===================================================================================================================
 #==============================================================================
def Initialize_db(database_file):
    # Connect to SQLite database. It will be created if it doesn't exist.
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()
    
    # Create table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ROMS
        (id INTEGER PRIMARY KEY AUTOINCREMENT, 
          game_name TEXT,
          game_system TEXT,
          file_name TEXT, 
          file_path TEXT, 
          file_size INTEGER)
    ''')
    # Create table if it doesn't exist
    # id INTEGER PRIMARY KEY AUTOINCREMENT, 
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS IMAGES
        (id INTEGER PRIMARY KEY AUTOINCREMENT, 
          game_name TEXT,
          game_system TEXT,
          file_name TEXT, 
          file_path TEXT,    
          file_size INTEGER)
    ''')
    if 1==1:
        cursor.execute('''
        DELETE FROM IMAGES;
        ''')
        cursor.execute('''
        DELETE FROM ROMS;
        ''')
    conn.commit()
    conn.close()
             
#----------------------------
#===================================================================================================================
#===================================================================================================================
def upload_to_roms(database_file,file_info_list):
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()

    try:
            cursor.executemany('''
                INSERT INTO roms (game_name,game_system,file_name, file_path, file_size)
                VALUES (?, ?, ?,?,?)
            ''', file_info_list)
            conn.commit()
            print(f"Uploaded {len(file_info_list)} files to database.")
    except sqlite3.Error as e:
            print(f"Error uploading to database: {e}")
    conn.commit()
    conn.close()
    #----------------------------
def upload_to_images(database_file,file_info_list):
        conn = sqlite3.connect(database_file)
        cursor = conn.cursor()

        try:
            cursor.executemany('''
                INSERT INTO images (game_name,game_system,file_name, file_path, file_size)
                VALUES (?, ?, ?,?,?)
            ''', file_info_list)
            conn.commit()
            print(f"Uploaded {len(file_info_list)} files to database.")
        except sqlite3.Error as e:
            print(f"Error uploading to database: {e}")
        conn.commit()
        conn.close()
    
#===================================================================================================================
#===================================================================================================================
#===================================================================================================================
def main():
    
    #----------------------------
    # Define the SQLite database file
    database_file = 'ROM_IMAGE.db'
    Initialize_db(database_file)   

   
    lConsole={1:'mastersystem',
              2:'famicom',
              3:'mame',
              4:'arcade',
              5:'psp',
              6:'intellivision',
              7:'megadrive',
              8:'coleco',
              9:'neogeo',
              10:'nds',
              11:'n64',
              12:'nes',
              13:'snes',
              14:'atari2600',
              15:'atari7800',
              16:'atari5200',
              17:'pcengine',
              18:'atari7800',
              16:'atari5200',
              19:'pcengine',
              20:'sg-1000',
              21:'sega32x',
              22:'intellivision',
              23:'msx',
              25:'n64',
              26:'neogeo',
              27:'nds',
              28:'sfc',
              29:'cps1',
              30:'vectrex',
              31:'END',
              }
    
    #for sConsole in lConsole:
 #===================================================================================================================       
    sConsole=lConsole[14]   # choice final
    listConsole=[14,15,16]
    listConsole=[30]
    
    root_dir='/media/pi/EASYROMS/'
 

#===================================================================================================================
    for nConsole in listConsole:
        sConsole=lConsole[nConsole]
        stextlog=sConsole +'\n'
        print('=======================================================')
        print(f'Console Name= {sConsole}')
        print('=======================================================')
        # -----------------Direct LOG files-----------------------
        # sys.stdout = sys.__stdout__  # Restore the original stdout
        # logfile=root_dir+ sConsole +'/scraping.log'        
        # with open(logfile, 'w') as file:
        #     sys.stdout = file            
        # if 1==2:
        #     sys.stdout = sys.__stdout__  # Restore the original stdout
        # -----------------SCAN FOR IMAGES---------------------------------------------------------
        directory_root2='/media/pi/EASYROMS/'
        
        directory_to_scan2 = directory_root2 +sConsole+'/' + sConsole                 
        print(f"Scan for IMAGES:: {directory_to_scan2}")
        file_info_list = scan_directory(directory_to_scan2)
        upload_to_images(database_file,file_info_list)        
        
        
          # -----------------SCAN FOR ROMS---------------------------------------------------------
        # directory_to_scan1 = '/media/pi/INTENSO/emulators_ROM_EXTRA/roms/mastersystems'
        directory_root1='/media/pi/EASYROMS/'
        
        directory_to_scan1 = directory_root1+ sConsole        
        print(f"Scan for ROMS:: {directory_to_scan1}")
        file_info_list = scan_directory(directory_to_scan1)
        upload_to_roms(database_file,file_info_list)
        
        
        
      # -----------------CREATE GAMESLIST---------------------------------------------------------
        sPathFileDB=database_file
        sRoot=''   
        # sFileNameXML='/media/pi/INTENSO/emulators_R36S/mastersystem/gamelist.xml'  
        # sFileNameXML='/media/pi/INTENSO/emulators_R36S/'+ sConsole+ '/gamelist.xml' 
        
        # sFileNameXML='/media/pi/A87B-2C84/'+ sConsole+ '/gamelist.xml' 
        # sFileNameXML2='/media/pi/A87B-2C84/'+ sConsole+ '/gamelist_mirek.xml'     
        
        sFileNameXML=directory_root1+ sConsole+ '/gamelist.xml' 
        sFileNameXML2=directory_root1+ sConsole+ '/gamelist_mirek.xml'         
        
        stextlog+= make_xml(sPathFileDB, sRoot,sConsole,sFileNameXML)
        make_xml(sPathFileDB, sRoot,sConsole,sFileNameXML2)    
        
        
      # -----------------CREATE SCRIPT TO MOVE IMAGES---------------------------------------------------------  
      
        sFileNameSH=directory_root1+ sConsole+ '/game_images.sh' 
        sFilePath=directory_root1+ sConsole
      
        print(f'sFileNameSH= {sFileNameSH}')
        make_bash(sPathFileDB,sConsole, sFilePath, sFileNameSH)  
        
                    #         #!/bin/bash
                    
                    # # Define source and destination
                    # SOURCE="/source/path/filename"
                    # DESTINATION="/destination/path/"
                    
                    # # Copy the file
                    # cp -p "$SOURCE" "$DESTINATION"
    # -----------------CREATE LOG---------------------------------------------------------     
        make_log(sConsole,root_dir,stextlog)
            
            
        
        print('==COMPLETED EXECUTION =================================')
        print(f'Console Name= {sConsole}')
        print('=======================================================')
#===================================================================================================================
#===================================================================================================================
#===================================================================================================================
if __name__ == "__main__":
    main()

