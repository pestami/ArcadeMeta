#==================================================================================== 
# Created by Gweno 16/08/2019 for tutolibro.tech
# https://github.com/Gweno/tutolibro.tech/blob/master/lopy/part9/ReverseRange.py
#C:\ProgrammeApps\LibreOffice\share\Scripts\python\
    #HELP=============  
    #print(dir(oCell))
    #Help(oCell)
    #print("\n".join(sorted(dir(oCell), key=lambda s: s.lower())))
#====================================================================================  
# 2024 04 18 : def _ExecuteProgram(sAPPNAME);  Check program exists  before execute
# 2024 04 18 : LINUX compatable
# 2024 04 18 : process = subprocess.Popen([sAPP, sCMD])
#===HELPER FUNCTIONS=================================================================
# CAX User Modules
#import sys
#sys.path.append('D:\\MIDDLEWARE_PYTHON\\cax_modules')
#from CAX_Module_Cad import cax_cad   #cax
#====================================================================================  
#
#
#====================================================================================  

def _getSelectionAddresses(horizontalOffset = 0 , verticalOffset = 0):
    # get the range of addresses from selection
    desktop = XSCRIPTCONTEXT.getDesktop()
    model = desktop.getCurrentComponent()
    oSelection = model.getCurrentSelection()
    oArea = oSelection.getRangeAddress()
    return oArea.StartColumn + horizontalOffset, oArea.StartRow + verticalOffset, oArea.EndColumn + horizontalOffset, oArea.EndRow + verticalOffset

#====================================================================    
#===LIBRARY FUNCTIONS=================================================================
def _getVariables():
    print('\n')
    print('============================================================')
    print('=========_getVariables()============================')
    print('============================================================')

    # get the range of addresses from selection
    oDesktop = XSCRIPTCONTEXT.getDesktop()
    oModel = oDesktop.getCurrentComponent()
    
       # print("\n".join(sorted(dir(oModel.CurrentController), key=lambda s: s.lower())))
       # oSheet = model.CurrentController.ActiveSheet
       #oModel.CurrentController.setActiveSheet.getByName("SETUP")
       
    #oSheet = oModel.CurrentController.getByName("SETUP")
    
    oSheet = oModel.CurrentController.ActiveSheet
    oSheet2 = oModel.getSheets().getByName('SETUP')
    
    
    oModel.CurrentController.setActiveSheet(oSheet2) # CHANGE SHEETS OTHER
    
    oRange = oSheet2.getCellRangeByName('rngVARIABLE')
    
    tRange = oRange.getDataArray()
    print('\n--_getVariables()--------------')

    
    
    oModel.CurrentController.setActiveSheet(oSheet) # CHANGE SHEETS BACK
    
    tVARS=tRange
    lVARS=[]
    for i in list(tVARS):
        lVARS.append(list(i))

    dVARS_WIN={}
    for i in lVARS:
        dVARS_WIN[i[0]] = i[1]

    dVARS_LIN={}
    for i in lVARS:
        dVARS_LIN[i[0]] = i[2]

    print('-------------------------------')
    print('Dictionary Variables Lines')
    for key in dVARS_LIN:
        print(key, ' : ', dVARS_LIN[key])   
    print('-------------------------------')
   

    print('-------------------------------')
    
    return dVARS_WIN , dVARS_LIN
    #--------------------------------------------------------------------   
def _getCommandLines():
    print('\n')
    print('============================================================')
    print('=========_getCommandLines()============================')
    print('============================================================')
 
    # get the range of addresses from selection
    oDesktop = XSCRIPTCONTEXT.getDesktop()
    oModel = oDesktop.getCurrentComponent()    
   
    oSheet = oModel.CurrentController.ActiveSheet               # CHANGE SHEETS CURRENT
    
    oSheetCMD = oModel.getSheets().getByName('CMDLINE')         
    oModel.CurrentController.setActiveSheet(oSheetCMD)    
    oRange = oSheetCMD.getCellRangeByName('rngCOMMANDLINES')
    
    oModel.CurrentController.setActiveSheet(oSheet)             # CHANGE SHEETS BACK
    
    tRange = oRange.getDataArray()

    #print(tRange)       
            
    tCMD=tRange    
    lCMD=[]
    
    for i in list(tCMD):
        lCMD.append(list(i))
        
    #---build dictionary------------
    dCOMD_LINES={}
    for i in lCMD:
        dCOMD_LINES[i[0]] = i[1]
        
    print('-------------------------------')
    print('Dictionary CMD Lines')
    for key in dCOMD_LINES:
        print(key, ' : ', dCOMD_LINES[key])   
    print('-------------------------------')

    
    return dCOMD_LINES 
    print('============================================================')
    # {'SCRAPE_LIST_ROM_IMAGE_XML.py': '10010000X 100000000010000000000000001X', '': ''}

#--------------------------------------------------------------------    
def _ResolveVariables(sPathFile):
    print('\n')
    print('============================================================')
    print('=========_ResolveVariables(sPathFile)============================')
    print('============================================================')
    print('sPathFile=' + sPathFile)    
    import re 
    #sCMD=sCMD.replace('%ROOT%', 'C:/Users/sesa237770/Documents/ArcadeMeta')
    
    dVARS_WIN,dVARS_LIN, = _getVariables()

    sPath=sPathFile
    
    ReString='%[A-Za-z0-9_-]*%'
    resVAR= re.search(ReString,sPath,0)
    if resVAR:
        sVAR=resVAR.group(0)
        print('RE Result=' + sVAR)    
        sPathFile=sPathFile.replace(sVAR, dVARS_WIN[sVAR])
 
    print('Resolved sPathFile=' + sPathFile)   
    return sPathFile
    print('============================================================')
#============================================================================
def _getProgramPath():
    print('\n')
    print('============================================================')
    print('=========_getProgramPath()============================')
    print('============================================================')
      
    # get the range of addresses from selection
    oDesktop = XSCRIPTCONTEXT.getDesktop()
    oModel = oDesktop.getCurrentComponent()    
    
    oSheet = oModel.CurrentController.ActiveSheet
    oSheet2 = oModel.getSheets().getByName('SETUP')
    oModel.CurrentController.setActiveSheet(oSheet2)
    
    oRange = oSheet2.getCellRangeByName('rngPROGRAMS')
    
    tRange = oRange.getDataArray()
   
    oModel.CurrentController.setActiveSheet(oSheet)
    
    tVARS=tRange
    lVARS=[]
    for i in list(tVARS):
        lVARS.append(list(i))

    dVARS_WIN={}
    for i in lVARS:
        dVARS_WIN[i[0]] = i[1]

    dVARS_LIN={}
    for i in lVARS:
        dVARS_LIN[i[0]] = i[2]
        
    print('-------------------------------')
    print('\nDictionary WIN:')    
    for key in dVARS_WIN:
        print(key, ' : ', dVARS_WIN[key])  
    print('-------------------------------')        
    
    return dVARS_WIN , dVARS_LIN
    print('============================================================')
#--------------------------------------------------------------------    
def _ResolveProgramPath(sPathFile):
    print('\n')
    print('============================================================')
    print('=========_ResolveProgramPath(sCMD)============================')
    print('============================================================')
    import re 
    print('Caption Text=' + sPathFile)
    #sCMD=sCMD.replace('%ROOT%', 'C:/Users/sesa237770/Documents/ArcadeMeta')

    dVARS_WIN,dVARS_LIN, = _getProgramPath()
    sPathProgramName=dVARS_WIN[sPathFile]   
    print('Resolved Text=' + sPathProgramName)
    return sPathProgramName
    print('============================================================')
#====================================================================
#====================================================================
#====================================================================
# 'PyScripter'  
def _ExecuteProgram(sAPPTYPE, bCMDLINE=False):  
#====================================================================================  
#EXAMPLE: sAPPTYPE = python
#EXAMPLE: sAPP_EXE = C:\ProgrammeApps\python3\python.exe
#EXAMPLE: sARGUMENT_A =\\10.236.177.4\D_Drive\MIDDLEWARE_PYTHON\epl_stammdaten\PDM_Unzip_pdm.py
#EXAMPLE: sARGUMENT_B =
#EXAMPLE: sSCRIPT_NAME =PDM_Unzip_pdm.py
#
#EXAMPLE: sAPPTYPE = explorer
#EXAMPLE: sAPP_EXE = C:\Windows\explorer.exe
#EXAMPLE: sARGUMENT_A =\\10.236.177.4\D_Drive\MIDDLEWARE_PYTHON\epl_stammdaten
#EXAMPLE: sARGUMENT_B =
#EXAMPLE: sSCRIPT_NAME =
#
#====================================================================================    
    #  sAPPTYPE in explorer notepad++ PyScripter SQLiteStudio python
    # C:/Windows/System32/notepad.exe

    import os
    from os.path import exists
    from pathlib import Path
    #os.system('"C:/Windows/System32/notepad.exe"')

    desktop = XSCRIPTCONTEXT.getDesktop()
    model = desktop.getCurrentComponent()
    oSheet = model.CurrentController.ActiveSheet
    oSelection = model.getCurrentSelection()
    
    sSelectionType=oSelection.ElementType.typeName
    print("ExecuteProgram Selected: " +sSelectionType)
#...........................................................    
    if sSelectionType=='com.sun.star.text.XTextRange':     
        sARGUMENT_A = oSelection.String        #setString                
    if sSelectionType=='com.sun.star.drawing.XShape':     
        oShape = oSelection.getByIndex(0)
        sARGUMENT_A = oShape.String        #setString   
 #...........................................................    
    sARGUMENT_A=_ResolveVariables(sARGUMENT_A) # like %ROOT%  etc.
    sARGUMENT_A=sARGUMENT_A.replace('\n', '')
    sARGUMENT_A=sARGUMENT_A.replace('\r', '')  
    
    sAPP_EXE=_ResolveProgramPath(sAPPTYPE)     
    sSCRIPT_NAME = sARGUMENT_A.split('\\')[-1]     # sSCRIPT_NAME can also be a command line path or path-file
    dCMDLINES= _getCommandLines()
    if sSCRIPT_NAME in dCMDLINES:
        sARGUMENT_B=dCMDLINES[sSCRIPT_NAME]
    else: 
        sARGUMENT_B=''
 #...........................................................    
    sOS=os.name    
    print('============================================================')
    print('=========ExecuteProgram() ==================================')
    print('============================================================')
    print('OS= ' + sOS)
    print('sAPPTYPE             = ' + sAPPTYPE)
    print("Executable file      =" + sAPP_EXE)        
    print(".............Script to execute OR path OR path-file.........")
    print("sARGUMENT (TextFlow) =" + sARGUMENT_A)
    print("Script(sample.py ,sample.vbs etc =" + sSCRIPT_NAME)
    print("Script argument Required         =" + str(bCMDLINE)  )
    if sSCRIPT_NAME in dCMDLINES:
        print("Script extra argument Detected=" + dCMDLINES[sSCRIPT_NAME] )  # flase name sAPPTYPE        
    else:
        print("No extra script arguments found !"  )
    print('============================================================')
#...........................................................       
    pathApp = Path(sAPP_EXE)
    pathCMD = Path(sARGUMENT_A)
    
    if sARGUMENT_B !='':
        sCMD_FULL = '\"'+ sAPP_EXE + '\"'  +' ' + sARGUMENT_A +' '  + sARGUMENT_B
        sCMD=sARGUMENT_A +' '  + sARGUMENT_B
    else:
        sCMD_FULL = '\"'+ sAPP_EXE + '\"'  +' ' + sARGUMENT_A
        sCMD=sARGUMENT_A
    print(".............Full Commands to be run ........")
    print('sCMD= ' + sCMD)
    print('sCMD_FULL= ' + sCMD_FULL) 
    print('============================================================')
   
 #...........................................................    
   
    if sOS=='posix':  # LINUX  
        print('\n======================================')
        print('===LINUX OS DETECTED==================') 
        print('======================================')
        sCMD=sCMD.replace('\\', '/')  

        print('\n======================================')
        print('LINUX Program to Execute     = '+ sAPP_EXE) 
        print('LINUX With Command Parameter = ' + sCMD) 
        print('======================================')

        import subprocess                          # LINUX  
        process = subprocess.Popen([sAPP_EXE, sCMD])   # LINUX  
        
    else:   # WINDOWS
        print('\n======================================')
        print('===WINDOWS OS DETECTED==================') 
        print('======================================')
        if not pathApp.is_file():
            print('Not found:' + sAPP_EXE)
        if not pathCMD.is_file():
            print('Not found:' + sCMD)    
        print('\n======================================')
        print('WINDOWS Program to Execute     = '+ sAPP_EXE) 
        print('WINDOWS With Command Parameter = ' + sCMD) 
        print('======================================')        
        #os.system(sCMD_FULL)        
        import subprocess                          # WINDOWS  
        process = subprocess.Popen([sAPP_EXE, sCMD])   # WINDOWS  
        
    print('-------------------------------------\n')
    
#====================================================================
#====================================================================  
# EXECUTE PROGRAMS IN FLOWCHART
#====================================================================
#====================================================================   
#explorer notepad++ PyScripter SQLiteStudio 

def Execute_Selection():  
    _ExecuteProgram('')
#====================================================================
def Open_Explorer():  
   _ExecuteProgram('explorer')
    
#====================================================================
def Open_Notepad_PP():  
   _ExecuteProgram('notepad++')
    
#====================================================================
def Open_SQLite():  
    _ExecuteProgram('SQLiteStudio')
    
#====================================================================
def Open_PythonIDE():  
   _ExecuteProgram('PyScripter')
#====================================================================
def Open_Python3():     
   _ExecuteProgram('python', bCMDLINE=True)  # if python then has CMD line
    
#====================================================================
def _Execute():  
    import os
    #os.system('"C:/Windows/System32/notepad.exe"')
    os.system('"C:\PortableApps\SQLiteStudio\SQLiteStudio.exe C:/Users/sesa237770/Documents/Projects_DIY/2024-ROMS-DB/ROM_DB_PY/DB/RetroRoms_20240301.db"')
    
def TEST_Macro():
    #_Ranges()
    #_Execute()    
   # _getVariables()
    _getCommandLines()
#====================================================================
g_exportedScripts = (TEST_Macro,Execute_Selection,Open_Explorer,Open_Notepad_PP,Open_SQLite,Open_PythonIDE,Open_Python3)
#====================================================================

# oShapes = model.getCurrentSelection() 
# sSelectionType= oShapes.ElementType.typeName 
#if sSelectionType='# oShapes.ElementType.typeName'
# oShape = oShapes.getByIndex(0)
# sCMD =oShape.String	

# oShapes.ElementType
# <Type instance com.sun.star.drawing.XShape (<Enum instance com.sun.star.uno.TypeClass ('INTERFACE')>)>   
