import cv2
import time
import math

# Print OpenCV version for debugging
print(cv2.__version__)

# Initial position of the rectangle
X_Coordinate = 0
Y_Coordinate = 0

# Rectangle dimensions
rectangle_width = 50
rectangle_height = 50

# Display dimensions for the camera
dispW = 640
dispH = 480

# Flip method for NVIDIA camera
flip = 2

# Initialize movement vector
angle = math.radians(80)  # Start at 80 degrees
speed = 5
dx = speed * math.cos(angle)
dy = speed * math.sin(angle)

# Camera setup
# Uncomment the appropriate lines for your camera

# For NVIDIA Jetson (pyCamera):
#camSet = f'nvarguscamerasrc ! video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method={flip} ! video/x-raw, width={dispW}, height={dispH}, format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
#cam = cv2.VideoCapture(camSet)

# For Logitech camera:
#cam = cv2.VideoCapture(1)
#cam.set(cv2.CAP_PROP_FRAME_WIDTH, dispW)
#cam.set(cv2.CAP_PROP_FRAME_HEIGHT, dispH)

def reflect(dx, dy, normal_x, normal_y):
    """
    Calculate the reflection vector.
    
    Args:
    dx, dy: Components of the incident vector
    normal_x, normal_y: Components of the normal vector
    
    Returns:
    reflection_x, reflection_y: Components of the reflection vector
    """
    dot_product = dx * normal_x + dy * normal_y
    reflection_x = dx - 2 * dot_product * normal_x
    reflection_y = dy - 2 * dot_product * normal_y
    return reflection_x, reflection_y

# Main loop
while True:
    # Capture frame from the camera
    ret, frame = cam.read()
    
    if ret:
        # Update position
        X_Coordinate += dx
        Y_Coordinate += dy
        
        # Check for collisions with horizontal edges
        if X_Coordinate <= 0 or X_Coordinate >= dispW - rectangle_width:
            normal_x = -1 if X_Coordinate <= 0 else 1
            normal_y = 0
            dx, dy = reflect(dx, dy, normal_x, normal_y)
            
            # Add additional rotation for more dynamic movement
            angle = math.atan2(dy, dx)
            angle += math.radians(70)  # Add 70 degrees
            dx = speed * math.cos(angle)
            dy = speed * math.sin(angle)
            
            # Ensure rectangle stays within bounds
            X_Coordinate = max(0, min(X_Coordinate, dispW - rectangle_width))
        
        # Check for collisions with vertical edges
        if Y_Coordinate <= 0 or Y_Coordinate >= dispH - rectangle_height:
            normal_x = 0
            normal_y = -1 if Y_Coordinate <= 0 else 1
            dx, dy = reflect(dx, dy, normal_x, normal_y)
            
            # Add additional rotation for more dynamic movement
            angle = math.atan2(dy, dx)
            angle += math.radians(70)  # Add 70 degrees
            dx = speed * math.cos(angle)
            dy = speed * math.sin(angle)
            
            # Ensure rectangle stays within bounds
            Y_Coordinate = max(0, min(Y_Coordinate, dispH - rectangle_height))
        
        # Draw rectangle on the frame
        frame = cv2.rectangle(frame, (int(X_Coordinate), int(Y_Coordinate)),
                              (int(X_Coordinate + rectangle_width), int(Y_Coordinate + rectangle_height)),
                              (255, 0, 255), 3)
        cv2.imshow('Camera', frame)
        cv2.moveWindow('Camera', 0, 0)
        
        # Add a small delay to control frame rate
        time.sleep(0.03)
    
    # Check for 'q' key to quit the program
    if cv2.waitKey(1) == ord('q'):
        break

# Release resources
cam.release()
cv2.destroyAllWindows()
