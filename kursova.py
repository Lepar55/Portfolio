from main import Sunrise
from main import Eagles
import sqlite3

class Data:
    def __init__(self,base_file):
        self.conn = sqlite3.connect(base_file)
        self.cursor = self.conn.cursor()

    def add_sunrise(self,sunrise):
        self.cursor.execute("INSERT INTO Sunrise(id,name,city,humanitarian) VALUES(?,?,?,?)",
                            (sunrise.id,  sunrise.name, sunrise.city, sunrise.hum))
    def add_eagles(self,eagles):
        self.cursor.execute("INSERT INTO EaglesGroup(id,name,city,humanitarian) VALUES(?,?,?,?)",
                            (eagles.id, eagles.name, eagles.city, eagles.hum))
    def watch_sunrise(self):
        self.cursor.execute("SELECT * FROM Sunrise")
        return self.cursor.fetchall()
    def watch_eagles(self):
        self.cursor.execute ("SELECT * FROM EaglesGroup")
        return self.cursor.fetchall()

class Ui:
    def __init__(self,base):
        self.base = Data(base)
    def add_sunrise(self):
        s_id = int(input("Введіть id волонтера 2: \n"))
        s_name = str(input("Введіть ім'я волонтера: \n"))
        s_city = str(input("Введіть місто куди прямує волонтер: \n"))
        s_hum = str(input("Введіть яку гуманітарну допомогу везе волонтер: \n"))
        sunrise = Sunrise(s_id, s_name, s_city, s_hum)
        self.base.add_sunrise(sunrise)

    def add_eagles(self):
        e_id = int(input("Введіть id волонтера 1: \n"))
        e_name = str(input("Введіть ім'я волонтера: \n"))
        e_city = str(input("Введіть місто куди прямує волонтер: \n"))
        e_hum = str(input("Введіть яку гуманітарну допомогу везе волонтер: \n"))
        eagles = Eagles(e_id, e_name, e_city, e_hum)
        self.base.add_eagles(eagles)
    def watch_all_sunrise(self):
        sunrises =self.base.watch_sunrise()
        for sunrise in sunrises:
            print(sunrise)


    def watch_all_eagles(self):
        eagles =self.base.watch_eagles()
        for eagle in eagles:
            print(eagle)
    def close (self):
        self.base.cursor.close()

intarface = Ui("D:\kirs\wolunteers.db")
o = True
def choose ():
    while o==True:
        x = input("Якщо ви хочете переглянути дані введіть 1\nЯкщо ви хочете ввести дані введіть 2\nЯкщо ви хочете вийти введіть 3\n")
        match x :

            case"1":
                y = input("Якщо ви хочете переглянути дані волонтерської групи Sunrise введіть 1 \nЯкщо ви хочете переглянути дані волонтерської групи введіть 2 \nЯкщо ви хочете вийти введіть 3\n")
                match y :
                    case "1":
                     print("Ви вибрали групу Sunrise , введіть дані\n")
                     intarface.watch_all_sunrise()

                    case "2":
                     print("Ви вибрали групу EaglesGroup , введіть дані\n")
                     intarface.watch_all_eagles()
                    case"3":
                     intarface.close()
                     break

            case "2":
                while o==True:
                    l = input(
                        "Якщо ви хочете ввести дані волонтерської групи Sunrise введіть 1 \nЯкщо ви хочете ввести дані волонтерської групи введіть 2\nЯкщо ви хочете вийти введіть 3\n")
                    match l :
                        case "1":
                         intarface.add_sunrise()
                         break
                        case"2":
                         intarface.add_eagles()
                         break
                        case "3":
                         intarface.close()
                         break
            case"3":
                break



choose()