from ipey.primitive import Primitive
import xml.etree.ElementTree as ET
import math

class Arc(Primitive):

    def __init__(self, p1, p2, p3, prototype=None):
        '''
        Create a arc starting at p1, going through p2 and ending at p3.
        '''
        super().__init__(prototype=prototype)

        self.p1 = p1
        self.p2 = p2
        self.p3 = p3

        self.points = [p1,p2,p3]

    #TODO fix bounding box
    def getBB(self):
        maxX = max(self.points, key=lambda item:item[0])[0]
        maxY = max(self.points, key=lambda item:item[1])[1]
        minX = min(self.points, key=lambda item:item[0])[0]
        minY = min(self.points, key=lambda item:item[1])[1]

        return ((minX, minY), (maxX, maxY))


    def translate(self, x, y):
        self.p1 = (self.p1[0] + x, self.p1[1] + y)
        self.p2 = (self.p1[0] + x, self.p1[1] + y)
        self.p3 = (self.p1[0] + x, self.p1[1] + y)

    #TODO fix rotation
    def rotate(self, a, pivot=None):
        if pivot:
            xP, yP = pivot
        else:
            xP = 0
            yP = 0
            for p in self.points:
                xP += p[0]
                yP += p[1]
                
            yP /= len(self.points)
            xP /= len(self.points)


        s = math.sin(a)
        c = math.cos(a)
        for i, p in enumerate(self.points):
            p = (p[0] - xP, p[1] - yP)
            p = (p[0] * c + p[1] * s, p[0] * s + p[1] * c)
            self.points[i] = (p[0] + xP, p[1] + yP)

    def draw(self):
        elem = ET.Element('path')
        self.addProperties(elem)

        cx, cy, r = self.findCircle(self.p1[0], self.p1[1], self.p2[0], self.p2[1], self.p3[0], self.p3[1])
        elem.text = f'{self.p1[0]} {self.p1[1]} m \n {r} 0 0 {r} {cx} {cy} {self.p3[0]} {self.p3[1]} a'
        return elem


    def findCircle(self, x1, y1, x2, y2, x3, y3):
        x12 = x1 - x2
        x13 = x1 - x3
    
        y12 = y1 - y2
        y13 = y1 - y3
    
        y31 = y3 - y1
        y21 = y2 - y1

        x31 = x3 - x1
        x21 = x2 - x1
    
        # x1^2 - x3^2
        sx13 = pow(x1, 2) - pow(x3, 2)
    
        # y1^2 - y3^2
        sy13 = pow(y1, 2) - pow(y3, 2)
    
        sx21 = pow(x2, 2) - pow(x1, 2)
        sy21 = pow(y2, 2) - pow(y1, 2)
    
        f = (((sx13) * (x12) + (sy13) * (x12) + (sx21) * (x13) + (sy21) * (x13)) // (2 * ((y31) * (x12) - (y21) * (x13))))
                
        g = (((sx13) * (y12) + (sy13) * (y12) + (sx21) * (y13) + (sy21) * (y13)) // (2 * ((x31) * (y12) - (x21) * (y13))))
    
        c = (-pow(x1, 2) - pow(y1, 2) - 2 * g * x1 - 2 * f * y1)
    
        # eqn of circle be x^2 + y^2 + 2*g*x + 2*f*y + c = 0
        # where centre is (h = -g, k = -f) and
        # radius r as r^2 = h^2 + k^2 - c
        cx = -g
        cy = -f
        sqr_of_r = cx**2 + cy ** 2 - c
    
        # r is the radius
        r = math.sqrt(sqr_of_r)
    
        return cx, cy, r
