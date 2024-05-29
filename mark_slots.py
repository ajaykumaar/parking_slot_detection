"""
Summary: Python code to mark empty parking slots and save it to a text file for inference
Author: Ajay
Date Created: 5/24/24
Last Updated: 5/24/24
"""

import cv2
import os
import re
# import numpy as np

slot_coordinates_path = "slot_coordinates.txt"
img_path = "empty_slot_img.png"
image = cv2.imread(img_path)

if os.path.exists(slot_coordinates_path):

    file = open("slot_coordinates.txt","r")
    print("[INFO] The file is not empty... displaying the contents of the file:")
    print(file.read())

else:
    file = open("slot_coordinates.txt","w")
    file.close()

# mark the points
points=[]
def mouse_callback(event, x, y, flags, param):
    
    if event == cv2.EVENT_LBUTTONDOWN:
        points.append(x)
        points.append(y)
        print("[INFO] Marked points: ", points)

parking_lot = 0
cv2.namedWindow("Parking area")
while True:

    if len(points) > 0:
        cv2.circle(image,(points[0],points[1]),2,(255,0,0),cv2.FILLED)

    cv2.imshow("Parking area", image)
    
    cv2.setMouseCallback("Parking area", mouse_callback)
    
    if cv2.waitKey(33) == ord('s'):

        parking_lot += 1

        print("[INFO] Number of parking lots marked: {}".format(parking_lot))
        
        with open('slot_coordinates.txt', 'a') as file:
            
            file.write("# " + str(points[0]) + " " + str(points[1]) + "\n")
            points.clear()

        continue
    
    if cv2.waitKey(5) == 27:
        
        print("[INFO] Exit drawing parking area.")
        
        break
    
cv2.destroyAllWindows()

# display the boundary for parking slot 
print("[INFO] Displaying marked boundaries for parking slots...")
length = 30
breadth = 30

file = open("slot_coordinates.txt","r")
coordinates = file.read()
hash_ids = [m.start() for m in re.finditer('#', coordinates)]

for i,hash_id in enumerate(hash_ids):
    center_pt = coordinates[hash_id+2: hash_id+9]
    start_point = [int(center_pt[:3]) + int(breadth/2), int(center_pt[4:]) - int(length/2)]
    end_point = [int(center_pt[:3]) - int(breadth/2), int(center_pt[4:]) + int(length/2)]
    image = cv2.rectangle(image, start_point, end_point, (0,255,0), 1) 

    #center point
    image = cv2.circle(image,(int(center_pt[:3]),int(center_pt[4:])),2,(255,0,0),cv2.FILLED)


cv2.imshow("parking slot boundaries", image)
cv2.waitKey(0)

cv2.destroyAllWindows()







