
import threading,time,traceback,json,sys,os
os.chdir(os.path.dirname(os.path.abspath(sys.argv[0]))) 	#switch to script directory
import child

def sanitize(path):											#to prevent directory traversal
	return path.replace("/","").replace("\\","")

mode = ""													#parser for args: -d = debug mode, -p path = playerpath, file = file
debug = False
if sys.platform[0:3] == "win":
	playerpath = os.path.abspath("./bin/windows/mpg123.exe")
else:
	playerpath = os.path.abspath("./bin/unix/mpg123")

for param in sys.argv[1:]:
	if mode == "-p":
		playerpath = os.path.abspath(param)
		mode = ""
	else:
		if param == "-p":
			mode = "-p"
		elif param == "-d":
			debug = True
		else:
			file = os.path.abspath(param)
if debug:
	print("Argv : " + str(sys.argv[1:]))
	print("Debug : True")
	print("Playerpath : " + str(playerpath))
	print("File : " + file)
			
file_content = json.load(open(file,"r"))
tact = file_content["header"]["tact"]
base = file_content["header"]["base"]
packdb = {}
for include in file_content["header"]["includes"]:			#create pack database
	try:
		packdata = json.load(open("./packs/" + sanitize(include) + "/pack.json","r"))
		packdb[include] = [packdata["samplerate"],os.path.abspath("./packs/" + sanitize(include)),sanitize(packdata["extension"])]
	except:
		sys.exit("Error: failed to include " + include)
if debug:
	print("Packdb : " + str(packdb),end="\n\n")

for group in file_content["notes"]:							#start playing notes
	counter = 0
	for sound in file_content["notes"][group]["sounds"]:
		file = packdb[file_content["notes"][group]["packs"][counter]]
		file = file[1] + "/" + sanitize(sound) + file[2]
		frames = base * ((1/file_content["notes"][group]["types"][counter])/tact) * packdb[file_content["notes"][group]["packs"][counter]][0]   #base * (type/tact) * samplerate = time
		if debug:
			print("Playerpath : " + str(playerpath))
			print("File : " + file)
			print("Frames : " + str(frames),end="\n\n")
		threading.Thread(target=child.run,daemon=True,args=(playerpath,file,frames/1000)).start()	#play note with child
		counter = counter + 1
	if file_content["notes"][group]["wait"]:
			if debug:	
				print("Wait : " + str(base * (1/sorted(file_content["notes"][group]["types"])[0]/tact)),end="\n\n\n")
			time.sleep(float(base * (1/sorted(file_content["notes"][group]["types"])[0]/tact)))

counter = 0
while threading.active_count() > 1 and counter < 100: 	#exit after 10 seconds or with no threads
	counter = counter + 1
	if debug:
		print("Threads : " + str(threading.active_count()-1))
		print("Counter : " + str(counter))
	time.sleep(0.1)
if counter >= 100:
	print("Warning: terminated with " + str(threading.active_count()-1) + " threads remaining")		
