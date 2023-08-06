import cv2
import numpy as np
import colour

# Creates a eraser
def eraser(height, width, ToErase, edges, radius, Opacity):
    
    # Creates an eraser
    eraser = np.array([0, 0, 0, Opacity])

    for i in range(height):
        for j in range(width):
            if edges[i][j] != 0:
                ToErase = cv2.circle(ToErase, (j,i), radius, eraser*1.0,-1)
    return ToErase

def OuterGlow(height,width,light_color, Lradius, Iradius, background, edges, first, last, SavePath):

    # Creates the background
    back = np.zeros((height, width, 4), dtype=background.dtype)
    back1 = np.zeros((height, width, 4), dtype=background.dtype)
    back2 = np.zeros((height, width, 4), dtype=background.dtype)
    back3 = np.zeros((height, width, 4), dtype=background.dtype)
    back4 = np.zeros((height, width, 4), dtype=background.dtype)

    k=0
    temp=[]

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
        light_color = temp

    # Converts a list of lists, [[.. , .. , ..] .. [.. , .. , ..]] with values from 0 to 1 to a numpy array with values from 0 to 255
    elif isinstance(light_color[0], list) and np.all(light_color) <=1:
        light_color=np.array(light_color)*255

    # Converts a list of lists, [[.. , .. , ..] .. [.. , .. , ..]] to a numpy array
    elif isinstance(light_color[0], list):
        light_color=np.array(light_color)

    # Adds the alpha channel
    b = np.full((len(light_color),4),255)
    b[:,:-1] = light_color
    light_color = np.array(b)

    # Creates step to change color if there is more than one
    x=int((last - first + 1)/len(light_color))

    # Adds the outer glow along the lines
    for i in range(first, last+1):
        for j in range(width):
            if edges[i][j] != 0:
                
                layer1 = cv2.circle(back1, (j,i), Lradius*5+Iradius, light_color[k]*1.0,-1)
                layer2 = cv2.circle(back2, (j,i), Lradius*10+Iradius, light_color[k]*1.0 ,-1)
                #layer3 = cv2.circle(back3, (j,i), Lradius*10, light_color[k]*1.0,-1)
                
        if i >= x * (k+1) + first and k < len(light_color)-1:
            k = k+1
    
    # Adds the different layers together with different opacities
    cv2.addWeighted(layer1, 0.8, back.copy(), 0.2, 0, layer1)
    cv2.addWeighted(layer2, 0.6, back.copy(), 0.4, 0, layer2)

    res = layer2[::]
    # Erases the outer glow over the line and inner glow
    res = eraser(height, width, res, edges, Lradius + Iradius, 0)
    OutputPathOuter = SavePath + '\\OuterGlow2.png'
    cv2.imwrite(OutputPathOuter, res)
    
    res = layer1[::]
    # Erases the outer glow over the line and inner glow
    res = eraser(height, width, res, edges, Lradius + Iradius, 0)
    OutputPathOuter = SavePath + '\\OuterGlow1.png'
    cv2.imwrite(OutputPathOuter, res)
    
    

    OutputPathOuter = SavePath + '\\OuterGlow1.png'
    cv2.imwrite(OutputPathOuter, res)
    
    
    
