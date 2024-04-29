#==========================================================
# Download custom playlists
#==========================================================

#https://github.com/pestami/ArcadeMeta/blob/main/collections/custom-search_invaders.cfg

target=/home/pi/.emulationstation/collections


source=https://github.com/pestami/ArcadeMeta/collections/custom-search_invaders.cfg
source=https://github.com/pestami/ArcadeMeta/blob/6f243a43de05397906e12ee12ce4a13a28609123/collections/custom-search_invaders.cfg
source=https://github.com/pestami/ArcadeMeta/blob/6f243a43de05397906e12ee12ce4a13a28609123/collections/


#WORKS:

source=https://github.com/pestami/ArcadeMeta/blob/main/collections/custom-search_invaders.cfg


wget -P $target $source

pause
