import cv2
import numpy as np 
from NeonLightEffect import AddLine, OuterGlow, InnerGlow, NeonLight 
#from Outer_glow import OuterGlow
#from Inner_glow import InnerGlow
#from PyPS import NeonLight
#import os

def GetLines(Edges, Background, Lradius, Iradius, line_color, light_color, SavePath):

    back = Background.copy()
    height, width = Edges.shape[:2]

    first_h = height
    last_h = 0
    first_w = width
    last_w=0

    # Find the region where the lines are
    for i in range(height):
        for j in range(width):
            if Edges[i][j] != 0:
                if i < first_h:
                    first_h = i
                if i >last_h:
                    last_h = i
                if j < first_w:
                    first_w = j
                if j > last_w:
                    last_w = j

    Inner_Glow = InnerGlow(height, width, light_color, Lradius, Iradius, Edges, back, first_h, last_h, SavePath)
    Line = AddLine(height, width, line_color, Lradius, Edges, Inner_Glow, first_h, last_h, SavePath)
    OuterGlow(height, width, light_color, Lradius, Iradius, back, Edges, first_h, last_h, SavePath)
    NeonLight(first_h, last_h, first_w, last_w, Edges, Lradius, SavePath)




