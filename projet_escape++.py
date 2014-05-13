from Tkinter import *
import random
import pygame
import time
from SprManaging import *
from ScoreManaging import *

#Chargement de la musique, et lancement de cette derniere
pygame.mixer.init()
pygame.mixer.music.load("Soundtrack.ogg")
pygame.mixer.music.set_volume(0.7)
pygame.mixer.music.play(-1)

#Sortie du programme et arret de la musique
def exitApplication():
    fenetre.destroy()
    pygame.mixer.music.stop()

# Renvoie l'heure en millisecondes
def getTime():
    return int(round(time.time() * 1000))
# Incrémente timerSecond a chaque seconde de jeu
def computeElapsedTime():
    global timerSecond,startingTime
    if getTime()-startingTime>=1000:
        startingTime=getTime()
        timerSecond+=1


#Creation fenetre
fenetre = Tk()
#Modifie le protocole associe a la touche de sortie de la fenetre
fenetre.protocol("WM_DELETE_WINDOW", exitApplication)
fenetre.geometry("%dx%d%+d%+d" % (480,480,(fenetre.winfo_screenwidth()-480)//2,(fenetre.winfo_screenheight()-480)//2))
fenetre.iconbitmap('icon.ico')
fenetre.title('Escape')

#Creation d'un canevas

resolution=32
ecart_ecran=7
quit=False
z=0
q=0
s=0
d=0
mobSpawnZone=[[[1,1],[5,5]],[[1,1],[3,3],[5,5],[5,1]],[[4,0],[2,2],[0,4],[2,6],[4,4],[6,2]]]
charSpeed=75
charTimer=0
mobSpeed=200
whipping=0
whipTimer=0
whipCooldown=1000
whipSpeed=500
X=1
Y=0
alphabet=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']


#Correspondances dans le matrice :
# 0: Mur
# 1: Sol
# 2: Porte
# 3: Personnage regard vers le bas
# 4: Personnage regard vers la gauche
# 5: Personnage regard vers la droite
# 6: Personnage regard vers le haut
# 7: Monstre regard vers le bas
# 8: Monstre regard vers la gauche
# 9: Monstre regard vers la droite
# 10: Monstre regard vers le haut
# 11: Fouet droit vers le bas
# 12: Fouet droit vers la gauche
# 13: Fouet droit vers la droite
# 14: Fouet droit vers le haut
# 15: Fin du fouet vers le bas
# 16: Fin du fouet vers la gauche
# 17: Fin du fouet vers la droite
# 18: Fin du fouet vers le haut
# 19: Clé
# 23: Personnage regard vers le bas fouettant
# 24: Personnage regard vers la gauche fouettant
# 25: Personnage regard vers la droite fouettant
# 26: Personnage regard vers le haut fouettant
# 27: Monstre regard vers le bas au-dessus d'un mur
# 28: Monstre regard vers la gauche au-dessus d'un mur
# 29: Monstre regard vers la droite au-dessus d'un mur
# 30: Monstre regard vers le haut au-dessus d'un mur

#Charge les sprites du jeu. Fonction definie dans SprManaging.py
loadSprites()

#Génération d'une matrice labyrinthique de dimensions widthxheight
def creerLabyrinthe(width,height,nbMonsters):
    global charPos,charVel,look,mobPos,mobVel,deadMob,seen,mobLook,mobTimer,matrice,keyIsFound,startingTime,timerSecond
    #matrice remplie de 0
    matrice2=[[0]*(width/2) for i in range(height/2)]
    matrice=[[0]*width for i in range(height)]
    #définition du point de départ du personnage
    x=1
    y=height/2-2
    chemin=[[x,y]]      #liste contenant toutes les cases du chemin
    matrice2[y][x]=1
    k=0
    while (k==0):
        n=[]
        n1=1    #Bloc au-dessus du bloc actuel
        n2=1    #Bloc à droite du bloc actuel
        n3=1    #Bloc en-dessous du bloc actuel
        n4=1    #Bloc à gauche du bloc actuel

        #Attribution de la valeur de chaque bloc
        if y>1:
            n1=matrice2[y-2][x]+matrice2[y-1][x-1]+matrice2[y-1][x+1]+matrice2[y-1][x]+matrice2[y-2][x+1]+matrice2[y-2][x-1]
        if x<width/2-2:
            n2=matrice2[y][x+2]+matrice2[y-1][x+1]+matrice2[y+1][x+1]+matrice2[y][x+1]+matrice2[y-1][x+2]+matrice2[y+1][x+2]
        if y<height/2-2:
            n3=matrice2[y+2][x]+matrice2[y+1][x-1]+matrice2[y+1][x+1]+matrice2[y+1][x]+matrice2[y+2][x+1]+matrice2[y+2][x-1]
        if x>1:
            n4=matrice2[y][x-2]+matrice2[y-1][x-1]+matrice2[y+1][x-1]+matrice2[y][x-1]+matrice2[y-1][x-2]+matrice2[y+1][x-2]

        #Pour chaque bloc : est-il disponible? Stockage de tous les blocs disponibles dans la variable n
        if n1==0:
            n.append(1)
        if n2==0:
            n.append(2)
        if n3==0:
            n.append(3)
        if n4==0:
            n.append(4)
        if len(n)>0:
            m=random.randint(1,len(n))      #Bloc choisit aleatoirement parmi les blocs disponibles
            direction=n[m-1]
            if direction==1:                #Progression du "chemin" vers le bloc sélectionné
                y-=1
            if direction==2:
                x+=1
            if direction==3:
                y+=1
            if direction==4:
                x-=1
            chemin.append([x,y])
            matrice2[y][x]=1
        else:
            chemin.remove([x,y])            #Décrémentation de la liste "chemin" du dernier bloc, car c'est une voie sans issue
            alea=random.randint(0,(len(chemin)-1))      #Choix d'un bloc aleatoire du "chemin" pour repartir
            x=chemin[alea][0]
            y=chemin[alea][1]
        if len(chemin)==1:                  #Explorer tous les chemins, jusqu'à ce que la liste "chemin" ne contienne plus que le bloc de départ
            k+=1

    for j in range(height/2):
        for i in range(width/2):
            x=matrice2[j][i]
            matrice[2*j][2*i]=x
            matrice[2*j+1][2*i]=x
            matrice[2*j][2*i+1]=x
            matrice[2*j+1][2*i+1]=x

    possible=[]
    #Placement aleatoire de la porte
    for loop in range(2,width-3):
        if isBlockEmpty(loop,2):
            possible.append([1,loop])
    for loop in range(2,height-3):
        if isBlockEmpty(width-3,loop):
            possible.append([loop,width-2])
    alea=random.randint(0,len(possible)-1)
    matrice[possible[alea][Y]][possible[alea][X]]=2
    #Placement d'un bloc de sol derriere la porte
    if possible[alea][Y]<2:
        matrice[possible[alea][Y]-1][possible[alea][X]]=1
    else:
        matrice[possible[alea][Y]][possible[alea][X]+1]=1
    #Placement du personnage, que l'on informe dans la liste CharPos[y,x] et initialisation de sa vitesse CharVel[y,x]
    matrice[height-3][2]=3
    charPos=[height-3,2]
    charVel=[0,0]
    look=3
    #Placement de la clé
    possible=[]
    for j in range (height/3,2*height/3):
        for i in range (width/3,2*width/3):
            if isBlockEmpty(i,j):
                possible.append([j,i])
    alea=random.randint(0,len(possible)-1)
    matrice[possible[alea][Y]][possible[alea][X]]=19
    keyIsFound=False
    #Apparition des monstres
    possible=[]
    mobPos=[]
    mobVel=[]
    for mobID in range(nbMonsters):
        for j in range(mobSpawnZone[nbMonsters/2-1][mobID][Y]*height/8,(mobSpawnZone[nbMonsters/2-1][mobID][Y]+2)*height/8):
            for i in range(mobSpawnZone[nbMonsters/2-1][mobID][X]*width/8,(mobSpawnZone[nbMonsters/2-1][mobID][X]+2)*width/8):
                if matrice[j][i]==1:
                    possible.append([j,i])
        alea=random.randint(0,len(possible)-1)
        matrice[possible[alea][Y]][possible[alea][X]]=7
        mobPos.append([possible[alea][Y],possible[alea][X]])
        mobVel.append([0,0])
        possible=[]
    deadMob=[0 for loop in range(nbMonsters)]
    seen=[0 for loop in range(nbMonsters)]
    mobLook=[7 for loop in range(nbMonsters)]
    mobTimer=[0 for loop in range(nbMonsters)]
    startingTime=getTime()
    timerSecond=0
    return matrice

#Gere les deplacements et interactions du monstre
def mobManagement(mobID):
    global mobVel,mobPos,matrice,mobLook,mobTimer,seen
    #Le monstre est-il tue?
    if isBlockWhip(mobPos[mobID][X],mobPos[mobID][Y]):
        deadMob[mobID]=1
        mobPos[mobID]=[0,0]
    #Si il n'est pas encore mort, le deplacer
    if deadMob[mobID]==0:
        #Si le joueur n'est pas detecte
        if seen[mobID]==0:
            alea=random.randint(1,4)
            if alea==1:
                mobVel[mobID]=[0,1]
            elif alea==2:
                mobVel[mobID]=[0,-1]
            elif alea==3:
                mobVel[mobID]=[1,0]
            elif alea==4:
                mobVel[mobID]=[-1,0]
            if not isBlockEmpty(mobPos[mobID][X]+mobVel[mobID][X],mobPos[mobID][Y]+mobVel[mobID][Y]):
                mobVel[mobID]=[0,0]
        #Si le joueur est detecte
        else:
            xDiff=charPos[X]-mobPos[mobID][X]
            yDiff=charPos[Y]-mobPos[mobID][Y]
            if abs(xDiff)>abs(yDiff) and xDiff!=0:
                mobVel[mobID]=[0,xDiff/abs(xDiff)]
            elif yDiff!=0:
                mobVel[mobID]=[yDiff/abs(yDiff),0]
            #Permet de contourner un obstacle
            if not isBlockFlyable(mobPos[mobID][X]+mobVel[mobID][X],mobPos[mobID][Y]+mobVel[mobID][Y]):
                mobVelCopy=mobVel
                if xDiff==0 or yDiff==0:
                    mobVel[mobID][X]=mobVelCopy[mobID][Y]
                    mobVel[mobID][Y]=mobVelCopy[mobID][X]
                else:
                    mobVel[mobID][X]=abs(mobVelCopy[mobID][Y])*xDiff/abs(xDiff)
                    mobVel[mobID][Y]=abs(mobVelCopy[mobID][X])*yDiff/abs(yDiff)
        #Deplacer le monstre dans la matrice si il peut se deplacer sur le bloc et que le timer le permet
        if getTime()>=mobTimer[mobID]+mobSpeed and isBlockFlyable(mobPos[mobID][X]+mobVel[mobID][X],mobPos[mobID][Y]+mobVel[mobID][Y]):
            mobTimer[mobID]=getTime()
            if mobLook[mobID]<11:
                matrice[mobPos[mobID][Y]][mobPos[mobID][X]]=1
            else :
                matrice[mobPos[mobID][Y]][mobPos[mobID][X]]=0
            mobPos[mobID][X]+=mobVel[mobID][X]
            mobPos[mobID][Y]+=mobVel[mobID][Y]
            if mobVel[mobID][Y]==1:
                mobLook[mobID]=7
            elif mobVel[mobID][X]==-1:
                mobLook[mobID]=8
            elif mobVel[mobID][X]==1:
                mobLook[mobID]=9
            elif mobVel[mobID][Y]==-1:
                mobLook[mobID]=10
            if matrice[mobPos[mobID][Y]][mobPos[mobID][X]]==0:
                mobLook[mobID]+=20
            matrice[mobPos[mobID][Y]][mobPos[mobID][X]]=mobLook[mobID]
        #Detection du joueur
        if charPos[Y]-5<=mobPos[mobID][Y] and charPos[Y]+5>=mobPos[mobID][Y] and charPos[X]-5<=mobPos[mobID][X] and charPos[X]+5>=mobPos[mobID][X]:
            seen[mobID]=1

#Affiche la matrice dans le canevas
def displayScreen(canevas,matrice,charPos):
    #ecran= zone de la matrice autour du personnage que l'on souhaite afficher
    ecran = [charPos[X]-ecart_ecran,charPos[X]+ecart_ecran,charPos[Y]-ecart_ecran,charPos[Y]+ecart_ecran] #premierx,dernierx,premier y, et dernier y de l'ecran
    # recadrage de l'ecran: si le personnage se situe pres d'un bord du labyrinthe alors on deplace l'écran pour ne pas afficher ce qui hors du labyritnhe
    if ecran[0]<0:
        ecran[0]=0                           #Par exemple, si le personage se situe en dessous de "ecart_ecran" sur la gauche, alors l'écran ne le suit plus et se cale sur le bord gauche
        ecran[1]=2*ecart_ecran
    if ecran[1]>=width:
        ecran[1]=width-1
        ecran[0]=width-(2*ecart_ecran)-1
    if ecran[2]<0:
        ecran[2]=0
        ecran[3]=2*ecart_ecran
    if ecran[3]>=height:
        ecran[3]=height-1
        ecran[2]=height-(2*ecart_ecran)-1
    #recuperation des cases correspondantes dans la matrice pour les afficher
    for j in range(ecran[2],ecran[3]+1):
        for i in range(ecran[0],ecran[1]+1):
            # la variable x prend la valeur de chaque bloc a afficher successivement
            x=matrice[j][i]
            # les variables i2 et j2 informent la position relative du bloc cible dans l' "ecran"
            j2=j-charPos[Y]+ecart_ecran
            i2=i-charPos[X]+ecart_ecran
             # ces tests permettent d'eviter les erreurs pour i2 et j2 suite a un recadrage de l'ecran
            if charPos[Y]<ecart_ecran:
                j2-=(ecart_ecran-charPos[Y])
            if charPos[X]<ecart_ecran:
                i2-=(ecart_ecran-charPos[X])
            if charPos[Y]>=(height-ecart_ecran):
                j2-=(height-ecart_ecran-charPos[Y]-1)
            if charPos[X]>=(width-ecart_ecran):
                i2-=(width-ecart_ecran-charPos[X]-1)
            # on cree une image aux coordonnees i2 j2 selon la valeur de x
            displayBlock(canevas,x,i2,j2)

def displayBlock(canevas,x,i2,j2):
    canevas.create_image(i2*resolution+17,j2*resolution+17,image=SG.blocks[x])

#Fais fouetter le personnage seulement si le cooldown est ecoule
def doWhip():
    global whipTimer,whipping,charVel
    if getTime()>=whipCooldown+whipTimer:
        whipping=1
        charVel=[0,0]
        whipTimer=getTime()

#Si une touche est enfoncée
def keypress(event):
    key=event.keysym
    global charVel,z,q,s,d,whipping,whipTimer,gameInProgress,gamePaused
    if key=="Up" and whipping==0:
        charVel[X]=0                #Si le personnage se deplace horizontalement, alors il perd sa vitesse selon l'axe x
        charVel[Y]=-1               #Quand on appuye sur "z" le personnage se dirige vers le haut
        z=1                         #la variable "z" permet de se souvenir qu'on a appuyé sur "z"
    elif key=="Left" and whipping==0:
        charVel[X]=-1
        charVel[Y]=0
        q=1
    elif key=="Down" and whipping==0:
        charVel[X]=0
        charVel[Y]=1
        s=1
    elif key=="Right" and whipping==0:
        charVel[X]=1
        charVel[Y]=0
        d=1
    elif key=="space":
        doWhip()
    elif key=="Escape":
        gameInProgress=False
        gamePaused=True

#Si une touche est relachée
def keyrelease(event):
    global charVel,z,q,s,d
    key=event.keysym
    if key=="Up":
        z=0                      #La variable "z" permet de se souvenir qu'on a relaché la touche"z"
        if charVel[Y]==-1:
            charVel[Y]=0         #Si le personnage se deplace vers le haut alors qu'on relache la touche "z", il s'arrete
        if s==1:
            charVel[Y]=1         #Si le joueur a appuye sur "s" et qu'il n'a toujours pas relache la touche alors le personnage recommence a descendre
        if q==1:
            charVel[X]=-1
        if d==1:
            charVel[X]=1
    elif key=="Down":
        s=0
        if charVel[Y]==1:
            charVel[Y]=0
        if z==1:
            charVel[Y]=-1
        if q==1:
            charVel[X]=-1
        if d==1:
            charVel[X]=1
    if key=="Left":
        q=0
        if charVel[X]==-1:
            charVel[X]=0
        if z==1:
            charVel[Y]=-1
        if s==1:
            charVel[Y]=1
        if d==1:
            charVel[X]=1
    if key=="Right":
        d=0
        if charVel[X]==1:
            charVel[X]=0
        if z==1:
            charVel[Y]=-1
        if s==1:
            charVel[Y]=1
        if q==1:
            charVel[X]=-1


#Recalcule la matrice, et l'affiche
def draw(canevas):
    global matrice,charPos,charVel,charTimer,mobPos,mobVel,mobTimer,look,gameInProgress,doorReached,charKilled,keyIsFound
    # si le personnage est sur la porte
    computeElapsedTime()
    if matrice[charPos[Y]+charVel[Y]][charPos[X]+charVel[X]]==2 and keyIsFound:
        gameInProgress=False
        doorReached=True
    else:
        if matrice[charPos[Y]+charVel[Y]][charPos[X]+charVel[X]]==19:
            keyIsFound=True
        #Si la nouvelle position du personnage est un bloc de sol
        if isBlockOnFloor(charPos[X]+charVel[X],charPos[Y]+charVel[Y]) and getTime()>=charTimer+charSpeed:
            charTimer=getTime()
            #On le deplace dans la matrice
            matrice[charPos[Y]][charPos[X]]=1
            #On informe la variable "CharPos" de sa nouvelle position
            charPos[X]+=charVel[X]
            charPos[Y]+=charVel[Y]
        #La variable look informe le regard du personnage en fonction de la derniere touche appuyee
        if charVel[Y]==1:
            look=3
        elif charVel[X]==-1:
            look=4
        elif charVel[X]==1:
            look=5
        elif charVel[Y]==-1:
            look=6
        matrice[charPos[Y]][charPos[X]]=look    #On place le personnage a sa nouvelle position dans la matrice

        # gestion des monstres
        for mobID in range(nbMonsters):
            mobManagement(mobID)
            if mobPos[mobID][Y]==charPos[Y] and mobPos[mobID][X]==charPos[X]:
                gameInProgress=0
                charKilled=1

        # gestion du fouet
        whipManagement(charPos,look)
        #Affichage
        displayScreen(canevas,matrice,charPos)

#Gere le fouet
def whipManagement(charPos,look):
    global matrice,whipTimer,whipping,deadMob
    endedwhip=0
    if whipping==1:
        if look==3:
            dx=0
            dy=1
        elif look==4:
            dx=-1
            dy=0
        elif look==5:
            dx=1
            dy=0
        else:       # elif look==6:
            dx=0
            dy=-1
        for loop in range(3):
            xposition=charPos[X]+dx*(loop+1)
            yposition=charPos[Y]+dy*(loop+1)
            xposition2=xposition+dx
            yposition2=yposition+dy
            if (not isBlockOnFloor(xposition,yposition) or isBlockKey(xposition,yposition)) and endedwhip==0 :
                endedwhip=1
            elif endedwhip==0:
                matrice[charPos[Y]][charPos[X]]=look+20
                if not isBlockKey(xposition2,yposition2) and isBlockOnFloor(xposition2,yposition2) and loop<2:
                    matrice[yposition][xposition]=look+8
                else:
                    matrice[yposition][xposition]=look+12
                    endedwhip=1
        if getTime()>=whipTimer+whipSpeed:
            whipping=0
            whipTimer=getTime()
            for j in range(height):
                for i in range(width):
                    if matrice[j][i]>=11 and matrice[j][i]<=18:
                        matrice[j][i]=1

# Renvoie TRUE si le block est un sol (même avec un objet/personnage dessus).
# Renvoie FALSE si on est en dehors de la matrice
def isBlockOnFloor(x,y):
    if x<0 or x>=width:
        return False
    if y<0 or y>=height:
        return False
    if matrice[y][x]!=0 and matrice[y][x]!=2 and matrice[y][x]<27:
        return True
    else:
        return False

# Renvoie TRUE si le block est un monstre sur le sol
# Renvoie FALSE si on est en dehors de la matrice
def isBlockMobOnFloor(x,y):
    if x<0 or x>=width:
        return False
    if y<0 or y>=height:
        return False
    if matrice[y][x]>=7 and matrice[y][x]<=10:
        return True
    else:
        return False

# Renvoie TRUE si le block est un morceau de fouet (bout compris)
# Renvoie FALSE si on est en dehors de la matrice
def isBlockWhip(x,y):
    if x<0 or x>=width:
        return False
    if y<0 or y>=height:
        return False
    if matrice[y][x]>=11 and matrice[y][x]<=18:
        return True
    else:
        return False

# Renvoie TRUE si le block est une cle
# Renvoie FALSE si on est en dehors de la matrice
def isBlockKey(x,y):
    if x<0 or x>=width:
        return False
    if y<0 or y>=height:
        return False
    if matrice[y][x]==19:
        return True
    else:
        return False

# Renvoie TRUE si le block est un sol vide
# Renvoie FALSE si on est en dehors de la matrice
def isBlockEmpty(x,y):
    if x<0 or x>=width:
        return False
    if y<0 or y>=height:
        return False
    if matrice[y][x]==1:
        return True
    else:
        return False

# Renvoie TRUE si le block est un sol vide, un sol avec un joueur ou un mur
# Renvoie FALSE si on est en dehors de la matrice
def isBlockFlyable(x,y):
    if x<0 or x>=width:
        return False
    if y<0 or y>=height:
        return False
    if matrice[y][x]==1 or matrice[y][x]==0 or (matrice[y][x]>=3 and matrice[y][x]<=6) or (matrice[y][x]>=23 and matrice[y][x]<=26):
        return True
    else:
        return False

#Vide la fenetre, sauf le widget passé en paramètre
def emptyMainWindow(survivor=None):
    for child in fenetre.winfo_children():
        if child!=survivor:
            child.destroy()

#Menu principal
def displayMainMenu():
    emptyMainWindow()
    title=Label(fenetre,image=SG.title,bd=-2)
    title.place(x=0,y=0)
    border1=Label(fenetre,image=SG.border,bd=-2)
    border1.place(x=0,y=4*32)
    border2=Label(fenetre,image=SG.border,bd=-2)
    border2.place(x=9*32,y=4*32)
    line1=Label(fenetre,image=SG.line,bd=-2)
    line1.place(x=6*32,y=4*32)
    line2=Label(fenetre,image=SG.line,bd=-2)
    line2.place(x=6*32,y=6*32)
    line3=Label(fenetre,image=SG.line,bd=-2)
    line3.place(x=6*32,y=8*32)
    line4=Label(fenetre,image=SG.line,bd=-2)
    line4.place(x=6*32,y=10*32)
    line5=Label(fenetre,image=SG.line,bd=-2)
    line5.place(x=6*32,y=12*32)
    line6=Label(fenetre,image=SG.line,bd=-2)
    line6.place(x=6*32,y=14*32)
    button1=Button(fenetre, text="Easy" ,command=setEasyGame ,image=SG.button,compound=CENTER,bd=0,fg='White',highlightthickness=0)
    button1.place(x=6*32,y=5*32)
    button2=Button(fenetre, text="Medium", command=setMediumGame,image=SG.button,compound=CENTER,bd=0,fg='White',highlightthickness=0)
    button2.place(x=6*32,y=7*32)
    button3=Button(fenetre, text="Hard", command=setHardGame,image=SG.button,compound=CENTER,bd=0,fg='White',highlightthickness=0)
    button3.place(x=6*32,y=9*32)
    button4=Button(fenetre, text="Highscores", command=displayChooseScore,image=SG.button,compound=CENTER,bd=0,fg='White',highlightthickness=0)
    button4.place(x=6*32,y=11*32)
    button5=Button(fenetre, text="Quit", command=exitApplication,image=SG.button,compound=CENTER,bd=0,fg='White',highlightthickness=0)
    button5.place(x=6*32,y=13*32)

def setEasyGame():
    displayControls(1)
def setMediumGame():
    displayControls(2)
def setHardGame():
    displayControls(3)

#Menu des controles
def displayControls(diff):
    global canevas
    emptyMainWindow()
    canevas = Canvas(fenetre, width = resolution*(ecart_ecran*2+1)-2, height = resolution*(ecart_ecran*2+1)-2,bg="white")
    canevas.place(x=0,y=0)
    canevas.create_image(240,240,image=SG.textsheet)
    canevas.create_text(240,100,text="Welcome in Escape!",fill="Black", font=1500)
    canevas.create_text(240,180,text="Move with the arrows",fill="Black", font=1500)
    canevas.create_text(240,210,text="Whip with the space bar",fill="Black", font=1500)
    canevas.create_text(240,240,text="Pause with Esc",fill="Black", font=1500)
    canevas.create_text(240,270,text="Find the key, and Escape!",fill="Black", font=1500)
    if diff==1:
        button1=Button(fenetre, text="GO!", command=launchEasyGame,image=SG.button,compound=CENTER,bd=0,highlightthickness=0,fg='White')
    elif diff==2:
        button1=Button(fenetre, text="GO!", command=launchMediumGame,image=SG.button,compound=CENTER,bd=0,highlightthickness=0,fg='White')
    else:
        button1=Button(fenetre, text="GO!", command=launchHardGame,image=SG.button,compound=CENTER,bd=0,highlightthickness=0,fg='White')
    button1.place(x=6*32,y=300)
    button2=Button(fenetre, text="Return to Main", command=displayMainMenu,image=SG.button,compound=CENTER,bd=0,highlightthickness=0,fg='White')
    button2.place(x=6*32,y=340)

def launchEasyGame():
    canevas.delete(ALL)
    createNewGame(1)
def launchMediumGame():
    canevas.delete(ALL)
    createNewGame(2)
def launchHardGame():
    canevas.delete(ALL)
    createNewGame(3)

#Cree une nouvelle partie
def createNewGame(diff):
    global nbMonsters,height,width,matrice,gameMode
    gameMode=diff
    nbMonsters=2*diff
    height=50*diff
    width=50*diff
    matrice=creerLabyrinthe(width,height,nbMonsters)
    runGame()

#Lance le jeu et l'affiche
def runGame():
    global matrice,gameInProgress,gamePaused,doorReached,charKilled,canevas
    emptyMainWindow(canevas)
    gameInProgress=True
    gamePaused=False
    doorReached=False
    charKilled=False
    while(gameInProgress):
        canevas.after(1)
        canevas.update()
        canevas.delete(ALL)
        draw(canevas)

    if gamePaused:
        displayPauseMenu()
    if doorReached:
        displayVictoryScreen()
    if charKilled:
        displayDeathScreen()

#Menu de pause
def displayPauseMenu():
    label1=Label(fenetre,image=SG.pause,bd=-2)
    label1.place(x=161,y=97)
    button1=Button(fenetre, text="Resume" ,command=runGame ,image=SG.button,compound=CENTER,bd=0,fg='White',highlightthickness=0)
    button1.place(x=6*32,y=4*32)
    button2=Button(fenetre, text="New Game", command=displayMainMenu,image=SG.button,compound=CENTER,bd=0,fg='White',highlightthickness=0)
    button2.place(x=6*32,y=6*32)
    button3=Button(fenetre, text="Quit", command=exitApplication,image=SG.button,compound=CENTER,bd=0,fg='White',highlightthickness=0)
    button3.place(x=6*32,y=8*32)

#Ecran de victoire
def displayVictoryScreen():
    global timerSecond,rank
    canevas.delete(ALL)
    canevas.create_image(240,240,image=SG.textsheet)
    canevas.create_text(240,240,text="You escaped in %02d:%02d" % (timerSecond/60 , timerSecond%60)+" !",fill="Black",font=1500)
    canevas.update()
    canevas.after(5000)
    rank=isHighScore(gameMode,timerSecond)
    if rank>0:
        displayEnterName()
    else:
        displayMainMenu()

#Ecran de defaite
def displayDeathScreen():
    canevas.delete(ALL)
    canevas.create_image(240,240,image=SG.textsheet)
    canevas.create_text(240,225,text="The demon devoured your flesh",fill="Black", font=1500)
    canevas.create_text(240,245,text="and your soul is now wandering in the limbos...",fill="Black", font=1500)
    canevas.update()
    canevas.after(5000)
    displayMainMenu()

#Ecran de selection du tag
def displayEnterName():
    global letter,button
    canevas.delete(ALL)
    canevas.create_image(240,240,image=SG.textsheet)
    canevas.create_text(240,225,text="Enter your Pseudo :",fill="Black", font=1500)
    button=[0,0,0]
    letter=[0,0,0]
    button[0]=Button(fenetre, text="A" ,command=changeLetter1,compound=CENTER,bd=0,highlightthickness=0,font=1000)
    button[0].place(x=210,y=240)
    button[1]=Button(fenetre, text="A", command=changeLetter2,compound=CENTER,bd=0,highlightthickness=0,font=1000)
    button[1].place(x=230,y=240)
    button[2]=Button(fenetre, text="A", command=changeLetter3,compound=CENTER,bd=0,highlightthickness=0,font=1000)
    button[2].place(x=250,y=240)
    button4=Button(fenetre, text="Submit", command=submitNewScore,image=SG.button,compound=CENTER,bd=0,highlightthickness=0,fg='White')
    button4.place(x=6*32,y=270)

def changeLetter1():
    changeLetter(0)
def changeLetter2():
    changeLetter(1)
def changeLetter3():
    changeLetter(2)

#Change la lettre selectionnee
def changeLetter(order):
    global letter,button
    char=letter[order]
    char+=1
    if char>=26:
        char=0
    button[order]["text"]=alphabet[char]
    letter[order]=char

#Enregistre le nouveau score dans les fichiers de score
def submitNewScore():
    global gameMode,timerSecond,letter
    name=alphabet[letter[0]]+alphabet[letter[1]]+alphabet[letter[2]]
    submitScore(gameMode,name,timerSecond)
    displayScoreboard(gameMode)

#Menu de selection de l'ecran des highscores
def displayChooseScore():
    emptyMainWindow()
    title=Label(fenetre,image=SG.title,bd=-2)
    title.place(x=0,y=0)
    border1=Label(fenetre,image=SG.border,bd=-2)
    border1.place(x=0,y=4*32)
    border2=Label(fenetre,image=SG.border,bd=-2)
    border2.place(x=9*32,y=4*32)
    line1=Label(fenetre,image=SG.line,bd=-2)
    line1.place(x=6*32,y=4*32)
    line2=Label(fenetre,image=SG.line,bd=-2)
    line2.place(x=6*32,y=6*32)
    line3=Label(fenetre,image=SG.line,bd=-2)
    line3.place(x=6*32,y=8*32)
    line4=Label(fenetre,image=SG.line,bd=-2)
    line4.place(x=6*32,y=10*32)
    line5=Label(fenetre,image=SG.line,bd=-2)
    line5.place(x=6*32,y=11*32)
    line6=Label(fenetre,image=SG.line,bd=-2)
    line6.place(x=6*32,y=12*32)
    line7=Label(fenetre,image=SG.line,bd=-2)
    line7.place(x=6*32,y=13*32)
    line8=Label(fenetre,image=SG.line,bd=-2)
    line8.place(x=6*32,y=14*32)
    button1=Button(fenetre, text="Easy" ,command=setEasyScore ,image=SG.button,compound=CENTER,bd=0,fg='White',highlightthickness=0)
    button1.place(x=6*32,y=5*32)
    button2=Button(fenetre, text="Medium", command=setMediumScore,image=SG.button,compound=CENTER,bd=0,fg='White',highlightthickness=0)
    button2.place(x=6*32,y=7*32)
    button3=Button(fenetre, text="Hard", command=setHardScore,image=SG.button,compound=CENTER,bd=0,fg='White',highlightthickness=0)
    button3.place(x=6*32,y=9*32)

def setEasyScore():
    global canevas
    canevas = Canvas(fenetre, width = resolution*(ecart_ecran*2+1)-2, height = resolution*(ecart_ecran*2+1)-2,bg="white")
    canevas.place(x=0,y=0)
    displayScoreboard(1)

def setMediumScore():
    global canevas
    canevas = Canvas(fenetre, width = resolution*(ecart_ecran*2+1)-2, height = resolution*(ecart_ecran*2+1)-2,bg="white")
    canevas.place(x=0,y=0)
    displayScoreboard(2)

def setHardScore():
    global canevas
    canevas = Canvas(fenetre, width = resolution*(ecart_ecran*2+1)-2, height = resolution*(ecart_ecran*2+1)-2,bg="white")
    canevas.place(x=0,y=0)
    displayScoreboard(3)

#Tableau des highscores
def displayScoreboard(gameMode):
    emptyMainWindow(canevas)
    canevas.delete(ALL)
    canevas.create_image(240,240,image=SG.textsheet)
    scoreBoard=readScore(gameMode)
    if gameMode==1:
        head="EASY HIGHSCORES"
    elif gameMode==2:
        head="MEDIUM HIGHSCORES"
    else:
        head="HARD HIGHSCORES"
    canevas.create_text(240,100,text=head,fill="Black", font=1500)
    for player in range(10):
        canevas.create_text(240,140+20*player,text=scoreBoard[player][0]+"      %02d:%02d" % (scoreBoard[player][1]/60 , scoreBoard[player][1]%60),fill="Black", font=1500)
    button=Button(fenetre, text="Back to Main", command=displayMainMenu,image=SG.button,compound=CENTER,bd=0,highlightthickness=0,fg='White')
    button.place(x=6*32,y=350)

#Traitement des entrees clavier
fenetre.bind_all("<KeyPress>",keypress)
fenetre.bind_all("<KeyRelease>",keyrelease)


displayMainMenu()
fenetre.mainloop()

