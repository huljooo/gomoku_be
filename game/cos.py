class Animal:
    counter = 0
    animals_list = []
    def __init__(self, waga, wiek):
        self.waga = waga
        self.wiek = wiek

        Animal.counter += 1
        Animal.animals_list.append(self)

    def make_sound(self):
        print("daje glos")

    def sleep(self):
        print("to zwierze spi")

    def wake_up(self):
        print("to zwierze wstało")

    def eat(self, food):
        self.food = food
        print("to zwierze je", self.food)
        self.waga += 1

class Bird(Animal):
    def __init__(self, waga, wiek, latanie):
        super().__init__(waga, wiek)

        self.latanie = latanie

    def latanie(self):
        if self.latanie:
            print("lata")
        else:
            print("nie lata")

    def make_sound(self): 
        print("spiewa")


class Mammal(Animal):
    def __init__(self, waga, wiek, can_swim):
        super().__init__(waga, wiek)
        self.can_swim = can_swim

    def swim(self):
        if self.can_swim:
            print("plywa")
        else:
            print("nie plywa")

    def make_sound(self):
        print("daje glos")


class Dog(Mammal):
    def __init__(self, waga, wiek, can_swim, breed):
        super().__init__(waga, wiek, can_swim)
        self.breed = breed

    def fetch(self):
        print("ten pies aportuje")

    def make_sound(self):
        print("szczeka")


animal = Animal(10, 10)
mammal = Mammal(10, 10, False)
dog = Dog(10, 10, False, "buldog")
bird = Bird(10, 10, False)

for animal in Animal.animals_list:
    animal.make_sound()













