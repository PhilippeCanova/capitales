from pathlib import Path
import csv
import random
from dataclasses import dataclass

@dataclass
class Pays:
    nom: str
    nom_alpha: str
    code: str
    article: str
    nom_long: str
    capitale: str
    continent: str


class AllPays:
    def __init__(self, fichier):
        self.pays = []
        self.continents = []
        with open(fichier, "r", encoding="utf-8", newline="") as f:
            lecteur = csv.DictReader(f, delimiter=";")

            for ligne in lecteur:
                self.pays.append(
                    Pays(
                        nom=ligne["NOM"],
                        nom_alpha=ligne["NOM_ALPHA"],
                        code=ligne["CODE"],
                        article=ligne["ARTICLE"],
                        nom_long=ligne["NOM_LONG"],
                        capitale=ligne["CAPITALE"],
                        continent=ligne["CONTINENT"],
                    )
                )

        self.continents = self.get_continents()
    
    def get_continents(self):
        continents = []
        for p in self.pays:
            continents.append(p.continent)
        return list(set(continents))


    def get_countries_from_continent(self, continent):
        if continent is None:
            return self.pays

        datas = []
        for p in self.pays:
            if p.continent == continent:
                datas.append(p)
        return datas

class GamePlay:
    def __init__(self, dico_pays):
        self.nb_coups = 0
        self.nb_ok = 0
        self.dico_pays = dico_pays


    def start(self):
        continent = self.choix_continent()
        print(continent)
        
        print("Extraction des pays...")
        list_pays = self.dico_pays.get_countries_from_continent(continent)
        print(f"{len(list_pays)} pays trouvés !")

        self.displays_rules()

        while True:
            try:
                proposal = self.proposal(list_pays)
            except:
                print()
                print("Partie terminée !")
                return


    def proposal(self, list_pays):
        self.nb_coups = self.nb_coups + 1
        pays = random.choice(list_pays)
        list_pays.remove(pays)

        capitale = input(f"Quelle est la capitale de {pays.nom} : ")
        if capitale == "":
            # Mode oral
            print(pays.capitale)
            ok = input("Tu as bon (0/1) ? ")
            if ok == '1':
                self.nb_ok = self.nb_ok + 1
        if capitale in ["q", "Q"]:
            raise RuntimeError("Exit")
        else:
            if capitale.upper() == pays.capitale.upper():
                print("Bonne réponse !")
                self.nb_ok = self.nb_ok + 1
            else:
                print("Mauvaise réponse ========> ", pays.capitale)
        print(f"({self.nb_ok}/{self.nb_coups})")
        print()


    def choix_continent(self):
            print("Choix du continent :")
            for ind, c in enumerate(self.dico_pays.continents):
                if c == '':
                    c = "Tous"
                print(f"\t{ind}: {c}")
            choix = input("Choix du continent : ")
            choix = int(choix)
            if choix == 0:
                return None
            return self.dico_pays.continents[choix]

    
    def displays_rules(self):
        print()
        print("Rappel des commandes :")
        print("\tSaisir la capitale si mode évaluation avec saisie.")
        print("\tLaisser vide si mode oral ou révision, puis :")
        print("\t\t0 pour une erreur")
        print("\t\t1 pour une réussite")
        
        print("C'est parti !")
        print()


if __name__ == "__main__":
    WORKING_DIR = Path(__file__).parent
    cap_file = WORKING_DIR.joinpath("capitales.csv")

    pays = AllPays(cap_file)
    game = GamePlay(pays)

    game.start()
    





    

