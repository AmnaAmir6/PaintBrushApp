
from tkinter import *
from tkinter import colorchooser
from abc import ABC,abstractmethod
import math
from tkinter import filedialog
from tkinter import simpledialog
from PIL import Image, ImageTk, ImageGrab
import webcolors


#shape
class Shape(ABC):
    def __init__(self,canvas):
        self.shape_id=None
        self.canvas=canvas
    @abstractmethod
    def draw(self,event,brush_color):
        pass
    #@abstractmethod
    def draw_end(self):
        return None,None,None
    def remove(self):
        if self.shape_id:
            self.canvas.delete(self.shape_id)
            self.shape_id = None

#circle
class Circle(Shape):
    def __init__(self, canvas, x, y,brush_width):
        super().__init__(canvas)
        self.last_x=x
        self.last_y=y
        self.radius = 0
        self.shape_id = None
        self.brush_width=brush_width

    def draw(self, event, brush_color):
        if self.shape_id is not None:
            self.canvas.delete(self.shape_id)
        if self.last_x is None:
            self.last_x, self.last_y = event.x, event.y
            return event.x, event.y, self.shape_id
    
        self.radius = abs(self.last_x - event.x) + abs(self.last_y - event.y)
        x1, y1 = self.last_x - self.radius, self.last_y - self.radius
        x2, y2 = self.last_x + self.radius, self.last_y + self.radius
    
        points = []
        num_points = 360 
        angle_increment = 360 / num_points
    
        for angle in range(0, 360, int(angle_increment)):
            radians = math.radians(angle)
            x = self.last_x + (self.radius * math.cos(radians))
            y = self.last_y + (self.radius * math.sin(radians))
            points.extend([x, y])
    
        self.shape_id = self.canvas.create_polygon(points, outline=brush_color, width=self.brush_width,fill="")
        return event.x, event.y, self.shape_id
    

#rectangle
class Rectangle(Shape):
    def __init__(self, canvas, x, y,brush_width):
        super().__init__(canvas)
        self.last_x=x
        self.last_y=y
        self.shape_id = None
        self.brush_width=brush_width

    def draw(self, event, brush_color):
        if self.shape_id is not None:
            self.canvas.delete(self.shape_id)
        if self.last_x is None:
            self.last_x, self.last_y = event.x, event.y
            return event.x, event.y, self.shape_id

        x0, y0 = self.last_x, self.last_y
        x1, y1 = event.x, event.y

        points = [x0, y0, x0, y1, x1, y1, x1, y0]
        self.shape_id = self.canvas.create_polygon(points, outline=brush_color, width=self.brush_width,fill="")
        return event.x, event.y, self.shape_id


#square
class Square(Shape):
    def __init__(self, canvas, x, y,brush_width):
        super().__init__(canvas)
        self.last_x = x
        self.last_y = y
        self.shape_id = None
        self.brush_width=brush_width

    def draw(self, event, brush_color):
        if self.shape_id is not None:
            self.canvas.delete(self.shape_id)
        if self.last_x is None:
            self.last_x, self.last_y = event.x, event.y
            return event.x, event.y, self.shape_id

        x0, y0 = self.last_x, self.last_y
        x1, y1 = event.x, event.y
        size = max(abs(x1 - x0), abs(y1 - y0))

        if x1 < x0:
            x0 = x0 - size
        if y1 < y0:
            y0 = y0 - size
        x1 = x0 + size
        y1 = y0 + size

        points = [x0, y0, x0, y1, x1, y1, x1, y0]
        self.shape_id = self.canvas.create_polygon(points, outline=brush_color, width=self.brush_width,fill="")
        return event.x, event.y, self.shape_id


#oval
class Oval(Shape):
    def __init__(self, canvas, x, y,brush_width):
        super().__init__(canvas)
        self.last_x = x
        self.last_y = y
        self.shape_id = None
        self.brush_width=brush_width

    def draw(self, event, brush_color):
        if self.shape_id is not None:
            self.canvas.delete(self.shape_id)
        if self.last_x is None:
            self.last_x, self.last_y = event.x, event.y
            return event.x, event.y, self.shape_id
    
        x0, y0 = self.last_x, self.last_y
        x1, y1 = event.x, event.y
        center_x = (x0 + x1) / 2
        center_y = (y0 + y1) / 2
    
        radius_x = abs(x1 - x0) / 2
        radius_y = abs(y1 - y0) / 2
        num_vertices = 100
        angle_increment = 2 * math.pi / num_vertices
        vertices = []
        for i in range(num_vertices):
            angle = i * angle_increment
            vertex_x = center_x + radius_x * math.cos(angle)
            vertex_y = center_y + radius_y * math.sin(angle)
            vertices.extend([vertex_x, vertex_y])
    
        self.shape_id = self.canvas.create_polygon(vertices, outline=brush_color, width=self.brush_width,fill="")
        return event.x, event.y, self.shape_id
    

#Star
#class Star(Shape):
#    def __init__(self, canvas, x, y, brush_width):
#        super().__init__(canvas)
#        self.start_x = x
#        self.start_y = y
#        self.shape_id = None
#        self.brush_width = brush_width

    #def draw(self, event, brush_color):
    #    if self.shape_id is not None:
    #        self.canvas.delete(self.shape_id)

    #    if self.start_x is None:
    #        self.start_x, self.start_y = event.x, event.y
    #        return event.x, event.y, self.shape_id

    #    x0, y0 = self.start_x, self.start_y
    #    x1, y1 = event.x, event.y

    #    width = abs(x1 - x0)
    #    height = abs(y1 - y0)

    #    # Calculate the coordinates of the five outer points of the star
    #    outer_points = self.calculate_star_outer_points(x0, y0, width, height)

    #    # Calculate the coordinates of the five inner points of the star
    #    vertices=[]
    #    inner_points = self.calculate_star_inner_points(x0, y0, width, height)
    #    i=0
    #    for item in inner_points:
    #        vertices.append(item)
    #        vertices.append(outer_points[i])
    #        i+=1

        
    #    # Combine the outer and inner points to create the star shape
    #    #vertices =  inner_points+outer_points

    #    # Create the star shape
    #    self.shape_id = self.canvas.create_polygon(vertices, outline=brush_color, width=self.brush_width,fill="")

    #    return event.x, event.y, self.shape_id

    #def calculate_star_outer_points(self, x, y, width, height):
    #    points = []
    #    angle_deg = -18

    #    for i in range(5):
    #        angle_rad = math.radians(angle_deg)
    #        dx = width / 2 * math.cos(angle_rad)
    #        dy = height / 2 * math.sin(angle_rad)
    #        point_x = x + width / 2 + dx
    #        point_y = y + height / 2 + dy
    #        points.append(point_x)
    #        points.append(point_y)
    #        angle_deg += 72

    #    return points

    #def calculate_star_inner_points(self, x, y, width, height):
    #    points = []
    #    angle_deg = 90

    #    for i in range(5):
    #        angle_rad = math.radians(angle_deg)
    #        dx = width / 4 * math.cos(angle_rad)
    #        dy = height / 4 * math.sin(angle_rad)
    #        point_x = x + width / 2 + dx
    #        point_y = y + height / 2 + dy
    #        points.append(point_x)
    #        points.append(point_y)
    #        angle_deg += 72

    #    return points

class Star(Shape):
    def __init__(self, canvas, x, y,brush_width):
        super().__init__(canvas)
        self.center_x = x
        self.center_y = y
        self.outer_radius = 0
        self.inner_radius = 0
        self.shape_id = None
        self.brush_width=brush_width

    def draw(self, event, brush_color):
        if self.shape_id is not None:
            self.canvas.delete(self.shape_id)

        if self.center_x is None:
            self.center_x, self.center_y = event.x, event.y
            return event.x, event.y, self.shape_id

        x0, y0 = self.center_x, self.center_y
        x1, y1 = event.x, event.y
        self.outer_radius = max(abs(x1 - x0), abs(y1 - y0))
        self.inner_radius = self.outer_radius / 2

        points = []
        for i in range(5):
            outer_angle = 2 * math.pi * i / 5 + math.pi / 2
            inner_angle = outer_angle + math.pi / 5
            x_outer = self.center_x + self.outer_radius * math.cos(outer_angle)
            y_outer = self.center_y + self.outer_radius * math.sin(outer_angle)
            x_inner = self.center_x + self.inner_radius * math.cos(inner_angle)
            y_inner = self.center_y + self.inner_radius * math.sin(inner_angle)
            points.extend([x_outer, y_outer, x_inner, y_inner])

        self.shape_id = self.canvas.create_polygon(points, outline=brush_color, width=self.brush_width, fill="")
        return event.x, event.y, self.shape_id

#pentagon
class Pentagon(Shape):
    def __init__(self, canvas, x, y, brush_width):
        super().__init__(canvas)
        self.start_x = x
        self.start_y = y
        self.shape_id = None
        self.brush_width = brush_width

    def draw(self, event, brush_color):
        if self.shape_id is not None:
            self.canvas.delete(self.shape_id)

        if self.start_x is None:
            self.start_x, self.start_y = event.x, event.y
            return event.x, event.y, self.shape_id

        x0, y0 = self.start_x, self.start_y
        x1, y1 = event.x, event.y

        width = abs(x1 - x0)
        height = abs(y1 - y0)

        vertices = self.calculate_pentagon_vertices(x0, y0, width, height)

        self.shape_id = self.canvas.create_polygon(vertices, outline=brush_color, width=self.brush_width,fill="")

        return event.x, event.y, self.shape_id

    def calculate_pentagon_vertices(self, x, y, width, height):
        vertices = []
        angle_deg = 54  

        for i in range(5):
            angle_rad = math.radians(angle_deg)
            dx = width * math.cos(angle_rad)
            dy = height * math.sin(angle_rad)
            vertex_x = x + dx
            vertex_y = y + dy
            vertices.append(vertex_x)
            vertices.append(vertex_y)
            angle_deg += 72  

        return vertices

#hexagon
class Hexagon(Shape):
    def __init__(self, canvas, x, y, brush_width):
        super().__init__(canvas)
        self.start_x = x
        self.start_y = y
        self.shape_id = None
        self.brush_width = brush_width

    def draw(self, event, brush_color):
        if self.shape_id is not None:
            self.canvas.delete(self.shape_id)
        if self.start_x is None:
            self.start_x, self.start_y = event.x, event.y
            return event.x, event.y, self.shape_id

        x0, y0 = self.start_x, self.start_y
        x1, y1 = event.x, event.y

        width = abs(x1 - x0)
        height = abs(y1 - y0)

        vertices = self.calculate_hexagon_vertices(x0, y0, width, height)
        self.shape_id = self.canvas.create_polygon(vertices, outline=brush_color, width=self.brush_width,fill="")
        return event.x, event.y, self.shape_id

    def calculate_hexagon_vertices(self, x, y, width, height):
        vertices = []
        angle_deg = 30

        for i in range(6):
            angle_rad = math.radians(angle_deg)
            dx = width * math.cos(angle_rad)
            dy = height * math.sin(angle_rad)
            vertex_x = x + dx
            vertex_y = y + dy
            vertices.append(vertex_x)
            vertices.append(vertex_y)
            angle_deg += 60

        return vertices

#triangle
class Triangle(Shape):
    def __init__(self, canvas, x, y, brush_width):
        super().__init__(canvas)
        self.start_x = x
        self.start_y = y
        self.shape_id = None
        self.brush_width = brush_width

    def draw(self, event, brush_color):
        if self.shape_id is not None:
            self.canvas.delete(self.shape_id)

        if self.start_x is None:
            self.start_x, self.start_y = event.x, event.y
            return event.x, event.y, self.shape_id        

        x0, y0 = self.start_x, self.start_y
        x1, y1 = event.x, event.y

        width = abs(x1 - x0)
        height = abs(y1 - y0)
        vertices = self.calculate_triangle_vertices(x0, y0, width, height)
        self.shape_id = self.canvas.create_polygon(vertices, outline=brush_color, width=self.brush_width,fill="")
        return event.x, event.y, self.shape_id

    def calculate_triangle_vertices(self, x, y, width, height):
        vertices = []
        vertices.append(x + width / 2) 
        vertices.append(y)
        vertices.append(x) 
        vertices.append(y + height)
        vertices.append(x + width) 
        vertices.append(y + height)

        return vertices

#line
class Line(Shape):
    def __init__(self, canvas, x, y,brush_width):
        super().__init__(canvas)
        self.start_x = x
        self.start_y = y
        self.shape_id = None
        self.brush_width=brush_width

    def draw(self, event, brush_color):
        if self.shape_id is not None:
            self.canvas.delete(self.shape_id)
        if self.start_x is None:
            self.start_x, self.start_y = event.x, event.y
            return event.x, event.y, self.shape_id
        end_x, end_y = event.x, event.y

        self.shape_id = self.canvas.create_line(self.start_x, self.start_y, end_x, end_y, fill=brush_color, width=self.brush_width)
        return event.x, event.y, self.shape_id

#n polygon
class Polygon(Shape):
    def __init__(self, canvas, x, y, brush_width, sides):
        super().__init__(canvas)
        self.start_x = x
        self.start_y = y
        self.shape_id = None
        self.brush_width = brush_width
        self.sides = sides

    def draw(self, event, brush_color):
        if self.shape_id is not None:
            self.canvas.delete(self.shape_id)

        if self.start_x is None:
            self.start_x, self.start_y = event.x, event.y
            return event.x, event.y, self.shape_id

        x0, y0 = self.start_x, self.start_y
        x1, y1 = event.x, event.y
        width = abs(x1 - x0)
        height = abs(y1 - y0)
        vertices = self.calculate_polygon_vertices(x0, y0, width, height)
        self.shape_id = self.canvas.create_polygon(vertices, outline=brush_color, width=self.brush_width,fill="")
        return event.x, event.y, self.shape_id

    def calculate_polygon_vertices(self, x, y, width, height):
        vertices = []
        angle_deg = 360 / self.sides

        for i in range(self.sides):
            angle_rad = math.radians(angle_deg * i)
            dx = width * math.cos(angle_rad)
            dy = height * math.sin(angle_rad)
            vertex_x = x + dx
            vertex_y = y + dy
            vertices.append(vertex_x)
            vertices.append(vertex_y)
        return vertices

#brush
class Brush:
    def __init__(self, canvas,b_color,width):
        self.brush_color=b_color
        self.canvas=canvas
        self.width=width

    def draw(self,event,last_x,last_y,b_color,brush_width):
        if last_x==None:
            return event.x,event.y
        self.canvas.create_line(last_x,last_y,event.x,event.y,width=brush_width,capstyle=ROUND,fill=b_color)
        return event.x,event.y

    def draw_end(self,event):
        return None,None

#eraser
class Eraser:
    def __init__(self, canvas,b_color,width):
        self.brush_color=b_color
        self.canvas=canvas
        self.width=width

    def draw(self,event,last_x,last_y,b_color,brush_width):
        if last_x==None:
            return event.x,event.y
        self.canvas.create_line(last_x,last_y,event.x,event.y,width=brush_width,capstyle=ROUND,fill=b_color)
        return event.x,event.y

    def draw_end(self,event):
        return None,None
        
class PaintApp:
    def __init__(self,width,height,title):
        #screen
        self.screen=Tk()
        self.screen.title(title)
        self.screen.geometry(str(width)+"x"+str(height))

        #variables
        self.brush_color='black'
        self.eraser_color='white'
        self.last_x,self.last_y=None,None
        self.shape_id = None
        self.brush_width = 1
        self.isFirst = True
        self.BrushActive = True
        self.zoom_factor = 1.0
        self.circles = []
        self.circle_no=0;
        self.copied_image=[]
        self.copied_image_count= 0
        self.select_rect = None
        self.start_x=0
        self.start_y=0
        self.isStartArea= True
        self.control1_x=None
        self.control1_y=None
        self.control2_x=None
        self.control2_y=None
        self.curve=None
        
        #create button area frame
        self.button_area = Frame(self.screen,width=width,height=130, bg="light blue")
        self.button_area.pack()

        #create select frame
        self.select_area = LabelFrame(self.button_area,text="Select",relief=RIDGE, bg="light cyan")
        self.select_area.place(x=0,y=30,width=85,height=100)

        #create tools frame
        self.tool_area = LabelFrame(self.button_area,text="Tools",relief=RIDGE, bg="light cyan")
        self.tool_area.place(x=86,y=30,width=100,height=100)

        #create shapes frame
        self.shapes_area = LabelFrame(self.button_area,text="Shapes",relief=RIDGE, bg="light cyan")
        self.shapes_area.place(x=187,y=30,width=259,height=100)

        #create size frame
        self.size_area = LabelFrame(self.button_area,text="Size",relief=RIDGE, bg="light cyan")
        self.size_area.place(x=448,y=30,width=160,height=100)

        #create color1 frame
        self.color1_area = LabelFrame(self.button_area,text="Color1",relief=RIDGE, bg="light cyan")
        self.color1_area.place(x=609,y=30,width=85,height=100)

        #create color2 frame
        self.color2_area = LabelFrame(self.button_area,text="Color2",relief=RIDGE, bg="light cyan")
        self.color2_area.place(x=694,y=30,width=85,height=100)

        #create colors frame
        self.colors_area = LabelFrame(self.button_area,text="Colors",relief=RIDGE, bg="light cyan")
        self.colors_area.place(x=781,y=30,width=350,height=100)

        #create Bazier Curve frame
        self.curve_area = LabelFrame(self.button_area,text="Bezier Curve",relief=RIDGE, bg="light cyan")
        self.curve_area.place(x=1132,y=30,width=75,height=100)

        #create zoom frame
        self.zoom_area = LabelFrame(self.button_area,text="Zoom",relief=RIDGE, bg="light cyan")
        self.zoom_area.place(x=1208,y=30,width=75,height=100)

        #create delete frame
        self.delete_area = LabelFrame(self.button_area,text="Delete",relief=RIDGE, bg="light cyan")
        self.delete_area.place(x=1284,y=30,width=80,height=100)

        #create canvas
        self.canvas=Canvas(self.screen,width=width,height=height-100,bg="white")
        self.canvas.pack()

        #creating save and load
        self.save_image = PhotoImage(file="save.png")
        self.save_button=Button(self.button_area,width=25,height=25,relief=FLAT,bg="light blue",borderwidth=0, activebackground="light blue", image=self.save_image,command=self.save_canvas)
        self.save_button.place(x=15, y=0)

        self.load_image = PhotoImage(file="load.png")
        self.load_button=Button(self.button_area,width=25,height=25,relief=FLAT,bg="light blue",borderwidth=0, activebackground="light blue", image=self.load_image,command=self.load_canvas)
        self.load_button.place(x=55, y=0)

        #creating delete button
        self.delete_image = PhotoImage(file="delete.png")
        self.delete_button=Button(self.delete_area,width=55,height=70,relief=FLAT,bg="light cyan",borderwidth=0, activebackground="light cyan", image=self.delete_image,command=self.clear_canvas)
        self.delete_button.place(x=5, y=10)

        #creating bazierCurve button
        self.bazierCurve_image = PhotoImage(file="bazierCurve.png")
        self.bazierCurve_button=Button(self.curve_area,width=45,height=70,relief=FLAT,bg="light cyan",borderwidth=0, activebackground="light cyan", image=self.bazierCurve_image,command=self.on_bazierCurveButton_pressed)
        self.bazierCurve_button.place(x=15, y=10)

        #creating zoomIn button
        self.zoomIn_image = PhotoImage(file="zoomIn.png")
        self.zoomIn_button=Button(self.zoom_area,width=45,height=35,relief=FLAT,bg="light cyan",borderwidth=0, activebackground="light cyan", image=self.zoomIn_image,command=self.on_ZoomInButton_pressed)
        self.zoomIn_button.place(x=15, y=5)

        #creating zoomOut button
        self.zoomOut_image = PhotoImage(file="zoomOut.png")
        self.zoomOut_button=Button(self.zoom_area,width=45,height=35,relief=FLAT,bg="light cyan",borderwidth=0, activebackground="light cyan", image=self.zoomOut_image,command=self.on_ZoomOutButton_pressed)
        self.zoomOut_button.place(x=15, y=40)

        #creating selectarea button
        self.selectarea_image = PhotoImage(file="select_area.png")
        self.selectarea_button=Button(self.select_area,width=70,height=70,relief=FLAT,bg="light cyan",borderwidth=0, activebackground="light cyan", image=self.selectarea_image,command=self.on_selectareaButton_pressed)
        self.selectarea_button.place(x=5, y=10)

        #creating thinline button
        self.thinline_image = PhotoImage(file="thinline.png")
        self.thinline_button=Button(self.size_area,width=140,height=20,relief=FLAT,bg="light cyan",borderwidth=0, activebackground="light cyan", image=self.thinline_image,command=lambda:self.set_brush_width(4))
        self.thinline_button.place(x=5, y=0)

        #creating normalline button
        self.normalline_image = PhotoImage(file="normalline.png")
        self.normalline_button=Button(self.size_area,width=140,height=20,relief=FLAT,bg="light cyan",borderwidth=0, highlightthickness=0,activebackground="light cyan", image=self.normalline_image,command=lambda:self.set_brush_width(8))
        self.normalline_button.place(x=5, y=20)

        #creating thickline button
        self.thickline_image = PhotoImage(file="thickline.png")
        self.thickline_button=Button(self.size_area,width=140,height=20,relief=FLAT,bg="light cyan",borderwidth=0, highlightthickness=0,activebackground="light cyan", image=self.thickline_image,command=lambda:self.set_brush_width(12))
        self.thickline_button.place(x=5, y=40)

        #creating eraser button
        self.eraser_image = PhotoImage(file="eraser.png")
        self.eraser_button=Button(self.tool_area,width=30,height=30,relief=FLAT,bg="light cyan",borderwidth=0, activebackground="light cyan", image=self.eraser_image,command=self.on_eraserButton_pressed)
        self.eraser_button.place(x=10, y=45)

        #creating selectClr button
        self.selectClr_image = PhotoImage(file="selectClr.png")
        self.selectClr_button=Button(self.tool_area,width=30,height=30,relief=FLAT,bg="light cyan",borderwidth=0, highlightthickness=0,activebackground="light cyan", image=self.selectClr_image,command=self.on_selectClrButton_pressed)
        self.selectClr_button.place(x=55, y=5)

        #creating paintbrush button
        self.paintbrush_image = PhotoImage(file="paintbrush.png")
        self.paintbrush_button=Button(self.tool_area,width=30,height=30,relief=FLAT,bg="light cyan",borderwidth=0, highlightthickness=0,activebackground="light cyan", image=self.paintbrush_image,command=self.on_paintbrushButton_pressed)
        self.paintbrush_button.place(x=10, y=5)

        #creating paintbucket button
        self.paintbucket_image = PhotoImage(file="paintbucket.png")
        self.paintbucket_button=Button(self.tool_area,width=30,height=30,relief=FLAT,bg="light cyan",borderwidth=0, highlightthickness=0, activebackground="light cyan",image=self.paintbucket_image,command=self.on_paintbucketButton_pressed)
        self.paintbucket_button.place(x=55, y=45)

        #creating circle button
        self.circle_image = PhotoImage(file="circle.png")
        self.circle_button=Button(self.shapes_area,width=30,height=30,relief=FLAT,bg="light cyan",borderwidth=0, activebackground="light cyan", image=self.circle_image,command=self.on_circleButton_pressed)
        self.circle_button.place(x=15, y=5)

        #creating rectangle button
        self.rectangle_image = PhotoImage(file="rectangle.png")
        self.rectangle_button=Button(self.shapes_area,width=30,height=30,relief=FLAT,bg="light cyan",borderwidth=0, highlightthickness=0, image=self.rectangle_image,command=self.on_rectangleButton_pressed)
        self.rectangle_button.place(x=65, y=5)

        #creating square button
        self.square_image = PhotoImage(file="square.png")
        self.square_button=Button(self.shapes_area,width=30,height=30,relief=FLAT,bg="light cyan",borderwidth=0, highlightthickness=0, image=self.square_image,command=self.on_squareButton_pressed)
        self.square_button.place(x=215, y=5)

        #creating triangle button
        self.triangle_image = PhotoImage(file="triangle.png")
        self.triangle_button=Button(self.shapes_area,width=30,height=30,relief=FLAT,bg="light cyan",borderwidth=0, highlightthickness=0, image=self.triangle_image,command=self.on_triangleButton_pressed)
        self.triangle_button.place(x=165, y=5)

        #creating oval button
        self.oval_image = PhotoImage(file="oval.png")
        self.oval_button=Button(self.shapes_area,width=30,height=30,relief=FLAT,bg="light cyan",borderwidth=0, highlightthickness=0, image=self.oval_image,command=self.on_ovalButton_pressed)
        self.oval_button.place(x=115, y=5)

        #creating star button
        self.star_image = PhotoImage(file="star.png")
        self.star_button=Button(self.shapes_area,width=30,height=30,relief=FLAT,bg="light cyan",borderwidth=0, highlightthickness=0, image=self.star_image,command=self.on_starButton_pressed)
        self.star_button.place(x=165, y=43)

        #creating pentagon button
        self.pentagon_image = PhotoImage(file="pentagon.png")
        self.pentagon_button=Button(self.shapes_area,width=30,height=30,relief=FLAT,bg="light cyan",borderwidth=0, highlightthickness=0, image=self.pentagon_image,command=self.on_pentagonButton_pressed)
        self.pentagon_button.place(x=65, y=43)

        #creating hexagon button
        self.hexagon_image = PhotoImage(file="hexagon.png")
        self.hexagon_button=Button(self.shapes_area,width=30,height=30,relief=FLAT,bg="light cyan",borderwidth=0, highlightthickness=0, image=self.hexagon_image,command=self.on_hexagonButton_pressed)
        self.hexagon_button.place(x=115, y=43)

        #creating npolygon button
        self.npolygon_image = PhotoImage(file="npolygon.png")
        self.npolygon_button=Button(self.shapes_area,width=30,height=30,relief=FLAT,bg="light cyan",borderwidth=0, highlightthickness=0, image=self.npolygon_image,command=self.on_polygonButton_pressed)
        self.npolygon_button.place(x=215, y=43)

        #creating line button
        self.line_image = PhotoImage(file="line.png")
        self.line_button=Button(self.shapes_area,width=30,height=30,relief=FLAT,bg="light cyan",borderwidth=0, highlightthickness=0, image=self.line_image,command=self.on_lineButton_pressed)
        self.line_button.place(x=15, y=43)
       
        #creating select color button
        self.select_color_image = PhotoImage(file="colorwheel.png")
        self.select_color_button=Button(self.colors_area,width=60,height=60,relief=FLAT,bg="light cyan",borderwidth=0, highlightthickness=0, image=self.select_color_image,command=self.select_color)
        self.select_color_button.place(x=270, y=8)

        #creating color1 button
        self.select_color1_button=Button(self.color1_area,width=7,height=3,relief=RIDGE,bg=self.brush_color,state="disabled")
        self.select_color1_button.place(x=10, y=11)

        #creating color2 button
        self.select_color2_button=Button(self.color2_area,width=7,height=3,relief=RIDGE,bg=self.eraser_color,state="disabled")
        self.select_color2_button.place(x=10, y=11)

        #creating red color button
        self.red_color_button=Button(self.colors_area,width=2,height=1,relief=RIDGE,bg="red",command=lambda:self.set_color("red"))
        self.red_color_button.place(x=10, y=5)
        #creating green color button
        self.green_color_button=Button(self.colors_area,width=2,height=1,relief=RIDGE,bg="green",command=lambda:self.set_color("green"))
        self.green_color_button.place(x=40, y=5)
        #creating blue color button
        self.blue_color_button=Button(self.colors_area,width=2,height=1,relief=RIDGE,bg="blue",command=lambda:self.set_color("blue"))
        self.blue_color_button.place(x=70, y=5)
        #creating black color button
        self.black_color_button=Button(self.colors_area,width=2,height=1,relief=RIDGE,bg="black",command=lambda:self.set_color("black"))
        self.black_color_button.place(x=100, y=5)
        #creating yellow color button
        self.yellow_color_button=Button(self.colors_area,width=2,height=1,relief=RIDGE,bg="yellow",command=lambda:self.set_color("yellow"))
        self.yellow_color_button.place(x=130, y=5)
        #creating pink color button
        self.pink_color_button=Button(self.colors_area,width=2,height=1,relief=RIDGE,bg="pink",command=lambda:self.set_color("pink"))
        self.pink_color_button.place(x=160, y=5)
        #creating purple color button
        self.purple_color_button=Button(self.colors_area,width=2,height=1,relief=RIDGE,bg="purple",command=lambda:self.set_color("purple"))
        self.purple_color_button.place(x=190, y=5)
        #creating grey color button
        self.grey_color_button=Button(self.colors_area,width=2,height=1,relief=RIDGE,bg="grey",command=lambda:self.set_color("grey"))
        self.grey_color_button.place(x=220, y=5)
        #creating brown color button
        self.brown_color_button=Button(self.colors_area,width=2,height=1,relief=RIDGE,bg="brown",command=lambda:self.set_color("brown"))
        self.brown_color_button.place(x=10, y=43)
        #creating white color button
        self.white_color_button=Button(self.colors_area,width=2,height=1,relief=RIDGE,bg="white",command=lambda:self.set_color("white"))
        self.white_color_button.place(x=40, y=43)
        #creating cyan color button
        self.cyan_color_button=Button(self.colors_area,width=2,height=1,relief=RIDGE,bg="cyan",command=lambda:self.set_color("cyan"))
        self.cyan_color_button.place(x=70, y=43)
        #creating lightgreen color button
        self.lightgreen_color_button=Button(self.colors_area,width=2,height=1,relief=RIDGE,bg="light green",command=lambda:self.set_color("light green"))
        self.lightgreen_color_button.place(x=100, y=43)
        #creating lightblue color button
        self.lightblue_color_button=Button(self.colors_area,width=2,height=1,relief=RIDGE,bg="light blue",command=lambda:self.set_color("light blue"))
        self.lightblue_color_button.place(x=130, y=43)
        #creating lightgrey color button
        self.lightgrey_color_button=Button(self.colors_area,width=2,height=1,relief=RIDGE,bg="light grey",command=lambda:self.set_color("light grey"))
        self.lightgrey_color_button.place(x=160, y=43)
        #creating orange color button
        self.orange_color_button=Button(self.colors_area,width=2,height=1,relief=RIDGE,bg="orange",command=lambda:self.set_color("orange"))
        self.orange_color_button.place(x=190, y=43)
        #creating magenta color button
        self.magenta_color_button=Button(self.colors_area,width=2,height=1,relief=RIDGE,bg="magenta",command=lambda:self.set_color("magenta"))
        self.magenta_color_button.place(x=220, y=43)

        #bind the functions to the mouse event
        self.canvas.bind("<B1-Motion>",self.brush_draw)
        self.canvas.bind("<ButtonRelease-1>",self.brush_draw_end)

        #creating objects
        self.eraser = Eraser(self.canvas,self.eraser_color,self.brush_width)
        self.brush = Brush(self.canvas,self.brush_color,self.brush_width)

        #creating enter area for width
        self.brush_width_entry = Entry(self.size_area, width=20)
        self.brush_width_entry.place(x=5,y=60)
        self.increase_image = PhotoImage(file="plus.png")
        self.increase_button=Button(self.size_area,width=10,height=10,relief=FLAT,borderwidth=0,bg="light cyan", activebackground="light cyan", image=self.increase_image,command=self.increase_brush_width)
        self.increase_button.place(x=135, y=60)
        self.decrease_image = PhotoImage(file="thinline.png")
        self.decrease_button=Button(self.size_area,width=10,height=10,relief=FLAT,bg="light cyan",borderwidth=0, activebackground="light cyan", image=self.decrease_image,command=self.decrease_brush_width)
        self.decrease_button.place(x=135, y=70)
        self.update_brush_width_entry()


    def clear_canvas(self):
        self.canvas.delete("all")

    def unbind(self):
        self.canvas.unbind("<Button-1>")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")
        
    def run(self):
        self.screen.mainloop()

    def set_brush_width(self,width):
        self.brush_width=width
        
    def set_color(self,color):
        if self.BrushActive==True:
            self.brush_color=color
            self.select_color1_button.config(bg=color)
        else:
            self.eraser_color=color
            self.select_color2_button.config(bg=color)

#bizeir Curve
    def on_bazierCurveButton_pressed(self):
        self.unbind()
        self.canvas.bind('<Button-1>', self.draw_bazierline)

    def draw_bazierline(self,event):
        self.start_x = event.x
        self.start_y = event.y
        self.curve = self.canvas.create_line(self.start_x, self.start_y, self.start_x, self.start_y, smooth=True, width=self.brush_width,fill=self.brush_color)
        self.canvas.bind('<B1-Motion>', self.move_bazierline)
        self.canvas.bind('<ButtonRelease-1>', self.end_bazierline)

    def move_bazierline(self,event):
        self.canvas.coords(self.curve, self.start_x, self.start_y, event.x, event.y)

    def end_bazierline(self,event):
        self.unbind()
        self.last_x = event.x
        self.last_y = event.y
        self.start_curve(event,event.x,event.y)

    def start_curve(self,event,x,y):
        self.control1_x = event.x
        self.control1_y = event.y
        self.canvas.bind('<B1-Motion>', self.move_curve1)
        self.canvas.bind('<ButtonRelease-1>', self.end_curve1)
    
    def move_curve1(self,event):
        self.control1_x = event.x
        self.control1_y = event.y
        self.canvas.delete(self.curve)
        self.curve = self.canvas.create_line(self.start_x, self.start_y, self.control1_x, self.control1_y, self.last_x, self.last_y, smooth=True, width=self.brush_width,fill=self.brush_color)
 
    def end_curve1(self,event):
        self.canvas.unbind('<B1-Motion>')
        self.canvas.unbind('<ButtonRelease-1>')
        self.canvas.bind('<B1-Motion>', self.move_curve2)
        self.canvas.bind('<ButtonRelease-1>', self.end_curve2)
    
    def move_curve2(self,event):
        self.control2_x = event.x
        self.control2_y = event.y
        self.canvas.delete(self.curve)
        self.curve = self.canvas.create_line(self.start_x, self.start_y, self.control1_x, self.control1_y, self.control2_x, self.control2_y, self.last_x, self.last_y, smooth=True, width=2, fill=self.brush_color)
    
    def end_curve2(self,event):
        self.control1_x = None
        self.control1_y = None
        self.control2_x = None
        self.control2_y = None
        self.last_x = None
        self.last_y = None
        self.start_x = None
        self.start_y = None
        self.canvas.bind('<Button-1>', self.draw_bazierline)
        self.canvas.unbind('<B1-Motion>')
        self.canvas.unbind('<ButtonRelease-1>')

#change brush width   
    def increase_brush_width(self):
        self.brush_width += 1
        self.update_brush_width_entry()

    def decrease_brush_width(self):
        if self.brush_width > 1:
            self.brush_width -= 1
            self.update_brush_width_entry()

    def update_brush_width_entry(self):
        self.brush_width_entry.delete(0, END)
        self.brush_width_entry.insert(0, str(self.brush_width))

#color picker
    def on_selectClrButton_pressed(self):
        self.unbind()
        self.canvas.bind("<Button-1>", self.get_pixel_color)

    def get_pixel_color(self, event):
        image=ImageGrab.grab()
        pixel_color = image.getpixel((event.x+6, event.y+168))
        Color= webcolors.rgb_to_name(pixel_color)
        self.brush_color=Color
        if self.BrushActive==True:
            self.brush_color=Color
            self.select_color1_button.config(bg=Color)
        else:
            self.eraser_color=Color
            self.select_color2_button.config(bg=Color)

#zoom the canvas
    def on_ZoomInButton_pressed(self):
        self.unbind()
        self.canvas.bind("<Button-1>", self.zoomIn)

    def zoomIn(self,event):
        print("zoomin")
        self.canvas.scale("all", event.x, event.y, 1.2, 1.2)#1.2 0.8

    def on_ZoomOutButton_pressed(self):
        self.unbind()
        self.canvas.bind("<Button-1>", self.zoomOut)

    def zoomOut(self,event):
        print("zoomout")
        self.canvas.scale("all",event.x, event.y, 0.8, 0.8)

#save and load
    def save_canvas(self):
        file_path = filedialog.asksaveasfilename(defaultextension='.png')
        if file_path:
            x=self.screen.winfo_rootx()+self.canvas.winfo_x()
            y=self.screen.winfo_rooty()+self.canvas.winfo_y()
            x1=x+self.canvas.winfo_width()
            y1=y+self.canvas.winfo_height()-50
            self.image=ImageGrab.grab().crop((x, y, x1, y1))
            self.image.save(file_path)

    def load_canvas(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            image = Image.open(file_path)
            print(file_path)
            self.canvas.delete("all")
            self.canvas.image = ImageTk.PhotoImage(image)
            self.canvas.create_image(0, 0, anchor=NW, image=self.canvas.image)
   
#select area
    def on_selectareaButton_pressed(self):
        self.unbind()
        self.canvas.bind("<Button-1>", self.start_selection)
        self.canvas.bind("<B1-Motion>", self.select_area_update)
        self.canvas.bind("<ButtonRelease-1>", self.end_selection)
    
    def start_selection(self, event):
        if self.isStartArea:
            self.start_x = event.x
            self.start_y = event.y
            print("Event Started")
            self.isStartArea = False
    
    def select_area_update(self, event):
        if self.select_rect is not None:
            self.canvas.delete(self.select_rect)
        self.select_rect = self.canvas.create_rectangle(self.start_x, self.start_y, event.x, event.y, outline="red", dash=(4, 4))

    
    def end_selection(self, event):
        self.canvas.delete(self.select_rect)
        self.select_rect = None
        self.canvas.update()

        self.end_x = event.x
        self.end_y = event.y
        
        x1 = self.screen.winfo_rootx() + min(self.start_x, self.end_x)
        y1 = self.screen.winfo_rooty() + min(self.start_y, self.end_y)+134 #84
        x2 = self.screen.winfo_rootx() + max(self.start_x, self.end_x)
        y2 = self.screen.winfo_rooty() + max(self.start_y, self.end_y)+130 #80
        selected_area = ImageGrab.grab(bbox=(x1, y1, x2, y2))
        self.copied_image.append(ImageTk.PhotoImage(selected_area))
        self.copied_image_count+=1
    
        self.canvas.create_rectangle(self.start_x, self.start_y, self.end_x, self.end_y, outline="", fill="white")
        self.Im = self.canvas.create_image(self.start_x, self.start_y, image=self.copied_image[self.copied_image_count-1], anchor="nw")
        self.canvas.update()
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.canvas.bind("<B1-Motion>", self.paste_area)
        self.canvas.bind("<ButtonRelease-1>", self.paste_area_end)
    
    def paste_area(self, event):
        dx = event.x - self.start_x
        dy = event.y - self.start_y
        self.canvas.move(self.Im, dx, dy)
        self.start_x = event.x
        self.start_y = event.y

    
    def paste_area_end(self, event):
        dx = event.x - self.start_x
        dy = event.y - self.start_y
        self.canvas.move(self.Im, dx, dy)
        print("Event Pasted Ended", dx, dy)
        self.start_x=0
        self.start_y=0
        self.end_x, self.end_y=0,0
        self.isStartArea = True
        self.canvas.unbind("<Button-1>")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.canvas.bind("<B1-Motion>", self.brush_draw)
        self.canvas.bind("<ButtonRelease-1>", self.brush_draw_end)
   
#fill color
    def on_paintbucketButton_pressed(self):
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.canvas.bind("<Button-1>",self.on_canvas_click)

    def on_canvas_click(self, event):
        fill_color = self.brush_color
        x = event.x
        y = event.y
        image = ImageGrab.grab()
        pixel_color = image.getpixel((event.x + 6, event.y + 168))
        current_color = webcolors.rgb_to_name(pixel_color)

        checked_pixels = set()

        shape_ids = [obj.shape_id for obj in self.circles]
        clicked_item = self.canvas.find_overlapping(x, y, x, y)
        print(clicked_item)

        if clicked_item in shape_ids:
            self.canvas.itemconfig(clicked_item, fill=fill_color)
            return

        if current_color != fill_color:
            stack = [(x, y)]
            while stack:
                x, y = stack.pop()
                if (x, y) in checked_pixels:
                    continue
                
                checked_pixels.add((x, y))

                p_color = image.getpixel((x + 8, y + 161))
                color = webcolors.rgb_to_name(p_color)
                if color == current_color:
                    self.canvas.create_rectangle(x, y, x + 1, y + 1, fill=fill_color, outline="")
                    stack.extend([(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)])
 
#brush drawing
    def on_paintbrushButton_pressed(self):
        self.BrushActive = True
        self.unbind()
        self.canvas.bind("<B1-Motion>",self.brush_draw)
        self.canvas.bind("<ButtonRelease-1>",self.brush_draw_end)

    def brush_draw(self,event):
        self.last_x,self.last_y=self.brush.draw(event,self.last_x,self.last_y,self.brush_color,self.brush_width)

    def brush_draw_end(self,event):
        self.last_x,self.last_y=self.brush.draw_end(event)

#eraser drawing
    def on_eraserButton_pressed(self):
        self.BrushActive = False
        self.unbind()
        self.canvas.bind("<B1-Motion>",self.eraser_draw)
        self.canvas.bind("<ButtonRelease-1>",self.eraser_draw_end)

    def eraser_draw(self,event):
        self.last_x,self.last_y=self.eraser.draw(event,self.last_x,self.last_y,self.eraser_color,self.brush_width)

    def eraser_draw_end(self,event):
        self.last_x,self.last_y=self.eraser.draw_end(event)

#circle drawing
    def on_circleButton_pressed(self):
        self.unbind()
        self.canvas.bind("<B1-Motion>",self.draw_circle)
        self.canvas.bind("<ButtonRelease-1>",self.draw_circle_end)

    def draw_circle(self,event):
        if self.isFirst==True:
            circle = Circle(self.canvas,self.last_x,self.last_y,self.brush_width)
            self.circles.append(circle)
            self.circle_no=self.circle_no+1
            print("Circle created")
        self.isFirst=False
        self.last_x,self.last_y,self.shape_id=self.circles[self.circle_no-1].draw(event,self.brush_color)

    def draw_circle_end(self,event):
        self.last_x,self.last_y,self.shape_id=self.circles[self.circle_no-1].draw_end()
        self.shape_id=None
        self.isFirst=True

#rectangle drawing
    def on_rectangleButton_pressed(self):
        self.unbind()
        self.canvas.bind("<B1-Motion>",self.draw_rectangle)
        self.canvas.bind("<ButtonRelease-1>",self.draw_rectangle_end)

    def draw_rectangle(self,event):
        if self.isFirst==True:
            rectangle = Rectangle(self.canvas,self.last_x,self.last_y,self.brush_width)
            self.circles.append(rectangle)
            self.circle_no=self.circle_no+1
            print("Rectangle created")
        self.isFirst=False
        self.last_x,self.last_y,self.shape_id=self.circles[self.circle_no-1].draw(event,self.brush_color)

    def draw_rectangle_end(self,event):
        self.last_x,self.last_y,self.shape_id=self.circles[self.circle_no-1].draw_end()
        self.isFirst=True

#square drawing
    def on_squareButton_pressed(self):
        self.unbind()
        self.canvas.bind("<B1-Motion>",self.draw_square)
        self.canvas.bind("<ButtonRelease-1>",self.draw_square_end)

    def draw_square(self,event):
        if self.isFirst==True:
            square = Square(self.canvas,self.last_x,self.last_y,self.brush_width)
            self.circles.append(square)
            self.circle_no=self.circle_no+1
        self.isFirst=False
        self.last_x,self.last_y,self.shape_id=self.circles[self.circle_no-1].draw(event,self.brush_color)

    def draw_square_end(self,event):
        self.last_x,self.last_y,self.shape_id=self.circles[self.circle_no-1].draw_end()
        self.isFirst=True

#oval drawing
    def on_ovalButton_pressed(self):
        self.unbind()
        self.canvas.bind("<B1-Motion>",self.draw_oval)
        self.canvas.bind("<ButtonRelease-1>",self.draw_oval_end)

    def draw_oval(self,event):
        if self.isFirst==True:
            oval = Oval(self.canvas,self.last_x,self.last_y,self.brush_width)
            self.circles.append(oval)
            self.circle_no=self.circle_no+1
        self.isFirst=False
        self.last_x,self.last_y,self.shape_id=self.circles[self.circle_no-1].draw(event,self.brush_color)

    def draw_oval_end(self,event):
        self.last_x,self.last_y,self.shape_id=self.circles[self.circle_no-1].draw_end()
        self.isFirst=True

#pentagon drawing
    def on_pentagonButton_pressed(self):
        self.unbind()
        self.canvas.bind("<B1-Motion>",self.draw_pentagon)
        self.canvas.bind("<ButtonRelease-1>",self.draw_pentagon_end)

    def draw_pentagon(self,event):
        if self.isFirst==True:
            pentagon = Pentagon(self.canvas,self.last_x,self.last_y,self.brush_width)
            self.circles.append(pentagon)
            self.circle_no=self.circle_no+1
        self.isFirst=False
        self.last_x,self.last_y,self.shape_id=self.circles[self.circle_no-1].draw(event,self.brush_color)

    def draw_pentagon_end(self,event):
        self.last_x,self.last_y,self.shape_id=self.circles[self.circle_no-1].draw_end()
        self.isFirst=True

#hexagon drawing
    def on_hexagonButton_pressed(self):
        self.unbind()
        self.canvas.bind("<B1-Motion>",self.draw_hexagon)
        self.canvas.bind("<ButtonRelease-1>",self.draw_hexagon_end)

    def draw_hexagon(self,event):
        if self.isFirst==True:
            hexagon = Hexagon(self.canvas,self.last_x,self.last_y,self.brush_width)
            self.circles.append(hexagon)
            self.circle_no=self.circle_no+1
        self.isFirst=False
        self.last_x,self.last_y,self.shape_id=self.circles[self.circle_no-1].draw(event,self.brush_color)

    def draw_hexagon_end(self,event):
        self.last_x,self.last_y,self.shape_id=self.circles[self.circle_no-1].draw_end()
        self.isFirst=True

#drawing n polygon
    def on_polygonButton_pressed(self):
        self.unbind()
        self.canvas.bind("<B1-Motion>",self.draw_polygon)
        self.canvas.bind("<ButtonRelease-1>",self.draw_polygon_end)
        value = simpledialog.askstring("Input", "Enter sides:")
        if value:
            print("User entered:", value)
            self.polygon_side=int(value)
        else:
            print("No value entered.")

    def draw_polygon(self,event):
        if self.isFirst==True:
            polygon = Polygon(self.canvas,self.last_x,self.last_y,self.brush_width,self.polygon_side)
            self.circles.append(polygon)
            self.circle_no=self.circle_no+1
        self.isFirst=False
        self.last_x,self.last_y,self.shape_id=self.circles[self.circle_no-1].draw(event,self.brush_color)

    def draw_polygon_end(self,event):
        self.last_x,self.last_y,self.shape_id=self.circles[self.circle_no-1].draw_end()
        self.isFirst=True


#star drawing
    def on_starButton_pressed(self):
        self.unbind()
        self.canvas.bind("<B1-Motion>",self.draw_star)
        self.canvas.bind("<ButtonRelease-1>",self.draw_star_end)

    def draw_star(self,event):
        if self.isFirst==True:
            star = Star(self.canvas,self.last_x,self.last_y,self.brush_width)
            self.circles.append(star)
            self.circle_no=self.circle_no+1
        self.isFirst=False
        self.last_x,self.last_y,self.shape_id=self.circles[self.circle_no-1].draw(event,self.brush_color)

    def draw_star_end(self,event):
        self.last_x,self.last_y,self.shape_id=self.circles[self.circle_no-1].draw_end()
        self.isFirst=True


#triangle drawing
    def on_triangleButton_pressed(self):
        self.unbind()
        self.canvas.bind("<B1-Motion>",self.draw_triangle)
        self.canvas.bind("<ButtonRelease-1>",self.draw_triangle_end)

    def draw_triangle(self,event):
        if self.isFirst==True:
            triangle = Triangle(self.canvas,self.last_x,self.last_y,self.brush_width)
            self.circles.append(triangle)
            self.circle_no=self.circle_no+1
        self.isFirst=False
        self.last_x,self.last_y,self.shape_id=self.circles[self.circle_no-1].draw(event,self.brush_color)

    def draw_triangle_end(self,event):
        self.last_x,self.last_y,self.shape_id=self.circles[self.circle_no-1].draw_end()
        self.isFirst=True

#Line drawing
    def on_lineButton_pressed(self):
        self.unbind()
        self.canvas.bind("<B1-Motion>",self.draw_line)
        self.canvas.bind("<ButtonRelease-1>",self.draw_line_end)

    def draw_line(self,event):
        if self.isFirst==True:
            line = Line(self.canvas,self.last_x,self.last_y,self.brush_width)
            self.circles.append(line)
            self.circle_no=self.circle_no+1
        self.isFirst=False
        self.last_x,self.last_y,self.shape_id=self.circles[self.circle_no-1].draw(event,self.brush_color)

    def draw_line_end(self,event):
        self.last_x,self.last_y,self.shape_id=self.circles[self.circle_no-1].draw_end()
        self.isFirst=True

    def select_color(self):
        selected_color = colorchooser.askcolor()
        print(selected_color[1])
        if selected_color[1]!=None:
            self.brush_color=selected_color[1]
            if self.BrushActive==True:
                self.select_color1_button.config(bg=self.brush_color)
            else:
                self.select_color2_button.config(bg=self.brush_color)

PaintApp(1400,800,"Paint App").run()
   
