#!/usr/bin/env bash


# Akimov D. 2021@ MACH UNIT


# Path to executables
EXEC_PATH=/home/pi/Desktop/otis_project/pngview/

# Check if temp video dir exists
cd $EXEC_PATH
[ -d video ] || (mkdir video && echo "Local video directrory was created")


# Check if usb flash drive is present as block device
if ls /./dev/sd*
then
   echo "Found USB disk!"
   
   # Find usb drive mountpoint path and cd to it
   MOUNT_DIR=$(lsblk -o mountpoint | grep 'media')
   cd $MOUNT_DIR
   
   # Try to find video files with estimated names 01.mp4-99.mp4
   if ls [0-9][1-9].mp4
   then
        echo "Found some videos!"
        
		# Check if output.mp4 already exists and delete if it is
		cd $EXEC_PATH
		[ -e video/output.mp4 ] && rm -f video/output.mp4
                		
		cd $MOUNT_DIR
		
		# Delete temp files
        rm -f *.ts
                
		for video in [0-9][1-9].mp4 
		do
			ffmpeg -y -i $video -c copy -bsf:v h264_mp4toannexb -f mpegts $video.ts
		done

		CONCAT=$(echo $(ls -v *.ts) | sed -e "s/ /|/g")
		
		# Merge videos into one file
		ffmpeg -y -i "concat:$CONCAT" -c copy -bsf:a aac_adtstoasc /home/pi/Desktop/otis_project/pngview/video/output.mp4

		# Delete temp files
        rm -f *.ts

         echo "Dynamic mode"
         cd $EXEC_PATH
        
		omxplayer  --loop --no-osd video/output.mp4 &
        ./rasp_uim -dynamic /dev/ttyAMA0  &
        ./supervisor.sh  &
   else
        echo "Video files aren't present! Static image mode"
    
		cd $EXEC_PATH
		 
        ./rasp_uim -static  /dev/ttyAMA0 &
        ./supervisor.sh &
   fi
   
else
    echo "Can't find USB disk! Static image mode"
    
	cd $EXEC_PATH
	
    ./rasp_uim -static  /dev/ttyAMA0 &
    ./supervisor.sh &
fi

exit 0





