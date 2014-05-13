from PIL import Image , ImageTk

# Liste des variables "sprites"
class SG:
    title=None
    textsheet=None
    pause=None
    charD=None
    charL=None
    charU=None
    charR=None
    charDW=None
    charLW=None
    charUW=None
    charRW=None
    wall=None
    floor=None
    door=None
    key=None
    mobD=None
    mobU=None
    mobL=None
    mobR=None
    mobDW=None
    mobUW=None
    mobLW=None
    mobRW=None
    button=None
    border=None
    line=None
    whipD=None
    whipH=None
    whipU=None
    whipEndD=None
    whipEndL=None
    whipEndU=None
    whipEndR=None
    blocks=[]

# Extrait un sprite de la page des sprites, aux coords (x,y) et de taille (width, height)
def cutSprite(sprites,y,x,width,height):
    subSprite = Image.new("RGB", (width,height))
    for i in range(0,width):
        for j in range(0,height):
            pixel=sprites.getpixel((x+i,y+j))
            subSprite.putpixel((i,j),(pixel[0],pixel[1],pixel[2]))
    return ImageTk.PhotoImage(subSprite)

#SG.chargement des sprites
def loadSprites():
    sprites=Image.open(r"Sprites.jpg")
    SG.title=Image.open(r"Title.jpg")
    SG.title = ImageTk.PhotoImage(SG.title)
    background=Image.open(r"Background.jpg")
    SG.textsheet=Image.open(r"TextSheet.jpg")
    SG.textsheet = ImageTk.PhotoImage(SG.textsheet)
    SG.pause=Image.open(r"Pause.jpg")
    SG.pause = ImageTk.PhotoImage(SG.pause)
    #Decoupage de l'image en petites images, avec SG.charD pour SG.character down, soit le personnage vers le bas, etc
    SG.charD = cutSprite(sprites,0,32,32,32)
    SG.charL = cutSprite(sprites,32,32,32,32)
    SG.charR = cutSprite(sprites,64,32,32,32)
    SG.charU = cutSprite(sprites,96,32,32,32)

    SG.charRW = cutSprite(sprites,64,0,32,32)
    SG.charLW = cutSprite(sprites,32,0,32,32)
    SG.charUW = cutSprite(sprites,96,0,32,32)
    SG.charDW = cutSprite(sprites,0,0,32,32)

    SG.wall = cutSprite(sprites,0,64,32,32)
    SG.floor = cutSprite(sprites,0,96,32,32)
    SG.door = cutSprite(sprites,32,64,32,32)
    SG.key = cutSprite(sprites,32,96,32,32)
    SG.button = cutSprite(sprites,64,128,96,32)

    SG.mobD = cutSprite(sprites,64,64,32,32)
    SG.mobL = cutSprite(sprites,96,96,32,32)
    SG.mobR = cutSprite(sprites,96,64,32,32)
    SG.mobU = cutSprite(sprites,64,96,32,32)

    SG.mobDW = cutSprite(sprites,96,128,32,32)
    SG.mobUW = cutSprite(sprites,96,160,32,32)
    SG.mobRW = cutSprite(sprites,96,192,32,32)
    SG.mobLW = cutSprite(sprites,96,224,32,32)

    SG.whipH = cutSprite(sprites,0,160,32,32)
    SG.whipD = cutSprite(sprites,0,192,32,32)
    SG.whipU = cutSprite(sprites,0,128,32,32)

    SG.whipEndU = cutSprite(sprites,32,128,32,32)
    SG.whipEndD = cutSprite(sprites,32,160,32,32)
    SG.whipEndR = cutSprite(sprites,32,192,32,32)
    SG.whipEndL = cutSprite(sprites,32,224,32,32)

    SG.border = cutSprite(background,0,0,192,352)
    SG.line = cutSprite(background,0,0,96,32)
    #Liste ordonnee des blocks, selon leur ID
    SG.blocks = [ SG.wall, SG.floor, SG.door, \
               SG.charD, SG.charL, SG.charR, SG.charU, \
               SG.mobD, SG.mobL, SG.mobR, SG.mobU, \
               SG.whipD, SG.whipH, SG.whipH, SG.whipU, SG.whipEndD, SG.whipEndL, SG.whipEndR, SG.whipEndU, \
               SG.key, 0, 0, 0, SG.charDW, SG.charLW, SG.charRW, SG.charUW, \
               SG.mobDW, SG.mobLW, SG.mobRW, SG.mobUW ]

