import cv2
import numpy as np
import colour

def AddLine(height, width, line_color, Lradius, edges, InnerGlow, first, last, SavePath):

    temp=[]
    k=0
    
    # Converst an list of colors from the library colour to a numpy array
    if isinstance(line_color[0], colour.Color):
        for i in range(len(line_color)):
            line_color[i]=(line_color[i].rgb)
            line_color[i] = list(line_color[i])
            line_color[i].reverse()
        line_color=np.array(line_color)*255

    # Converts a single color represented like [.. , .. , ..] to a numpy array
    elif isinstance(line_color[0], int):
        temp.append(line_color)
        line_color = np.array(temp)

    # Converts a list of lists, [[.. , .. , ..] .. [.. , .. , ..]] with values from 0 to 1 to a numpy array with values from 0 to 255
    elif isinstance(line_color[0], list) and np.all(line_color) <=1:
        line_color=np.array(line_color)*255

    # Converts a list of lists, [[.. , .. , ..] .. [.. , .. , ..]] to a numpy array
    elif isinstance(line_color[0], list):
        line_color=np.array(line_color)

    # Creates step to change color if there is more than one
    x=int((last - first + 1)/(len(line_color)))
    
    # Adds thickness to the line
    for i in range(first, last+1):
        for j in range(width):
            if edges[i][j] != 0:
                InnerGlow = cv2.circle(InnerGlow, (j,i), Lradius, line_color[k] * 1.0, -1)

        if i >= x * (k+1) + first and k < len(line_color)-1:
            k = k+1 
            
    OutputPathLine = SavePath + '\\Line.jpg'
    cv2.imwrite(OutputPathLine, InnerGlow)
    return InnerGlow
