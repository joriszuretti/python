import core
from classes.Predateurs import Predateur
from classes.Proies import Proie

def setup():

        print("Setup START---------")
        core.WINDOW_SIZE = (800,800)
        core.fps = 60

        core.memory("proies",[])
        core.memory("predateurs", [])

        core.memory("nbProies", 100)
        core.memory("nbPredateurs", 10)

        for i in range(0,core.memory("nbProies")):
            core.memory("proies").append(Proie())
        for i in range(0, core.memory("nbPredateurs")):
            core.memory("predateurs").append(Predateur())

        print("Setup END-----------")


def reset():
    core.memory("proies", [])
    core.memory("predateurs", [])
    for i in range(0,core.memory("nbProies")):
        core.memory("proies").append(Proie())
    for i in range(0,core.memory("nbPredateurs")):
        core.memory("predateurs").append(Predateur())

def run():
    core.cleanScreen()

    #AFFICHAGE
    for p in core.memory("proies"):
        p.afficher()

    #AFFICHAGE
    for p in core.memory("proies"):
        p.afficher()

    #CONTROL
    if core.getKeyPressList("r"):
        reset()

    #MAJ DES POSITIONS
    for p in core.memory("proies"):
        p.deplacement()
        #p.bordure(core.WINDOW_SIZE)

    for p in core.memory("predateurs"):
        p.deplacement()
        #p.bordure(core.WINDOW_SIZE)

core.main(setup,run)