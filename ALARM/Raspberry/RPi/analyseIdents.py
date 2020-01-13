#!/usr/bin/python3

import pandas as pd
import glob

def listeFichiers():
	liste = glob.glob("./casdemplois/*.csv")
	#print(liste)
	return liste

def listeIdentXlsx():
	liste = glob.glob("./casdemplois/export*.XLSX")
	return liste

def parse_casemploiXlsx():
	donnees = pd.DataFrame()
	for f in listeIdentXlsx():
		table = pd.read_excel(f)
		table["ID objet"] = table["Composante"].astype(str)
		table["ident"]=f[-14:-8]
		donnees = donnees.append(table)
	#print(donnees.head)
	donnees = donnees[["ident","ID objet"]]

	return donnees 	
def listeIdents():
	liste = listeFichiers()
	for f in liste:
		yield f[-10:-4]

def parse_casemploi():
	donnees = pd.DataFrame()
	for f in listeFichiers():
		table = pd.read_csv(f,encoding='utf-16',skiprows=[0,1,2,3,4,5,6,8])
		print(table["ID objet"])
		table["ID objet"] = table["ID objet"].astype(int)
		table["ident"]=f[-10:-4]
		donnees = donnees.append(table)
	
	donnees = donnees[["ident","ID objet"]]
	donnees = donnees.dropna()
	return donnees
	
if __name__ == "__main__":
	#table = pd.read_csv("configuration.csv",encoding='utf-8',sep=";")
	#print(table["indent"])
	#print(parse_casemploi())
	#print(listeIdentXlsx())
	dfx = parse_casemploiXlsx()
	df = parse_casemploi()
	df = pd.concat([df,dfx])
	export_csv = df.to_csv (r'./idents.csv', index = None, header=True) #Don't forget to add '.csv' at the end of the path


