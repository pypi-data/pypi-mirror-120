import cv2
import numpy as np
import colour


# Gives the inner glow of the neon light
def InnerGlow(height, width, light_color, Lradius, Iradius, edges, back, first, last, SavePath):

    temp=[]
    k=0

    # Brightness intesity
    l = 1.0

    # Converst an list of colors from the library colour to a numpy array
    if isinstance(light_color[0], colour.Color):
        for i in range(len(light_color)):
            light_color[i]=(light_color[i].rgb)
            light_color[i] = list(light_color[i])
            light_color[i].reverse()
        light_color=np.array(light_color)*255

    # Converts a single color represented like [.. , .. , ..] to a numpy array
    elif isinstance(light_color[0], int):
        temp.append(light_color)
        light_color = np.array(temp)

    # Converts a list of lists, [[.. , .. , ..] .. [.. , .. , ..]] with values from 0 to 1 to a numpy array with values from 0 to 255
    elif isinstance(light_color[0], list) and np.all(light_color) <=1:
        light_color=np.array(light_color)*255

    # Converts a list of lists, [[.. , .. , ..] .. [.. , .. , ..]] to a numpy array
    elif isinstance(light_color[0], list):
        light_color=np.array(light_color)
    
    # Creates step to change color if there is more than one
    y=int((last - first + 1)/(len(light_color)))

    # Creates the inner glow alog the line
    while Iradius > 0:
        for i in range(first, last+1):
            for j in range(width):
                if edges[i][j] != 0:
                    back = cv2.circle(back, (j,i), Iradius + Lradius, light_color[k] * l, 1)

            if i >= y * (k+1) + first and k < len(light_color)-1:
                k = k+1 
        k = 0
        Iradius = Iradius - 1
        l = l * 0.8
    
    OutputPathInner = SavePath + '\\InnerGlow.jpg'
    cv2.imwrite(OutputPathInner, back)
    return back