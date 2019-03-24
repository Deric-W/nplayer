import threading,time,traceback,json,os,sys,child

def sanitize(path):
	return path.replace("/","").replace("\\","")

#args: -p path to mpg123 file
try:
	if sys.argv[1] == "-p":
		playerpath = os.path.abspath(sys.argv[2])
		file = sys.argv[3]
	else:
		if sys.platform[0:3] == "win": #windows
			playerpath = os.path.abspath("./bin/windows/mpg123.exe")
		else:
			playerpath = os.path.abspath("./bin/unix/mpg123")
		file = sys.argv[1]
except IndexError:
	sys.exit("Error: bad parameters")

file_content = json.load(open(file,"r"))
tact = file_content["header"]["tact"]
base = file_content["header"]["base"]
packdb = {}
for include in file_content["header"]["includes"]:
	try:
		packdata = json.load(open("./packs/" + sanitize(include) + "/pack.json","r"))
		packdb[include] = [packdata["samplerate"],os.path.abspath("./packs/" + sanitize(include)),sanitize(packdata["extension"])]
	except:
		sys.exit("Error: failed to include " + include)
#print(packdb)
#print(playerpath)
for group in file_content["notes"]:
	counter = 0
	for sound in file_content["notes"][group]["sounds"]:
		file = packdb[file_content["notes"][group]["packs"][counter]]
		file = file[1] + "/" + sanitize(sound) + file[2]
		frames = base * ((1/file_content["notes"][group]["types"][counter])/tact) * packdb[file_content["notes"][group]["packs"][counter]][0]   #base * (type/tact) * samplerate
		#print(playerpath)
		#print(file)
		#print(frames)
		#print()
		threading.Thread(target=child.run,daemon=True,args=(playerpath,file,frames/1000)).start()
		counter = counter + 1
	if file_content["notes"][group]["wait"]:
			#print(base * (sorted(file_content["notes"][group]["types"])[-1]/tact))
			time.sleep(int(base * (1/sorted(file_content["notes"][group]["types"])[-1]/tact)))

counter = 0
while threading.active_count() > 1 and counter < 10: #Abbruch nach 1 Sekunden
	time.sleep(0.1)
	counter = counter + 1
	#print(threading.active_count())
if counter >= 10:
	print("Warning: terminated with " + str(threading.active_count()-1) + " threads remaining")		
