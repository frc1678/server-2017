# CSV Exporter, by Bryton 2/10/16
import utils
from collections import OrderedDict
import pdb
import csv
from DataModel import Team

def CSVExportAll(comp):
	s = ""
	firstTeam = True
	excluded = ['calculatedData', 'name', 'imageKeys']
	with open('./dataExportAll.csv', 'w') as f:
		defaultKeys = [k for k in Team().__dict__.keys() if k not in excluded]
		defaultKeys += Team().calculatedData.__dict__.keys()
		defaultKeys = sorted(defaultKeys, key=lambda k: (k != "number", k.lower()))
		writer = csv.DictWriter(f, fieldnames=defaultKeys)
		writer.writeheader()
		for team in comp.teams:
			tDict = team.__dict__
			tDict.update(team.calculatedData.__dict__)
			keys = sorted(defaultKeys,key=lambda k: (k != "number", k.lower()))
			writer.writerow({k : tDict[k] for k in keys})

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