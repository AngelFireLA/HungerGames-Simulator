enzo = ["océane", "jade", "joanna", "sylvia", "valentine", "bianca"]

print("Simulateur Enzo")
input("Tu trouves une meuf sur Insta belle, quel est son nom : ")
print("Whoa le gormiti, mais quand même, que veux-tu faire ?")
choix = input("Choisi : 1. La DM sur Insta 2. L'ajouter sur Snap 3. Lui parler IRL.")

if choix not in ["1", "2", "3"]:
    print("Ce n'est pas un choix, carton rouge !!!")
    exit()

if choix == "3":
    print("Carton rouge !!!")
    print("Ce n'est pas possible, recommence.")

    choix = input("Choisi : 1. La DM sur Snap 2. L'ajouter sur Insta.")
    if choix not in ["1", "2", "3"]:
        print("Ce n'est pas un choix, carton rouge !!!")
        exit()

if choix == "1":
    print("Tu vas la DM sur Snap, mais tu es enzo donc elle te réponds pas que fais Tu ?")
    print("Whoa le gormiti, mais quand même, que veux-tu faire :")
    choix = input("Choisi : 1. Lui renvoyer un message 2. Attendre. 3. Lui parler IRL.")
    if choix not in ["1", "2", "3"]:
        print("Ce n'est pas un choix, carton rouge !!!")
        exit()
    if choix == "1":
        print("Carton rouge !!!")
        print("Sans faire exprès tu l'appelles et elle ne te répondra jamais, recommence.")
        exit()
    elif choix == "2":
        print("Elle t'envoies enfin un message, un 'Salut', que réponds-tu ?")
        choix = input("Choisi : 1. Lui demander un Snap Rouge 2. Lui mettre un remis en retour. 3. Lui parler IRL.")
        if choix not in ["1", "2", "3"]:
            print("Ce n'est pas un choix, carton rouge !!!")
            exit()
        if choix == "1":
            print("Carton rouge !!!")
            print("Elle t'en envoies un mais c'est une taïwannaise, recommence.")
            exit()
        elif choix == "2":
            print("Carton rouge !!!")
            print("T'oublies de lui renvoyer un message et elle te bloque, recommence.")
            exit()
        elif choix == "3":
            print("Carton rouge !!!")
            print("Ce n'est pas possible, recommence.")
            exit()
    elif choix == "3":
        print("Carton rouge !!!")
        print("Ce n'est pas possible, recommence.")
        exit()

elif choix == "2":
    print("Carton rouge !!!")
    print("Elle t'ajoutes en retour mais sans faire exprès tu la refuse, recommence.")
    exit()
