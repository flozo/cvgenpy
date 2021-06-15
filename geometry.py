class Box(object):
    def __init__(self, height, width, color):
        self.height = height
        self.width = width
        self.color = color


class Layout(Box):
    def __init__(self, height, width, color, box_top, box_bottom, box_left, box_right):
        self.box_top = box_top
        self.box_bottom = box_bottom
        self.box_left = box_left
        self.box_right = box_right
        super().__init__(height, width, color)


class SkillCircle(object):
    def __init__(self, radius, fillcolor, linecolor, showline=False):
        self.radius = radius
        self.fillcolor = fillcolor
        self.linecolor = linecolor
        self.showline = showline


class SkillLayout(object):
    def __init__(self, SkillCircle, number=5, distance=5):
        self.skillcircle = SkillCircle
        self.number = number
        self.distance = distance
#        super().__init__(radius=2, fillcolor, linecolor, showline=False)

