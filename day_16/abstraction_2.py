from abc import ABC, abstractmethod

# Abstract Base Class
class Shape(ABC):
    def __init__(self, shapeType):
        self.shapeType = shapeType

    @abstractmethod
    def area(self):
        pass

    @abstractmethod
    def perimeter(self):
        pass

# Concrete subclass: Rectangle
class Rectangle(Shape):
    def __init__(self, length, breadth):
        super().__init__('Rectangle')
        self.length = length
        self.breadth = breadth

    def area(self):
        return self.length * self.breadth

    def perimeter(self):
        return 2 * (self.length + self.breadth)

# Concrete subclass: Circle
class Circle(Shape):
    pi = 3.14

    def __init__(self, radius):
        super().__init__('Circle')
        self.radius = radius

    def area(self):
        return round(Circle.pi * (self.radius ** 2), 2)

    def perimeter(self):
        return round(2 * Circle.pi * self.radius, 2)

# Example usage
# shape = Shape()
rectangle = Rectangle(4, 6)
circle = Circle(5)

print(f"Rectangle Area: {rectangle.area()}")
print(f"Rectangle Perimeter: {rectangle.perimeter()}")
print(f"Circle Area: {circle.area()}")
print(f"Circle Perimeter: {circle.perimeter()}")   