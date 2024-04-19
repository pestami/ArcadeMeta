#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      SESA237770
#
# Created:     15.04.2024
# Copyright:   (c) SESA237770 2024
# Licence:     <your licence>
#-------------------------------------------------------------------------------

def main():
    pass


import re

if __name__ == '__main__':
    main()



    print ("=====================================")
    print ("Tupples to dictionary ===============")
    print ("=====================================")


    tVARS=(('%ROOT%', 'C:\\Users\\sesa237770\\Documents\\ArcadeMeta', ''), ('%ROOT_GAMES%', '', '/home/pi/ROMS_EXTRA'), ('%ROOT_DB%', '', '/home/pi/Documents/Projects_DIY/2024-ROMS-DB/ROM_DB_PY'), ('%ROOT_USB%', '', '/media/pi/ROM_EXTRA/'), ('%screanshots&', '', '/opt/retropie/configs/all/retroarch/screenshots/'), ('', '', ''), ('', '', ''), ('', '', ''), ('', '', ''), ('', '', ''), ('', '', ''), ('', '', ''), ('', '', ''), ('', '', ''))

    lVARS=[]
    for i in list(tVARS):
        lVARS.append(list(i))

    dVARS_WIN={}
    for i in lVARS:
        dVARS_WIN[i[0]] = i[1]

    dVARS_LIN={}
    for i in lVARS:
        dVARS_LIN[i[0]] = i[2]

    print ("===RE ==================================")

    print('PATH=' + dVARS_WIN['%ROOT%'])


    sPath='%ROOT%\SYMPHONY_Do1234567wnload_MLS_PART\DataBases\DB'
    ReString=r'SYM'
    ReString='%[A-Za-z0-9%]*'

    resVAR= re.search(ReString,sPath,0)


    if resVAR:
        print('Result=')
        sVAR=resVAR.group(0)
        print(sVAR)
















