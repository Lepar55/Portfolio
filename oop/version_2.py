import sqlite3


conn  = sqlite3.connect("/home/vova/Стільниця/kurso/da.db")

class Animal:
    def __init__(self,id, name,much,dep_numb):
      self.id = id
      self.name = name
      self.much = much
      self.dep_numb =dep_numb
    
      

class Cow(Animal):
    def __init__(self ,id,name,a_name1,much,dep_numb) :
        super().__init__(id,name,much,dep_numb)
        self.a_name1 = a_name1
    

    @classmethod
    def from_input(cls):
        id= input(" Введіть ваш id ")
        name = input("Введіть ваше ім'я ")
        a_name1 = input("Введіть коди корів за якими ви доглядаєте")
        much = input(" Введіть скільки літрів молока ви отримали")
        dep_numb = input("Введіть номер відділу(частини) в якій ви працюєте  ")
        return cls(id=id,name=name,a_name1=a_name1,much=much,dep_numb=dep_numb)
    


class Chicken(Animal):
    def __init__(self ,id,name,a_name,much,dep_numb) :
        super().__init__(id,name,much,dep_numb)
        
        self.a_name = a_name

        
    @classmethod
    def from_input(cls):
        id= input(" Введіть ваш id ")
        name = input("Введіть ваше ім'я ")
        a_name = input("Введіть кількість курей за якими ви доглядаєте")
        much = input(" Введіть скільки яєць ви отримали")
        dep_numb = input("Введіть номер відділу(частини) в якій ви працюєте  ")
        
        return cls(id=id,name=name,a_name=a_name,much=much,dep_numb=dep_numb)







