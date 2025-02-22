import numpy as np
import matplotlib.pyplot as plt

def drawline(image, x0, y0, x1, y1, color):
    flag = abs(x0-x1) < abs(y0-y1)
    if flag:
        x0, y0, x1, y1 = y0, x0, y1, x1

    if x0 > x1:
        x0, x1, y0, y1 = x1, x0, y1, y0

    dy = abs(y1 - y0)
    dx = x1 - x0
    y_step = 1 if y1 > y0 else -1
    error = 0
    y = y0

    for x in range(x0, x1):
        if flag:
            image[x, y] = color
        else:
            image[y, x] = color

        error += dy
        if 2 * error >= dx:
            y += y_step
            error -= dx

def parser(src: str, points: list, tops: list) -> None:
    if src is None:
        print("Src is None")
        return
    for line in src.splitlines()[4:]:
        if line.startswith("v"):
            parts = line.split()
            x, y = float(parts[1]), float(parts[2])
            points.append((x, y))
        elif line.startswith("f"):
            parts = line.split()
            t1, t2, t3 = int(parts[1].split('/')[0]), int(parts[2].split('/')[0]), int(parts[3].split('/')[0])
            tops.append((t1, t2, t3))

def open_obj(src):
    try:
        with open(src, "r") as file:
            return file.read()
    except FileNotFoundError:
        print("File not found:", src)
        return None

file = open_obj("mo.obj")
points = []
tops = []
parser(file, points, tops)

width, height = 1000, 1000
image = np.ones((height, width, 3), dtype=np.uint8) * 0

for top in tops:
    for i in range(3):
        x0, y0 = points[top[i-1]-1]
        x1, y1 = points[top[i]-1]
        x0, y0 = int(500 + x0 * 5000), int(500 + y0 * 5000)
        x1, y1 = int(500 + x1 * 5000), int(500 + y1 * 5000)
        drawline(image, x0, y0, x1, y1, (255, 255, 255))

plt.title("Заяц")
image = np.flipud(image)
plt.imshow(image, extent=[0, width, 0, height])
plt.show()