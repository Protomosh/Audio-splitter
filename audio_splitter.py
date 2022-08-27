import sys
import subprocess
import os
import traceback

class WrongFileType(Exception):
    """Raised when the input file is not supported"""
    pass


def split(droppedFile,mode,debug):
    ''' Dropped file as mp3 or wav , Mode 1 = analyze Mode 2 = normalize Mode 3 = Split only Mode 4 = Split with silence removal
     debug = 0/1 keeps terminal open '''

    # create new Output folder if missing
    try:
        os.makedirs((os.getcwd()+'/output'), exist_ok=False)
    except OSError:
        pass

    try:
        extension = os.path.splitext(droppedFile)[1]    # Get file extension

        if not extension in [".wav",".mp3"]:            # Raise exeption if other than .wav file dragged.
            raise WrongFileType

        inputfile = (droppedFile.replace('\\', '/'))    # Fixing correct filepath style

        full_filename = os.path.basename(inputfile)
        filename = os.path.splitext(full_filename)[0]

        if not (filename[:2].isdigit()):                   # Checking if file doesnt have index number.
            file_number = "01" 
            new_filename = "_" + filename     

        else :
            file_number = filename[:2]                  # Gettings first 2 characters from filename to file_numbers
            new_filename = filename[2:]                 # Creating new filename without first 2 characters.

        # Creating ffmpeg command parameters for 
        # Removing silence from end and begining
        # Splitting audio files and create right filenumbers for new ones
        # Converting to 32KHz 16bit Mono .wav file

        if mode == 1:
            # Analyze audio file
            cmd = analyze_cmd = (
            "ffmpeg -hide_banner \
            -i {} \
            -af volumedetect -vn -sn -dn -f null NUL".format(inputfile))

            print("Analyzing...")

        if mode == 2:
            # Split only
            cmd = split_cmd = (
            "ffmpeg -hide_banner \
            -i {}  \
            -f segment -segment_time 2 -segment_start_number {} -map_metadata -1 -bitexact\
            -acodec pcm_s16le -ac 1 -ar 32000 output/%02d{}.wav"
            .format(inputfile,file_number,new_filename))

            print("Splitting...")
        
        if mode == 3:
            # Split with silence removal
            #  buggy
            cmd = split_silence= (
            "ffmpeg -hide_banner \
            -i {}  \
            -af silenceremove=start_periods=1:detection=peak:start_duration=1:start_silence=0.05:start_threshold=0.02:stop_periods=1:stop_duration=1:stop_silence=0.05:stop_threshold=0.02\
            -f -segment_time 2 -segment_start_number {} -map_metadata -1 -bitexact\
            -acodec pcm_s16le -ac 1 -ar 32000 output/%02d{}.wav"
            .format(inputfile,file_number,new_filename))

            print("Deleting silence and splitting...")

        subprocess.run(cmd,shell=True, check=True)


    #Error catching to keep terminal in case of errors.
    except WrongFileType:
        print("Wrong file type. Only [.wav .mp3] files are supported.")
        print("\nPress enter to exit.")
        input()
        sys.exit(1)

    except subprocess.CalledProcessError as e:
        print("\nPress enter to exit.")
        input()
        sys.exit(1)

    except BaseException:
        print ("\n",sys.exc_info()[0])
        print("\n",traceback.format_exc())
        input()
        sys.exit(1)

    print("\nExited without errors.")

    if debug:
        print("\nPress enter to exit.")
        input()