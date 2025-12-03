import os
import sqlite3
from pathlib import Path

#==============================================================================
def make_xml(sPathFileDB, sRoot,sConsole,sFileNameXML):

    print ("===BEGIN make_xml=============================================")
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
        ET.SubElement(doc, "path").text = './'+GAME[0]
        ET.SubElement(doc, "name").text = GAME[1]
        if GAME[2] :
                ET.SubElement(doc, "image").text = './downloaded_images/'+sConsole + '/'+GAME[2]
        else:
            ET.SubElement(doc, "image").text = './downloaded_images/'+sConsole + '/'+'1Aghost.jpg'
        
       # ET.SubElement(doc, "path").text = GAME[1]
       # ET.SubElement(doc, "name").text = GAME[2]
       # ET.SubElement(doc, "desc").text = GAME[3]
       # ET.SubElement(doc, "image").text = GAME[4]
       # ET.SubElement(doc, "releasedate").text =GAME[5]
       # ET.SubElement(doc, "publisher").text = GAME[6]
       # ET.SubElement(doc, "players").text = GAME[7]
 

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

    print (sPathFilenameXML)
    
    print ("===DONE XML===================================================")

 #==============================================================================
def remove_file_extension(filename):
    return filename.rsplit('.', 1)[0]

def substring_until(text,str_until):
    index = text.find(str_until)
    if index != -1:
        return text[:index]
    else:
        return text

# Define the directory you want to scan
directory_to_scan = '/media/pi/INTENSO/emulators_ROM_EXTRA/roms/mastersystems'
#----------------------------
# Define the SQLite database file
database_file = 'ROM_IMAGE.db'

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
if 1==2:
    cursor.execute('''
    DELETE FROM IMAGES;
    ''')
    cursor.execute('''
    DELETE FROM ROMS;
    ''')

#----------------------------
def scan_directory(directory):
    file_info_list = []
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
            
                        
            file_info_list.append((game_name,game_system,file_name, file_path, file_size))
            print(f"Found file: {file_path}")
        elif entry.is_dir():
            file_info_list.extend(scan_directory(entry.path))
    return file_info_list
#----------------------------
def upload_to_roms(file_info_list):
    try:
        cursor.executemany('''
            INSERT INTO roms (game_name,game_system,file_name, file_path, file_size)
            VALUES (?, ?, ?,?,?)
        ''', file_info_list)
        conn.commit()
        print(f"Uploaded {len(file_info_list)} files to database.")
    except sqlite3.Error as e:
        print(f"Error uploading to database: {e}")
#----------------------------
def upload_to_images(file_info_list):
    try:
        cursor.executemany('''
            INSERT INTO images (game_name,game_system,file_name, file_path, file_size)
            VALUES (?, ?, ?,?,?)
        ''', file_info_list)
        conn.commit()
        print(f"Uploaded {len(file_info_list)} files to database.")
    except sqlite3.Error as e:
        print(f"Error uploading to database: {e}")
#----------------------------
#===================================================================================================================
#===================================================================================================================
#===================================================================================================================
def main():
    
    sConsole='mastersystem'
    sConsole='famicom'
    sConsole='mame'
    sConsole='arcade'
    sConsole='psp'
    sConsole='intellivision'
    sConsole='megadrive'
    sConsole='coleco'
    sConsole='neogeo'
    sConsole='nds'
    sConsole='n64'
    sConsole='neogeo'
    
    sConsole='n64'

   
    lConsole=['mastersystem',
              'famicom',
              'mame',
              'arcade',
              'psp',
              'intellivision',
              'megadrive',
              'coleco',
              'neogeo',
              'nds',
              'n64',
              'nes',
              'snes']
    
    #for sConsole in lConsole:
    sConsole=lConsole[12]
    if 1==1:
        print('=======================================================')
        print(sConsole)
        print('=======================================================')
        # -----------------SCAN FOR ROMS---------------------------------------------------------
        directory_to_scan1 = '/media/pi/INTENSO/emulators_ROM_EXTRA/roms/mastersystems'
        directory_to_scan1 = '/media/pi/INTENSO/emulators_R36S/mastersystem'
        directory_to_scan1 = '/media/pi/INTENSO/emulators_R36S/' + sConsole
        directory_to_scan1 = '/media/pi/A87B-2C84/' + sConsole
    
        file_info_list = scan_directory(directory_to_scan1)
        upload_to_roms(file_info_list)
        
        # -----------------SCAN FOR IMAGES---------------------------------------------------------
        directory_to_scan2 = '/media/pi/INTENSO/emulators_ROM_EXTRA/downloaded_images/mastersystem'
        directory_to_scan2 = '/media/pi/INTENSO/emulators_R36S/'+sConsole+'/downloaded_images/mastersystem' 
        directory_to_scan2 = '/media/pi/INTENSO/emulators_R36S/'+sConsole+'/downloaded_images/' + sConsole
        directory_to_scan2 = '/media/pi/A87B-2C84/' +sConsole+'/downloaded_images/' + sConsole
                 
        file_info_list = scan_directory(directory_to_scan2)
        upload_to_images(file_info_list)
        conn.close()
          
        # directory_to_scan2 = '/media/pi/A87B-2C84/' +sConsole+'/downloaded_images/' + sConsole+ '_box'
                 
        # file_info_list = scan_directory(directory_to_scan2)
        # upload_to_images(file_info_list)
        # conn.close()
        
        
        
      # -----------------CREATE GAMESLIST---------------------------------------------------------
        sPathFileDB='ROM_IMAGE.db'
        sRoot=''   
        sFileNameXML='/media/pi/INTENSO/emulators_R36S/mastersystem/gamelist.xml'  
        sFileNameXML='/media/pi/INTENSO/emulators_R36S/'+ sConsole+ '/gamelist.xml' 
        sFileNameXML='/media/pi/A87B-2C84/'+ sConsole+ '/gamelist.xml' 
        sFileNameXML2='/media/pi/A87B-2C84/'+ sConsole+ '/gamelist_mirek.xml'                 
        
        make_xml(sPathFileDB, sRoot,sConsole,sFileNameXML)
        #make_xml(sPathFileDB, sRoot,sConsole,sFileNameXML2)    
        print('==COMPLETED EXECUTION =================================')
        print(sConsole)
        print('=======================================================')
#===================================================================================================================
#===================================================================================================================
#===================================================================================================================
if __name__ == "__main__":
    main()

