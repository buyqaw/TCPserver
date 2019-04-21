#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Bauyrzhan Ospan"
__copyright__ = "Copyright 2019, Buyqaw LLP"
__version__ = "1.0.1"
__maintainer__ = "Bauyrzhan Ospan"
__email__ = "bospan@cleverest.tech"
__status__ = "Development"


# import socket programming library
import socket

# import thread module
from _thread import *
import threading

# import module to parse json
import json

# import datetime to deal with timestamps
from datetime import datetime


# global variables
print_lock = threading.Lock()

# classes

# class to deal with new user
class Newuser:
    def __init__(self, data):
        # Request from mobile app:
        # r/o;56303h43;930423;[{"name": "Зеленый Квартал", "id": "Some ID", "enter": [{"name": "1A"}]}];BIClients
        self.type = data[2]
        self.data = data.split(";")
        self.id = self.data[1]
        self.origin = self.data[-1]
        self.day = int(self.data[2][4:6])
        self.month = int(self.data[2][2:4])
        self.year, self.age = self.defineage()
        self.doors = json.loads(self.data[3])
        self.givepass()
        self.output = "r/" + self.type + ";" + self.id + ";" + \
                      str(self.year)[-2:] + str(self.month) + \
                      str(self.day) + ";" + str(self.doors) + \
                      ";" + str(self.origin)

    def defineage(self): # Определить возраст человека
        iin = self.data[2]
        year = iin[0:2]
        now = datetime.now()
        if int(year) <= int(str(now.year)[-2:]):
            prefix = "20"
        else:
            prefix = "19"
        year = int(prefix + year)
        birthdate = datetime.strptime(str(self.day) + str(self.month) + str(year), '%d%m%Y')
        age = now.year - birthdate.year - ((now.month, now.day) < (birthdate.month, birthdate.day))
        return year, age

    def givepass(self):
        for i in range(len(self.doors)):
            for j in range(len(self.doors[i]["enter"])):
                self.doors[i]["enter"][j]["key"], self.doors[i]["enter"][j]["ttl"] = \
                    doorbyid(self.doors[i]["id"], self.doors[i]["enter"][j]["name"])
    # TODO: save users in users.json



# class to deal with new door
class Newdoor:
    def __init__(self, data, days=365):
        # Request from admin`s page is: x/a4:b4:fc:se;Name;
        data = data.split(";")
        self.days = days
        self.id = data[0][2::]
        self.name = data[1]
        self.password = "060593"
        self.ttl = datetime.now().second + self.days*86400


# function to find door by id and name
# will be replaced by mongodb client
def doorbyid(id, name):
    with open('doors.json', 'r') as f:
        buildings = json.load(f)
    for building in buildings:
        if building["id"] == id:
            ourbuilding = building
            break
    for door in ourbuilding["enter"]:
        if door["name"] == name:
            password = door["key"]
            ttl = door["ttl"]
    return password, ttl


# thread function
def threaded(c):
    while True:

        # data received from client
        data = c.recv(50000).decode('utf-8')
        if not data:
            print('Bye')

            # lock released on exit
            print_lock.release()
            break

        control = data[0]


        # # reverse the given string from client
        # data = data[::-1]
        #
        # # send back reversed string to client
        # c.send(data)

        # connection closed
    c.close()


def Main():
    host = "0.0.0.0"

    # reverse a port on your computer
    # in our case it is 12345 but it
    # can be anything
    port = 7777
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    print("socket binded to post", port)

    # put the socket into listening mode
    s.listen(50)
    print("socket is listening")

    # a forever loop until client wants to exit
    while True:
        # establish connection with client
        c, addr = s.accept()

        # lock acquired by client
        print_lock.acquire()
        print('Connected to :', addr[0], ':', addr[1])

        # Start a new thread and return its identifier
        start_new_thread(threaded, (c,))
    s.close()


if __name__ == '__main__':
    Arman = Newuser('r/o;56303h43;930423;[{"name": "Зеленый Квартал", "id": "555444333", "enter": [{"name": "1A"}]}];BIClients')
    print(Arman.output)
