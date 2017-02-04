import pyrebase
def startFirebaseCacheStream(FBC):	
	config = {
		"apiKey": "mykey",
		"authDomain": "scouting-2017-5f51c.firebaseapp.com",
		"databaseURL": "https://scouting-2017-5f51c.firebaseio.com/",
		"storageBucket": "scouting-2017-5f51c.appspot.com"
	}

	f = pyrebase.initialize_app(config)
	fb = f.database()
	fb.stream(FBC.cacheFirebase)