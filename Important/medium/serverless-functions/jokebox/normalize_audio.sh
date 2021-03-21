#!/bin/bash

# maybe you want to edit this parameter
TARGET_VOLUME=-14.0

# rename files with UUIDs
for file in *.mp3; do mv "$file" `uuidgen | tr '[:upper:]' '[:lower:]'`.mp3; done

# set file counters
NUMBER_OF_FILES=$(ls *.mp3 | wc | awk '{print $1}')
COUNTER=1

# loop and convert audio files
for FILE_NAME in $(ls *.mp3)
do
  # print some output
  echo "(${COUNTER}/${NUMBER_OF_FILES}) normalizing ${FILE_NAME}..."
  # find out current file mean volume
  FILE_MEAN_VOLUME=$(ffmpeg -i $FILE_NAME -filter:a volumedetect -f null /dev/null 2>&1 | grep mean_volume | awk -F':' '{print $2}' | awk '{print $1}')
  # calculate delta from current file versus desired volume
  MEAN_DIFFERENCE=$(echo "$TARGET_VOLUME- $FILE_MEAN_VOLUME" | bc)
  # normalize volume from current file
  ffmpeg -loglevel panic -i ${FILE_NAME} -filter:a "volume=${MEAN_DIFFERENCE}dB" "normalized_"${FILE_NAME}
  let COUNTER=COUNTER+1
done