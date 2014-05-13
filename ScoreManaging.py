
#Charge le fichier correspondant a la difficulte entree en parametre
#Renvoie un liste de listes de la forme [['NOM',123],...] avec le score en secondes
def readScore(gameMode):
    try:
        if gameMode==1:
            f = open("easyScore.txt", "r")
        elif gameMode==2:
            f = open("mediumScore.txt", "r")
        else:
            f = open("hardScore.txt", "r")
        try:
            lines = f.read()
        finally:
            f.close()
    except IOError:
        if gameMode==1:
            return [['AAA', 30], ['AAA', 35], ['AAA', 40], ['AAA', 45], ['AAA', 50], ['AAA', 55], ['AAA', 60], ['AAA', 65], ['AAA', 70], ['AAA', 75]]
        elif gameMode==2:
            return [['AAA', 60], ['AAA', 75], ['AAA', 90], ['AAA', 105], ['AAA', 120], ['AAA', 135], ['AAA', 150], ['AAA', 165], ['AAA', 180], ['AAA', 195]]
        else:
            return [['AAA', 120], ['AAA', 150], ['AAA', 180], ['AAA', 210], ['AAA', 240], ['AAA', 270], ['AAA', 300], ['AAA', 330], ['AAA', 360], ['AAA', 390]]
    # table contient ['NOM 123',...]
    tableinit=lines.split("\n")
    table=[]
    for loop in range(10):
        table.append(tableinit[loop])
    scores=[]
    for loop in range(len(table)):
        line = table[loop].split(' ') # line = [ 'NOM', '123' ]
        line[1]=int(line[1])
        scores.append(line)
    return scores


#Compare le score entre avec les autres scores de la difficulte sélectionnee
#Renvoie le rang du score ou 0 si le score est trop faible
def isHighScore(gameMode,score):
    scoreBoard=readScore(gameMode)
    compteur=0
    if scoreBoard[9][1]<=score:
        return 0
    while scoreBoard[compteur][1]<=score:
        compteur+=1
    return compteur+1

#Insere le score du joueur dans la liste des scores
#Renvoie une liste decalee
def insertScore(gameMode,name,score):
    scoreBoard=readScore(gameMode)
    rank=isHighScore(gameMode,score)
    for loop in range (10-rank):
        scoreBoard[9-loop]=scoreBoard[8-loop]
    scoreBoard[rank-1]=[name,score]
    return scoreBoard

#Transforme la liste en entree pour qu'elle soit enregistrable
#Enregistre le nouveau fichier de scores
def writeScore(gameMode,scoreBoard):
    for loop in range(len(scoreBoard)):
        scoreBoard[loop]=scoreBoard[loop][0]+' '+str(scoreBoard[loop][1])+'\n'
    try:
        if gameMode==1:
            f = open("easyScore.txt", "w")
        elif gameMode==2:
            f = open("mediumScore.txt", "w")
        else:
            f = open("hardScore.txt", "w")
        try:
            f.writelines(scoreBoard)
        finally:
            f.close()
    except IOError:
        pass

#Insere le score du joueur dans une liste et l'enregistre
def submitScore(gameMode,name,score):
    scoreBoard=insertScore(gameMode,name,score)
    writeScore(gameMode,scoreBoard)