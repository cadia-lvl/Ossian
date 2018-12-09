#!/usr/bin/env bash

# Define bash variables
OSSIAN=/home/alexander/Documents/text_to_speech/projects/Ossian_py3
LANGUAGE=ice
SPEAKER=ivona
RECIPE=lvl_lex_01_nn
TEXT_DIR=/home/alexander/Documents/text_to_speech/projects/Ossian_py3/test/txt
WAV_DIR=/home/alexander/Documents/text_to_speech/projects/Ossian_py3/test/wav
FILELIST=/home/alexander/Documents/text_to_speech/projects/Ossian_py3/voices/ice/ivona/lvl_lex_01_nn/output/filelist.txt


# TODO: delete files in voice directories

# Create filelist file
touch $FILELIST

# Run through all files in TEXT_DIR
cd $OSSIAN
for x in `find $TEXT_DIR -name "*.txt" | sort`; do
  x=`basename $x | sed 's:\.txt$::'`
  scripts/speak.py -l $LANGUAGE -s $SPEAKER -o $WAV_DIR/$x.wav $RECIPE $TEXT_DIR/$x.txt
  echo $x >> $FILELIST
done
