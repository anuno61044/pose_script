import json
import cv2
import mediapipe as mp
from comparePose import evaluatePose

def drawCircle(frame):
    # Define las coordenadas del centro del círculo y su radio
    center_coordinates = (60, 60)  # Cambia estas coordenadas según sea necesario
    
    radius = 50  # Cambia el radio según sea necesario

    # Dibuja el círculo en la imagen
    if evaluatePose():
        newframe = cv2.circle(frame, center_coordinates, radius, (0,255,0), thickness=-1)
    else:
        newframe = cv2.circle(frame, center_coordinates, radius, (0,0, 255), thickness=-1)
            
    return newframe

mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic

# cap = cv2.VideoCapture("./ganga.webm")
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# Configuración para el escritor de video
# fourcc = cv2.VideoWriter_fourcc(*'MJPG')
# out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))  # Ajusta la resolución según sea necesario

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
            
          with open('pose_info3.json', 'w') as f:
            json.dump(data, f, indent=4)

          frame = drawCircle(frame)
        
          cv2.imshow("Frame", frame)
          if cv2.waitKey(1) & 0xFF == 27:
               break

cap.release()
# out.release()
cv2.destroyAllWindows()