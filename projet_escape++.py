from Tkinter import *
import random
import pygame
from SprManaging import *

pygame.mixer.init()
pygame.mixer.music.load("Soundtrack.ogg")
pygame.mixer.music.set_volume(0.7)
pygame.mixer.music.play(-1)

#Sortie du programme
def exitApplication():
    fenetre.destroy()
    pygame.mixer.music.stop()

#Creation fenetre
fenetre = Tk()
fenetre.protocol("WM_DELETE_WINDOW", exitApplication)
fenetre.geometry("%dx%d%+d%+d" % (480,480,(fenetre.winfo_screenwidth()-480)//2,(fenetre.winfo_screenheight()-480)//2))

#Creation d'un canevas

resolution=32
ecart_ecran=7
mobSpeed=3
quit=False
z=0
q=0
s=0
d=0
mobSpawnZone=[[3],[2,4],[1,3,5]]
whipping=0
whipTimer=0
X=1
Y=0

timerMinute=2
timerSecond=34

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
# 23: Personnage regard vers le bas fouettant
# 24: Personnage regard vers la gauche fouettant
# 25: Personnage regard vers la droite fouettant
# 26: Personnage regard vers le haut fouettant
# 27: Monstre regard vers le bas au-dessus d'un mur
# 28: Monstre regard vers la gauche au-dessus d'un mur
# 29: Monstre regard vers la droite au-dessus d'un mur
# 30: Monstre regard vers le haut au-dessus d'un mur

loadSprites()

#Génération d'une matrice labyrinthique de dimensions widthxheight
def creerLabyrinthe(width,height,nbMonsters):
    global charPos,charVel,look,mobPos,mobVel,deadMob,seen,mobLook,mobTimer,matrice
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

    l=[]
    #Placement aleatoire de la porte
    for loop in range(2,width-3):
        if isBlockEmpty(loop,2):
            l.append([1,loop])
    for loop in range(2,height-3):
        if isBlockEmpty(width-3,loop):
            l.append([loop,width-2])
    alea2=random.randint(0,len(l)-1)
    matrice[l[alea2][Y]][l[alea2][X]]=2
    if l[alea2][Y]<2:
        matrice[l[alea2][Y]-1][l[alea2][X]]=1
    else:
        matrice[l[alea2][Y]][l[alea2][X]+1]=1
    #Placement du personnage, que l'on informe dans la liste CharPos[y,x] et initialisation de sa vitesse CharVel[y,x]
    matrice[height-3][2]=3
    charPos=[height-3,2]
    charVel=[0,0]
    look=3
    #Apparition des monstres
    possible=[]
    mobPos=[]
    mobVel=[]
    for loop in range(nbMonsters):
        for j in range(mobSpawnZone[nbMonsters-1][loop]*height/8,(mobSpawnZone[nbMonsters-1][loop]+2)*height/8):
            for i in range(mobSpawnZone[nbMonsters-1][loop]*width/8,(mobSpawnZone[nbMonsters-1][loop]+2)*width/8):
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
    return matrice

def mobManagement(mobID):
    global mobVel,mobPos,matrice,mobLook,mobTimer,seen
    if isBlockWhip(mobPos[mobID][X],mobPos[mobID][Y]):
        deadMob[mobID]=1
        mobPos[mobID]=[0,0]
    if deadMob[mobID]==0:
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
        else:
            xDiff=charPos[X]-mobPos[mobID][X]
            yDiff=charPos[Y]-mobPos[mobID][Y]
            if abs(xDiff)>abs(yDiff) and xDiff!=0:
                mobVel[mobID]=[0,xDiff/abs(xDiff)]
            elif yDiff!=0:
                mobVel[mobID]=[yDiff/abs(yDiff),0]
            if not isBlockFlyable(mobPos[mobID][X]+mobVel[mobID][X],mobPos[mobID][Y]+mobVel[mobID][Y]):
                mobVelCopy=mobVel
                if xDiff==0 or yDiff==0:
                    mobVel[mobID][X]=mobVelCopy[mobID][Y]
                    mobVel[mobID][Y]=mobVelCopy[mobID][X]
                else:
                    mobVel[mobID][X]=abs(mobVelCopy[mobID][Y])*xDiff/abs(xDiff)
                    mobVel[mobID][Y]=abs(mobVelCopy[mobID][X])*yDiff/abs(yDiff)

        if mobTimer[mobID]>=mobSpeed and isBlockFlyable(mobPos[mobID][X]+mobVel[mobID][X],mobPos[mobID][Y]+mobVel[mobID][Y]):
            mobTimer[mobID]=1
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
        else:
            mobTimer[mobID]+=1

        if charPos[Y]-5<=mobPos[mobID][Y] and charPos[Y]+5>=mobPos[mobID][Y] and charPos[X]-5<=mobPos[mobID][X] and charPos[X]+5>=mobPos[mobID][X]:
            seen[mobID]=1

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
    if x==1 :
        canevas.create_image(i2*resolution+17,j2*resolution+17,image=SG.floor) #Sol
    elif x==0 :
        canevas.create_image(i2*resolution+17,j2*resolution+17,image=SG.wall) #Mur
    elif x==2 :
        canevas.create_image(i2*resolution+17,j2*resolution+17,image=SG.door) #Porte
    elif x==3 :
        canevas.create_image(i2*resolution+17,j2*resolution+17,image=SG.charD) #Personnage vers le bas
    elif x==4 :
        canevas.create_image(i2*resolution+17,j2*resolution+17,image=SG.charL) #Personnage vers la gauche
    elif x==5 :
        canevas.create_image(i2*resolution+17,j2*resolution+17,image=SG.charR) #Personnage vers la droite
    elif x==6 :
        canevas.create_image(i2*resolution+17,j2*resolution+17,image=SG.charU) #Personnage vers le haut
    elif x==7 :
        canevas.create_image(i2*resolution+17,j2*resolution+17,image=SG.mobD) #Monstre vers le bas
    elif x==8 :
        canevas.create_image(i2*resolution+17,j2*resolution+17,image=SG.mobL) #Monstre vers la gauche
    elif x==9 :
        canevas.create_image(i2*resolution+17,j2*resolution+17,image=SG.mobR) #Monstre vers la droite
    elif x==10 :
        canevas.create_image(i2*resolution+17,j2*resolution+17,image=SG.mobU) #Monstre vers le haut
    elif x==11 :
        canevas.create_image(i2*resolution+17,j2*resolution+17,image=SG.whipD) #Fouet droit vers le bas
    elif x==12 or x==13:
        canevas.create_image(i2*resolution+17,j2*resolution+17,image=SG.whipH) #Fouet droit horizontal
    elif x==14 :
        canevas.create_image(i2*resolution+17,j2*resolution+17,image=SG.whipU) #Fouet droit vers le haut
    elif x==15 :
        canevas.create_image(i2*resolution+17,j2*resolution+17,image=SG.whipEndD) #Fin du fouet vers le bas
    elif x==16 :
        canevas.create_image(i2*resolution+17,j2*resolution+17,image=SG.whipEndL) #Fin du fouet vers la gauche
    elif x==17 :
        canevas.create_image(i2*resolution+17,j2*resolution+17,image=SG.whipEndR) #Fin du fouet vers la droite
    elif x==18 :
        canevas.create_image(i2*resolution+17,j2*resolution+17,image=SG.whipEndU) #Fin du fouet vers le haut
    elif x==23 :
        canevas.create_image(i2*resolution+17,j2*resolution+17,image=SG.charDW) #Personnage vers le bas fouettant
    elif x==24 :
        canevas.create_image(i2*resolution+17,j2*resolution+17,image=SG.charLW) #Personnage vers la gauche fouettant
    elif x==25 :
        canevas.create_image(i2*resolution+17,j2*resolution+17,image=SG.charRW) #Personnage vers la droite fouettant
    elif x==26 :
        canevas.create_image(i2*resolution+17,j2*resolution+17,image=SG.charUW) #Personnage vers le haut fouettant
    elif x==27 :
        canevas.create_image(i2*resolution+17,j2*resolution+17,image=SG.mobDW) #Monstre vers le bas au-dessus d'un mur
    elif x==28 :
        canevas.create_image(i2*resolution+17,j2*resolution+17,image=SG.mobLW) #Monstre vers la gauche au-dessus d'un mur
    elif x==29 :
        canevas.create_image(i2*resolution+17,j2*resolution+17,image=SG.mobRW) #Monstre vers la droite au-dessus d'un mur
    elif x==30 :
        canevas.create_image(i2*resolution+17,j2*resolution+17,image=SG.mobUW) #Monstre vers le haut au-dessus d'un mur



#Si une touche est enfoncée
def keydown(event):
    key=event.keysym
    global charVel,z,q,s,d,whipping,gameInProgress,gamePaused
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
        whipping=1
        charVel=[0,0]
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



#Dessin du canevas de jeu
def draw(canevas):
    global matrice,charPos,charVel,mobPos,mobVel,mobTimer,look,gameInProgress,doorReached,charKilled
    # si le personnage est sur la porte
    if matrice[charPos[Y]+charVel[Y]][charPos[X]+charVel[X]]==2:
        gameInProgress=0
        doorReached=1
    else:
        #Si la nouvelle position du personnage est un bloc de sol
        if isBlockOnFloor(charPos[X]+charVel[X],charPos[Y]+charVel[Y]):
            #On le deplace dans la matrice
            matrice[charPos[Y]][charPos[X]]=1
            #On informe la variable "CharPos" de sa nouvelle position
            charPos[X]+=charVel[X]
            charPos[Y]+=charVel[Y]
            #La variable look informe le regard du personnage en fonction de son dernier deplacement
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

            if not isBlockOnFloor(xposition,yposition) and endedwhip==0:
                endedwhip=1
            elif endedwhip==0:
                matrice[charPos[Y]][charPos[X]]=look+20
                if (isBlockOnFloor(xposition2,yposition2)) and loop<2:
                    matrice[yposition][xposition]=look+8
                else:
                    matrice[yposition][xposition]=look+12
                    endedwhip=1
        whipTimer+=1
        if whipTimer>=10:
            whipping=0
            whipTimer=0
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

def displayMainMenu():
    emptyMainWindow()
    label1=Label(fenetre,image=SG.title,bd=-2)
    label1.place(x=0,y=0)
    label2=Label(fenetre,image=SG.border,bd=-2)
    label2.place(x=0,y=4*32)
    label3=Label(fenetre,image=SG.border,bd=-2)
    label3.place(x=9*32,y=4*32)
    label4=Label(fenetre,image=SG.line,bd=-2)
    label4.place(x=6*32,y=5*32)
    label5=Label(fenetre,image=SG.line,bd=-2)
    label5.place(x=6*32,y=7*32)
    label6=Label(fenetre,image=SG.bottom,bd=-2)
    label6.place(x=6*32,y=9*32)
    button1=Button(fenetre, text="Easy" ,command=setEasyGame ,image=SG.button,compound=CENTER,bd=0,fg='White',highlightthickness=0)
    button1.place(x=6*32,y=4*32)
    button2=Button(fenetre, text="Medium", command=setMediumGame,image=SG.button,compound=CENTER,bd=0,fg='White',highlightthickness=0)
    button2.place(x=6*32,y=6*32)
    button3=Button(fenetre, text="Hard", command=setHardGame,image=SG.button,compound=CENTER,bd=0,fg='White',highlightthickness=0)
    button3.place(x=6*32,y=8*32)

def setEasyGame():
    createNewGame(1)
def setMediumGame():
    createNewGame(2)
def setHardGame():
    createNewGame(3)

def createNewGame(diff):
    global nbMonsters,height,width,matrice,canevas
    nbMonsters=diff
    height=50*diff
    width=50*diff
    matrice=creerLabyrinthe(width,height,nbMonsters)
    canevas = Canvas(fenetre, width = resolution*(ecart_ecran*2+1)-2, height = resolution*(ecart_ecran*2+1)-2,bg="white")
    canevas.place(x=0,y=0)
    runGame()

def runGame():
    global matrice,gameInProgress,gamePaused,doorReached,charKilled,canevas
    emptyMainWindow(canevas)
    gameInProgress=True
    gamePaused=False
    doorReached=False
    charKilled=False
    while(gameInProgress):
        canevas.after(75)
        canevas.update()
        canevas.delete(ALL)
        draw(canevas)
    if gamePaused:
        displayPauseMenu()
    if doorReached:
        displayVictoryScreen()
    if charKilled:
        displayDeathScreen()

def displayPauseMenu():
    button1=Button(fenetre, text="Resume" ,command=runGame ,image=SG.button,compound=CENTER,bd=0,fg='White',highlightthickness=0)
    button1.place(x=6*32,y=4*32)
    button2=Button(fenetre, text="New Game", command=displayMainMenu,image=SG.button,compound=CENTER,bd=0,fg='White',highlightthickness=0)
    button2.place(x=6*32,y=6*32)
    button3=Button(fenetre, text="Quit", command=exitApplication,image=SG.button,compound=CENTER,bd=0,fg='White',highlightthickness=0)
    button3.place(x=6*32,y=8*32)

def displayVictoryScreen():
    canevas.delete(ALL)
    canevas.create_image(240,240,image=SG.textsheet)
    canevas.create_text(240,240,text="You escaped in "+str(timerMinute)+":"+str(timerSecond)+" !",fill="Black",font=1500)
    canevas.update()
    canevas.after(5000)
    displayMainMenu()

def displayDeathScreen():
    canevas.delete(ALL)
    canevas.create_image(240,240,image=SG.textsheet)
    canevas.create_text(235,225,text="The demon devoured your flesh",fill="Black", font=1500)
    canevas.create_text(235,245,text="and your soul is now wandering in the limbos...",fill="Black", font=1500)
    canevas.update()
    canevas.after(5000)
    displayMainMenu()


#Traitement des entrees clavier
fenetre.bind_all("<KeyPress>",keydown)
fenetre.bind_all("<KeyRelease>",keyrelease)


displayMainMenu()
fenetre.mainloop()

