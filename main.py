import json
import cv2
import mediapipe as mp
from comparePose import evaluatePose

def drawCircle(frame, data, pose):
    # Define las coordenadas del centro del círculo y su radio
    center_coordinates = (60, 60)  # Cambia estas coordenadas según sea necesario
    
    radius = 50  # Cambia el radio según sea necesario

    # Dibuja el círculo en la imagen
    if evaluatePose(data, pose):
        newframe = cv2.circle(frame, center_coordinates, radius, (0,255,0), thickness=-1)
    else:
        newframe = cv2.circle(frame, center_coordinates, radius, (0,0, 255), thickness=-1)
            
    return newframe

mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

with mp_holistic.Holistic(
     static_image_mode=False,
     model_complexity=1) as holistic:

     while True:
          ret, frame = cap.read()
          if ret == False:
               break

          frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
          results = holistic.process(frame_rgb)

          # Mano izquieda (azul)
          mp_drawing.draw_landmarks(
               frame, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
               mp_drawing.DrawingSpec(color=(255, 255, 0), thickness=2, circle_radius=1),
               mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2))
          
          # Mano derecha (verde)
          mp_drawing.draw_landmarks(
               frame, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
               mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=1),
               mp_drawing.DrawingSpec(color=(57, 143, 0), thickness=2))
          
          # Postura
          mp_drawing.draw_landmarks(
               frame, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS,
               mp_drawing.DrawingSpec(color=(128, 0, 255), thickness=2, circle_radius=1),
               mp_drawing.DrawingSpec(color=(255, 255, 255), thickness=2))

          if results.pose_landmarks:
            pose_landmarks = results.pose_landmarks.landmark
            data = {
                "pose_landmarks": [
                    {"name": landmark_type, "position": [lm.x, lm.y, lm.z] if hasattr(lm, 'z') else [lm.x, lm.y]}
                    for landmark_type, lm in enumerate(pose_landmarks)
                ]
            }
            
          frame = drawCircle(frame, data, 'hitler')
        
          cv2.imshow("Frame", frame)
          if cv2.waitKey(1) & 0xFF == 27:
               break

cap.release()
cv2.destroyAllWindows()