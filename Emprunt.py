from sqlite3 import sqlite3
from datetime import datetime

BD = sqlite3.connect(':memory:')

CREATE TABLE IF NOT EXISTS `Emprunt` (
`idEmprunt` str(6) NOT NULL,
`idAdherent` int(6) NOT NULL,
`idJeu` int(6) NOT NULL,
`idExtension` int(6) NOT NULL,
`dateDebutEmprunt` date NOT NULL,
`dureePrevue` int(3) NOT NULL,
KEY `fk_idAdherent` (`idAdherent`),
KEY `fk_idExtension` (`idExtension`),
KEY `fk_idJeu` (`idJeu`)
)


class Emprunt :
    
	def __init__(self, dataBase = BD):
    		self.cursor = dataBase.cursor()
    		self.Table = "Emprunt"

    		self.cursor.execute("""INSERT INTO Emprunt(
		idEmprunt, idJeu, idAdh, idExt, dateDebutEmprunt, dureePrevue)
		VALUES(?, ?, ?, ?, ?, ?)""",
    (self.idEmprunt, self.idJeu, self.idAdh,
   	date, 14)) #14 jours

	#setters ?
	def setIdEmprunt(self, idEmprunt : str) :       
    		self.cursor.execute("""UPDATE Emprunt SET idEmprunt = ? WHERE idEmprunt = ?""",
                        	(idEmprunt, self.idEmprunt))
    		self.idEmprunt = idEmprunt
    		return self
   	 
	def setDateDebutEmprunt(self, dateDebutEmprunt : date) :    
    		self.cursor.execute("""UPDATE Emprunt SET dateDebutEmprunt = ? WHERE idEmprunt = ?""",
                        	(dateDebutEmprunt, self.idEmprunt))
    		return self

	def setDureePrevue(self, dureePrevue : int) : 	
    		self.cursor.execute("""UPDATE Emprunt SET dureePrevue = ? WHERE idEmprunt = ?""",
                        	(dureePrevue, self.idEmprunt))
    		return self


	#getters ?
	def getIdEmprunt(self):
		 return self.idEmprunt
	  
	def getDateDebutEmprunt(self):
		 return self.dateDebutEmprunt
	  
	def getDureePrevue(self):
		 return self.dureePrevue

	#Fonctions usuelles:

	def rendre(self):
		self.cursor("""DELETE FROM Emprunt WHERE idEmprunt = ?""",
			(self.idEmprunt))
			
