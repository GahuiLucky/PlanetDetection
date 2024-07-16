import cv2 as cv                                                                    # Import OpenCV for classic image processing
import numpy as np                                                                  # Import Numpy for basic Vector and Matrix calculation
from read_capturedevice import Camera                                               # Import Kamera function to open capture device
from define_planets import isPlanet                                                 # Import isPlanet for statistical evaluation
from planet_functions import CountLines, cleanarray, CountContours, Create4ZeroArrays


hue_array, crater_array, line_array = Create4ZeroArrays(11, dType=np.float16)
counter_array = 0

while(1):        
        # Get camera frame
        capture, camera = Camera(ID=1,                                              # Open camera with id=1
                                 Preference=cv.CAP_ANY)                             # Gives an API Preference
        cv.imshow("Camera", camera)                                                 # Show original camera frame

        # Preparing original Image        
        hsv = cv.cvtColor(camera, cv.COLOR_RGB2HSV)                                 # Convert to hsv
        gray = cv.cvtColor(camera, cv.COLOR_RGB2GRAY)                               # Convert to grayscale
        canny = cv.Canny(gray, 0, 100)                                              # Convert to canny
        
        # Search for Circles 
        detected_circles = cv.HoughCircles(image=gray,                              # Image to look for circles
                                           method=cv.HOUGH_GRADIENT_ALT,            # Method uses the gradient information of the edges
                                           dp=3,                                    # Inverse ratio of the accumulator resolution to the image resolution
                                           minDist=100,                             # Minimum distance between 2 detected circles
                                           param1=350,                              # First method-specific parameter
                                           param2=0.65,                             # Second method-specific parameter
                                           minRadius=65,                            # Minimum radius of detected circles
                                           maxRadius=camera.shape[0]//2)            # Maximum radius of detected circles (max. half size of image width)

        if detected_circles is not None:
            detected_circles = np.uint16(np.around(detected_circles))               # Convert detected circles to 16 Bit integer
            for center in detected_circles[0, :]:
                a, b, r = center[0], center[1], center[2]

                # Create shape of Mask
                mask = np.zeros(hsv.shape[:2], dtype=np.uint8)                      # Create Mask with Values of (0,0,0) in shape of the circle
                cv.circle(mask, (a, b), r, (255, 255, 255), thickness=-1)           # Create Mask with Values of (255,255,255) in shape of the circle

                # Create Masks
                masked_hsv = cv.bitwise_and(hsv, hsv, mask=mask)                    # HSV Mask                
                masked_canny = cv.bitwise_and(canny, canny, mask=mask)              # Canny Mask                
                masked_gray = cv.bitwise_and(gray, gray, mask=mask)                 # Greyscale Mask
                
                # Extract Values in Circle boundary
                hue_values = masked_hsv[:, :, 0][mask == 255]                       # Get Hue Values in Circle Boundary
                sat_values = masked_hsv[:, :, 1][mask == 255]                       # Get Saturation Values in Circle Boundary

                # Find Contours
                contours, _ = cv.findContours(image=masked_canny,                   # Find contours in masked frame  
                                              mode=cv.RETR_EXTERNAL,                # Contour retrieval mode
                                              method=cv.CHAIN_APPROX_SIMPLE)        # Contour approximation method

                # Count the Crater
                crater_count = CountContours(contours,                              # Count contours
                                             MinContourLength=5,                    # Minimum contour length
                                             MaxContourLength=500)                  # Maximum contour length    

                # Find and Count the Lines
                lines = cv.HoughLinesP(image=masked_canny,                          # Find lines in masked frame
                                       rho=1,                                       # Distance resolution of the accumulator in pixels
                                       theta=np.pi/90,                              # Angle resolution of the accumulator in radians
                                       threshold=50,                                # Accumulator threshold parameter. Return just lines with votes > threshold
                                       lines=None,                                  # Output vector of lines
                                       minLineLength=r*2/4,                         # Minimum line length
                                       maxLineGap=3)                                # Maximum allowed gap between points on the same line to link them
                line_count = CountLines(lines, minLineLength=5)                     # Counts lines with minimum line length of 5 Pixel         
                
                # Delete Hue-Values with low Saturation Value
                new_array1,counter=cleanarray(sat_values,minValue=5)                # Sets values in array < 5 to 0 and values > 5 to 1                          
                new_array2=list(new_array1*hue_values)                              # Multiplies array with binary array to get rid of low valued hue values
                new_array3= [x for x in new_array2 if x != 0 ]

                # Calculate mean of hue and saturation
                average_hue = np.mean(new_array3)                                   # Calculates mean hue of masked frame
                
                # Put Element in Array
                hue_array[counter_array] = average_hue                              # Puts one element of average hue in the hue array
                crater_array[counter_array] = crater_count                          # Puts one element of crater count in the crater array
                line_array[counter_array] = line_count                              # Puts one element of line count in the line array

                if counter_array == 10:                                             # Every 10th iteration the programm evalutates which planet is detected
                    counter_array = 0
                    # Terminate which planet is seen in the frame  
                    Planet = isPlanet(average_hue=np.mean(hue_array[1:10]),         
                                      crater_count=np.mean(crater_array[1:10]),         
                                      average_lines=np.mean(line_array[1:10]))      
                    
                    planet_output = cv.putText(img=camera,                          # Puts Planetname in camera frame
                                                text=Planet,                        # Text string to be drawn
                                                org=(50,50),                        # Bottom-left corner of the text string in the image
                                                fontFace=cv.FONT_HERSHEY_SIMPLEX,   # Font type
                                                fontScale=2,                        # Font scale factor that is multiplied by the font-specific base size
                                                color=(0, 0, 255),                  # Text color in RGB
                                                thickness=2)                        # Thickness of the lines used to draw a text
                    
                    cv.circle(camera, (a, b), r, (255, 255, 255), 2)                # paint circle around detected circle
                    cv.circle(camera, (a, b), 2, (255, 255, 255), 3)                # paint point in origin of detected circle 
                    cv.imshow("Output", planet_output)                              # shows output frame
                counter_array=counter_array+1                                       # increment counter by 1
               
        if cv.waitKey(1) & 0xFF == ord("q"):                                        # Program runs till the button "q" is pressed 
            capture.release()                                                       # Releases the camera (capture device)
            cv.destroyAllWindows()                                                  # Closes all windows
            break


