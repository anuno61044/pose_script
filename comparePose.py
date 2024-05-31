# from PosePoints import LANDMARK_NAMES as points
import json
import math

def calcular_coseno_angulo(a, b):
    # Producto escalar
    dot_product = sum([ai * bi for ai, bi in zip(a, b)])
    
    # Magnitudes de los vectores
    mag_a = math.sqrt(sum([ai**2 for ai in a]))
    mag_b = math.sqrt(sum([bi**2 for bi in b]))
    
    # Cálculo del coseno del ángulo
    cos_theta = dot_product / (mag_a * mag_b)
    
    return cos_theta

def calcular_angulo(P,Q,R):
    # Paso 1: Calcular los vectores PQ y PR
    a = [Q[0] - P[0], Q[1] - P[1]]
    b = [R[0] - P[0], R[1] - P[1]]
    
    cos_theta = calcular_coseno_angulo(a, b)
    theta_rad = math.acos(cos_theta)
    theta_deg = math.degrees(theta_rad)
    
    return theta_deg

def evaluatePose():
    # Abrir los archivos JSON y cargar su contenido
    with open('./pose_info1.json', 'r') as file:
        pose_data1 = json.load(file)
    with open('./pose_info3.json', 'r') as file:
        pose_data3 = json.load(file)

    # Acceder a los landmarks de la pose
    pose_landmarks1 = pose_data1['pose_landmarks']
    pose_landmarks3 = pose_data3['pose_landmarks']

    # Ahora `pose_data` es un objeto Python que contiene los datos del archivo JSON
    # for i in range(32):
    #     print(f'atributo: {pose_landmarks1[i]['name']} en {pose_landmarks1[i]['position']}')
    #     print(f'atributo: {pose_landmarks3[i]['name']} en {pose_landmarks3[i]['position']}\n')

    angles = [
        {"name": 'codoI',
        "points": [14,12,16]},
        {"name": 'codoD',
        "points": [13,15,11]},
        {"name": 'hombroI',
        "points": [12,14,24]},
        {"name": 'hombroD',
        "points": [11, 13, 23]},
        {"name": 'caderaI',
        "points": [24, 12, 26]},
        {"name": 'caderaD',
        "points": [23, 25, 11]},
        {"name": 'rodillaI',
        "points": [26, 28, 24]},
        {"name": 'rodillaD',
        "points": [25, 27, 23]},
    ]

    angles1 = []
    angles2 = []

    for angle in angles:
        angles1.append(calcular_angulo(pose_landmarks1[angle['points'][0]]['position'], pose_landmarks1[angle['points'][1]]['position'], pose_landmarks1[angle['points'][2]]['position']))
        angles2.append(calcular_angulo(pose_landmarks3[angle['points'][0]]['position'], pose_landmarks3[angle['points'][1]]['position'], pose_landmarks3[angle['points'][2]]['position']))
        
        # print(f'Angulo de la {angle['name']} de David: {calcular_angulo(pose_landmarks3[angle['points'][0]]['position'], pose_landmarks3[angle['points'][1]]['position'], pose_landmarks3[angle['points'][2]]['position'])}')
        # print(f'Angulo de la {angle['name']} de Hitler: {calcular_angulo(pose_landmarks1[angle['points'][0]]['position'], pose_landmarks1[angle['points'][1]]['position'], pose_landmarks1[angle['points'][2]]['position'])}\n')

    umbral = 25
    countWrong = 0
    # print(angles2)
    # print(angles1)
    for i in range(len(angles1)):
        # print(angles1[i] - angles2[i])
        if abs(angles1[i] - angles2[i]) > umbral:
            countWrong += 1

    print(f'Tienes {countWrong} cosas mal')
    
    if countWrong > 0:
        return False

    return True

if __name__ == "__main__":
    print(evaluatePose())



