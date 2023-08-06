import os
import comtypes.client
import comtypes
import cv2
from NeonLightEffect import eraser

def NeonLight(first_h, last_h, first_w, last_w, edges, Lradius, SavePath):

    # Opens saved files
    OutputPathOuter1 = SavePath + '\\OuterGlow1.png'
    OutputPathOuter2 = SavePath + '\\OuterGlow2.png'
    OutputPathLine = SavePath + '\\Line.jpg'

    # Opens photoshop
    psApp = comtypes.client.CreateObject('Photoshop.Application', dynamic = True)
    psApp.Preferences.RulerUnits = 1

    # Opens second layer of outer glow and applies blur and pastes on background
    psApp.Open(OutputPathOuter2)
    doc1 = psApp.Application.ActiveDocument
    doc1.ActiveLayer.ApplyGaussianBlur(Lradius*3)
    blur=doc1.ActiveLayer.Copy()
    psApp.Open(OutputPathLine)
    doc2 = psApp.Application.ActiveDocument
    #Makes sure it pastes in the right position
    selRegion= [[first_w,first_h], [first_w, last_h], [last_w, last_h], [last_w, first_h]]
    doc2.Selection.select(selRegion)
    doc2.Paste()
    doc1.Close(2)

    # Opens first layer of outer glow and applies blur
    psApp.Open(OutputPathOuter1)
    doc1 = psApp.Application.ActiveDocument
    doc1.ActiveLayer.ApplyGaussianBlur(Lradius*1.5)
    options = comtypes.client.CreateObject("Photoshop.PNGSaveOptions", dynamic = True)
    options.interlaced = False
    doc1.SaveAs(OutputPathOuter1, options, True)
    doc1.Close(2)
    outer_glow=cv2.imread(OutputPathOuter1, cv2.IMREAD_UNCHANGED)

    #Erases the blur that covers the middle line and saves changes
    outer_glow = eraser(last_h, last_w, outer_glow, edges, Lradius, 0)
    cv2.imwrite(OutputPathOuter1, outer_glow)

    # Opens first layer of outer glow copies and pastes it in the background
    psApp.Open(OutputPathOuter1)
    doc1 = psApp.Application.ActiveDocument
    doc1.ActiveLayer.Copy()
    psApp.Open(OutputPathLine)
    doc2 = psApp.Application.ActiveDocument
    #Makes sure it pastes in the right position
    selRegion= [[first_w,first_h], [first_w, last_h], [last_w, last_h], [last_w, first_h]]
    doc2.Selection.select(selRegion)
    doc2.Paste()
    doc1.Close(2)

    # Saves final file
    jpg= SavePath + '\\NeonLight.jpg'
    options = comtypes.client.CreateObject("Photoshop.JPEGSaveOptions", dynamic = True)
    options.quality = 10
    doc2.SaveAs(jpg, options, True)
    doc2.Close(2)
    

