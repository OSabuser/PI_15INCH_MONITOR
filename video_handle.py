import os
import subprocess

path_to_video = "/./home/mach/PI_15INCH_MONITOR/video/test_1024x768.mp4"

is_video_exist = os.path.exists(path_to_video)

if is_video_exist:
    command = ['/./usr/bin/cvlc', '--no-osd', path_to_video]
    subprocess.run(command)