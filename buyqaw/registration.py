import time


class Request:
    def __init__(self, data):
        self.type = ""
        self.user = {"id": "", "year": 1900, "month": 0, "day": 0, "age": 0, "status": "", "origin": ""}
        self.doors = []



class Newdoor:
    def __init__(self, data, days=365):
        # Request from admin`s page is: x/a4:b4:fc:se;Name;
        data = data.split(";")
        self.days = days
        self.id = data[0][2::]
        self.name = data[1]
        self.password = "060593"
        self.ttl = time.time() + self.days*86400



def registration(data):
    type = data[2]
    msg = data.split(";")
    print(msg)



registration('r/o;56303h43;930423;[{name: "Зеленый Квартал", id: "Some ID", enter: [{name: "1A"}]}];BIClients')