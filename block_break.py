import tkinter as tk


class Shape:

    def __init__(self, x, y, width, height, center=False):
        if center:
            x -= width // 2
            y -= height // 2
        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 = y + height

    def intersect(self, target):
        hit_x = max(self.x1, target.x1) <= min(self.x2, target.x2)
        hit_y = max(self.y1, target.y1) <= min(self.y2, target.y2)
        return hit_x and hit_y


class Paddle(Shape):

    def __init__(self, x, y, width=45, height=8, speed=18, color="blue"):
        super().__init__(x, y, width, height, center=True)
        self.speed = speed
        self.color = color
        self.name = "paddle"

    def right(self, event):
        self.x1 += self.speed
        self.x2 += self.speed

    def left(self, event):
        self.x1 -= self.speed
        self.x2 -= self.speed

    def limit(self, area):
        adjust = (max(self.x1, area.x1) - self.x1 or
                  min(self.x2, area.x2) - self.x2)
        self.x1 += adjust
        self.x2 += adjust

    def move(self):
        pass

    def draw(self, canvas):
        canvas.delete(self.name)
        canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2,
                                fill=self.color, tag=self.name)

    def delete(self, canvas):
        canvas.delete(self.name)


class Ball(Shape):

    def __init__(self, x, y, size=10, dx=2, dy=2, color="red"):
        super().__init__(x, y, size, size, center=True)
        self.dx = dx
        self.dy = dy
        self.color = color
        self.name = "ball"

    def move(self):
        self.x1 += self.dx
        self.y1 += self.dy
        self.x2 += self.dx
        self.y2 += self.dy

    def limit(self, area):
        if self.x1 <= area.x1 or area.x2 <= self.x2:
            self.dx *= -1
        if self.y1 <= area.y1 or area.y2 <= self.y2:
            self.dy *= -1

    def bound(self, target):
        if not self.intersect(target):
            return False
        center_x = (self.x1 + self.x2) // 2
        center_y = (self.y1 + self.y2) // 2
        if (self.dx > 0 and center_x <= target.x1 or
            self.dx < 0 and target.x2 <= center_x):
                self.dx *= -1
        if (self.dy > 0 and center_y <= target.y1 or
            self.dy < 0 and target.y2 <= center_y):
                self.dy *= -1
        return True

    def draw(self, canvas):
        canvas.delete(self.name)
        canvas.create_oval(self.x1, self.y1, self.x2, self.y2,
                           fill=self.color, tag=self.name)

    def delete(self, canvas):
        canvas.delete(self.name)


class Block(Shape):

    def __init__(self, x, y, width, height, gap_x=0, gap_y=0, center=False,
                 color="orange", point=1):
        super().__init__(x + gap_x, y + gap_y,
                         width - gap_x * 2, height - gap_y * 2, center=center)
        self.point = point
        self.color = color
        self.name = f"block{x}.{y}"
        self.exists = True

    def break_and_bound(self, target):
        if self.exists and target.bound(self):
            self.exists = False
            return self.point
        else:
            return 0

    def is_broken(self):
        return not self.exists

    def draw(self, canvas):
        canvas.delete(self.name)
        if self.exists:
            canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2,
                                    fill=self.color, tag=self.name)
