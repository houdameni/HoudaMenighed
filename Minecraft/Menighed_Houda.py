import pygame
import numpy as np
from camera import Camera
from cube3d import Cube


couleurBlue = (135, 206, 235)
couleurBlanc = (255, 255, 255)
hauteur = 600
largeur = 1000

pygame.init()
pygame.mixer.init()
sound_effect = pygame.mixer.Sound('grass1.ogg')
sound_effect2 = pygame.mixer.Sound('hit1.ogg')
sound_effect3 = pygame.mixer.Sound('fallsmall1.ogg')
sound_effect4 = pygame.mixer.Sound('wood3.ogg')

screen = pygame.display.set_mode((1000, 600))
clock = pygame.time.Clock()
cubeSize = 10
cubeSize2 = 5

vertices = np.array([
            (-1, -1, -1),
            (1, -1, -1),
            (1, 1, -1),
            (-1, 1, -1),
            (-1, -1, 1),
            (1, -1, 1),
            (1, 1, 1),
            (-1, 1, 1)
        ])


faces = [
     (0, 1, 2, 3),
     (4, 5, 6, 7),
     (0, 1, 5, 4),
     (3, 2, 6, 7),
     (0, 3, 7, 4),
     (1, 2, 6, 5)
]


(coordX, coordY, coordZ) = (0, 80, 50)

image1 = pygame.image.load('grass_side1.png')

image2 = pygame.image.load('grass1.png')
water = pygame.image.load('light_blue_wool.png')
image4 = pygame.image.load('img.png')
image5 = pygame.image.load('leaves_oak.png')
icon = pygame.image.load('grass s.png')

#camera = np.array([coordX, coordY, 0])
alpha = 50
beta = 50
u0 = 300
v0 = 300
f = 2.90
pos = np.array([coordX, coordY, 0])
camera = Camera(alpha, beta, u0, v0, f, pos)

cube = Cube(screen, vertices, faces, (coordY, coordX, coordZ), cubeSize, image1,image2, camera, 0)


coordX = 0
declageY = coordY - (cubeSize * 2)
decalageX = 0
decalageXRight = 0
click = False
left = False
right = False
ListDesCubes = []
ListDesCubes.append(cube)
#coord = coordX + (cubeSize *2)
for i in range(10):

    cubbe = Cube(screen, vertices, faces, (coordY, coordX, coordZ), cubeSize, image1,image2, camera, 0)
    coordX+=(cubeSize *2)

    ListDesCubes.append(cubbe)

for i in range(10):

    cubbe = Cube(screen, vertices, faces, (coordY, coordX, coordZ), cubeSize, water, water, camera, 1)
    coordX+=(cubeSize *2)

    ListDesCubes.append(cubbe)

(coordX, coordY, coordZ) = (0, 80, 50)
for i in range(20):

    cube2 = Cube(screen, vertices, faces, (coordY, coordX, (coordZ + (cubeSize * 2))), cubeSize, image1, image2, camera, 0)
    coordX+=(cubeSize *2)
    ListDesCubes.append(cube2)

(coordX, coordY, coordZ) = (0, 80, 50)
coordY-=(cubeSize *2)
for i in range(10):

    cube3 = Cube(screen, vertices, faces, (coordY, coordX, (coordZ + (cubeSize * 2))), cubeSize, image1, image2, camera, 0)
    coordX+=(cubeSize *2)
    ListDesCubes.append(cube3)

cubeSize4 = 3
coordX+=(cubeSize *2)

for i in range(2):

    cube4 = Cube(screen, vertices, faces, (coordY, coordX, (coordZ + (cubeSize * 2))), cubeSize, image4, image4, camera, 0)
    coordY-=(cubeSize *2)
    ListDesCubes.append(cube4)

cube7 = Cube(screen, vertices, faces, (coordY, coordX, (coordZ + (cubeSize * 2))), cubeSize, image5, image5, camera, 0)
coordX-=(cubeSize *2)
print(coordY, coordX, coordZ)
cube5 = Cube(screen, vertices, faces, (coordY, coordX, (coordZ + (cubeSize * 2))), cubeSize, image5, image5, camera, 0)
coordY2= coordY - (cubeSize *2)
cube10 = Cube(screen, vertices, faces, (coordY2, coordX, (coordZ + (cubeSize * 2))), cubeSize, image5, image5, camera, 0)
cube11 = Cube(screen, vertices, faces, (coordY2, coordX+(cubeSize *2), (coordZ + (cubeSize * 2))), cubeSize, image5, image5, camera, 0)
cube13 = Cube(screen, vertices, faces, (coordY2 - (cubeSize *2), coordX+(cubeSize *2), (coordZ + (cubeSize * 2))), cubeSize, image5, image5, camera, 0)

cube12 = Cube(screen, vertices, faces, (coordY2, coordX+(cubeSize *4), (coordZ + (cubeSize * 2))), cubeSize, image5, image5, camera, 0)
coordX-=(cubeSize *2)
cube9 = Cube(screen, vertices, faces, (coordY, coordX, (coordZ + (cubeSize * 2))), cubeSize, image5, image5, camera, 0)
coordX+=(cubeSize *6)
cube6 = Cube(screen, vertices, faces, (coordY, coordX, (coordZ + (cubeSize * 2))), cubeSize, image5, image5, camera, 0)
coordX+=(cubeSize *2)
cube8 = Cube(screen, vertices, faces, (coordY, coordX, (coordZ + (cubeSize * 2))), cubeSize, image5, image5, camera, 0)

ListDesCubes.append(cube5)
ListDesCubes.append(cube6)
ListDesCubes.append(cube7)
ListDesCubes.append(cube8)
ListDesCubes.append(cube9)
ListDesCubes.append(cube10)
ListDesCubes.append(cube11)
ListDesCubes.append(cube12)
ListDesCubes.append(cube13)

movement_speed = 0.05
rotation_speed = 0.5
jumpForce = 0
jumpRd = 0.1
gravity = 1
#ListDesCubes.append(cube2)

def collision_detected(point, vertices_of_face):
    # Vérifie si le point est à l'intérieur du polygone défini par ses sommets

    num_vertices = len(vertices_of_face)
    inside = False

    # Parcourir chaque arête du polygone
    for i in range(num_vertices):
        j = (i + 1) % num_vertices  # Indice du prochain sommet dans la liste circulaire
        print('j',j)
        # Coordonnées des sommets consécutifs
        x1, y1 = vertices_of_face[i][0], vertices_of_face[i][1]
        x2, y2 = vertices_of_face[j][0], vertices_of_face[j][1]

        print(x1, y1)
        print(x2, y2)

        # Vérification de l'intersection en fonction de la position du point
        if ((y1 > point[1]) != (y2 > point[1])) and (point[0] < (x2 - x1) * (point[1] - y1) / (y2 - y1) + x1):
            inside = not inside  # Inversion du statut si le point intersecte l'arête

    return inside

def dist(cube, camera):
    return sum(np.linalg.norm(np.array(i) - np.array(camera)) for i in cube.vertices) / len(cube.vertices)
sp = 1
debut = False
supr = False
existeC = False
existeK = False
while True:
    sorted_cubes = sorted(ListDesCubes, key=lambda x_: (dist(x_, camera.pos)), reverse=True)

    # Récupérer la position Z du cube le plus bas
    lowest_cube_z = min(c.pos[2] for c in ListDesCubes)
    # Calcul de la position de la caméra
    camera_pos_y = camera.pos[1]
    camera_pos_x = camera.pos[0]
    camera_pos_z = camera.pos[2]


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            camera.pos[1] -= 2

            """maxPozZ = (ListDesCubes[0].pos[1])
            #print(maxPozZ)
            for c in ListDesCubes:
                if c.pos[1] < maxPozZ:
                    maxPozZ = c.pos[1]

            if maxPozZ > (camera.pos[2] + 6):
                #print("in true")
                existeK = True

            else:
                camera.pos[1] -= 2  # Déplacement vers le bas"""

            """if camera.pos[2] <= 0:
                camera.pos[2] +=0"""
            if existeK:
                #print('===================')
                jumpForce = 4
                #print("supp")
        if keys[pygame.K_d]:
            camera.pos[1] += 2
        if keys[pygame.K_w]:
            sound_effect.play()
            matching = False

            if debut:
                camera.pos[2] += 4
                debut = False
            for c in ListDesCubes:

                """print('position cube in z')
                print(c.pos[2])
                print('position camera in z')
                print(camera.pos[2])"""
                if (c.pos[2] - (cubeSize * 2)) == (camera.pos[2] + (cubeSize * 2)):
                    """print("-----------matching-------------")
                    print('position cube in z')
                    print(c.pos[2])
                    print('position camera in z')
                    print(camera.pos[2] + (cubeSize * 2))"""
                    #camera.pos[2] += 0
                    matching = True
                    break
                """print('position cube in z')
                print(c.pos[2])
                print('position camera in z')
                print(camera.pos[2])"""
            maxPozZ = (ListDesCubes[0].pos[2])
            #print(maxPozZ)
            for c in ListDesCubes:
                if c.pos[2] > maxPozZ:
                    maxPozZ = c.pos[2]

            if maxPozZ <= (camera.pos[2] + 6):
                #print("in true")
                existeC = True


            if matching or (camera.pos[2] == 0):
                camera.pos[2] += 0
                matching = False
                sound_effect2.play()
            else:
                camera.pos[2] += 2  # Déplacement vers le bas

                """if camera.pos[2] <= 0:
                    camera.pos[2] +=0"""
            if existeC:
                #print('===================')
                jumpForce = 4
                #print("supp")

        if keys[pygame.K_s]:
            sound_effect.play()
            camera.pos[2] -= 2
            #print(camera.pos[2])
        """if keys[pygame.K_UP]:
            camera.pos[2]
            click = True"""

        """if keys[pygame.K_UP] or keys[ord('w')]:
            camera.pos[2] -= 0.1 * np.cos(camera.pos[2])
            camera.pos[0] += 0.1 * np.sin(camera.pos[2])"""

        # Ajuster la caméra seulement si la position Z actuelle de la caméra est proche du cube le plus bas
        """if keys[pygame.K_UP] or keys[pygame.K_w]:
            min_visible_distance = 10  # Ajuster cette valeur selon vos besoins
            if camera.pos[2] > lowest_cube_z - min_visible_distance:
                camera.pos[2] -= 0.1 * np.cos(camera.pos[2])
                camera.pos[0] += 0.1 * np.sin(camera.pos[2])"""
        if keys[pygame.K_RIGHT]:
            camera.rotate_x(0.05)
            left = True

        if keys[pygame.K_LEFT]:
            right = True

        if keys[pygame.K_q]:
            camera.pos[0] += 2
        """if keys[pygame.K_a]:
            for c in ListDesCubes:
                c.Zrotation(-3, camera.pos)
        if keys[pygame.K_e]:
            for c in ListDesCubes:
                c.Zrotation(3, camera.pos)"""

        """if keys[pygame.K_e]:
            for c in ListDesCubes:
                c.Zrotation(3, camera,pos)"""

        if keys[pygame.K_SPACE]:
            if sp == 1 :
                sp = 0
                debut = True
            if jumpForce == 0:
                jumpForce = 4
            if camera.pos[2] == 0:
                camera.pos[2] += 4
            elif camera.pos[2] < 0:
                camera.pos[2] += abs(camera.pos[2]) +1
            else:
                camera.pos[2] += 4
            sound_effect4.play()


        """if event.type == pygame.MOUSEBUTTONDOWN:
            position_x, posY = pygame.mouse.get_pos()
            print(pygame.mouse.get_pos())
            cubee = Cube(screen, vertices, faces, (position_x, coordX, coordZ), cubeSize, image1, camera)
            ListDesCubes.append(cubee)"""

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            mouse_world_pos = camera.screenToWorldCoordinates((mouse_x, mouse_y))

            # Recherche d'un cube existant à cette position
            existing_cube = None
            for cube in ListDesCubes:
                if np.allclose(cube.pos, mouse_world_pos, atol=0.1):  # Tolérance pour la comparaison
                    existing_cube = cube
                    break

            if existing_cube:
                # Si un cube existe à cette position, créer un nouveau cube au-dessus de celui-ci
                new_cube_pos = existing_cube.pos + np.array(
                    [0, 0, cubeSize])  # Ajuster la hauteur du nouveau cube
                new_cube = Cube(screen, vertices, faces, new_cube_pos, 2, image1, image2, camera, 0)
                ListDesCubes.append(new_cube)
            else:
                # Si aucun cube n'existe à cette position, créer un nouveau cube à la position de la souris
                new_cube = Cube(screen, vertices, faces, mouse_world_pos, 2, image1, image2, camera, 0)
                ListDesCubes.append(new_cube)

    if camera.pos[0] > 100:
        camera.pos[0] = coordX

    #print(existeC, existeK)
    jumpForce = max(0, jumpForce - jumpRd)
    if existeC:
        camera.pos[0] = max(0, camera.pos[0] - jumpForce + gravity)
        #existeC = False
    else:
        camera.pos[0] = min(0, camera.pos[0] - jumpForce + gravity)
    #camera.pos[0] = min(0, camera.pos[0] - jumpForce + gravity)

    if existeC :
        sound_effect3.play()
        (coordX, coordY, coordZ) = (0, 80, 50)
        camera.pos[2] = 0
        camera.pos[1] = coordY
        camera.pos[0] = coordX
        sp = 1
        debut = False
        supr = False
        existeC = False
        existeK = False
        movement_speed = 0.05
        rotation_speed = 0.5
        jumpForce = 0
        jumpRd = 0.1
        gravity = 1
    for i in range(hauteur):
        proportion = i / hauteur

        couleurIntermediaire = (
            int(couleurBlue[0] * (1 - proportion) + couleurBlanc[0] * proportion),
            int(couleurBlue[1] * (1 - proportion) + couleurBlanc[1] * proportion),
            int(couleurBlue[2] * (1 - proportion) + couleurBlanc[2] * proportion),
        )

        pygame.draw.line(screen, couleurIntermediaire, (0, i), (largeur, i))

    for c in sorted_cubes:
        c.draw(camera.pos)


    pygame.display.set_caption('Minecraft')
    pygame.display.set_icon(icon)
    pygame.display.update()
    clock.tick(60)

pygame.quit()
