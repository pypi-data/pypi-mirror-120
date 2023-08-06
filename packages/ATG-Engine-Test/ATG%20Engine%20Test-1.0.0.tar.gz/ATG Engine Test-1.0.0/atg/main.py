textCPS = 2

import time
from inspect import signature

def slowprint(text, cps = textCPS, color = "white") :
    black = "\033[0;30m"
    purple = "\033[0;35m"
    blue = "\033[0;34m"
    green = "\033[0;32m"
    red = "\033[0;31m"
    yellow = "\033[0;33m"
    white = "\033[0;37m"
    cps = 1/cps
    if color == "white" :
        print(white)
    if color == "blue" :
        print(blue)
    if color == "black" :
        print(black)
    if color == "purple" :
        print(purple)
    if color == "green" :
        print(green)
    if color == "red" :
        print(red)
    if color == "yellow" :
        print(yellow)
    for i in text:
        print(i, end="")
        time.sleep(cps)

def chngCPS(newCPS):
    global textCPS
    textCPS = newCPS

class Object():
    def __init__(self, name):
        self.name = name
        self.value = name

class WeaponSource(Object):
    def __init__(self):
        pass
class Weapon(Object):
    def __init__(self, name, dmg, owner, exhaustible = False, source = None):
        self.name = name
        self.value = name
        self.damage = damage
        self.owner = owner
        self.exhaustible = exhaustible
        if self.exhaustible:
            self.source = source
        
    def destroy(self):
        slowprint(self.value + " got destroyed", color = "green")
        
    def addDamage(self, dmg):
        self.damage += dmg

    def subDamage(self, dmg):
        self.damage -= dmg

    def chngDamage(self, dmg):
        self.damage = dmg
    
    def use(self, attacker, prey):
        if self.exhaustible:
            if not attacker.findInv(self.source):
                slowprint("No source available for " + self.value, color = "red")
class Enemy():
    def __init__(self, name, dmg, health, enType = ""):
        self.name = name
        self.value = name
        self.damage = dmg
        self.health = health
        if enType == "":
           self.enType = name
        else:
            self.enType = enType
    
    def addHealth(self, health):
        self.health += health
        
    def subHealth(self, health):
        self.health -= health
    
    def chngHealth(self, health):
        self.health = health
    
    def addDamage(self, dmg):
        self.damage += dmg
        
    def subDamage(self, dmg):
        self.damage -= dmg
    
    def chngDamage(self, dmg):
        self.damage = dmg
        
    def kill(self):
        slowprint(self.name + " was killed.", color = "green")
        del(self)
    
    def killPlyr(self, plyr):
        slowprint(plyr.name + " was killed by " + self.enType + ".", config.textCPS, color = "red")
        plyr.health = 0

class Room():
    def __init__(self, enemies, teleports, events):
        self.enemies = enemies
        self.teleports = teleports
        self.events = events
        
    def runEvent(self, index, parameters):
        sig = signature(self.events[index])
        params = sig.parameters
        paramlen = len(params)
        while len(parameters) > paramlen:
            parameters.pop()
        self.events[index](*parameters)
    
    def teleport(self, index, newRoomVar):
        newRoomVar = self.teleports[index]
        return
        
class Inventory():
    inv = []
    def __init__(self, limit):
        self.limit = limit
        
    def addInv(self, obj):
        if self.limit > len(self.inv):
            self.inv.append(obj.value)
        else:
            slowprint("Inventory is full", 5, "red")
    
    def delInv(self, obj, plyr):
        for i in range(0, len(self.inv)):
            if self.inv[i] == obj.value:
                self.inv.pop(i)
                return
        
        slowprint("Object '" + obj.value + "' doesn't exist in the inventory of " + plyr.name + ".", 20, "red")

class Player():
    def __init__(self, name, health, willpower):
        self.name = name
        self.health = health
        self.willpower = willpower
        self.invMake()
    
    def chngHealth(self, newHealth):
        self.health = newHealth
        
    def addHealth(self, health):
        self.health += health
    
    def subHealth(self, health):
        self.health -= health
    
    def chngName(newName):
        self.name = newName
    
    def addWill(self, will):
        self.willpower += will
    
    def subWill(self, will):
        self.willpower -= will
        
    def invMake(self, starters = []) :
        self.inventory = Inventory(10)
        self.inv = self.inventory.inv
    
    def retInv(self):
        return self.inventory.inv
    
    def addInv(self, obj):
        self.inventory.addInv(obj = obj)
        self.inv = self.inventory.inv
    
    def delInv(self, obj):
        self.inventory.delInv(obj = obj, plyr = self)
        self.inv = self.inventory
    
    def findInv(self, obj):
        j = 0
        for i in self.inv:
            if i.value == obj.value:
                return j
            j+=1
        return False

def dialogue(plyr, text, color = "white"):
    global textCPS
    refText = plyr.name + " : " + text
    refText = refText.upper()
    slowprint(refText, textCPS, color)

def narrate(text, expression = "statement"):
    global textCPS
    if expression == "statement":
        slowprint(text, textCPS, "white")
    elif expression == "expression":
        slowprint("*" + text + "*", textCPS, color = "purple")
        
def ynQuestion(question, assumption = False, assumptionText = ""):
    global textCPS
    narrate(question + "[y/n] : ")
    answer = input()
    if answer not in ["yes", "y", "n", "no"]:
        if assumption == False:
            slowprint("Invalid option!", color = "red")
            return ynQuestion(question = question, options = options)
        slowprint(assumptionText)
        return "assumption"
    answer = answer.lower()
    if answer in ['yes', 'y']:
        return True
    return False

def multiChoiceQ(question, options, assumption = False, assumptionText = ""):
    global textCPS
    narrate(question + '\n')
    for i in range(0, len(options)):
        slowprint("    [" + str(i + 1) + "]. " + options[i], textCPS, color = "yellow")
    print('\n' + "\033[0;37m" + "    Answer : ", end="")
    optionsLower = []
    for i in range(0, len(options)):
        optionsLower.append(options[i].lower())
    answer = input()
    try:
        answer = int(answer)
    except:
        pass
    try:
        assumptions = 0 < answer <= len(options)
    except:
        assumptions = answer in optionsLower
        if not assumptions:
            assumptions = answer in options
    if not assumptions:
        if assumption == False:
            slowprint("Invalid option!", color = "red")
            return multiChoiceQ(question = question, options = options)
        slowprint(assumptionText)
        return "assumption"
    for i in range(0, len(options)):
        if answer.lower() in optionsLower[i] or answer in str(i):
            return i+1

def ndefstrQ(question):
    global textCPS
    narrate(question + " : ")
    answer = input()
    return answer.lower()