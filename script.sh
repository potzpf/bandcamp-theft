#!/bin/bash

# About this script
#
# Bandcamp is an online platform to promote and sell music. Kindly they let us
# listen to all tracks, even without having bought them. So we are able to
# download all tracks published for .
# Bandcamp is aware of this "feature":
# http://bandcamp.com/help/audio_basics#steal


#download album page from bandcamp
echo Download information from $1
wget -c -O album-page $1

echo Extract album data
#extract album album data
grep -Pzo "(?<=var TralbumData = ){[\s\S]*?}(?=;)" album-page > extract0


# Re-format to JSON
#
# Since the source code we downloaded above is still to be interpreted by a
# JS-Engine we do not have a valid JSON-string. We need to re-format the source
# in order to process it with the python-json.
#
# Things to do:
# 1. Insert double quotes around first-level names
# 2. Concatenate strings seperated by PLUS (+)
# 3. Remove comments
# 4. Remove trailing null-byte

# 1. Insert double quotes
sed -E "s/^(\s*)(\w*):/\1\"\2\":/" extract0 > extract1

# 2. Concatenate strings
sed "s/\" + \"//" extract1 > extract2

# 3. Remove comments
sed "s/ \/\/.*$//" extract2 > extract3

#4. Remove null-byte
echo `cat extract3` > album-data

echo steal
./steal.py < album-data

echo cleanup
rm extract* album-*
