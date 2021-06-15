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

