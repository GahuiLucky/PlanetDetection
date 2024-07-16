import cv2 as cv
import numpy as np
import math as mt

# Create array of zeros
def Create4ZeroArrays(ArrayLength, dType=np.float16):
    hue_array = np.zeros((ArrayLength), dtype=dType)
    crater_array = np.zeros((ArrayLength), dtype=dType)
    line_array = np.zeros((ArrayLength), dtype=dType)
    return hue_array, crater_array, line_array

# Count lines that: minLineLength < value
def CountLines (lines, minLineLength = 1):            
    line_count = 0
    if lines is not None:
        for line in lines:
            x_start = line[0,0]
            y_start = line[0,1]
            x_end = line[0,2]
            y_end = line[0,3]
            alpha = np.abs(mt.atan((y_end-y_start)/(x_end-x_start))*180/np.pi)                    
            line_length = np.abs((x_end-x_start)/mt.sin(alpha))
            if alpha > 45:
                alpha = np.abs(mt.atan((x_end-x_start)/(y_end-y_start))*180/np.pi)
                line_length = np.abs((y_end-y_start)/mt.sin(alpha))                            
            if line_length > minLineLength:
                line_count += 1
    return line_count

# Create binary array of zeros for value < minValue and ones for value > minValue
def cleanarray(array, minValue=5, counter_zeros=0,counter_ones=0):
    for i in range(0, len(array)):
        if array[i] < minValue:
            array[i] = 0
            counter_zeros = counter_zeros + 1
        if array[i] > minValue:
            array[i] = 1
            counter_ones = counter_ones + 1
    return array,counter_zeros

# Count contours that: MinContourLength < value < MaxContourLength
def CountContours(contours, MinContourLength, MaxContourLength):
    MinContourLength = 5
    MaxContourLength = 500
    contourcounter = 0
    for contour in contours:
        contour_length = cv.arcLength(contour, True)
        if contour_length > MinContourLength and contour_length < MaxContourLength:
            contourcounter += 1
    return contourcounter