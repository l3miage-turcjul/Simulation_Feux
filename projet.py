#0,1,2 : pas cramé, craming et cendre

def creTable(haut,larg):
    table=[]
    for comp in range(haut):
        ligne=[]
        for comp2 in range(larg):
            ligne.append(0)
        table.append(ligne)
    return table

def setEtat(x,y,table,etat):
    match etat:
        case "craming":
            table[x][y]=1
        case "cramé" :
            table[x][y]=2
    return table


def main():
    valHaut=5
    valLarg=5
    proba=0.5
    X,Y=1,2
    print(creTable(valHaut,valHaut))
    setEtat 


  

if __name__ == '__main__':
    main()