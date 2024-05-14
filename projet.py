# 0 : pas de feux
# 1 : en feux à l'instant T
# 2 : cendre

import random
import copy
import json

#Fonction créant la table et la remplissant
def creTable(haut,larg):
    table=[]
    for comp in range(haut):
        ligne=[]
        for comp2 in range(larg):
            ligne.append(0)
        table.append(ligne)
    return table

#Fonction mettant à jour l'état des cellules 
def setEtat(x,y,table,posicram,etat):
    match etat:
        case "craming":
            #On met à jour l'état de la case dans la table et on ajoute la position à la liste des positions en feux
            table[x][y]=1
            posicram.append([x,y])
        case "cramé" :
            #On met à jour l'état de la case dans la table et on retire la position à la liste des positions en feux
            table[x][y]=2
            posicram.remove([x,y])
    return table,posicram

#Fonction de vérification si la position est bien comprise dans la table
def posiEstVld(posi):
    if (posi[1]<0) or (posi[1]> valLarg-1) :
        return False
    if (posi[0]<0) or (posi[0]> valHaut-1) :
        return False
    return True

#Fonction de passage à l'état suivant
def passEtSv(table,lstposicram,proba):
    #On effectue une copie de la table pour pouvoir travailler pendant ce tour et ne pas altérer la table sur laquelle on itère
    posicramtemp=copy.copy(lstposicram)
    for posi in lstposicram:
        #génération des positions à tester pour chaque position en feu
        positest=[[posi[0]-1,posi[1]],[posi[0]+1,posi[1]],[posi[0],posi[1]-1],[posi[0],posi[1]+1]]
        for test in positest:
            #Vérification que la position est valide et pas déjà en feux
            if posiEstVld(test) and table[test[0]][test[1]]==0:
                #Vérification que le tirage aléatoire est favorable au départ de feux sur cette position
                if (random.randint(0,100)/100<=proba):
                    table,posicramtemp=setEtat(test[0],test[1],table,posicramtemp,"craming")
        table,posicramtemp=setEtat(posi[0],posi[1],table,posicramtemp,"cramé")
    #Copie de la table temporaire dans la table réelle
    lstposicram=copy.copy(posicramtemp)  
    return table,lstposicram

#Fonction d'affichage de la table dans la console
def affichBase(table):
    aff=""
    for ligne in table:
        aff+="["
        for case in ligne:
            match case:
                case 0:
                    #Affichage du symbole de l'arbre
                    aff+="\U0001F333,"
                case 1:
                    #Affichage du symbole du feux
                    aff+="\U0001F525,"
                case 2:
                    #Affichage du symbole des cendres
                    aff+="\U000026AB,"
        aff+="]\n"
    print(aff)
    aff=""
    return


def main():
    #variable de paramétrage lors du fonctionnement du programme
    mode=""
    res=""
    #variable pour définition de la table
    global valHaut
    global valLarg
    valHaut=33
    valLarg=77
    #variable de probabilité de départ du feux
    proba=0.8
    #Tableau stockant les positions en feu à un instant T
    posicram=[]
    #Variables pour la localisation du départ du feux
    departY=valLarg-1
    departX=valHaut-1


    #Lecture des valeurs dans le fichier de configuration
    fic=open("config.txt","r")
    params=json.load(fic)
    valHaut=params['Hauteur']
    valLarg=params['Largeur']
    proba=params['Probabilite']
    departX=params['Depart']['x']
    departY=params['Depart']['y']
    fic.close()
    print("Départ du feux : \nx :",departX," y :",departY)

    #Début de la simulation
    table=creTable(valHaut,valLarg)
    table,posicram=setEtat(departX-1,departY-1,table,posicram,"craming")
    print("Etat init :")
    affichBase(table)
    print(posicram)
    print("Quel mode d'execution voulez-vous ?\nauto: exécution automatique jusqu'à ce que plus aucune parcelle ne brule\npas: pas à pas; demande à chaque tour si on doit continuer l'exécution")
    print("[n'importe quel autre instruction mettera fin au programme]")
    mode=input(":").lower()
    if mode=="pas":
        print("o: continuer l'execution\nn: terminer l'exécution")
    while len(posicram)!=0 and ((res!="n" and mode=="pas") or (mode=="auto")):
        table,posicram=passEtSv(table,posicram,proba)
        print("Etat suivant :")
        print(posicram)
        affichBase(table)
        if mode=="pas":
            res=input("Continuer ?\n")

  

if __name__ == '__main__':
    main()