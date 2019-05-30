import csv
import math
import random
import time
import tkinter as tk
from tkinter import ttk

from os1 import OS1
from os1.utils import OS_16_CHANNELS


class Frame(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        pass


class Application(Frame):
    def __init__(self, *args, **kwargs):
        self.os1_mode = tk.StringVar()
        self.os1_mode.set(OS1.MODES[0])  # default value
        self.os1_sensor_ip = tk.StringVar()
        self.os1_dest_ip = tk.StringVar()
        self.os1 = None
        super().__init__(*args, **kwargs)

    def create_widgets(self):
        ttk.Label(self, text="OS1 Configuration").pack()

        sensor_frame = ttk.Frame(self)
        ttk.Label(sensor_frame, text="Sensor IP").pack(side=tk.LEFT)
        ttk.Entry(sensor_frame, textvariable=self.os1_sensor_ip).pack(side=tk.LEFT)
        sensor_frame.pack(anchor=tk.W, padx=5, pady=5)

        dest_frame = ttk.Frame(self)
        ttk.Label(dest_frame, text="Destination IP").pack(side=tk.LEFT)
        ttk.Entry(dest_frame, textvariable=self.os1_dest_ip).pack(side=tk.LEFT)
        dest_frame.pack(anchor=tk.W, padx=5, pady=5)

        radio_frame = ttk.Frame(self)
        for mode in OS1.MODES:
            ttk.Radiobutton(
                radio_frame, text=mode, variable=self.os1_mode, value=mode
            ).pack(side=tk.LEFT)
        radio_frame.pack(anchor=tk.W, padx=5, pady=5)

        ttk.Button(self, text="Run", command=self.run_os1).pack(padx=5, pady=5)

    def run_os1(self):
        sensor = self.os1_sensor_ip.get()
        dest = self.os1_dest_ip.get()
        mode = self.os1_mode.get()
        toplevel = tk.Toplevel(self)
        pc = PointCloud(toplevel)
        pc.draw_frame()

        # try:
        #     self.os1 = OS1(sensor, dest, mode=mode)
        #     self.os1.start()
        # except Exception as e:
        #     self.display_error(e)

    def display_error(self, error):
        error_frame = ttk.Frame(self)
        ttk.Label(text=str(error)).pack()
        error_frame.pack()

    def display_point_cloud(self):
        point_cloud = tk.Toplevel(self)


class PointCloud(Frame):
    def __init__(self, *args, **kwargs):
        # TODO: Handle 16 or 64 devices
        self.channels = []
        self.canvas = None
        self.dots = []
        self.start = time.time()
        self.frame_count = 0
        super().__init__(*args, **kwargs)

    def create_widgets(self):
        channel_frame = ttk.Frame(self)
        ttk.Label(channel_frame, text="Channels").pack()
        for channel in range(len(OS_16_CHANNELS)):
            variable = tk.IntVar(value=1)
            self.channels.append(variable)
            ttk.Checkbutton(channel_frame, text=channel + 1, variable=variable).pack(
                anchor=tk.W
            )
        channel_frame.pack(side=tk.RIGHT)

        self.canvas = tk.Canvas(self, width=500, height=500)
        self.canvas.pack(side=tk.LEFT, padx=5, pady=5)

        width = int(self.canvas.cget("width"))
        height = int(self.canvas.cget("height"))
        Point.CONTEXT = {
            "width": width,
            "height": height,
            "radius": width * 0.2,
            "perspective": width * 0.8,
            "projection_center_x": width / 2,
            "projection_center_y": height / 2,
        }

        with open('mb15_sept_tls_capitola.csv') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # skip header
            count = 0
            for row in reader:
                if len(row) == 6 and count <= 1000:
                    x, y, z, r, g, b = row
                    hex = '#%02x%02x%02x' % (int(r), int(g), int(b))
                    p = Point(float(x), float(y), float(z), self.canvas)
                    self.dots.append(p)
                    count += 1
        # for i in range(2000):
        #     self.dots.append(Dot(self.canvas, context))

    def clear(self):
        """Clears the canvas so its ready to draw a new frame"""
        self.canvas.delete(tk.ALL)

    def draw_frame(self):
        """Draws a new frame to the canvas"""
        self.clear()
        self.frame_count += 1
        now = time.time()
        delta = now - self.start
        avg_fps = self.frame_count / delta
        # rot = delta * 0.06
        # sin_rot = math.sin(rot)
        # cos_rot = math.cos(rot)

        self.canvas.create_text(
            50, 25, fill="black", text="FPS: {:.2f}".format(avg_fps)
        )
        for dot in self.dots:
            dot.draw()
        # self.canvas.after(10, self.draw_frame)


class Point(object):
    CONTEXT = {}
    __slots__ = [
        "x",
        "y",
        "z",
        "canvas",
        "radius",
        "fill",
        "x_projected",
        "y_projected",
        "scale_projected",
    ]

    def __init__(self, x, y, z, canvas, radius=5, fill='black'):
        self.x = x
        self.y = y
        self.z = z
        self.canvas = canvas
        self.radius = radius
        self.fill = fill

        self.x_projected = 0
        self.y_projected = 0
        self.scale_projected = 0

    def project(self):
        perspective = self.ctx("perspective")
        projection_center_x = self.ctx("projection_center_x")
        projection_center_y = self.ctx("projection_center_y")

        # scale of the dot based on its distance from the 'camera'
        self.scale_projected = perspective / (perspective - self.z)
        # the x_projected is the x position on the 2d world
        self.x_projected = (self.x * self.scale_projected) + projection_center_x
        # the y_projected is the y position on the 2d world
        self.y_projected = (self.y * self.scale_projected) + projection_center_y

    def ctx(self, item):
        return self.CONTEXT.get(item)

    def draw(self):
        self.project()
        self.canvas.create_oval(
            self.x_projected,
            self.y_projected,
            self.x_projected + (self.radius * self.scale_projected),
            self.y_projected + (self.radius * self.scale_projected),
            fill=self.fill
        )


class Dot(object):
    def __init__(self, canvas, context):
        self.canvas = canvas
        self.context = context
        self.theta = random.uniform(0, 1) * 2 * math.pi
        self.phi = math.acos((random.uniform(0, 1) * 2) - 1)
        self.x = self.context["radius"] * math.sin(self.phi) * math.cos(self.theta)
        self.y = self.context["radius"] * math.sin(self.phi) * math.sin(self.theta)
        self.z = self.context["radius"] * math.cos(self.phi) + -self.context["radius"]
        # self.x = (random.uniform(0, 1) - 0.5) * self.context["width"]
        # self.y = (random.uniform(0, 1) - 0.5) * self.context["height"]
        # self.z = random.uniform(0, 1) * self.context["width"]
        self.radius = 4
        self.x_projected = 0
        self.y_projected = 0
        self.scale_projected = 0

    def project(self, sin_rot, cos_rot):
        perspective = self.context["perspective"]
        projection_center_x = self.context["projection_center_x"]
        projection_center_y = self.context["projection_center_y"]

        rotx = cos_rot * self.x + sin_rot * (self.z - -self.context["radius"])
        rotz = (
            -sin_rot * self.x
            + cos_rot * (self.z - -self.context["radius"])
            + self.context["radius"]
        )
        # scale of the dot based on its distance from the 'camera'
        self.scale_projected = perspective / (perspective - rotz)
        # the x_projected is the x position on the 2d world
        self.x_projected = (rotx * self.scale_projected) + projection_center_x
        # the y_projected is the y position on the 2d world
        self.y_projected = (self.y * self.scale_projected) + projection_center_y

    def draw(self, sin_rot, cos_rot):
        self.project(sin_rot, cos_rot)
        self.canvas.create_oval(
            self.x_projected,
            self.y_projected,
            self.x_projected + (self.radius * self.scale_projected),
            self.y_projected + (self.radius * self.scale_projected),
            fill="black",
        )


def run_gui():
    root = tk.Tk()
    app = Application(root)
    app.mainloop()
