#!/bin/bash
#
# This script updates Atlassian Stash on Linux
#
# Change the following parameters according if needed
 
# This parameter defines the download root folder for the new version
DLLOCATION=/tmp/download/atlassian/stash
# This parameter defines the root program folder (assuming that "stash" is the main program folder)
ATLASSIAN_ROOT_DIR=/opt/atlassian/
# This parameter defines the data folder of Stash
ATLASSIAN_STASH_DATA=/var/atlassian/application-data/stash
 
echo ############################
echo Stash Migration Script
echo ############################
echo
echo
 
echo Please enter the new version number:
read VERSION
 
echo
echo Please enter the dowload URI from the Atlassian website.
read DL
 
echo
echo Creating new Stash directory
mkdir $DLLOCATION$VERSION/
echo
echo
echo Downloading new version.
cd $DLLOCATION$VERSION
wget $DL
 
echo Extracting new version
tar xf atlassian-stash-$VERSION.tar.gz
cd atlassian-stash-$VERSION
 
echo Stopping stash
$ATLASSIAN_ROOT_DIR/stash/bin/stop-stash.sh
 
echo Removing old backup directory
rm -rf $ATLASSIAN_ROOT_DIR/stash_old
 
echo Move current Stash directory as backup directory
mv $ATLASSIAN_ROOT_DIR/stash $ATLASSIAN_ROOT_DIR/stash_old
 
echo Create new Stash directory
mkdir $ATLASSIAN_ROOT_DIR/stash
 
echo Copy new Stash version
cp -rp * $ATLASSIAN_ROOT_DIR/stash
 
echo Set user and group permissions
chown -R stash $ATLASSIAN_ROOT_DIR/stash
chgrp -R stash $ATLASSIAN_ROOT_DIR/stash
 
echo SQL-Lib directory verification
if [ ! -d "$ATLASSIAN_ROOT_DIR/stash/lib"]; then
        mkdir $ATLASSIAN_ROOT_DIR/stash/lib
fi
cp -rp $ATLASSIAN_ROOT_DIR/stash_old/lib/mysql* $ATLASSIAN_ROOT_DIR/stash/lib/
 
echo Copy server config from backup
cp -rp $ATLASSIAN_ROOT_DIR/stash_old/conf/server.xml $ATLASSIAN_ROOT_DIR/stash/conf
 
echo Set the Stash executable directory
export STASH_HOME=$ATLASSIAN_STASH_DATA
 
echo Stash
export JAVA_HOME=/usr/java/latest
$ATLASSIAN_ROOT_DIR/stash/bin/start-stash.sh