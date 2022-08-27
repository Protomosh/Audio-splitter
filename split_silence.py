import audio_splitter as a
import sys

# (filepath,mode,debug)
# Mode 1= analyze ,Mode 2= Split only, Mode 3= Split with silence removal
# debug = 0/1 keeps terminal open
# !! BUGGY !!

a.split(sys.argv[1],3,1)

