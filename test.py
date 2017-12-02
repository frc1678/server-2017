
'''
 timds = pbc.firebase.child('TeamInMatchDatas').get().val()
 for key, timd in timds.items():
 	 superNotesVal = timd.get('superNotes')
	 if superNotesVal:
	 	 supNotes = superNotesVal.get('finalNotes') if superNotesVal.get('finalNotes') else superNotesVal.get('firstNotes')
	 	 timd['superNotes'] = supNotes
	 print(type(timd.get('superNotes')))
	 print(key)
	 if type(timd.get('superNotes')) == dict:
		 print('DICT')
		 pbc.firebase.child('TeamInMatchDatas').child(key).child('superNotes').set(timd.get('superNotes').get('firstNotes'))	

 matches = pbc.firebase.child('Matches').get().val()
 for m in matches[1:]:
 	 if m.get('redAllianceTeamNumbers') == None:
		 print(m)
'''
teams = [
	{
		'pitSelectedImageName': '6060_2017-04-06 17:48:16.6290 -0700',
		'name': 'Circuit Serpents',
		'pitDriveTrain': 'Tank Drive',
		'pitProgrammingLanguage': 'Java',
		'pitAllImageURLs': {
			'-Kh4scRWFreei8VEQPZp': 'https:\/\/firebasestorage.googleapis.com\/v0\/b\/scouting-2017-5f51c.appspot.com\/o\/6060_2017-04-06%2017:48:16.6290%20-0700.png?alt=media&token=1ae4dfbb-a487-4306-ac11-91283c8cfaba'
		},
		'imageKeys': {
			'-Kh4sWOYZrNIeEulM6KG': '6060_2017-04-06 17:48:16.6290 -0700'
		},
		'number': 6060,
		'pitDidDemonstrateCheesecakePotential': False
	}, {
		'pitSelectedImageName': '1138_2017-04-06 12:36:15.1470 -0700',
		'name': 'Eagle Engineering',
		'pitDriveTrain': 'Tank Drive',
		'pitProgrammingLanguage': 'C++',
		'pitAllImageURLs': {
			'-Kh3lNL0FRoRNHNS1Sc2': 'https:\/\/firebasestorage.googleapis.com\/v0\/b\/scouting-2017-5f51c.appspot.com\/o\/1138_2017-04-06%2012:36:15.1470%20-0700.png?alt=media&token=77b134d1-db84-4ed6-9fc6-07d1f4727ac5'
		},
		'imageKeys': {
			'-Kh3l5ipIrUBcZY1oIPQ': '1138_2017-04-06 12:36:15.1470 -0700'
		},
		'number': 1138,
		'pitDidDemonstrateCheesecakePotential': False
	}, {
		'pitSelectedImageName': '6436_2017-04-06 13:46:47.0020 -0700',
		'name': 'PARS ROBOTIC TEAM',
		'pitDriveTrain': 'Tank Drive',
		'pitProgrammingLanguage': 'Labview',
		'pitAllImageURLs': {
			'-Kh40W0t1qezjWjAMPOu': 'https:\/\/firebasestorage.googleapis.com\/v0\/b\/scouting-2017-5f51c.appspot.com\/o\/6436_2017-04-06%2013:46:47.0020%20-0700.png?alt=media&token=88e765df-1d6f-4369-9e18-827ad93d526a'
		},
		'imageKeys': {
			'-Kh40EsMc0JN6fCYPA10': '6436_2017-04-06 13:46:47.0020 -0700'
		},
		'number': 6436,
		'pitDidDemonstrateCheesecakePotential': False
	}, {
		'name': 'Robowranglers',
		'number': 148
	}, {
		'pitSelectedImageName': '3011_2017-04-06 10:34:34.5800 -0700',
		'name': 'RoboWarriors',
		'pitDriveTrain': 'Swerve',
		'pitProgrammingLanguage': 'Java',
		'pitAllImageURLs': {
			'-Kh3KrMJJW_MCjO1odvl': 'https:\/\/firebasestorage.googleapis.com\/v0\/b\/scouting-2017-5f51c.appspot.com\/o\/3011_2017-04-06%2010:34:34.5800%20-0700.png?alt=media&token=3e484d15-4a7e-4b2e-993a-4fcad3702157'
		},
		'imageKeys': {
			'-Kh3KFMs8T08nz7D9vjA': '3011_2017-04-06 10:34:34.5800 -0700'
		},
		'number': 3011,
		'pitDidDemonstrateCheesecakePotential': False
	}, {
		'pitSelectedImageName': '5089_2017-04-06 11:16:00.4760 -0700',
		'name': 'Robo-Nerds',
		'pitDriveTrain': 'Tank Drive',
		'pitProgrammingLanguage': 'Labview',
		'pitAllImageURLs': {
			'-Kh3TyK6go7okwKKeLQi': 'https:\/\/firebasestorage.googleapis.com\/v0\/b\/scouting-2017-5f51c.appspot.com\/o\/5089_2017-04-06%2011:16:00.4760%20-0700.png?alt=media&token=cf422311-0088-4fa0-854c-f2c7c253d3ac'
		},
		'imageKeys': {
			'-Kh3TjHKwQjDr3qd9er3': '5089_2017-04-06 11:16:00.4760 -0700'
		},
		'number': 5089,
		'pitDidDemonstrateCheesecakePotential': False
	}, {
		'pitSelectedImageName': '691_2017-04-06 13:13:51.0150 -0700',
		'name': 'Project 691',
		'pitDriveTrain': 'Tank Drive',
		'pitProgrammingLanguage': 'Java',
		'pitAllImageURLs': {
			'-Kh3tzm3NcemHoazbEmh': 'https:\/\/firebasestorage.googleapis.com\/v0\/b\/scouting-2017-5f51c.appspot.com\/o\/691_2017-04-06%2013:13:51.0150%20-0700.png?alt=media&token=1d74d8d3-780a-40dd-bae6-83ae206e09d8'
		},
		'imageKeys': {
			'-Kh3thU3UZlTm_Di0Mja': '691_2017-04-06 13:13:51.0150 -0700'
		},
		'number': 691,
		'pitAvailableWeight': 23,
		'pitDidDemonstrateCheesecakePotential': True
	}, {
		'pitSelectedImageName': '5429_2017-04-06 15:27:44.1980 -0700',
		'name': 'Black Knights',
		'pitDriveTrain': 'Tank Drive',
		'pitProgrammingLanguage': 'Java',
		'pitAllImageURLs': {
			'-Kh4Ne2spNJNKcWpxKKh': 'https:\/\/firebasestorage.googleapis.com\/v0\/b\/scouting-2017-5f51c.appspot.com\/o\/5429_2017-04-06%2015:27:44.1980%20-0700.png?alt=media&token=027bae62-4102-4012-859f-3e8d0b3ed43a'
		},
		'imageKeys': {
			'-Kh4NLhfnaiolivveiFt': '5429_2017-04-06 15:27:44.1980 -0700'
		},
		'number': 5429,
		'pitDidDemonstrateCheesecakePotential': False
	}, {
		'pitSelectedImageName': '842_2017-04-06 15:13:47.9030 -0700',
		'name': 'Falcon Robotics',
		'pitDriveTrain': 'Tank Drive',
		'pitProgrammingLanguage': 'C++',
		'pitAllImageURLs': {
			'-Kh4KN1mkjHc3949CMX-': 'https:\/\/firebasestorage.googleapis.com\/v0\/b\/scouting-2017-5f51c.appspot.com\/o\/842_2017-04-06%2015:13:47.9030%20-0700.png?alt=media&token=d89961e8-5a0d-4303-87c5-33f812f140ec'
		},
		'imageKeys': {
			'-Kh4K9WDrcwqtPwzTl1I': '842_2017-04-06 15:13:47.9030 -0700'
		},
		'number': 842,
		'pitDidDemonstrateCheesecakePotential': False
	}, {
		'pitSelectedImageName': '5199_2017-04-06 11:18:54.9550 -0700',
		'name': 'Robot Dolphins From Outer Space',
		'pitDriveTrain': 'Tank Drive',
		'pitProgrammingLanguage': 'Java',
		'pitAllImageURLs': {
			'-Kh3UUdZ1zcnIxKTSwfI': 'https:\/\/firebasestorage.googleapis.com\/v0\/b\/scouting-2017-5f51c.appspot.com\/o\/5199_2017-04-06%2011:18:54.9550%20-0700.png?alt=media&token=bf0d05b4-0684-4d3c-b484-4036cb65aef1'
		},
		'imageKeys': {
			'-Kh3UOt3td1wyu_i_uHu': '5199_2017-04-06 11:18:54.9550 -0700'
		},
		'number': 5199,
		'pitDidDemonstrateCheesecakePotential': False
	}, {
		'name': 'EntreBots',
		'number': 6405,
		'pitDidDemonstrateCheesecakePotential': False
	}, {
		'pitSelectedImageName': '1538_2017-04-06 09:43:06.5430 -0700',
		'name': 'The Holy Cows',
		'pitDriveTrain': 'Tank Drive',
		'pitProgrammingLanguage': 'C++',
		'pitAllImageURLs': {
			'-Kh38mR5fT8RF716nWwN': 'https:\/\/firebasestorage.googleapis.com\/v0\/b\/scouting-2017-5f51c.appspot.com\/o\/1538_2017-04-06%2009:43:06.5430%20-0700.png?alt=media&token=894ea78c-0419-4186-bec0-fb10a011647d'
		},
		'imageKeys': {
			'-Kh38TSIZIqjmUBU-Fp2': '1538_2017-04-06 09:43:06.5430 -0700'
		},
		'number': 1538,
		'pitDidDemonstrateCheesecakePotential': False
	}, {
		'pitSelectedImageName': '4160_2017-04-06 17:51:36.6540 -0700',
		'name': 'The RoBucs',
		'pitDriveTrain': 'Tank Drive',
		'pitProgrammingLanguage': 'C++',
		'pitAllImageURLs': {
			'-Kh4tYEU9lZtcC3GXvRd': 'https:\/\/firebasestorage.googleapis.com\/v0\/b\/scouting-2017-5f51c.appspot.com\/o\/4160_2017-04-06%2017:51:50.9200%20-0700.png?alt=media&token=4b106af4-f96d-448f-9357-af0dd51a8729',
			'-Kh4tQen8rzzEWu55HNp': 'https:\/\/firebasestorage.googleapis.com\/v0\/b\/scouting-2017-5f51c.appspot.com\/o\/4160_2017-04-06%2017:51:36.6540%20-0700.png?alt=media&token=118413c4-2a59-43ea-9fae-d9b4ae25d6e9'
		},
		'imageKeys': {
			'-Kh4tHEBsjMBdfkyQe1U': '4160_2017-04-06 17:51:36.6540 -0700',
			'-Kh4tKhjMXPnITFQVCm9': '4160_2017-04-06 17:51:50.9200 -0700'
		},
		'number': 4160,
		'pitDidDemonstrateCheesecakePotential': False
	}, {
		'pitSelectedImageName': '649_2017-04-06 09:22:04.9120 -0700',
		'name': 'M-SET Fish',
		'pitDriveTrain': 'Tank Drive',
		'pitProgrammingLanguage': 'Java',
		'pitAllImageURLs': {
			'-Kh33zjlfCiDLixoOIYv': 'https:\/\/firebasestorage.googleapis.com\/v0\/b\/scouting-2017-5f51c.appspot.com\/o\/649_2017-04-06%2009:22:04.9120%20-0700.png?alt=media&token=8143320f-d8fe-4b39-b8e4-2b60af1e44bc'
		},
		'imageKeys': {
			'-Kh33eS5F06buG46omUW': '649_2017-04-06 09:22:04.9120 -0700'
		},
		'number': 649,
		'pitDidDemonstrateCheesecakePotential': False
	}, {
		'pitSelectedImageName': '5453_2017-04-06 13:54:53.0260 -0700',
		'name': 'RED COMET',
		'pitDriveTrain': 'Mecanum',
		'pitProgrammingLanguage': 'Labview',
		'pitAllImageURLs': {
			'-Kh42COyqf0lQjC8M8WQ': 'https:\/\/firebasestorage.googleapis.com\/v0\/b\/scouting-2017-5f51c.appspot.com\/o\/5453_2017-04-06%2013:54:53.0260%20-0700.png?alt=media&token=65e22a3b-e44b-4f0d-8cbd-aa260eddf41a'
		},
		'imageKeys': {
			'-Kh425Y5WPTVl23I98t8': '5453_2017-04-06 13:54:53.0260 -0700'
		},
		'number': 5453,
		'pitDidDemonstrateCheesecakePotential': False
	}, {
		'pitSelectedImageName': '6519_2017-04-06 09:31:31.8110 -0700',
		'name': 'The Vegas Vortechs',
		'pitDriveTrain': 'Tank Drive',
		'pitProgrammingLanguage': 'Java',
		'pitAllImageURLs': {
			'-Kh362iu96hIRwPSsE_O': 'https:\/\/firebasestorage.googleapis.com\/v0\/b\/scouting-2017-5f51c.appspot.com\/o\/6519_2017-04-06%2009:31:31.8110%20-0700.png?alt=media&token=9876336d-f8cc-4c6c-bbcf-d7fe0fd4f98d'
		},
		'imageKeys': {
			'-Kh35oqJ9VkEUJx__d9N': '6519_2017-04-06 09:31:31.8110 -0700'
		},
		'number': 6519,
		'pitDidDemonstrateCheesecakePotential': False
	}, {
		'name': 'Robonauts',
		'number': 118,
		'pitDidDemonstrateCheesecakePotential': False
	}, {
		'pitSelectedImageName': '1828_2017-04-06 09:48:27.5800 -0700',
		'name': 'BoxerBots',
		'pitDriveTrain': 'Mecanum',
		'pitProgrammingLanguage': 'Labview',
		'pitAllImageURLs': {
			'-Kh39yRoXidEZQH4ihp3': 'https:\/\/firebasestorage.googleapis.com\/v0\/b\/scouting-2017-5f51c.appspot.com\/o\/1828_2017-04-06%2009:48:27.5800%20-0700.png?alt=media&token=2ce9d895-d0d7-4728-a400-a97497fb190a'
		},
		'imageKeys': {
			'-Kh39gqDhvq8xlwAj0eS': '1828_2017-04-06 09:48:27.5800 -0700'
		},
		'number': 1828,
		'pitDidDemonstrateCheesecakePotential': False
	}, {
		'pitSelectedImageName': '5677_2017-04-06 11:26:36.6500 -0700',
		'name': 'The Subatomic Smarticles',
		'pitDriveTrain': 'Tank Drive',
		'pitProgrammingLanguage': 'Java',
		'pitAllImageURLs': {
			'-Kh3WGBN6r6Kkh0lmLZa': 'https:\/\/firebasestorage.googleapis.com\/v0\/b\/scouting-2017-5f51c.appspot.com\/o\/5677_2017-04-06%2011:26:36.6500%20-0700.png?alt=media&token=24a9baa4-cae2-4868-9349-f6351a624d3a',
			'-Kh3WBjlHpsaQmHdrGpD': 'https:\/\/firebasestorage.googleapis.com\/v0\/b\/scouting-2017-5f51c.appspot.com\/o\/5677_2017-04-06%2011:26:20.9040%20-0700.png?alt=media&token=85223ba1-c856-4a09-8d66-6848c7a992e0'
		},
		'imageKeys': {
			'-Kh3W5kxuqkT_ZYrdLEs': '5677_2017-04-06 11:26:20.9040 -0700',
			'-Kh3W9aYQf4HN5gJ6YqN': '5677_2017-04-06 11:26:36.6500 -0700'
		},
		'number': 5677,
		'pitDidDemonstrateCheesecakePotential': False
	}, {
		'pitSelectedImageName': '60_2017-04-06 09:14:23.2340 -0700',
		'name': 'Bionic Bulldogs',
		'pitDriveTrain': 'Tank Drive',
		'pitProgrammingLanguage': 'Labview',
		'pitAllImageURLs': {
			'-Kh31z-35bjugQH_3ZKK': 'https:\/\/firebasestorage.googleapis.com\/v0\/b\/scouting-2017-5f51c.appspot.com\/o\/60_2017-04-06%2009:14:23.2340%20-0700.png?alt=media&token=566a99b2-5cfd-4a50-b57d-585b2be75bd1',
			'-Kh321UNTUWWTABD8LZd': 'https:\/\/firebasestorage.googleapis.com\/v0\/b\/scouting-2017-5f51c.appspot.com\/o\/60_2017-04-06%2009:14:36.7000%20-0700.png?alt=media&token=4470b471-d2c1-44a5-9e2a-dde20e05a1d1'
		},
		'imageKeys': {
			'-Kh31tj4yDW6UCzA_Xid': '60_2017-04-06 09:14:23.2340 -0700',
			'-Kh31x0FL2M7cJBX3tDK': '60_2017-04-06 09:14:36.7000 -0700'
		},
		'number': 60,
		'pitDidDemonstrateCheesecakePotential': False
	}, {
		'pitSelectedImageName': '3647_2017-04-06 10:49:21.8510 -0700',
		'name': 'Millennium Falcons',
		'pitDriveTrain': 'Tank Drive',
		'pitProgrammingLanguage': 'Java',
		'pitAllImageURLs': {
			'-Kh3O71x49l7Qg1-MXj3': 'https:\/\/firebasestorage.googleapis.com\/v0\/b\/scouting-2017-5f51c.appspot.com\/o\/3647_2017-04-06%2010:49:21.8510%20-0700.png?alt=media&token=27dceaea-effe-4f68-a4a3-d0c696a00850'
		},
		'imageKeys': {
			'-Kh3NczKn8jLfvNPcxhg': '3647_2017-04-06 10:49:21.8510 -0700'
		},
		'number': 3647,
		'pitDidDemonstrateCheesecakePotential': False
	}, {
		'pitSelectedImageName': '4470_2017-04-06 11:03:01.7860 -0700',
		'name': 'TiGears',
		'pitDriveTrain': 'Tank Drive',
		'pitProgrammingLanguage': 'C++',
		'pitAllImageURLs': {
			'-Kh3R-EKCsFknTIZQLmi': 'https:\/\/firebasestorage.googleapis.com\/v0\/b\/scouting-2017-5f51c.appspot.com\/o\/4470_2017-04-06%2011:03:01.7860%20-0700.png?alt=media&token=06cc60d9-c56f-45b9-8069-d3974de2462e'
		},
		'imageKeys': {
			'-Kh3QlA6DIumJr32igwl': '4470_2017-04-06 11:03:01.7860 -0700'
		},
		'number': 4470,
		'pitDidDemonstrateCheesecakePotential': False
	}, {
		'pitSelectedImageName': '5458_2017-04-06 11:23:27.4300 -0700',
		'name': 'Digital Minds',
		'pitDriveTrain': 'Tank Drive',
		'pitProgrammingLanguage': 'C++',
		'pitAllImageURLs': {
			'-Kh3Vf2iCg-BaCyQE6LV': 'https:\/\/firebasestorage.googleapis.com\/v0\/b\/scouting-2017-5f51c.appspot.com\/o\/5458_2017-04-06%2011:23:27.4300%20-0700.png?alt=media&token=a866501c-1cee-4b1b-b16c-d5f1a1c5666c'
		},
		'imageKeys': {
			'-Kh3VRP8ccdeQbg1z6mS': '5458_2017-04-06 11:23:27.4300 -0700'
		},
		'number': 5458,
		'pitDidDemonstrateCheesecakePotential': False
	}, {
		'pitSelectedImageName': '4501_2017-04-06 13:02:47.7300 -0700',
		'name': 'Humans',
		'pitDriveTrain': 'Tank Drive',
		'pitProgrammingLanguage': 'Java',
		'pitAllImageURLs': {
			'-Kh3s73Zi5KEtMQ0qSkv': 'https:\/\/firebasestorage.googleapis.com\/v0\/b\/scouting-2017-5f51c.appspot.com\/o\/4501_2017-04-06%2013:02:47.7300%20-0700.png?alt=media&token=c3ce8c1e-d91b-4750-979c-77de660b9f30',
			'-Kh3sRgTloEEuomabGOw': 'https:\/\/firebasestorage.googleapis.com\/v0\/b\/scouting-2017-5f51c.appspot.com\/o\/4501_2017-04-06%2013:02:47.7300%20-0700.png?alt=media&token=096fd78d-c95b-4b4b-8971-3a1cf491c864'
		},
		'imageKeys': {
			'-Kh3rAY4ujHTDwq4Mvvy': '4501_2017-04-06 13:02:47.7300 -0700'
		},
		'number': 4501,
		'pitDidDemonstrateCheesecakePotential': False
	}, {
		'pitSelectedImageName': '3009_2017-04-06 10:33:30.0620 -0700',
		'name': 'High Scalers',
		'pitDriveTrain': 'Tank Drive',
		'pitProgrammingLanguage': 'Labview',
		'pitAllImageURLs': {
			'-Kh3K57wkNYlmKSx_5mt': 'https:\/\/firebasestorage.googleapis.com\/v0\/b\/scouting-2017-5f51c.appspot.com\/o\/3009_2017-04-06%2010:33:30.0620%20-0700.png?alt=media&token=faae4cc3-2b4a-41bc-8401-06ffe26e3a1c'
		},
		'imageKeys': {
			'-Kh3K-buWIOYt6cVPaMy': '3009_2017-04-06 10:33:30.0620 -0700'
		},
		'number': 3009,
		'pitDidDemonstrateCheesecakePotential': False
	}, {
		'pitSelectedImageName': '968_2017-04-06 17:46:24.8750 -0700',
		'name': 'RAWC (Robotics Alliance Of West Covina)',
		'pitDriveTrain': 'Tank Drive',
		'pitProgrammingLanguage': 'C++',
		'pitAllImageURLs': {
			'-Kh4sIAX7eLPbXQhLJfZ': 'https:\/\/firebasestorage.googleapis.com\/v0\/b\/scouting-2017-5f51c.appspot.com\/o\/968_2017-04-06%2017:46:24.8750%20-0700.png?alt=media&token=eab04047-8b32-4f24-8eb0-852d967d5e41'
		},
		'imageKeys': {
			'-Kh4s56pACmZnyCif1MI': '968_2017-04-06 17:46:24.8750 -0700'
		},
		'number': 968,
		'pitDidDemonstrateCheesecakePotential': False
	}, {
		'pitSelectedImageName': '987_2017-04-06 09:28:38.1670 -0700',
		'name': 'HIGHROLLERS',
		'pitDriveTrain': 'Tank Drive',
		'pitProgrammingLanguage': 'C++',
		'pitAllImageURLs': {
			'-Kh35UOCnBsmheyfY-vX': 'https:\/\/firebasestorage.googleapis.com\/v0\/b\/scouting-2017-5f51c.appspot.com\/o\/987_2017-04-06%2009:28:38.1670%20-0700.png?alt=media&token=67ea3539-1b2a-440b-8632-927f88bd556d'
		},
		'imageKeys': {
			'-Kh359S9Yk26juteTRPP': '987_2017-04-06 09:28:38.1670 -0700'
		},
		'number': 987,
		'pitDidDemonstrateCheesecakePotential': False
	}, {
		'pitSelectedImageName': '3495_2017-04-06 10:40:41.2820 -0700',
		'name': 'MindCraft',
		'pitDriveTrain': 'Tank Drive',
		'pitProgrammingLanguage': 'Java',
		'pitAllImageURLs': {
			'-Kh3LwAcTJurRJxpzaX_': 'https:\/\/firebasestorage.googleapis.com\/v0\/b\/scouting-2017-5f51c.appspot.com\/o\/3495_2017-04-06%2010:40:41.2820%20-0700.png?alt=media&token=9b99e834-2571-4047-9451-213b9424668b'
		},
		'imageKeys': {
			'-Kh3Ldt-weEuAmTsRz7V': '3495_2017-04-06 10:40:41.2820 -0700'
		},
		'number': 3495,
		'pitDidDemonstrateCheesecakePotential': False
	}, {
		'pitSelectedImageName': '2429_2017-04-06 10:13:22.3890 -0700',
		'name': 'La Canada Engineerng Cub',
		'pitDriveTrain': 'Mecanum',
		'pitProgrammingLanguage': 'Java',
		'pitAllImageURLs': {
			'-Kh3FbNQSoxQgkbQUdP7': 'https:\/\/firebasestorage.googleapis.com\/v0\/b\/scouting-2017-5f51c.appspot.com\/o\/2429_2017-04-06%2010:13:22.3890%20-0700.png?alt=media&token=b1bb5ca6-8e60-4a41-816a-c682da35b92a'
		},
		'imageKeys': {
			'-Kh3FOmKM1yMGfTXn6lB': '2429_2017-04-06 10:13:22.3890 -0700'
		},
		'number': 2429,
		'pitDidDemonstrateCheesecakePotential': False
	}, {
		'pitSelectedImageName': '4792_2017-04-06 15:24:25.4480 -0700',
		'name': 'Desert Storm',
		'pitDriveTrain': 'Tank Drive',
		'pitProgrammingLanguage': 'Java',
		'pitAllImageURLs': {
			'-Kh4Mpgqmgp1PIfeFnVU': 'https:\/\/firebasestorage.googleapis.com\/v0\/b\/scouting-2017-5f51c.appspot.com\/o\/4792_2017-04-06%2015:24:25.4480%20-0700.png?alt=media&token=fd58ce6d-6220-41a3-9037-ea0724621987'
		},
		'imageKeys': {
			'-Kh4MaB5MtUOxuZCDwzb': '4792_2017-04-06 15:24:25.4480 -0700'
		},
		'number': 4792,
		'pitDidDemonstrateCheesecakePotential': False
	}, {
		'pitSelectedImageName': '585_2017-04-06 18:09:13.5580 -0700',
		'name': 'Cyber Penguins',
		'pitDriveTrain': 'Other',
		'pitProgrammingLanguage': 'Labview',
		'pitAllImageURLs': {
			'-Kh4xUWF64qhU8a7EglU': 'https:\/\/firebasestorage.googleapis.com\/v0\/b\/scouting-2017-5f51c.appspot.com\/o\/585_2017-04-06%2018:09:13.5580%20-0700.png?alt=media&token=a65d0986-7772-4142-98b4-deed29a441ba'
		},
		'imageKeys': {
			'-Kh4xJHh8_lhBLunF5-S': '585_2017-04-06 18:09:13.5580 -0700',
			'-Kh4xEadiDowtMFeddNa': '585_2017-04-06 18:08:54.3700 -0700'
		},
		'number': 585,
		'pitDidDemonstrateCheesecakePotential': False
	}, {
		'pitSelectedImageName': '988_2017-04-06 09:36:02.7700 -0700',
		'name': 'Steel Phoenix',
		'pitDriveTrain': 'Mecanum',
		'pitProgrammingLanguage': 'C++',
		'pitAllImageURLs': {
			'-Kh373ipOtLJNnvsQL7q': 'https:\/\/firebasestorage.googleapis.com\/v0\/b\/scouting-2017-5f51c.appspot.com\/o\/988_2017-04-06%2009:36:02.7700%20-0700.png?alt=media&token=9bb957e1-ee32-47f7-a7f8-6275893c8b7b'
		},
		'imageKeys': {
			'-Kh36qzN8RjMMiPJyp9a': '988_2017-04-06 09:36:02.7700 -0700'
		},
		'number': 988,
		'pitDidDemonstrateCheesecakePotential': False
	}, {
		'pitSelectedImageName': '3965_2017-04-06 12:49:36.6240 -0700',
		'name': 'Sultans',
		'pitDriveTrain': 'Tank Drive',
		'pitProgrammingLanguage': 'C++',
		'pitAllImageURLs': {
			'-Kh3oUp_OgX8AUTjv15Y': 'https:\/\/firebasestorage.googleapis.com\/v0\/b\/scouting-2017-5f51c.appspot.com\/o\/3965_2017-04-06%2012:49:36.6240%20-0700.png?alt=media&token=49fc1430-fc19-4a56-a25c-938dfc7ae06d'
		},
		'imageKeys': {
			'-Kh3o9N7okmEbm6TZY7N': '3965_2017-04-06 12:49:36.6240 -0700'
		},
		'number': 3965,
		'pitDidDemonstrateCheesecakePotential': False
	}, {
		'pitSelectedImageName': '3045_2017-04-06 10:38:25.6940 -0700',
		'name': 'The Gear Gremlins',
		'pitDriveTrain': 'Tank Drive',
		'pitProgrammingLanguage': 'C++',
		'pitAllImageURLs': {
			'-Kh3LOh4Xl2d__u6h7S8': 'https:\/\/firebasestorage.googleapis.com\/v0\/b\/scouting-2017-5f51c.appspot.com\/o\/3045_2017-04-06%2010:38:25.6940%20-0700.png?alt=media&token=4755ceb4-56e0-4a7f-9083-7758b0d11544'
		},
		'imageKeys': {
			'-Kh3L7mSdHWrcUTzxF_2': '3045_2017-04-06 10:38:25.6940 -0700'
		},
		'number': 3045,
		'pitDidDemonstrateCheesecakePotential': False
	}, {
		'pitSelectedImageName': '4499_2017-04-06 10:53:23.6710 -0700',
		'name': 'The Highlanders',
		'pitDriveTrain': 'Tank Drive',
		'pitProgrammingLanguage': 'Java',
		'pitAllImageURLs': {
			'-Kh3OfT88HN4TrXyJ1Ak': 'https:\/\/firebasestorage.googleapis.com\/v0\/b\/scouting-2017-5f51c.appspot.com\/o\/4499_2017-04-06%2010:53:23.6710%20-0700.png?alt=media&token=c45aba00-d77d-45ae-9e70-d54da073c0e2'
		},
		'imageKeys': {
			'-Kh3OZ1B94E_42l105Ul': '4499_2017-04-06 10:53:23.6710 -0700'
		},
		'number': 4499,
		'pitDidDemonstrateCheesecakePotential': False
	}, {
		'pitSelectedImageName': '5012_2017-04-06 11:09:23.3190 -0700',
		'name': 'Gryffingear',
		'pitDriveTrain': 'Tank Drive',
		'pitProgrammingLanguage': 'Java',
		'pitAllImageURLs': {
			'-Kh3SWsCeqJb0iTzCHkQ': 'https:\/\/firebasestorage.googleapis.com\/v0\/b\/scouting-2017-5f51c.appspot.com\/o\/5012_2017-04-06%2011:09:23.3190%20-0700.png?alt=media&token=fbbcfd2c-dd9d-4b74-9881-64e641eee54d'
		},
		'imageKeys': {
			'-Kh3SDJji-8HQ5d0XGpf': '5012_2017-04-06 11:09:23.3190 -0700'
		},
		'number': 5012,
		'pitDidDemonstrateCheesecakePotential': False
	}, {
		'pitSelectedImageName': '1266_2017-04-06 17:59:26.6960 -0700',
		'name': 'The Devil Duckies',
		'pitDriveTrain': 'Tank Drive',
		'pitProgrammingLanguage': 'Labview',
		'pitAllImageURLs': {
			'-Kh38gYcEApYE3L65mjy': 'https:\/\/firebasestorage.googleapis.com\/v0\/b\/scouting-2017-5f51c.appspot.com\/o\/1266_2017-04-06%2009:41:19.7410%20-0700.png?alt=media&token=cd28e40e-0316-4934-a112-1d2621c642c2',
			'-Kh4vKiWSSLWuOV5M6By': 'https:\/\/firebasestorage.googleapis.com\/v0\/b\/scouting-2017-5f51c.appspot.com\/o\/1266_2017-04-06%2017:59:26.6960%20-0700.png?alt=media&token=162063e4-cc4b-4f77-8931-7220bc424c80'
		},
		'imageKeys': {
			'-Kh4v40-VFb8yrm3S1XP': '1266_2017-04-06 17:59:26.6960 -0700',
			'-Kh383NVa8Rdt1JmQQBl': '1266_2017-04-06 09:41:19.7410 -0700'
		},
		'number': 1266,
		'pitDidDemonstrateCheesecakePotential': False
	}, {
		'pitSelectedImageName': '2637_2017-04-06 10:30:27.7760 -0700',
		'name': 'Phantom Catz',
		'pitDriveTrain': 'Tank Drive',
		'pitProgrammingLanguage': 'C++',
		'pitAllImageURLs': {
			'-Kh3JgkC49rJdOhTij9z': 'https:\/\/firebasestorage.googleapis.com\/v0\/b\/scouting-2017-5f51c.appspot.com\/o\/2637_2017-04-06%2010:30:27.7760%20-0700.png?alt=media&token=e352b7b3-5435-4d05-a108-bad880f7b49d',
			'-Kh3K-xN87rGUVVdGEyf': 'https:\/\/firebasestorage.googleapis.com\/v0\/b\/scouting-2017-5f51c.appspot.com\/o\/2637_2017-04-06%2010:30:27.7760%20-0700.png?alt=media&token=e3b07274-be50-491e-a330-815859c8f9fa'
		},
		'imageKeys': {
			'-Kh3JJ60pRYna-Ke2i0J': '2637_2017-04-06 10:30:27.7760 -0700'
		},
		'number': 2637,
		'pitDidDemonstrateCheesecakePotential': False
	}, {
		'pitSelectedImageName': '981_2017-04-06 12:33:42.7450 -0700',
		'name': 'Snobotics',
		'pitDriveTrain': 'Other',
		'pitProgrammingLanguage': 'Java',
		'pitAllImageURLs': {
			'-Kh3kpq5oH63Dz0uN22N': 'https:\/\/firebasestorage.googleapis.com\/v0\/b\/scouting-2017-5f51c.appspot.com\/o\/981_2017-04-06%2012:33:52.4300%20-0700.png?alt=media&token=9c8d2bfc-a104-4593-a313-3b07ad9fcd5c',
			'-Kh3klOzRW8KopTnegta': 'https:\/\/firebasestorage.googleapis.com\/v0\/b\/scouting-2017-5f51c.appspot.com\/o\/981_2017-04-06%2012:33:42.7450%20-0700.png?alt=media&token=31eddba5-3905-4285-9f41-3a0beb460601'
		},
		'imageKeys': {
			'-Kh3kWVhJktUubNdk3Y4': '981_2017-04-06 12:33:42.7450 -0700',
			'-Kh3kYrlNWIiA1B_1tIV': '981_2017-04-06 12:33:52.4300 -0700'
		},
		'number': 981,
		'pitDidDemonstrateCheesecakePotential': False
	}, {
		'pitSelectedImageName': '2144_2017-04-06 09:50:08.0010 -0700',
		'name': 'Gators',
		'pitDriveTrain': 'Mecanum',
		'pitProgrammingLanguage': 'Java',
		'pitAllImageURLs': {
			'-Kh3AKSGlHHO0GOXNWGI': 'https:\/\/firebasestorage.googleapis.com\/v0\/b\/scouting-2017-5f51c.appspot.com\/o\/2144_2017-04-06%2009:50:08.0010%20-0700.png?alt=media&token=49cbad2f-6d6c-4c68-a99e-f0c317580559'
		},
		'imageKeys': {
			'-Kh3A4MdXaBdRr8V0JOX': '2144_2017-04-06 09:50:08.0010 -0700'
		},
		'number': 2144,
		'pitDidDemonstrateCheesecakePotential': False
	}, {
		'pitSelectedImageName': '2485_2017-04-06 10:15:34.9320 -0700',
		'name': 'WARLords',
		'pitDriveTrain': 'Tank Drive',
		'pitProgrammingLanguage': 'Java',
		'pitAllImageURLs': {
			'-Kh3G8J_Mjj4XcAxEv5p': 'https:\/\/firebasestorage.googleapis.com\/v0\/b\/scouting-2017-5f51c.appspot.com\/o\/2485_2017-04-06%2010:15:34.9320%20-0700.png?alt=media&token=890be5b4-082f-4f86-9266-31698aaa873b'
		},
		'imageKeys': {
			'-Kh3Fu8-2zwB5aEw9tDR': '2485_2017-04-06 10:15:34.9320 -0700'
		},
		'number': 2485,
		'pitDidDemonstrateCheesecakePotential': False
	}, {
		'pitSelectedImageName': '4201_2017-04-06 14:52:16.1310 -0700',
		'name': 'Vitruvian Bots',
		'pitDriveTrain': 'Tank Drive',
		'pitProgrammingLanguage': 'Labview',
		'pitAllImageURLs': {
			'-Kh4GMTMJKoqi6mIKGU0': 'https:\/\/firebasestorage.googleapis.com\/v0\/b\/scouting-2017-5f51c.appspot.com\/o\/4201_2017-04-06%2014:52:16.1310%20-0700.png?alt=media&token=f692cac0-f946-4ffa-a4cf-407d94f684cf'
		},
		'imageKeys': {
			'-Kh4FE9E9PJU6G4iACvf': '4201_2017-04-06 14:52:16.1310 -0700'
		},
		'number': 4201,
		'pitDidDemonstrateCheesecakePotential': False
	}, {
		'pitSelectedImageName': '5823_2017-04-06 15:09:52.8840 -0700',
		'name': 'ACE',
		'pitDriveTrain': 'Mecanum',
		'pitProgrammingLanguage': 'Labview',
		'pitAllImageURLs': {
			'-Kh4JYMNEMt7ed8FVfLA': 'https:\/\/firebasestorage.googleapis.com\/v0\/b\/scouting-2017-5f51c.appspot.com\/o\/5823_2017-04-06%2015:09:52.8840%20-0700.png?alt=media&token=9dd5e55b-dcc0-4a77-aa43-4394e0304e92'
		},
		'imageKeys': {
			'-Kh4JG9JBJ9DTslGIZJK': '5823_2017-04-06 15:09:52.8840 -0700'
		},
		'number': 5823,
		'pitDidDemonstrateCheesecakePotential': False
	}, {
		'pitSelectedImageName': '5025_2017-04-06 14:42:04.5560 -0700',
		'name': 'ENIGMA',
		'pitDriveTrain': 'Tank Drive',
		'pitProgrammingLanguage': 'Labview',
		'pitAllImageURLs': {
			'-Kh4CyPVhmiE63IAYPZa': 'https:\/\/firebasestorage.googleapis.com\/v0\/b\/scouting-2017-5f51c.appspot.com\/o\/5025_2017-04-06%2014:42:04.5560%20-0700.png?alt=media&token=f40823d4-916a-4e33-8dd9-751ec7323418'
		},
		'imageKeys': {
			'-Kh4CtqLWl8V8uiUc6fR': '5025_2017-04-06 14:42:04.5560 -0700'
		},
		'number': 5025,
		'pitDidDemonstrateCheesecakePotential': False
	}, {
		'name': 'Citrus Circuits',
		'number': 1678
	}, {
		'pitSelectedImageName': '5049_2017-04-06 17:52:19.6530 -0700',
		'name': 'Techtonics',
		'pitDriveTrain': 'Tank Drive',
		'pitProgrammingLanguage': 'Java',
		'pitAllImageURLs': {
			'-Kh4thULzPyvs5EJKNDd': 'https:\/\/firebasestorage.googleapis.com\/v0\/b\/scouting-2017-5f51c.appspot.com\/o\/5049_2017-04-06%2017:52:19.6530%20-0700.png?alt=media&token=3ed84679-56d7-43ce-94f7-11770a88c118'
		},
		'imageKeys': {
			'-Kh4tRih0DpIodP5v9uc': '5049_2017-04-06 17:52:19.6530 -0700'
		},
		'number': 5049,
		'pitDidDemonstrateCheesecakePotential': False
	}, {
		'pitSelectedImageName': '5851_2017-04-06 13:09:40.4700 -0700',
		'name': 'Striking Vikings',
		'pitDriveTrain': 'Tank Drive',
		'pitProgrammingLanguage': 'Labview',
		'pitAllImageURLs': {
			'-Kh3t-T10B_cyi2XfBrl': 'https:\/\/firebasestorage.googleapis.com\/v0\/b\/scouting-2017-5f51c.appspot.com\/o\/5851_2017-04-06%2013:09:40.4700%20-0700.png?alt=media&token=a136d81f-dbc6-4821-a7b6-e710a3dcc75d'
		},
		'imageKeys': {
			'-Kh3skJe3nG5E1WcqL_W': '5851_2017-04-06 13:09:40.4700 -0700'
		},
		'number': 5851,
		'pitDidDemonstrateCheesecakePotential': False
	}, {
		'pitSelectedImageName': '295_2017-04-06 14:43:48.0620 -0700',
		'name': 'Grizzly Robotics Team',
		'pitDriveTrain': 'Tank Drive',
		'pitProgrammingLanguage': 'Java',
		'pitAllImageURLs': {
			'-Kh4DX3Z0LZNdUuOPL41': 'https:\/\/firebasestorage.googleapis.com\/v0\/b\/scouting-2017-5f51c.appspot.com\/o\/295_2017-04-06%2014:43:48.0620%20-0700.png?alt=media&token=3a2a2a71-279d-45aa-bcb4-b3313a723a1d'
		},
		'imageKeys': {
			'-Kh4DI71gchk5vKsZ-H-': '295_2017-04-06 14:43:48.0620 -0700'
		},
		'number': 295,
		'pitDidDemonstrateCheesecakePotentissal': False
	}
]
