#==========================================================
# Download custom playlists
#==========================================================

#https://github.com/pestami/ArcadeMeta/blob/main/collections/custom-search%20Invaders.cfg

target=/home/pi/.emulationstation/collections
source=https://raw.githubusercontent.com/pestami/ArcadeMeta/main/collections/custom-search%20Invaders.cfg
wget -P $target $source

read
