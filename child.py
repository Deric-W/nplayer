import subprocess,sys
def run(playerpath,file,frames):
    NULL = subprocess.run([playerpath,"-n",str(frames),"-q",file],shell=False,check=True)
    sys.exit(0)