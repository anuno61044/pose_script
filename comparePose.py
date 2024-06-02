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

def evaluatePose(human_data, pose):
    # Abrir los archivos JSON y cargar su contenido
    with open(f'./{pose}_info.json', 'r') as file:
        pose_data = json.load(file)

    # Acceder a los landmarks de la pose
    pose_landmarks1 = pose_data['pose_landmarks']
    pose_landmarks3 = human_data['pose_landmarks']

    # Ahora `pose_data` es un objeto Python que contiene los datos del archivo JSON
    # for i in range(32):
    #     print(f'atributo: {pose_landmarks1[i]['name']} en {pose_landmarks1[i]['position']}')
    #     print(f'atributo: {pose_landmarks3[i]['name']} en {pose_landmarks3[i]['position']}\n')

    angles = [
        {   
            "name": 'codoI',
            "points": [14,12,16],
            "rel": 2 #"hombroI"
        },
        {
            "name": 'codoD',
            "points": [13,15,11],
            "rel": 3 #"hombroD"
        },
        {
            "name": 'hombroI',
            "points": [12,14,24],
            "rel": 0 #"codoI"
        },
        {
            "name": 'hombroD',
            "points": [11, 13, 23],
            "rel": 1 #"codoD"
        },
        {
            "name": 'caderaI',
            "points": [24, 12, 26],
            "rel": 4 #"hombroD"
        },
        {
            "name": 'caderaD',
            "points": [23, 25, 11],
            "rel": 5 #"hombroD"
        },
        {
            "name": 'rodillaI',
            "points": [26, 28, 24],
            "rel": 6 #"hombroD"
        },
        {
            "name": 'rodillaD',
            "points": [25, 27, 23],
            "rel": 7 #"hombroD"
        },
    ]

    angles1 = []
    angles2 = []

    for angle in angles:
        angles1.append(calcular_angulo(pose_landmarks1[angle['points'][0]]['position'], pose_landmarks1[angle['points'][1]]['position'], pose_landmarks1[angle['points'][2]]['position']))
        angles2.append(calcular_angulo(pose_landmarks3[angle['points'][0]]['position'], pose_landmarks3[angle['points'][1]]['position'], pose_landmarks3[angle['points'][2]]['position']))
        
        # print(f'Angulo de la {angle['name']} de David: {calcular_angulo(pose_landmarks3[angle['points'][0]]['position'], pose_landmarks3[angle['points'][1]]['position'], pose_landmarks3[angle['points'][2]]['position'])}')
        # print(f'Angulo de la {angle['name']} de Hitler: {calcular_angulo(pose_landmarks1[angle['points'][0]]['position'], pose_landmarks1[angle['points'][1]]['position'], pose_landmarks1[angle['points'][2]]['position'])}\n')

    umbral = 30
    superUmbral = 45 
    countWrong = 0
    # print(angles2)
    # print(angles1)
    for i in range(len(angles1)):
        # si el angulo esta mal
        if abs(angles1[i] - angles2[i]) > umbral:
            print(f'El angulo {angles[i]['name']} está mal')
            countWrong += 1
        
        
        # si en angulo en relacion con otro estan mal
        if abs(angles1[i] - angles2[i]) + abs(angles1[angles[i]["rel"]] - angles2[angles[i]["rel"]]) > superUmbral:
            print(f'El angulo {angles[i]['name']} está mal por relacion con {angles[angles[i]["rel"]]["name"]}')
            countWrong += 0.5
        
    print('\n\n')
    
    if countWrong > 0:
        return False

    return True

if __name__ == "__main__":
    with open(f'./{"spider1"}_info.json', 'r') as file:
        human_data = json.load(file)
    print(evaluatePose(human_data, "spider2"))



