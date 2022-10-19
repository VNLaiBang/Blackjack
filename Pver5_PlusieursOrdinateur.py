# Hàm tạo bộ bài/ Fonction creer une paquet
def paquet():
    valeurs = [
        "as",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "10",
        "valet",
        "dame",
        "roi",
    ]
    couleurs = [" pique", " coeur", " trèfle", " carreau"]
    # Tạo liste bài với gtri + chất/ Renvoyer une liste avec les elements sous-forme valeur + couleur
    liste_des_cartes = [x + " de" + y for x in valeurs for y in couleurs]
    return liste_des_cartes


# Hàm lấy giá trị của lá bài/ Fonction qui revoie la valeur de la carte (argument)
def valeurCarte(la_carte):

    liste_des_valeurs = [a for a in range(2, 10)]
    premiere_lettre = [str(b) for b in liste_des_valeurs]
    # valeurs_particuliers = ["1", "v", "d", "r"]

    # Pour les valeurs de 2 à 9
    if la_carte[0] in premiere_lettre:
        for c in range(len(premiere_lettre)):
            if premiere_lettre[c] == la_carte[0]:
                valeur = liste_des_valeurs[c]

    # Pour les valeurs qui revoient 10
    elif la_carte[0] in "1vdr":
        valeur = 10

    # Mettre le as par default 11, on va compter le nombre de as libre et moins 10 chaque fois que ca dépasse 21
    elif la_carte[0] == "a":
        valeur = 11
    return valeur


from random import shuffle, randint

# Fonction cree un grand paquet combiné par n(nombre joueues) fois un paquet
def initPioche(n=1):
    la_pioche = []
    for d in range(n):
        la_pioche.extend(paquet())
    return la_pioche


def piocheCarte(la_pioche, x=1):
    liste_des_cartes_pioches = []
    for d in range(x):
        shuffle(la_pioche)
        liste_des_cartes_pioches.append(la_pioche.pop(0))
    return liste_des_cartes_pioches


# -----------------------------------------------------
def initJoueur(n):
    liste_des_joueurs = []
    for f in range(n):  # Demander chaque joueur en ordre
        liste_des_joueurs.append(input("Joueur %d? " % (f + 1)))
    return liste_des_joueurs


def initScore(joueurs, v=0):
    dict_score_de_joueurs = {x: v for x in joueurs}
    return dict_score_de_joueurs


# Fonction qui joue le premierTour pour
def premierTour(joueurs, la_pioche):
    # Creation du dictionnaire de scores initiales nulles
    scores = initScore(joueurs)

    # Dictionnaire contient les cartes inititales
    dict_CarteDistribue = {}

    for g in scores:  # Pour chaque joueur:
        carte_distribue = piocheCarte(la_pioche, 2)
        print("Pour ", g)
        print(carte_distribue)
        score = 0
        dict_CarteDistribue[g] = carte_distribue

        # On va ajouter la valeur dans le dictionnaire pour chacun
        for h in carte_distribue:
            score += valeurCarte(h)
        if score == 22:
            score -= 10
        scores[g] = score
    return scores, dict_CarteDistribue


# Fonction qui recpi
def gagnant(scores):
    gagnants = []
    gagnants21 = []
    ecart_minimum = 21
    for i in scores:
        if scores[i] <= 21:
            if scores[i] == 21:
                print(i, " WOW! Blackjack!")
                gagnants21.append(i)
            else:
                if (21 - scores[i]) < (ecart_minimum):
                    ecart_minimum = 21 - scores[i]

    for j in scores:
        if 21 - scores[j] == ecart_minimum:
            gagnants.append(j)

    if len(gagnants21) != 0:
        print("Winner: ", end="")
        for k in gagnants21:
            print(k, end=" ")
        return gagnants21
    elif len(gagnants) != 0:
        print("Winner: ", end="")
        for l in gagnants:
            print(l, "-", scores[l], end=" ")
        return gagnants
    else:
        print("No winner!")
        return []


# -----------------------------------------------------
# B


def continue_():
    souhait = input("Voulez vous continuer? go/stop?: ")
    while not (souhait in ["go", "stop"]):
        souhait = input("Retry! go/stop? ")
    else:
        if souhait == "go":
            return True
        else:
            return False


# Fonction tourJoueur pour f
def tourJoueur(tour, joueur, scores, la_pioche, dict_CarteDistribue):
    print(f"C'est le tour {tour} de {joueur}")
    print(f"Vos cartes: {dict_CarteDistribue[joueur]}")
    print(f"Vous avez {scores[joueur]}")

    # Nếu điểm trên 21 nhưng mà chứa as trong bài
    as_libre1 = 0
    for af in dict_CarteDistribue[joueur]:
        if valeurCarte(af) == 11:
            as_libre1 += 1

    # Nếu có 2 as trong bài ta sẽ trừ trước trong premierTour, như vậy số as_libre1 là 1
    if as_libre1 == 2:
        as_libre1 -= 1

    if scores[joueur] != 21:
        # Demander à joueur si il veut piocher l'autre carte
        continuer = continue_()
        while continuer != False:
            ajouter_carte = piocheCarte(la_pioche, 1)
            print(ajouter_carte)
            valeur = valeurCarte(ajouter_carte[0])
            scores[joueur] += valeur

            if valeur == 11:
                as_libre1 += 1

            if scores[joueur] > 21 and as_libre1 != 0:
                scores[joueur] -= 10
                as_libre1 -= 1

            print(f"Votre nouveau score: {scores[joueur]}")
            if scores[joueur] > 21:
                print("OOps! Vous avez dépassé 21!")
                break
            elif scores[joueur] == 21:
                break
            else:
                continuer = continue_()
    elif scores[joueur] == 21:
        print("Blackjack!")
    return scores


#
def tourComplet(scores, la_pioche, dict_CarteDistribue):
    scores1 = scores
    print(f"Scores Joueurs mtn:\n{scores}\n")
    for joueur in scores:
        scores1 = tourJoueur(
            nombreTour, joueur, scores1, la_pioche, dict_CarteDistribue
        )
        print("\n")
    return scores1


def partieComplete(dict_scores_de_joueurs, scores, la_pioche, dict_CarteDistribue):
    dictionnaire_victoire = dict_scores_de_joueurs
    full_tour = tourComplet(scores, la_pioche, dict_CarteDistribue)
    list_winner = gagnant(full_tour)
    for win in list_winner:
        dictionnaire_victoire[win] += 1
        print("\n")
    return dictionnaire_victoire, list_winner


# ----------------------------------------------------
"""MISE"""


def initKopecs(liste_des_joueurs, y=100):
    return {x: y for x in liste_des_joueurs}


# Demander chacun pour faire son mise
def demandeMise(dict_account):
    liste_des_mises = []
    for joueur in dict_account:
        mise = int(input(f"{joueur}, votre mise? "))
        # Tout doit faire la mise
        while (
            mise > dict_account[joueur]
            or mise <= 0
            or not (mise in [a for a in range(1000)])
        ):
            mise = int(input("Impossible!!! Votre mise again? "))
        liste_des_mises.append(mise)
        dict_account[joueur] -= mise
    return liste_des_mises


def compterKopecs(dict_account):
    elemine = []
    for money in dict_account:
        if dict_account[money] == 0:
            print(f"{money} Bye!")
            elemine.append(money)
    return elemine


# ----------------------------------------------------
"""-----------------Croupier tour-------------------"""
# Fonction aleatoire pour le croupier
def Aleatoire(Croupier_Tour, la_pioche, dict_CarteDistribue, croupier="Croupier"):
    print(f"{croupier}: {Croupier_Tour[croupier]}")

    # Compter le nombre de as
    as_libre = 0
    for af in dict_CarteDistribue[croupier]:
        if valeurCarte(af[0]) == 11:
            as_libre += 1

    # Si il y a 2 as apres le premierTour, il faut en eleminer un
    if as_libre == 2:
        as_libre -= 1

    if Croupier_Tour[croupier] != 21:
        continuer = randint(0, 1)

        # Si continuer = 1, alors piocher, else 0, stop! Alors le ratio de piocher c'est 1/2
        while continuer == 1:
            # Ajouter une carte
            ajouter_carte = piocheCarte(la_pioche, 1)
            print(ajouter_carte)
            valeur = valeurCarte(ajouter_carte[0])
            Croupier_Tour[croupier] += valeur

            # Si sa valeur = 11, donc c'est as, si son score dépasse 21 => as va etre 1
            if valeur == 11:
                as_libre += 1
            if Croupier_Tour[croupier] > 21 and as_libre > 0:
                Croupier_Tour[croupier] -= 10
                as_libre -= 1

            # Si son score depasse 21, et il n'y a plus de as, stop piocher
            print(f"{croupier}: {Croupier_Tour[croupier]}")
            if Croupier_Tour[croupier] >= 21:
                print("OOps! Depasser 21!")
                break
            else:
                continuer = randint(0, 1)
        else:
            print(f"{croupier} stop!")
    elif Croupier_Tour[croupier] == 21:
        print("Blackjack!")
    return Croupier_Tour


# risqueMinimum
def risqueMinimum(Croupier_Tour, la_pioche, dict_CarteDistribue, croupier="Croupier"):
    print(f"{croupier}: {Croupier_Tour[croupier]}")

    # Si son score est inferieur à 10, il va piocher, si non il va stopper
    while Croupier_Tour[croupier] <= 10:
        ajouter_carte = piocheCarte(la_pioche)

        print(ajouter_carte)
        Croupier_Tour[croupier] += valeurCarte(ajouter_carte[0])
        print(f"{croupier}: {Croupier_Tour[croupier]}")

    print(f"{croupier} stop!")
    return Croupier_Tour


# Par pourcentage
def Pourcentage(Croupier_Tour, la_pioche, dict_CarteDistribue, croupier="Croupier"):
    print(f"{croupier}: {Croupier_Tour[croupier]}")
    print(dict_CarteDistribue[croupier])

    # Compter le nombre de as
    as_libre = 0
    for af in dict_CarteDistribue[croupier]:
        if valeurCarte(af[0]) == 11:
            as_libre += 1

    # Nếu có 2 as trong bài ta sẽ từ trước trong premierTour, như vậy số as_libre1 là 1
    # Si il y a 2 as apres le premierTour, il faut en eleminer un
    if as_libre == 2:
        as_libre -= 1

    a = True
    while a == True:

        # Đếm số bài mà nếu tổng với bài trên tay bé hơn 21/ Verifier combien de carte possible à piocher
        if Croupier_Tour[croupier] < 21:
            cartePossible = 0
            for carte in la_pioche:
                temporary_value = valeurCarte(carte)
                somme = valeurCarte(carte) + Croupier_Tour[croupier]
                if temporary_value == 11:
                    somme -= 10
                if somme <= 21:
                    cartePossible += 1

            # Tỉ lệ bài có thể bốc/ Ratio de la carte secure
            pourcentageCartePossible = int((100 * cartePossible) / len(la_pioche))

            # Percentage, il doit le pourcentagePioche dans le pourcentageCartePossible!
            pourcentagePioche = randint(1, 100)
            if pourcentagePioche in [a for a in range(1, pourcentageCartePossible + 1)]:
                # Si il est de dans => pioche une carte
                ajouter_carte = piocheCarte(la_pioche)

                print(ajouter_carte)
                valeur = valeurCarte(ajouter_carte[0])
                Croupier_Tour[croupier] += valeur

                if valeur == 11:
                    as_libre += 1
                if Croupier_Tour[croupier] > 21 and as_libre > 0:
                    Croupier_Tour[croupier] -= 10
                    as_libre -= 1

                print(Croupier_Tour)
            else:
                # Si non il va arreter
                print(f"{croupier} stop")
                a = False
        elif Croupier_Tour[croupier] > 21:
            print("OOps! Depasser 21!")
            a = False
        elif Croupier_Tour[croupier] == 21:
            print("Blackjack!")
            a = False
    return Croupier_Tour


# RisqueTout = Marche
def risqueMaximum(Croupier_Tour, la_pioche, dict_CarteDistribue, croupier="Croupier"):
    print(f"{croupier}: {Croupier_Tour[croupier]}")
    # Compter le nombre de as
    as_libre = 0
    for af in dict_CarteDistribue[croupier]:
        if valeurCarte(af[0]) == 11:
            as_libre += 1

    # Si il y a 2 as apres le premierTour, il faut en eleminer un
    if as_libre == 2:
        as_libre -= 1

    # Si son score est != 21, il va piocher sans faute jusqu'à ce qu'il ait 21
    while Croupier_Tour[croupier] != 21:
        ajouter_carte = piocheCarte(la_pioche)
        print(ajouter_carte)
        valeur = valeurCarte(ajouter_carte[0])
        Croupier_Tour[croupier] += valeur

        # Thiết lập số as free và đếm:
        if valeur == 11:
            as_libre += 1
        if Croupier_Tour[croupier] > 21 and as_libre > 0:
            Croupier_Tour[croupier] -= 10
            as_libre -= 1

        print(f"{croupier}: {Croupier_Tour[croupier]}")

        return Croupier_Tour


# Fonction Tricheur
def Tricheur(Croupier_Tour, la_pioche, croupier="Croupier"):
    print(f"{croupier}: {Croupier_Tour[croupier]}")
    # la valeur maximale que l'on peut piocher dans la piocher c'est 11, donc il faut son score > 10 pour gagner tout de suite.
    if Croupier_Tour[croupier] == 21:
        print(f"{croupier} stop! Blackjack")
    while Croupier_Tour[croupier] <= 10:
        ajouter_carte = piocheCarte(la_pioche)
        print(ajouter_carte)
        Croupier_Tour[croupier] += valeurCarte(ajouter_carte[0])
        print(Croupier_Tour)

    # Si son score n'est pas 21
    while Croupier_Tour[croupier] < 21:
        ajouter_carte = piocheCarte(la_pioche)
        valeur = valeurCarte(ajouter_carte[0])
        # Tout as mtn va etre 1 car Croupier_Tour[croupier] > 11
        if valeur == 11:
            valeur -= 10
        Croupier_Tour[croupier] += valeur

        # Si son score != 21 apres avoir pioche, on doit rajouter la carte dans la pioche
        if not (Croupier_Tour[croupier] == 21):
            la_pioche.append(ajouter_carte[0])
            Croupier_Tour[croupier] -= valeur
        # Le croupier va piocher PAR HASARD une carte qui vaut ce dont le croupier a besoin pour avoir 21

    return Croupier_Tour


# Fonction professionnal
def professionnal(
    scoreCroupier, la_pioche, dict_CarteDistribueCroupier, croupier="Croupier"
):
    print(f"{croupier}: {scoreCroupier[croupier]}")

    as_libre = 0
    for af in dict_CarteDistribueCroupier[croupier]:
        if valeurCarte(af[0]) == 11:
            as_libre += 1

    if as_libre == 2:
        as_libre -= 1

    # Partie pioche
    a = True
    while a == True:
        # Compter la difference entre les cartes
        countingCard = 0
        for carte in la_pioche:
            if valeurCarte(carte) in [10, 11]:
                countingCard += 1
            elif valeurCarte(carte) in [2, 3, 4, 5, 6]:
                countingCard -= 1

        # Nếu điểm bé hơn 21
        if scoreCroupier[croupier] < 21:

            # Nếu số đếm >5, plus de carte de valeur 10 et 11
            if countingCard >= 5:
                if scoreCroupier[croupier] in [b for b in range(12)]:
                    ajouter_carte = piocheCarte(la_pioche)
                    print(ajouter_carte)
                    scoreCroupier[croupier] += valeurCarte(ajouter_carte[0])
                    if valeurCarte(ajouter_carte[0]) == 11:
                        as_libre += 1
                    if scoreCroupier[croupier] > 21 and as_libre > 0:
                        scoreCroupier[croupier] -= 10
                        as_libre -= 1

                elif scoreCroupier[croupier] in [12, 13, 14]:
                    pourcentagePioche = randint(0, 100)
                    if pourcentagePioche in [c for c in range(65)]:
                        ajouter_carte = piocheCarte(la_pioche)
                        print(ajouter_carte)
                        scoreCroupier[croupier] += valeurCarte(ajouter_carte[0])
                        if valeurCarte(ajouter_carte[0]) == 11:
                            as_libre += 1
                        if scoreCroupier[croupier] > 21 and as_libre > 0:
                            scoreCroupier[croupier] -= 10
                            as_libre -= 1
                    else:
                        print(f"{croupier} stop!")
                        a = False
                        break

                elif scoreCroupier[croupier] in [15, 16, 17, 18]:
                    pourcentagePioche = randint(0, 100)
                    if pourcentagePioche in [c for c in range(40)]:
                        ajouter_carte = piocheCarte(la_pioche)
                        print(ajouter_carte)
                        scoreCroupier[croupier] += valeurCarte(ajouter_carte[0])
                        if valeurCarte(ajouter_carte[0]) == 11:
                            as_libre += 1
                        if scoreCroupier[croupier] > 21 and as_libre > 0:
                            scoreCroupier[croupier] -= 10
                            as_libre -= 1
                    else:
                        print(f"{croupier} stop!")
                        a = False
                        break

                else:
                    pourcentagePioche = randint(0, 100)
                    if pourcentagePioche in [1, 2, 3, 4, 5]:
                        ajouter_carte = piocheCarte(la_pioche)
                        print(ajouter_carte)
                        scoreCroupier[croupier] += valeurCarte(ajouter_carte[0])
                        if valeurCarte(ajouter_carte[0]) == 11:
                            as_libre += 1
                        if scoreCroupier[croupier] > 21 and as_libre > 0:
                            scoreCroupier[croupier] -= 10
                            as_libre -= 1
                    else:
                        print(f"{croupier} stop!")
                        a = False
                        break

            # Le moyen des cartes entre les carte
            elif countingCard in [d for d in range(-5, 5)]:
                if scoreCroupier[croupier] in [b for b in range(12)]:
                    ajouter_carte = piocheCarte(la_pioche)
                    print(ajouter_carte)
                    scoreCroupier[croupier] += valeurCarte(ajouter_carte[0])
                    if valeurCarte(ajouter_carte[0]) == 11:
                        as_libre += 1
                    if scoreCroupier[croupier] > 21 and as_libre > 0:
                        scoreCroupier[croupier] -= 10
                        as_libre -= 1

                elif scoreCroupier[croupier] in [12, 13, 14]:
                    pourcentagePioche = randint(0, 100)
                    if pourcentagePioche in [c for c in range(75)]:
                        ajouter_carte = piocheCarte(la_pioche)
                        print(ajouter_carte)
                        scoreCroupier[croupier] += valeurCarte(ajouter_carte[0])
                        if valeurCarte(ajouter_carte[0]) == 11:
                            as_libre += 1
                        if scoreCroupier[croupier] > 21 and as_libre > 0:
                            scoreCroupier[croupier] -= 10
                            as_libre -= 1
                    else:
                        print(f"{croupier} stop!")
                        a = False
                        break

                elif scoreCroupier[croupier] in [15, 16, 17, 18]:
                    pourcentagePioche = randint(0, 100)
                    if pourcentagePioche in [c for c in range(50)]:
                        ajouter_carte = piocheCarte(la_pioche)
                        print(ajouter_carte)
                        scoreCroupier[croupier] += valeurCarte(ajouter_carte[0])
                        if valeurCarte(ajouter_carte[0]) == 11:
                            as_libre += 1
                        if scoreCroupier[croupier] > 21 and as_libre > 0:
                            scoreCroupier[croupier] -= 10
                            as_libre -= 1
                    else:
                        print(f"{croupier} stop!")
                        a = False
                        break

                else:
                    pourcentagePioche = randint(0, 100)
                    if pourcentagePioche in [c for c in range(10)]:
                        ajouter_carte = piocheCarte(la_pioche)
                        print(ajouter_carte)
                        scoreCroupier[croupier] += valeurCarte(ajouter_carte[0])
                        if valeurCarte(ajouter_carte[0]) == 11:
                            as_libre += 1
                        if scoreCroupier[croupier] > 21 and as_libre > 0:
                            scoreCroupier[croupier] -= 10
                            as_libre -= 1
                    else:
                        print(f"{croupier} stop!")
                        a = False
                        break

            # Dans le cas il a plus de carte de valeur 2,3,4,5,6 que l'autres
            elif countingCard < -5:
                if scoreCroupier[croupier] in [b for b in range(12)]:
                    ajouter_carte = piocheCarte(la_pioche)
                    print(ajouter_carte)
                    scoreCroupier[croupier] += valeurCarte(ajouter_carte[0])
                    if valeurCarte(ajouter_carte[0]) == 11:
                        as_libre += 1
                    if scoreCroupier[croupier] > 21 and as_libre > 0:
                        scoreCroupier[croupier] -= 10
                        as_libre -= 1

                elif scoreCroupier[croupier] in [12, 13, 14]:
                    pourcentagePioche = randint(0, 100)
                    if pourcentagePioche in [c for c in range(90)]:
                        ajouter_carte = piocheCarte(la_pioche)
                        print(ajouter_carte)
                        scoreCroupier[croupier] += valeurCarte(ajouter_carte[0])
                        if valeurCarte(ajouter_carte[0]) == 11:
                            as_libre += 1
                        if scoreCroupier[croupier] > 21 and as_libre > 0:
                            scoreCroupier[croupier] -= 10
                            as_libre -= 1
                    else:
                        print(f"{croupier} stop!")
                        a = False
                        break

                elif scoreCroupier[croupier] in [15, 16, 17, 18]:
                    pourcentagePioche = randint(0, 100)
                    if pourcentagePioche in [c for c in range(70)]:
                        ajouter_carte = piocheCarte(la_pioche)
                        print(ajouter_carte)
                        scoreCroupier[croupier] += valeurCarte(ajouter_carte[0])
                        if valeurCarte(ajouter_carte[0]) == 11:
                            as_libre += 1
                        if scoreCroupier[croupier] > 21 and as_libre > 0:
                            scoreCroupier[croupier] -= 10
                            as_libre -= 1
                    else:
                        print(f"{croupier} stop!")
                        a = False
                        break

                else:
                    pourcentagePioche = randint(0, 100)
                    if pourcentagePioche in [c for c in range(10)]:
                        ajouter_carte = piocheCarte(la_pioche)
                        print(ajouter_carte)
                        scoreCroupier[croupier] += valeurCarte(ajouter_carte[0])
                        if valeurCarte(ajouter_carte[0]) == 11:
                            as_libre += 1
                        if scoreCroupier[croupier] > 21 and as_libre > 0:
                            scoreCroupier[croupier] -= 10
                            as_libre -= 1
                    else:
                        print(f"{croupier} stop!")
                        a = False
                        break
        elif scoreCroupier[croupier] >= 21:
            a = False
    return scoreCroupier


"""-----------------Croupier Mise-----------------"""

# Fonction mise par défault = 15
def Croupier_Mise(dict_accountCroupier, croupier="Croupier"):
    # Si son compte est inferieur à 15, il doit miser tout
    if dict_accountCroupier[croupier] < 20:
        argentReste = dict_accountCroupier[croupier]
        dict_accountCroupier[croupier] -= argentReste
        return [argentReste]
    else:
        dict_accountCroupier[croupier] -= 15
        return [15]


# Fonction mise par pourcentage du restant
# Par le restant: toujours 20%, si le reste est inferieur à 15 => mise tout
def defautLeRestant(dict_accountCroupier, croupier="Croupier"):
    if dict_accountCroupier[croupier] < 20:
        tout = dict_accountCroupier[croupier]
        dict_accountCroupier[croupier] -= tout
        return [tout]
    else:
        mise = int(dict_accountCroupier[croupier] * 2 / 10)
        dict_accountCroupier[croupier] -= mise
        return [mise]


# Mise par l'autres joueurs
def cartesDesAutresJoueurs(scores, dict_accountCroupier, croupier="Croupier"):
    # Creer une liste pour comparer plus facilement
    listeDesAutresScores = []
    for autres in scores:
        if scores[autres] <= 21:
            listeDesAutresScores.append(scores[autres])

    if dict_accountCroupier[croupier] < 20:
        mise = dict_accountCroupier[croupier]
        dict_accountCroupier[croupier] -= mise
        return [mise]
    else:
        # Score max:
        scoreMax = max(listeDesAutresScores)
        # Faire les mises:
        # Si max = 21
        if scoreMax == 21:
            # a c'est le pourcentage de mise
            a = randint(10, 15)
        elif scoreMax in [18, 19, 20]:
            a = randint(15, 20)
        # Dans ce cas, on a plus de chance à gagner
        elif scoreMax in [12, 13, 14, 15, 16, 17]:
            a = randint(30, 45)
        # Si moins que 12
        else:
            a = randint(30, 35)

        mise = int(a * dict_accountCroupier[croupier] / 100)
        dict_accountCroupier[croupier] -= mise
        return [mise]


# Total initial des 2 cartes recues:
def cartesRecues(dict_accountCroupier, scoreCroupier, la_pioche, croupier="Croupier"):
    # Compter la difference entre 10 et 2 à 6.
    countingCard = 0
    for carte in la_pioche:
        if valeurCarte(carte) in [10, 11]:
            countingCard += 1
        elif valeurCarte(carte) in [2, 3, 4, 5, 6]:
            countingCard -= 1
    # Mise
    if dict_accountCroupier[croupier] <= 20:
        mise = dict_accountCroupier[croupier]
        dict_accountCroupier[croupier] -= mise
        return [mise]
    else:
        # Dans ce cas là, si on le point comme ca, il nous permet bcp de chance à gagner. De plus, si countingCard > 5, c'est à dire dans la pioche il y a plus de roi, dame, valet et as que les autres, qui nous autorise à avoir 20 ou 21 ou 19..
        if scoreCroupier[croupier] in [19, 20]:
            a = randint(30, 40)
        elif scoreCroupier[croupier] in [10, 11, 9]:
            if countingCard > 5:
                # mise entre 50% - 80%
                a = randint(50, 80)
            else:
                # mise entre 20% à 30%
                a = randint(20, 30)

        # Dans ce cas là, c'est pareil que le cas precedant
        elif scoreCroupier[croupier] in [15, 16, 17, 18]:
            if countingCard < -5:
                # mise entre 25%-30%
                a = randint(30, 40)
            else:
                a = randint(10, 15)

        # Si 21, all in
        elif scoreCroupier[croupier] == 21:
            a = randint(85, 100)
        elif scoreCroupier[croupier] in [12, 13, 14]:
            if countingCard in [a for a in range(-2, 2)]:
                a = randint(20, 25)
            else:
                a = randint(15, 20)
        # Si on a <9, il a bcp de risque ou 14
        else:
            a = randint(10, 15)
        mise = int(a * dict_accountCroupier[croupier] / 100)
        dict_accountCroupier[croupier] -= mise
        return [mise]


"""Fonction pour plusieurs croupiers"""


def miseDesCroupiers(dictAccountCroupier, niveauMise, scoresCroupiers, scoresJoueurs):
    listeDesMisesCroupiers = []
    for croupier in dictAccountCroupier:
        if niveauMise[croupier] == "Toujours15":
            liste_des_misesCroupier = Croupier_Mise(dictAccountCroupier, croupier)
        elif niveauMise[croupier] == "Restant":
            liste_des_misesCroupier = defautLeRestant(dictAccountCroupier, croupier)
        elif niveauMise[croupier] == "CarteRecues":
            liste_des_misesCroupier = cartesRecues(
                dictAccountCroupier, scoresCroupiers, la_pioche, croupier
            )
        elif niveauMise[croupier] == "DesAutresJoueurs":
            liste_des_misesCroupier = cartesDesAutresJoueurs(
                scoresJoueurs, dictAccountCroupier, croupier
            )
        print(f"{croupier} mise: {liste_des_misesCroupier[0]}")
        listeDesMisesCroupiers.append(liste_des_misesCroupier[0])
    return listeDesMisesCroupiers


def tourCompletCroupier(
    scoresCroupiers, la_pioche, dictCarteDistribueCroupier, niveauPioche
):
    print(f"Scores Croupiers: \n{scoresCroupiers}\n")
    for croupier in scoresCroupiers:
        if niveauPioche[croupier] == "Aleatoire":
            fullTourCroupier = Aleatoire(
                scoresCroupiers, la_pioche, dictCarteDistribueCroupier, croupier
            )
        elif niveauPioche[croupier] == "risqueMinimum":
            fullTourCroupier = risqueMinimum(
                scoresCroupiers, la_pioche, dictCarteDistribueCroupier, croupier
            )
        elif niveauPioche[croupier] == "risqueMaximum":
            fullTourCroupier = risqueMaximum(
                scoresCroupiers, la_pioche, dictCarteDistribueCroupier, croupier
            )
        elif niveauPioche[croupier] == "Pourcentage":
            fullTourCroupier = Pourcentage(
                scoresCroupiers, la_pioche, dictCarteDistribueCroupier, croupier
            )
        elif niveauPioche[croupier] == "Tricheur":
            fullTourCroupier = Tricheur(scoresCroupiers, la_pioche, croupier)
        elif niveauPioche[croupier] == "Professionnal":
            fullTourCroupier = professionnal(
                scoresCroupiers, la_pioche, dictCarteDistribueCroupier, croupier
            )
    return fullTourCroupier


# ---------------------------------------------
"""Programme Principal"""

# Số lượng người chơi tính cả máy/ Nombre de joueurs et croupier
nb_participe = int(input("Nombre de participants?: "))

# Tạo bộ bài/ Creer un grand paquet
la_pioche = initPioche(nb_participe)

# Hỏi là người hay là máy chơi/ Demander c'est homme ou croupier
listeDesJoueurs = []
listeDesCroupiers = []

for participant in range(nb_participe):
    indice = participant + 1
    typeParticipant = input(f"Participant {indice}, Ordinateur ou Joueur?: ")
    while not (typeParticipant in ["Ordinateur", "Joueur"]):
        typeParticipant = input("Again!! Ordinateur ou Joueur?: ")
    if typeParticipant == "Ordinateur":
        listeDesCroupiers.append(input("Nom du Ordinateur?: "))
    elif typeParticipant == "Joueur":
        listeDesJoueurs.append(input("Votre nom?: "))
    print("\n")

# Hỏi về level piocher và level mise/ demande le niveau piocher + mise
niveauPioche = {}
niveauMise = {}
for croupier in listeDesCroupiers:
    # Demander le niveau mise
    niveauMise[croupier] = {}
    difficultemise = input(
        f"Difficulte de {croupier}? Toujours15 / Restant / CarteRecues / DesAutresJoueurs "
    )
    while not (
        difficultemise in ["Toujours15", "Restant", "CarteRecues", "DesAutresJoueurs"]
    ):
        difficultemise = input(
            "Again!! Toujours15 / Restant / CarteRecues / DesAutresJoueurs "
        )
    niveauMise[croupier] = difficultemise

    # Demander le niveau pioche et le niveau mise
    difficulte = input(
        f"DifficultePioche de {croupier}? riqueMinimum / risqueMaximum / Aleatoire / Pourcentage / Tricheur / Professionnal "
    )
    while not (
        difficulte
        in [
            "risqueMinimum",
            "risqueMaximum",
            "Aleatoire",
            "Pourcentage",
            "Tricheur",
            "Professionnal",
        ]
    ):
        difficulte = input(
            "Again!! riqueMinimum / risqueMaximum / Aleatoire / Pourcentage / Tricheur / Professionnal "
        )
    niveauPioche[croupier] = difficulte

# Tạo từ điển tiền cho người chơi và từ điển tiền cho máy/ Creer les dictionnaires du compte
dictAccountJoueur = initKopecs(listeDesJoueurs)
dictAccountCroupier = initKopecs(listeDesCroupiers)

# Tạo từ điển điểm cho người chơi và croupier/ Creer les dictionnaires de score
dictScoresJoueurs = initScore(listeDesJoueurs)
dictScoresCroupiers = initScore(listeDesCroupiers)

"""Launch Game"""
rejouer = "oui"
nombreTour = 0

while rejouer == "oui":
    # Le nombre du tour
    nombreTour += 1
    print(f"\nTour {nombreTour}")
    """Le premier Tour"""
    # Tạo dict sau lượt bốc đầu tiên/ Creer les dictionnaites de scores apres le premierTour
    # Pour joueurs
    scoresJoueurs, dictCarteDistribueJoueur = premierTour(dictScoresJoueurs, la_pioche)
    print(f"Scores des joueurs maintenant: {scoresJoueurs}")

    # Pour croupiers
    scoresCroupiers, dictCarteDistribueCroupier = premierTour(
        dictScoresCroupiers, la_pioche
    )
    print(f"Scores des croupiers maintenant: {scoresCroupiers}\n")
    """Mise"""
    # Pour joueur
    listeDesMises = demandeMise(dictAccountJoueur)

    # Pour Croupier
    listeDesMisesCroupiers = miseDesCroupiers(
        dictAccountCroupier, niveauMise, dictScoresCroupiers, scoresJoueurs
    )
    # Somme des mises
    moneyGagne = sum(listeDesMises) + sum(listeDesMisesCroupiers)
    # Les restants
    print("\n")
    print(f"Les comptes des joueurs: {dictAccountJoueur}")
    print(f"Les comptes des croupiers: {dictAccountCroupier}\n")

    """Full tour"""
    # Pour joueur
    fullTour = tourComplet(scoresJoueurs, la_pioche, dictCarteDistribueJoueur)

    # Pour Croupier
    fullTourCroupier = tourCompletCroupier(
        scoresCroupiers, la_pioche, dictCarteDistribueCroupier, niveauPioche
    )
    print(fullTourCroupier)

    # Tạo từ điển chứa toàn bộ cả người lẫn máy/ Creer un dictionnare contenant même croupier et joueur
    dictForAllTempo = fullTour
    for croupier in fullTourCroupier:
        dictForAllTempo[croupier] = fullTourCroupier[croupier]

    print(dictForAllTempo)
    # Tìm người chiến thắng/ Gagnants times
    listWinner = gagnant(dictForAllTempo)
    print("\n")

    """Ramasser des mises"""
    if listWinner != 0:
        # Nếu có trên một nguòi chiến thắng ta cần phải chia đều tiền thưởng/ Si il y a plus 1 joueur qui gagne, on doit séparer la somme des mises
        for o in listWinner:
            if o in listeDesCroupiers:
                dictAccountCroupier[o] += int(moneyGagne / len(listWinner))
            else:
                dictAccountJoueur[o] += int(moneyGagne / len(listWinner))
        print(dictAccountJoueur)
        print(dictAccountCroupier, "\n")

    """Enlever les participants out of money"""
    # Joueur
    elemineJoueur = compterKopecs(dictAccountJoueur)
    for outJ in elemineJoueur:
        dictAccountJoueur.pop(outJ)
        dictScoresJoueurs.pop(outJ)

    # Croupier
    elemineCroupier = compterKopecs(dictAccountCroupier)
    for outC in elemineCroupier:
        dictAccountCroupier.pop(outC)
        dictScoresCroupiers.pop(outC)
        index = listeDesCroupiers.index(outC)
        listeDesCroupiers.pop(index)

    """Les cas restent"""
    # Si il a plus croupier
    if len(dictAccountCroupier) == 0:
        rejouer = "non"
    else:
        # Demander si qq1 veut quitter
        listeSayByeBye = []
        for joueurRester in dictAccountJoueur:
            rester = input(f"{joueurRester}, voulez vous rester? oui/non ")
            while not (rester in ["oui", "non"]):
                rester = input(f"Again! {joueurRester}, voulez vous rester? oui/non ")
            if rester == "non":
                listeSayByeBye.append(joueurRester)
                dictScoresJoueurs.pop(joueurRester)
                print(f"Bye {joueurRester}")
        for bye in listeSayByeBye:
            dictAccountJoueur.pop(bye)

    # Si il reste plus de personne
    if len(dictAccountJoueur) == 0:
        rejouer = "non"
    print("\n")

    # Renouveler le paquet
    if len(la_pioche) < 25:
        la_pioche = initPioche(nb_participe)


"""Finir Game"""
print("La partie est finie")
for croupier in dictAccountCroupier:
    dictAccountJoueur[croupier] = dictAccountCroupier[croupier]
    if len(dictAccountCroupier) != 0:
        lePlusRiche = 0
        for joueur in dictAccountJoueur:
            if dictAccountJoueur[joueur] > lePlusRiche:
                lePlusRiche = dictAccountJoueur[joueur]
                finalWinner = joueur
        print(f"Final Winner: {finalWinner}")
    else:
        print("No more Croupier! Tout gagne!")
