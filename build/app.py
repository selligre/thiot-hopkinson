import CalculusController
import GUImain


def main():
    calc = CalculusController.CalculusController()
    # calc.import_data_file()
    # calc.display_and_limiting()
    GUImain.run(calc)


if __name__ == "__main__":
    main()

# IMPLEMENTER FONCTIONS DE CALCUL
# GUIdata.import_data_file() devrait ensuite lancer l'affichage du graphe dans la fenetre dediee

# IMPLEMENTER FONCTION D'EXPORT (EXEMPLE)
# GUIspecimen.export()

# HASH/COMPILE/.EXE
