#!/bin/bash

# Try to upload pathologically-named files one file at a time via
# rclone, showing verbose output as we go.

# You'll probably need to adjust these two variables.
RCLONE_REMOTE="permanent-prod"
ARCHIVE_PATH="/archives/kfogel OTS uploaded 1 (14031)/My Files/"

# An alternative tactic would be to try to upload all the files at
# once, with a command like this:
# 
#   $ cd test-tree
#   $ rclone copy -v -P --size-only --sftp-set-modtime=false ./ "permanent-prod:/archives/kfogel OTS uploaded 1 (14031)/My Files/"
# 
# However, that runs into problems quite early.  So I wrote this
# script to try uploading one file at a time.  (Maybe we could also
# pass some kind of "no more than N retries" flag to rclone; I haven't
# looked into that yet.)
#
# This script hasn't gotten very far yet.  As of this writing on
# 2023-03-01, many of the files do not upload.  I haven't looked
# closely enough yet to see exactly what causes the errors (which
# usually look like retries).  Maybe the problem is in the shell
# escaping (though the shell escaping looks good to me), or maybe it's
# that rclone can't handle certain chars, or maybe that SFTP itself
# can't handle certain chars, or maybe that the Permanent SDK can't
# handle certain chars, or maybe that the Permanent back-end can't
# handle certain chars?  I don't know.
#
# The latest successfully-uploaded file in the list is "frontback.-"
# 
# Note that I removed these filenames from near the beginning of the
# list because they had problems from the get-go (there are similar
# filenames later on in the list, and my guess is once we get there
# that the'll have problems too and will also need to be taken out):
#
#   'frontback.'$'\001'
#   'frontback.'$'\002'
#   'frontback.'$'\003'
#   'frontback.'$'\004'
#   'frontback.'$'\005'
#   'frontback.'$'\006'
#   'frontback.'$'\a'
#   'frontback.'$'\b'
#   'frontback.'$'\016'
#   'frontback.'$'\017'
#   'frontback.'$'\020'
#   'frontback.'$'\021'
#   'frontback.'$'\022'
#   'frontback.'$'\023'
#   'frontback.'$'\024'
#   'frontback.'$'\025'
#   'frontback.'$'\026'
#   'frontback.'$'\027'
#   'frontback.'$'\030'
#   'frontback.'$'\031'
#   'frontback.'$'\032'
#   'frontback.'$'\033'
#   'frontback.'$'\034'
#   'frontback.'$'\035'
#   'frontback.'$'\036'
#   'frontback.'$'\037'
#   'frontback.'$'\177'
#   'frontback.'$'\t'
#   'frontback.'$'\n'
#   'frontback.'$'\v'
#   'frontback.'$'\f'
#   'frontback.'$'\r'
#
# I also saw trouble with these:
#
#   frontback.,
#   'frontback."'
#   'frontback.*'
#   frontback..
#   frontback.:
#
# And during one run, a previously successfully-uploaded file got this
# error:
#
#   *** STARTING ***
#   NAME: frontback.+
#   <3>ERROR : frontback.+: Failed to copy: Update Create failed: sftp: "" (SSH_FX_FAILURE)
#   <3>ERROR : Attempt 1/3 failed with 1 errors and: Update Create failed: sftp: "" (SSH_FX_FAILURE)
#   <3>ERROR : frontback.+: Failed to copy: Update Create failed: sftp: "" (SSH_FX_FAILURE)
#   <3>ERROR : Attempt 2/3 failed with 1 errors and: Update Create failed: sftp: "" (SSH_FX_FAILURE)
#   <3>ERROR : frontback.+: Failed to copy: Update Create failed: sftp: "" (SSH_FX_FAILURE)
#   <3>ERROR : Attempt 3/3 failed with 1 errors and: Update Create failed: sftp: "" (SSH_FX_FAILURE)
#   <6>INFO  : 
#   Transferred:   	          0 B / 0 B, -, 0 B/s, ETA -
#   Errors:                 1 (retrying may help)
#   Elapsed time:         8.1s
#   
#   Failed to copy: Update Create failed: sftp: "" (SSH_FX_FAILURE)
#   *** DONE ***
# 
# Whew.  FYI, I just did '(cd test-tree; ls -1)' to generate the list
# of filenames below -- my Bash shell provided the escaping -- and
# then, as mentioned above, I took a group of related files out
# because they were problematic right away.  There are, no doubt, more
# such remaining in the list.

cd test-tree

for name in                            \
            '$frontback.png'           \
            '$frontback.txt'           \
            'front$back.png'           \
            'front$back.txt'           \
            'frontback. '              \
            'frontback.!'              \
            'frontback."'              \
            frontback.#                \
            frontback.%                \
            'frontback.&'              \
            "frontback.'"              \
            'frontback.('              \
            'frontback.)'              \
            'frontback.*'              \
            frontback.+                \
            frontback.,                \
            frontback.-                \
            frontback..                \
            frontback.:                \
            'frontback.;'              \
            'frontback.<'              \
            'frontback.='              \
            'frontback.>'              \
            'frontback.?'              \
            'frontback.@'              \
            'frontback.['              \
            'frontback.\'              \
            frontback.]                \
            'frontback.^'              \
            frontback._                \
            'frontback.`'              \
            frontback.{                \
            'frontback.|'              \
            frontback.}                \
            frontback.~                \
            'frontback.$'              \
            'frontback$.png'           \
            'frontback.$png'           \
            'frontback$.txt'           \
            'frontback.$txt'           \
            ''$'\001''frontback.png'   \
            ''$'\002''frontback.png'   \
            ''$'\003''frontback.png'   \
            ''$'\004''frontback.png'   \
            ''$'\005''frontback.png'   \
            ''$'\006''frontback.png'   \
            ''$'\a''frontback.png'     \
            ''$'\b''frontback.png'     \
            ''$'\016''frontback.png'   \
            ''$'\017''frontback.png'   \
            ''$'\020''frontback.png'   \
            ''$'\021''frontback.png'   \
            ''$'\022''frontback.png'   \
            ''$'\023''frontback.png'   \
            ''$'\024''frontback.png'   \
            ''$'\025''frontback.png'   \
            ''$'\026''frontback.png'   \
            ''$'\027''frontback.png'   \
            ''$'\030''frontback.png'   \
            ''$'\031''frontback.png'   \
            ''$'\032''frontback.png'   \
            ''$'\033''frontback.png'   \
            ''$'\034''frontback.png'   \
            ''$'\035''frontback.png'   \
            ''$'\036''frontback.png'   \
            ''$'\037''frontback.png'   \
            ''$'\177''frontback.png'   \
            ''$'\t''frontback.png'     \
            ''$'\n''frontback.png'     \
            ''$'\v''frontback.png'     \
            ''$'\f''frontback.png'     \
            ''$'\r''frontback.png'     \
            ' frontback.png'           \
            '!frontback.png'           \
            '"frontback.png'           \
            '#frontback.png'           \
            %frontback.png             \
            '&frontback.png'           \
            "'frontback.png"           \
            '(frontback.png'           \
            ')frontback.png'           \
            '*frontback.png'           \
            +frontback.png             \
            ,frontback.png             \
            -frontback.png             \
            :frontback.png             \
            ';frontback.png'           \
            '<frontback.png'           \
            '=frontback.png'           \
            '>frontback.png'           \
            '?frontback.png'           \
            '@frontback.png'           \
            '[frontback.png'           \
            '\frontback.png'           \
            ]frontback.png             \
            '^frontback.png'           \
            _frontback.png             \
            '`frontback.png'           \
            {frontback.png             \
            '|frontback.png'           \
            }frontback.png             \
            '~frontback.png'           \
            'front'$'\001''back.png'   \
            'front'$'\002''back.png'   \
            'front'$'\003''back.png'   \
            'front'$'\004''back.png'   \
            'front'$'\005''back.png'   \
            'front'$'\006''back.png'   \
            'front'$'\a''back.png'     \
            'front'$'\b''back.png'     \
            'front'$'\016''back.png'   \
            'front'$'\017''back.png'   \
            'front'$'\020''back.png'   \
            'front'$'\021''back.png'   \
            'front'$'\022''back.png'   \
            'front'$'\023''back.png'   \
            'front'$'\024''back.png'   \
            'front'$'\025''back.png'   \
            'front'$'\026''back.png'   \
            'front'$'\027''back.png'   \
            'front'$'\030''back.png'   \
            'front'$'\031''back.png'   \
            'front'$'\032''back.png'   \
            'front'$'\033''back.png'   \
            'front'$'\034''back.png'   \
            'front'$'\035''back.png'   \
            'front'$'\036''back.png'   \
            'front'$'\037''back.png'   \
            'front'$'\177''back.png'   \
            'front'$'\t''back.png'     \
            'front'$'\n''back.png'     \
            'front'$'\v''back.png'     \
            'front'$'\f''back.png'     \
            'front'$'\r''back.png'     \
            'front back.png'           \
            'front!back.png'           \
            'front"back.png'           \
            front#back.png             \
            front%back.png             \
            'front&back.png'           \
            "front'back.png"           \
            'front(back.png'           \
            'front)back.png'           \
            'front*back.png'           \
            front+back.png             \
            front,back.png             \
            front-back.png             \
            front.back.png             \
            front:back.png             \
            'front;back.png'           \
            'front<back.png'           \
            'front=back.png'           \
            'front>back.png'           \
            'front?back.png'           \
            'front@back.png'           \
            'front[back.png'           \
            'front\back.png'           \
            front]back.png             \
            'front^back.png'           \
            front_back.png             \
            'front`back.png'           \
            front{back.png             \
            'front|back.png'           \
            front}back.png             \
            front~back.png             \
            'frontback'$'\001''.png'   \
            'frontback'$'\002''.png'   \
            'frontback'$'\003''.png'   \
            'frontback'$'\004''.png'   \
            'frontback'$'\005''.png'   \
            'frontback'$'\006''.png'   \
            'frontback'$'\a''.png'     \
            'frontback'$'\b''.png'     \
            'frontback'$'\016''.png'   \
            'frontback'$'\017''.png'   \
            'frontback'$'\020''.png'   \
            'frontback'$'\021''.png'   \
            'frontback'$'\022''.png'   \
            'frontback'$'\023''.png'   \
            'frontback'$'\024''.png'   \
            'frontback'$'\025''.png'   \
            'frontback'$'\026''.png'   \
            'frontback'$'\027''.png'   \
            'frontback'$'\030''.png'   \
            'frontback'$'\031''.png'   \
            'frontback'$'\032''.png'   \
            'frontback'$'\033''.png'   \
            'frontback'$'\034''.png'   \
            'frontback'$'\035''.png'   \
            'frontback'$'\036''.png'   \
            'frontback'$'\037''.png'   \
            'frontback'$'\177''.png'   \
            'frontback'$'\t''.png'     \
            'frontback'$'\n''.png'     \
            'frontback'$'\v''.png'     \
            'frontback'$'\f''.png'     \
            'frontback'$'\r''.png'     \
            'frontback .png'           \
            'frontback!.png'           \
            'frontback".png'           \
            frontback#.png             \
            frontback%.png             \
            'frontback&.png'           \
            "frontback'.png"           \
            'frontback(.png'           \
            'frontback).png'           \
            'frontback*.png'           \
            frontback+.png             \
            frontback,.png             \
            frontback-.png             \
            'frontback.'$'\001''png'   \
            'frontback.'$'\002''png'   \
            'frontback.'$'\003''png'   \
            'frontback.'$'\004''png'   \
            'frontback.'$'\005''png'   \
            'frontback.'$'\006''png'   \
            'frontback.'$'\a''png'     \
            'frontback.'$'\b''png'     \
            'frontback.'$'\016''png'   \
            'frontback.'$'\017''png'   \
            'frontback.'$'\020''png'   \
            'frontback.'$'\021''png'   \
            'frontback.'$'\022''png'   \
            'frontback.'$'\023''png'   \
            'frontback.'$'\024''png'   \
            'frontback.'$'\025''png'   \
            'frontback.'$'\026''png'   \
            'frontback.'$'\027''png'   \
            'frontback.'$'\030''png'   \
            'frontback.'$'\031''png'   \
            'frontback.'$'\032''png'   \
            'frontback.'$'\033''png'   \
            'frontback.'$'\034''png'   \
            'frontback.'$'\035''png'   \
            'frontback.'$'\036''png'   \
            'frontback.'$'\037''png'   \
            'frontback.'$'\177''png'   \
            'frontback.'$'\t''png'     \
            'frontback.'$'\n''png'     \
            'frontback.'$'\v''png'     \
            'frontback.'$'\f''png'     \
            'frontback.'$'\r''png'     \
            'frontback. png'           \
            'frontback.!png'           \
            'frontback."png'           \
            frontback.#png             \
            frontback.%png             \
            'frontback.&png'           \
            "frontback.'png"           \
            'frontback.(png'           \
            'frontback.)png'           \
            'frontback.*png'           \
            frontback.+png             \
            frontback.,png             \
            frontback.-png             \
            frontback..png             \
            frontback.:png             \
            'frontback.;png'           \
            'frontback.<png'           \
            'frontback.=png'           \
            'frontback.>png'           \
            'frontback.?png'           \
            'frontback.@png'           \
            'frontback.[png'           \
            'frontback.\png'           \
            frontback.]png             \
            'frontback.^png'           \
            frontback._png             \
            'frontback.`png'           \
            frontback.{png             \
            'frontback.|png'           \
            frontback.}png             \
            frontback.~png             \
            frontback:.png             \
            'frontback;.png'           \
            'frontback<.png'           \
            'frontback=.png'           \
            'frontback>.png'           \
            'frontback?.png'           \
            'frontback@.png'           \
            'frontback[.png'           \
            'frontback\.png'           \
            frontback].png             \
            'frontback^.png'           \
            frontback_.png             \
            'frontback`.png'           \
            frontback{.png             \
            'frontback|.png'           \
            frontback}.png             \
            frontback~.png             \
            ''$'\001''frontback.txt'   \
            ''$'\002''frontback.txt'   \
            ''$'\003''frontback.txt'   \
            ''$'\004''frontback.txt'   \
            ''$'\005''frontback.txt'   \
            ''$'\006''frontback.txt'   \
            ''$'\a''frontback.txt'     \
            ''$'\b''frontback.txt'     \
            ''$'\016''frontback.txt'   \
            ''$'\017''frontback.txt'   \
            ''$'\020''frontback.txt'   \
            ''$'\021''frontback.txt'   \
            ''$'\022''frontback.txt'   \
            ''$'\023''frontback.txt'   \
            ''$'\024''frontback.txt'   \
            ''$'\025''frontback.txt'   \
            ''$'\026''frontback.txt'   \
            ''$'\027''frontback.txt'   \
            ''$'\030''frontback.txt'   \
            ''$'\031''frontback.txt'   \
            ''$'\032''frontback.txt'   \
            ''$'\033''frontback.txt'   \
            ''$'\034''frontback.txt'   \
            ''$'\035''frontback.txt'   \
            ''$'\036''frontback.txt'   \
            ''$'\037''frontback.txt'   \
            ''$'\177''frontback.txt'   \
            ''$'\t''frontback.txt'     \
            ''$'\n''frontback.txt'     \
            ''$'\v''frontback.txt'     \
            ''$'\f''frontback.txt'     \
            ''$'\r''frontback.txt'     \
            ' frontback.txt'           \
            '!frontback.txt'           \
            '"frontback.txt'           \
            '#frontback.txt'           \
            %frontback.txt             \
            '&frontback.txt'           \
            "'frontback.txt"           \
            '(frontback.txt'           \
            ')frontback.txt'           \
            '*frontback.txt'           \
            +frontback.txt             \
            ,frontback.txt             \
            -frontback.txt             \
            :frontback.txt             \
            ';frontback.txt'           \
            '<frontback.txt'           \
            '=frontback.txt'           \
            '>frontback.txt'           \
            '?frontback.txt'           \
            '@frontback.txt'           \
            '[frontback.txt'           \
            '\frontback.txt'           \
            ]frontback.txt             \
            '^frontback.txt'           \
            _frontback.txt             \
            '`frontback.txt'           \
            {frontback.txt             \
            '|frontback.txt'           \
            }frontback.txt             \
            '~frontback.txt'           \
            'front'$'\001''back.txt'   \
            'front'$'\002''back.txt'   \
            'front'$'\003''back.txt'   \
            'front'$'\004''back.txt'   \
            'front'$'\005''back.txt'   \
            'front'$'\006''back.txt'   \
            'front'$'\a''back.txt'     \
            'front'$'\b''back.txt'     \
            'front'$'\016''back.txt'   \
            'front'$'\017''back.txt'   \
            'front'$'\020''back.txt'   \
            'front'$'\021''back.txt'   \
            'front'$'\022''back.txt'   \
            'front'$'\023''back.txt'   \
            'front'$'\024''back.txt'   \
            'front'$'\025''back.txt'   \
            'front'$'\026''back.txt'   \
            'front'$'\027''back.txt'   \
            'front'$'\030''back.txt'   \
            'front'$'\031''back.txt'   \
            'front'$'\032''back.txt'   \
            'front'$'\033''back.txt'   \
            'front'$'\034''back.txt'   \
            'front'$'\035''back.txt'   \
            'front'$'\036''back.txt'   \
            'front'$'\037''back.txt'   \
            'front'$'\177''back.txt'   \
            'front'$'\t''back.txt'     \
            'front'$'\n''back.txt'     \
            'front'$'\v''back.txt'     \
            'front'$'\f''back.txt'     \
            'front'$'\r''back.txt'     \
            'front back.txt'           \
            'front!back.txt'           \
            'front"back.txt'           \
            front#back.txt             \
            front%back.txt             \
            'front&back.txt'           \
            "front'back.txt"           \
            'front(back.txt'           \
            'front)back.txt'           \
            'front*back.txt'           \
            front+back.txt             \
            front,back.txt             \
            front-back.txt             \
            front.back.txt             \
            front:back.txt             \
            'front;back.txt'           \
            'front<back.txt'           \
            'front=back.txt'           \
            'front>back.txt'           \
            'front?back.txt'           \
            'front@back.txt'           \
            'front[back.txt'           \
            'front\back.txt'           \
            front]back.txt             \
            'front^back.txt'           \
            front_back.txt             \
            'front`back.txt'           \
            front{back.txt             \
            'front|back.txt'           \
            front}back.txt             \
            front~back.txt             \
            'frontback'$'\001''.txt'   \
            'frontback'$'\002''.txt'   \
            'frontback'$'\003''.txt'   \
            'frontback'$'\004''.txt'   \
            'frontback'$'\005''.txt'   \
            'frontback'$'\006''.txt'   \
            'frontback'$'\a''.txt'     \
            'frontback'$'\b''.txt'     \
            'frontback'$'\016''.txt'   \
            'frontback'$'\017''.txt'   \
            'frontback'$'\020''.txt'   \
            'frontback'$'\021''.txt'   \
            'frontback'$'\022''.txt'   \
            'frontback'$'\023''.txt'   \
            'frontback'$'\024''.txt'   \
            'frontback'$'\025''.txt'   \
            'frontback'$'\026''.txt'   \
            'frontback'$'\027''.txt'   \
            'frontback'$'\030''.txt'   \
            'frontback'$'\031''.txt'   \
            'frontback'$'\032''.txt'   \
            'frontback'$'\033''.txt'   \
            'frontback'$'\034''.txt'   \
            'frontback'$'\035''.txt'   \
            'frontback'$'\036''.txt'   \
            'frontback'$'\037''.txt'   \
            'frontback'$'\177''.txt'   \
            'frontback'$'\t''.txt'     \
            'frontback'$'\n''.txt'     \
            'frontback'$'\v''.txt'     \
            'frontback'$'\f''.txt'     \
            'frontback'$'\r''.txt'     \
            'frontback .txt'           \
            'frontback!.txt'           \
            'frontback".txt'           \
            frontback#.txt             \
            frontback%.txt             \
            'frontback&.txt'           \
            "frontback'.txt"           \
            'frontback(.txt'           \
            'frontback).txt'           \
            'frontback*.txt'           \
            frontback+.txt             \
            frontback,.txt             \
            frontback-.txt             \
            'frontback.'$'\001''txt'   \
            'frontback.'$'\002''txt'   \
            'frontback.'$'\003''txt'   \
            'frontback.'$'\004''txt'   \
            'frontback.'$'\005''txt'   \
            'frontback.'$'\006''txt'   \
            'frontback.'$'\a''txt'     \
            'frontback.'$'\b''txt'     \
            'frontback.'$'\016''txt'   \
            'frontback.'$'\017''txt'   \
            'frontback.'$'\020''txt'   \
            'frontback.'$'\021''txt'   \
            'frontback.'$'\022''txt'   \
            'frontback.'$'\023''txt'   \
            'frontback.'$'\024''txt'   \
            'frontback.'$'\025''txt'   \
            'frontback.'$'\026''txt'   \
            'frontback.'$'\027''txt'   \
            'frontback.'$'\030''txt'   \
            'frontback.'$'\031''txt'   \
            'frontback.'$'\032''txt'   \
            'frontback.'$'\033''txt'   \
            'frontback.'$'\034''txt'   \
            'frontback.'$'\035''txt'   \
            'frontback.'$'\036''txt'   \
            'frontback.'$'\037''txt'   \
            'frontback.'$'\177''txt'   \
            'frontback.'$'\t''txt'     \
            'frontback.'$'\n''txt'     \
            'frontback.'$'\v''txt'     \
            'frontback.'$'\f''txt'     \
            'frontback.'$'\r''txt'     \
            'frontback. txt'           \
            'frontback.!txt'           \
            'frontback."txt'           \
            frontback.#txt             \
            frontback.%txt             \
            'frontback.&txt'           \
            "frontback.'txt"           \
            'frontback.(txt'           \
            'frontback.)txt'           \
            'frontback.*txt'           \
            frontback.+txt             \
            frontback.,txt             \
            frontback.-txt             \
            frontback..txt             \
            frontback.:txt             \
            'frontback.;txt'           \
            'frontback.<txt'           \
            'frontback.=txt'           \
            'frontback.>txt'           \
            'frontback.?txt'           \
            'frontback.@txt'           \
            'frontback.[txt'           \
            'frontback.\txt'           \
            frontback.]txt             \
            'frontback.^txt'           \
            frontback._txt             \
            'frontback.`txt'           \
            frontback.{txt             \
            'frontback.|txt'           \
            frontback.}txt             \
            frontback.~txt             \
            frontback:.txt             \
            'frontback;.txt'           \
            'frontback<.txt'           \
            'frontback=.txt'           \
            'frontback>.txt'           \
            'frontback?.txt'           \
            'frontback@.txt'           \
            'frontback[.txt'           \
            'frontback\.txt'           \
            frontback].txt             \
            'frontback^.txt'           \
            frontback_.txt             \
            'frontback`.txt'           \
            frontback{.txt             \
            'frontback|.txt'           \
            frontback}.txt             \
            frontback~.txt             \
; do
  echo "*** STARTING ***"
  echo "NAME: ${name}"
  rclone copy -v --size-only --sftp-set-modtime=false ./"${name}" "${RCLONE_REMOTE}:${ARCHIVE_PATH}"
  echo "*** DONE ***"
  echo ""                       
done
