import cv2
import mediapipe as mp
import json

def process_image():
    
    mp_drawing = mp.solutions.drawing_utils
    mp_holistic = mp.solutions.holistic


    with mp_holistic.Holistic(
        static_image_mode=False,
        model_complexity=1) as holistic:

        # Cargar imagen
        image = cv2.imread('./hitler.jfif')

        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = holistic.process(image_rgb)

        # Mano izquieda (azul)
        mp_drawing.draw_landmarks(
            image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
            mp_drawing.DrawingSpec(color=(255, 255, 0), thickness=2, circle_radius=1),
            mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2))
        
        # Mano derecha (verde)
        mp_drawing.draw_landmarks(
            image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
            mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=1),
            mp_drawing.DrawingSpec(color=(57, 143, 0), thickness=2))
        
        # Postura
        mp_drawing.draw_landmarks(
            image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS,
            mp_drawing.DrawingSpec(color=(128, 0, 255), thickness=2, circle_radius=1),
            mp_drawing.DrawingSpec(color=(255, 255, 255), thickness=2))

        cv2.imwrite('hitlerOut.jpg', image)

        # Extraer landmarks
        pose_landmarks = results.pose_landmarks.landmark if results.pose_landmarks else None

        return pose_landmarks


def save_pose_data(pose_landmarks, output_file):
    if pose_landmarks:
        data = {
            "pose_landmarks": [
                {"name": landmark_type, "position": [lm.x, lm.y, lm.z] if hasattr(lm, 'z') else [lm.x, lm.y]}
                for landmark_type, lm in enumerate(pose_landmarks)
            ]
        }
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=4)
    else:
        print("No pose detected")

if __name__ == "__main__":
    output_json = 'hitler_info.json'

    pose_landmarks = process_image()
    save_pose_data(pose_landmarks, output_json)

    print(f"Pose information saved to {output_json}")