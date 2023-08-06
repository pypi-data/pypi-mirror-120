from abc import abstractmethod
import xml.etree.ElementTree as ET
import copy

class Primitive:
    '''
    Base class for representing elements in an IPE drawing.
    '''

    xP = 0
    yP = 0

    def __init__(self, prototype=None):

        if prototype:
            self.cloneProp(prototype)
        else:
            self.fill = None
            self.stroke = 'black'
            self.pen = 'normal'
            self.opacity = None
            self.stroke_opacity = None
            self.dash = None
            self.layer = None
            self.rarrow = None
            self.arrow = None

        

    def cloneProp(self, other):
        '''
        Clone the properties of an object.

        Parameters:
        other (Primitive): The other object.

        Returns:
        None
        '''
        self.fill = other.fill
        self.stroke = other.stroke
        self.pen = other.pen
        self.opacity = other.opacity
        self.stroke_opacity = other.stroke_opacity
        self.dash = other.dash
        self.layer = other.layer

    def addProperties(self, elem):
        elem.set('pen', f'{self.pen}')

        if self.opacity:
            elem.set('opacity', f'{self.opacity}')
        if self.stroke_opacity:
            elem.set('stroke-opacity', f'{self.stroke_opacity}')

        if self.fill:
            elem.set('fill', self.fill)

        if self.stroke:
            elem.set('stroke', self.stroke)
        
        if self.dash:
            elem.set('dash', self.dash)

        if self.layer:
            elem.set('layer', self.layer)

    def clone(self):
        return copy.deepcopy(self)
        # elem.set('matrix', f'{self.MR[0][0]} {self.MR[0][1]} {self.MR[1][0]} {self.MR[1][1]} {self.MT[0]} {self.MT[1]}')

    @abstractmethod
    def getBB(self):
        raise NotImplemented

    @abstractmethod
    def translate(self, x, y):
        raise NotImplemented

    @abstractmethod
    def rotate(self, a, point=None):
        '''
        Method to rotate an object around a point.
        '''
        raise NotImplemented

    @abstractmethod
    def draw() -> ET.Element:
        raise NotImplemented


