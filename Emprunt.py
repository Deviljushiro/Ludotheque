import sqlite3
import datetime
import Jeu

import BDD


BDD.cur.execute("""CREATE TABLE IF NOT EXISTS `Emprunt` (
                                `idEmprunt` int(6) NOT NULL,
                                `idAdherent` int(6) NOT NULL,
                                `idJeu` int(6) NOT NULL,
                                `idExtension` int(6) NOT NULL,
                                `dateDebutEmprunt` date NOT NULL,
                                `dateRenduEmprunt` date NOT NULL,
                                `dureePrevueEmprunt` int(3) NOT NULL,
                                PRIMARY KEY (`idEmprunt`),
                                FOREIGN KEY (`idAdherent`) REFERENCES Adherent(`idAdherent`),
                                FOREIGN KEY (`idExtension`) REFERENCES Extension(`idExtension`),
                                FOREIGN KEY (`idJeu`) REFERENCES Jeu(`idJeu`)
                                )""")
BDD.conn.commit()



class Emprunt :

        #setters ?
        @staticmethod
        def setDateDebutEmprunt(idEmprunt, dateDebutEmprunt) :    
                BDD.cur.execute("""UPDATE Emprunt SET dateDebutEmprunt = ? WHERE idEmprunt = ?""",
                                (dateDebutEmprunt, idEmprunt))
                BDD.conn.commit()
                
        @staticmethod
        def setDateRenduEmprunt(idEmprunt, dateRenduEmprunt) :    
                BDD.cur.execute("""UPDATE Emprunt SET dateRenduEmprunt = ? WHERE idEmprunt = ?""",
                                (dateRenduEmprunt, idEmprunt))
                BDD.conn.commit()
        
        @staticmethod
        def setDureePrevue(idEmprunt, dureePrevueEmprunt) :  
                BDD.cur.execute("""UPDATE Emprunt SET dureePrevueEmprunt = ? WHERE idEmprunt = ?""",
                                (dureePrevue, idEmprunt))
                BDD.conn.commit()


        #getters ?
        
        
        @staticmethod 
        def getIdEmprunt(idAdherent):
                BDD.cur.execute("""SELECT idEmprunt FROM Emprunt WHERE idAdherent =?""",(idAdherent,))
                return BDD.cur.fetchone()[0]
        
        @staticmethod 
        def getDateDebutEmprunt(idEmprunt):
                BDD.cur.execute("""SELECT dateDebutEmprunt FROM Emprunt WHERE idEmprunt = ?""",
                                (idEmprunt,))
                return BDD.cur.fetchone()[0]
                
        @staticmethod 
        def getDateRenduEmprunt(idEmprunt):
                BDD.cur.execute("""SELECT dateRenduEmprunt FROM Emprunt WHERE idEmprunt = ?""",
                                (idEmprunt,))
                return BDD.cur.fetchone()[0]
        
        @staticmethod  
        def getDateFinEmprunt(idEmprunt):
                dateFin = Emprunt.getDateDebutEmprunt(idEmprunt).day + Emprunt.getDureePrevue(idEmprunt)
                return dateFin
        
        @staticmethod 
        def getIdJeuEmprunt(idEmprunt):
                BDD.cur.execute("""SELECT idJeu FROM Emprunt WHERE idEmprunt = ?""",(idEmprunt,))
                return BDD.cur.fetchone()[0]
        
        @staticmethod
        def getIdAdherentEmprunt(idEmprunt):
                BDD.cur.execute("""SELECT idAdherent FROM Emprunt WHERE idEmprunt =?""",(idEmprunt,))
                return BDD.cur.fetchone()[0]
        
        @staticmethod
        def getIdExtensionEmprunt(idEmprunt):
                BDD.cur.execute("""SELECT idExtension FROM Emprunt WHERE idEmprunt = ?""",(idEmprunt,))
                return BDD.cur.fetchone()[0]
        
        @staticmethod
        def getDureePrevue(idEmprunt):
                BDD.cur.execute("""SELECT dureePrevueEmprunt FROM Emprunt WHERE idEmprunt = ?""",
                                (idEmprunt,))
                return BDD.cur.fetchone()[0]

        #Fonctions usuelles:
        
        @staticmethod
        def afficherTableEmprunt():
          BDD.cur.execute("""SELECT * FROM Emprunt""")
          return BDD.cur.fetchall()
        
        @staticmethod
        def ajoutEmprunt(idJeu, idAdherent, idExtension, dateDebutEmprunt, dureePrevueEmprunt = 7):
          BDD.cur.execute("""SELECT MAX(idEmprunt) FROM Emprunt""")
          f = BDD.cur.fetchone()[0]
          if (f==None):
            idEmprunt = 1
          else:
            idEmprunt =f+1
          BDD.cur.execute("""INSERT INTO Emprunt(
                  idEmprunt, idJeu, idAdherent, idExtension, dateDebutEmprunt, dateRenduEmprunt, dureePrevueEmprunt)
                  VALUES(?, ?, ?, ?, ?, ?)""",
                  (idEmprunt, idJeu, idAdherent, idExtension, dateDebutEmprunt, None, dureePrevueEmprunt)) #7 jours d'emprunt
          BDD.conn.commit() 
        
        @staticmethod
        def getJourRetard(idEmprunt):
                jourRetard = (Emprunt.getDateRenduEmprunt(idEmprunt) - Emprunt.getDateFinEmprunt(idEmprunt)).days
                return jourRetard
        
        @staticmethod
        def estEnRetard(idEmprunt):
                return(Emprunt.getDateRenduEmprunt(idEmprunt) > Emprunt.getDateFinEmprunt(idEmprunt))
                        
        @staticmethod
        def rendre(idEmprunt):
                if (estEnRetard(idEmprunt)):
                        Adherent.ajoutRetard(Emprunt.getIdAdherentEmprunt(idEmprunt))
                        Adherent.ajoutJourRetard(Emprunt.getIdAdherentEmprunt(idEmprunt),Emprunt.getJourRetard(idEmprunt))
                        Jeu.ajoutExemplaire(Emprunt.getIdJeuEmprunt(idEmprunt))
                BDD.cur.execute("""DELETE FROM Emprunt WHERE idEmprunt = ?""",
                        (idEmprunt,))
                BDD.conn.commit()
