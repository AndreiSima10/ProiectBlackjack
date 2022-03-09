import random
import os

class Carte:
    def __init__(self,numeCarte,culoareCarte):
        self.nume = numeCarte
        self.culoare = culoareCarte
        if(self.nume == 'Rege' or self.nume == 'Regina' or self.nume == 'Valet'):
            self.value = 10
        elif(self.nume == 'As'):
            self.value = 1
        else:
            self.value = int(self.nume)
    def getCarte(self):
        return self.nume + " de" + self.culoare
    def getValue(self):
        return self.value
    def getNume(self):
        return self.nume


class unPachet:
    def __init__(self):
        listaCulori = ['Cupa','Pica','Trefla','Carou']
        listaNume = ['As','2','3','4','5','6','7','8','9','10','Valet','Regina','Rege']
        self.Pachet =  list()
        for i in listaCulori:
            for j in listaNume:
                self.Pachet.append(Carte(j,i))

    def amesteca(self):
        random.shuffle(self.Pachet)

    def HitACard(self):
        return self.Pachet.pop(random.randint(0, len(self.Pachet) - 1))


class Jucator:
    def __init__(self,Nume,Prenume,Varsta,Origine,totalJetoane):
        self.nume = Nume
        self.prenume = Prenume
        self.varsta = int(Varsta)
        self.origine = Origine
        self.jetoane = int(totalJetoane)
        self.mana = list()
        self.pariu = 0

    def Hit(self,carte):
        self.mana.append(carte)

    def Pariu(self,sumaDorita):
        if(int(sumaDorita) <= self.jetoane and int(sumaDorita)>0):
            self.jetoane -= int(sumaDorita)
            self.pariu = sumaDorita
        else:
            self.pariu = -1
    def getName(self):
        return self.nume + self.prenume
    def getJetoane(self):
        return self.jetoane
    def addJetoane(self,castig):
        self.jetoane += castig
    def getPariu(self):
        return self.pariu
    def showHand(self):
        print(self.getName())
        for carte in self.mana:
            print(carte.getCarte())
        print('\n')
    def handValue(self):
        suma = 0
        for carte in self.mana:
            suma += carte.getValue()
        return suma
    def hasAce(self):
        for carte in self.mana:
            if (carte.getNume()=="As"):
                return True
        return False


#Creeare dealer
Dealer = Jucator('Sima','Andrei Mihai','20','Romania','9999999')

#Introducerea numarului de jucatori
number_of_players = int(input("Please enter the number of players: "))
while(number_of_players < 1 or number_of_players > 4):
    if(number_of_players > 4):
        print("The maximum number of players accepted for a game of blackjack is 4")
        number_of_players = int(input("Please enter a corret number of players: "))
    if(number_of_players < 0):
        print("The minimum number of players accepted for a game of blackjack is 1")
        number_of_players = int(input("Please enter a corret number of players: "))

#Citirea informatiilor despre jucatori
PlayerList = list()
with open(os.getcwd()+r"\Lista Participanti.txt",mode='rt') as file:
    fileBuffer = file.readlines()
    for i in range(number_of_players):
        lineBuffer = fileBuffer[i].split()
        PlayerList.append(Jucator(lineBuffer[0], lineBuffer[1], lineBuffer[2], lineBuffer[3], lineBuffer[4]))

#for i in range(number_of_players):
#    PlayerList.append(Jucator(lineBuffer[0], lineBuffer[1], lineBuffer[2], lineBuffer[3], lineBuffer[4]))

#Implementarea jocului
Game = 'Y'
while(Game == "Y"):
#Pariul jucatorilor
    for i in range(number_of_players):
        sumaPariata = int(input(PlayerList[i].getName()+' alege numarul de jetoane pe care doresti sa il pariezi: '))
        PlayerList[i].Pariu(sumaPariata)
        while(PlayerList[i].getPariu() == -1):
            if(sumaPariata > PlayerList[i].getJetoane()):
                sumaPariata = int(input('Numarul de jetoane e mai mare decat numarul de jetoane disponibile,va rog introduceti alta suma: '))
                PlayerList[i].Pariu(sumaPariata)
            if (sumaPariata < 25):
                sumaPariata = int(input('Trebuie sa pariati minim 25 de jetoane, va rog introduceti alta suma: '))
                PlayerList[i].Pariu(sumaPariata)
#Pariul dealerului
    Dealer.Pariu(random.randint(25,9999999))
#Amestecarea pachetului
    Pachetul = unPachet()
    Pachetul.amesteca()
#Impartirea cartilor pentru jucatori
    for i in range(number_of_players):
        PlayerList[i].Hit(Pachetul.HitACard())
        PlayerList[i].Hit(Pachetul.HitACard())
        PlayerList[i].showHand()
#Impartirea cartilor dealerului
    Dealer.Hit(Pachetul.HitACard())
    Dealer.showHand()
#Jocul in sine
    for i in range(number_of_players):
        while(PlayerList[i].handValue() < 21):
            HitOrStand = input(PlayerList[i].getName()+" Hit or Stand: ")
            while(HitOrStand!='Hit' and HitOrStand!='Stand'):
                HitOrStand = input("Invalid response, please select Hit or Stand: ")
            if(HitOrStand == 'Hit'):
                PlayerList[i].Hit(Pachetul.HitACard())
                PlayerList[i].showHand()
            elif(HitOrStand == 'Stand'):
                break

    while(Dealer.handValue()<=17):
        Dealer.Hit(Pachetul.HitACard())
        Dealer.showHand()
    if(Dealer.hasAce()):
        if(Dealer.handValue()<=11):
            DealerHand = Dealer.handValue() + 10
        else:
            DealerHand = Dealer.handValue()


#Verificare maini
    for i in range(number_of_players):
        if(PlayerList[i].hasAce()):
            if(PlayerList[i].handValue()<=11):
                PlayerHand = PlayerList[i].handValue() + 10
            else:
                PlayerHand = PlayerList[i].handValue()
        if(PlayerHand <= 21 and (PlayerHand > DealerHand or DealerHand > 21)):
            PlayerList[i].addJetoane(2 * PlayerList[i].getPariu())
            print("Felicitari, "+ PlayerList[i].getName() + ", ai castigat mana!")
        elif(PlayerHand <= 21 and PlayerHand == DealerHand):
            PlayerList[i].addJetoane(PlayerList[i].getPariu())
            print("Remiza")
        else:
            print(PlayerList[i].getName()+", ai pierdut mana")

