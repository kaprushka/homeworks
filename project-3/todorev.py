# -*- coding: utf-8 -*-
import re

soglanay = 'цкнгшщзхфвпрлджчсмтб'
glasn = 'йуеоаыяию'

# «Ъ» на конце после согласных
def addTvZnak(word):
    if len(word) <= 0: return word
    if word[-1] in soglanay:
        return word + 'ъ'
    return word

# «и десятеричное»
def addIs(word):
    if len(word) <= 0: return word
    newI = 'и'
    listChI = [] 
    listRus = list(word)
    for i in range(len(listRus)):
        try:
            if listRus[i] == 'и' and listRus[i+1] in glasn:
                listChI.append('i')
            else:
                listChI.append(listRus[i])
        except IndexError:
            listChI.append(listRus[i])
    return ('').join(listChI)

# «без», «через», «чрез» всегда оканчиваются на «з»
def sToZ(word):
    if word[:3] == "бес":
        return "без" + word[3:]
    if word[:4] == "чрес":
        return "чрез" + word[4:]
    if word[:5] == "черес":
        return "через" + word[5:]
    return word


def translateWord(word):
    return addIs(sToZ(addTvZnak(word)))

def translateString(rus_string):
    list = []
    for word in rus_string.split():
        EOS = word[-1]
        if EOS == ':' or EOS == '.' or EOS == ',' or EOS == '!' or EOS == '?':
            str = translateWord(word[:-1]) + EOS
            list.append(str)
        else: list.append(translateWord(word))
    return (" ").join(list)

