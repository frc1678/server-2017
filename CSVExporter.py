# CSV Exporter, by Bryton 2/10/16
import utils


def TSVExportAll(comp):
	s = ""
	firstTeam = True
	with open('./dataExportAll.tsv', 'w') as file:
		for team in comp.teams:
			cd = team.calculatedData.__dict__
			if firstTeam:
				firstTeam = False
				s += "number" + "	"
				for key in cd.keys():
					s += key + "	"
				s += "\n"
			s += str(team.number) + "	"
			for value in cd.values():
				s += str(value) + "	"
			s += "\n"
		file.write(s)
		file.close()

def TSVExportCVR(comp):
	s = ""
	CVRKeys = []
	firstTeam = True
	with open('./dataExportCVR.tsv', 'w') as file:
		for team in comp.teams:
			cd = team.calculatedData.__dict__
			if firstTeam:
				firstTeam = False
				s += "number" + "	"
				for key in CVRKeys:
					s += key + "	"
				s += "\n"
			s += str(team.number) + "	"
			for key in CVRKeys:
				s += str(cd[key]) + "	"
			s += "\n"
		file.write(s)
		file.close()

def TSVExportMini(comp):
	s = ""
	MiniKeys = []
	firstTeam = True
	with open('./dataExportMini.tsv', 'w') as file:
		for team in comp.teams:
			cd = team.calculatedData.__dict__
			if firstTeam:
				firstTeam = False
				s += "number" + "	"
				for key in MiniKeys:
					s += key + "	"
				s += "\n"
			s += str(team.number) + "	"
			for key in MiniKeys:
				if key == 'pitNumberOfWheels':
					s += str(team.pitNumberOfWheels)
				else:
					s += str(cd[key]) + "	"
			s += "\n"
		file.write(s)
		file.close()

def TSVExport(comp, keys, name):
	s = ""
	MiniKeys = keys
	firstTeam = True
	with open('./TSVExport-' + name + '.tsv', 'w') as file:
		for team in comp.teams:
			cd = team.calculatedData.__dict__
			t = team.__dict__
			if firstTeam:
				firstTeam = False
				s += "number" + "	"
				for key in MiniKeys:
					s += key + "	"
				s += "\n"
			s += str(team.number) + "	"
			for key in MiniKeys:
				try:
					s += str(cd[key]) + "	"
				except:
					try:
						s += str(t[key]) + "	"
					except:
						print "*** TSV EXPORT ERROR ***\nKEY: " + key + " NOT FOUND ON A CALCULATED TEAM DATA, NOR ON A TEAM DATA"
			s += "\n"
		file.write(s)
		file.close()
def TSVExportSAC(comp):
	keys = []
	TSVExport(comp, keys, "SAC")

def TSVExportCMP(comp): 
	keys = []
	TSVExport(comp, keys, "CHAMPS")