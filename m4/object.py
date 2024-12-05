import math as m

class Object:
    # constants
    STARTING_SPEED = (0, 0)
    POSITION = (0, 0)
    SIZE = (1, 1)
    MASS = 1
    TRACE_COLOR = (0, 0, 0)
    SHAPE = 'parallelogram'
    SHAPE_RADIUS = 'sphere'
    DRAG_COEFFICIENT = 1.05
    DRAG_COEFFICIENT_RADIUS = 0.47
    MOVABLE = True
    LAST_ACCELERATION = (0, 0)
    LAST_AMPLITUDE_TIME = None
    ATTACHMENT_POINT = None
    THREAD_LENGTH = 0
    # constants

    def __init__(self, image, **kwargs) -> None:
        self.image = image
        self.size = kwargs.get('size', self.SIZE)
        position = kwargs.get('position', self.POSITION)
        self.positions = [(position, 0), (position, 0), (position, 0)]
        self.speed = kwargs.get('speed', self.STARTING_SPEED)
        self.mass = kwargs.get('mass', self.MASS)
        self.shape = kwargs.get('shape', self.SHAPE)
        self.drag_coefficient = kwargs.get('drag_coefficient', self.DRAG_COEFFICIENT)
        if ('radius' in kwargs.keys()):
            self.radius = kwargs['radius']
            self.size = (self.radius * 2, self.radius * 2)
            self.shape = kwargs.get('shape', self.SHAPE_RADIUS)
            self.drag_coefficient = kwargs.get('drag_coefficient', self.DRAG_COEFFICIENT_RADIUS)
        self.trace_color = kwargs.get('trace_color', self.TRACE_COLOR)
        self.movable = kwargs.get('movable', self.MOVABLE)
        self.last_acceleration = kwargs.get('last_acceleration', self.LAST_ACCELERATION)
        self.last_amplitude_time = kwargs.get('last_amplitude_time', self.LAST_AMPLITUDE_TIME)
        self.attachment_point = kwargs.get('attachment_point', self.ATTACHMENT_POINT)
        self.thread_length = kwargs.get('thread_length', self.THREAD_LENGTH)

    def reference_area(self) -> float:
        if (self.shape == 'parallelogram'):
            w, h = self.size
            area = h * h # assuming it's a square from the side
        elif (self.shape == 'sphere'):
            r = self.radius
            area = m.pi * (r ** 2)
        else:
            area = 0
        return area
    
    def volume(self) -> float:
        if (self.shape == 'parallelogram'):
            w, h = self.size
            volume = w * h * h # assuming it's a square from the side
        elif (self.shape == 'sphere'):
            r = self.radius
            volume = (4 / 3) * m.pi * (r ** 3)
        else:
            volume = 0
        return volume