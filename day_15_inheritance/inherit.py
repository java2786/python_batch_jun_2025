class Parent:
    def greet(self):
        print("good morning from parent")
        
class Child(Parent):
    def greeting(self):
        print("good morning from child")

child = Child()

child.greet()
child.greeting()