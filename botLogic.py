import botBasic as bot
from os.path import exists
import queue
import random as rand
import time
import re
import threading as tr
import json
#--------------------------------
def getNewMessage(user):
    while 1:
        try:
            while bot.newMessage.queue[0].get("user") != user:
                time.sleep(0.1)
                continue
            break
        except IndexError:
            pass
    return bot.newMessage.get()
#--------------------------------
def init(user):
    mainLock = tr.Event()
    with open("technical/data.dat",encoding="utf-8") as file:
        data = json.load(file)

    while 1:
        mainLock.clear()
        messageSave = getNewMessage(user)
        message = messageSave.get("message").lower()
        admin = messageSave.get("admin")
        peer = messageSave.get("peer")

        if user[:3] != '200':
            if message == 'сохранить':
                with open("technical/data.dat","w",encoding="utf-8") as file:
                    json.dump(data,file)
                bot.printMessage("База успешно сохранена",user)
            elif message == 'добавить' or message == 'изменить':
                bot.printMessage("Введите название записи",user)
                name = getNewMessage(user).get("message")
                bot.printMessage("Введите значение записи",user)
                value = getNewMessage(user).get("message")
                if value.isdecimal() or (value[1:].isdecimal() and value[:1] == '-'):
                    value = int(value,10)
                data[name] = value;
                bot.printMessage("Создана запись {}".format(name),user)
            elif message == 'вывести':
                bot.printMessage("Введите название записи",user)
                name = getNewMessage(user).get("message")
                value = data.get(name)
                if value == None:
                    bot.printMessage("Такой записи не существует",user)
                else:
                    bot.printMessage("Значение: {}".format(value),user)
            elif message == 'консоль':
                print(data)

        elif admin != None:
            pass

        else:
            pass

        mainLock.set()
