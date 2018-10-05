#!/bin/bash

# About this script
#
# Bandcamp is an online platform to promote and sell music. Kindly they let us
# listen to all tracks, even without having bought them. So we are able to
# download all tracks published for .
# Bandcamp is aware of this "feature":
# http://bandcamp.com/help/audio_basics#steal


#download album page from bandcamp
wget -O - $1 |
# extract data structure
    grep -Pzo "(?<=var TralbumData = ){[\s\S]*?}(?=;)" |


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
    sed -E "s/^(\s*)(\w*):/\1\"\2\":/" |


# 2. Concatenate strings
    sed "s/\" + \"//" |

# 3. Remove comments
    sed "s/ \/\/.*$//" |

#4. Remove null-byte
    xargs -0 |

#finally: steal some music!    
    ./steal.py

