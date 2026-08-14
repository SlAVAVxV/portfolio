class Animal:
    def speak(self):
        return "Animal makes a sound"

class Dog(Animal):
    def speak(self):
        return "Woof!"

class Cat(Animal):
    def speak(self):
        return "Meow!"

def main():
    animal = Animal()
    dog = Dog()
    cat = Cat()
    print(animal.speak())
    print(dog.speak())
    print(cat.speak())

if __name__ == "__main__":
    main()