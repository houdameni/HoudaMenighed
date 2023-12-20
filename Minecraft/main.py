import pygame
import numpy as np
from camera import Camera
from cube3d import Cube


def draw_ground():
    ground_color = (100, 100, 100)  # Couleur du sol
    pygame.draw.polygon(screen, ground_color, [(0, hauteur), (largeur, hauteur), (largeur, 0), (0, 0)])

couleurBlue = (135, 206, 235)
couleurBlanc = (255, 255, 255)
hauteur = 600
largeur = 1000

pygame.init()
screen = pygame.display.set_mode((1000, 600))
clock = pygame.time.Clock()
cubeSize = 35
cubeSize2 = 10

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

image1 = pygame.image.load('grass2.png')

image2 = pygame.image.load('grass.png')
icon = pygame.image.load('textures\\blocks\\tbs\\grass s.png')

alpha = 50
beta = 50
u0 = 500
v0 = 300
f = 3
pos = np.array([coordX, coordY, 0])
camera = Camera(alpha, beta, u0, v0, f, pos)

cube = Cube(screen, vertices, faces, (coordY, coordX, coordZ), cubeSize, image1,image2, camera)

coordY2 = coordY - (cubeSize * 2)
cube2 = Cube(screen, vertices, faces, (coordY2, coordX, coordZ), cubeSize2, image1,image2, camera)

coordX = 0
declageY = coordY - (cubeSize * 2)
decalageX = 0
decalageXRight = 0
click = False
left = False
right = False
ListDesCubes = []
ListDesCubes.append(cube)
coord = coordX + (cubeSize *2)
for i in range(1):

    cubbe = Cube(screen, vertices, faces, (coordY, coord, coordZ), cubeSize, image1,image2, camera)
    coord+=(cubeSize *2)
    ListDesCubes.append(cubbe)

movement_speed = .05
rotation_speed = .5
jump_force = 0
jump_reduce = 0.1
gravity = 1
#ListDesCubes.append(cube2)
while True:
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
        if keys[pygame.K_d]:
            camera.pos[1] += 2
        if keys[pygame.K_w]:
            #camera.pos[2] += 2

            # Vérification de la présence de cubes au-dessus de la position de la caméra
            cube_above_camera = False
            for c in ListDesCubes:
                if (
                    camera_pos_x >= c.pos[0] - cubeSize / 2
                    and camera_pos_x <= c.pos[0] + cubeSize / 2
                    and camera_pos_y >= c.pos[1] - cubeSize / 2
                    and camera_pos_y <= c.pos[1] + cubeSize / 2
                    and camera_pos_z <= c.pos[2] + cubeSize / 2 + 1  # Vérification du cube au-dessus
                ):
                    camera.pos[2] = c.pos[2] + cubeSize / 2 + 1
                    cube_above_camera = True
                    break

            # Déplacement de la caméra si aucun cube n'est au-dessus
            if not cube_above_camera:
                camera.pos[2] -= 2  # Déplacement vers le bas
            else:
                print('do nothing')

        if keys[pygame.K_s]:
            existe = False
            for c in ListDesCubes:
                if c.pos[1] == 0:  # Vérifier si un cube est à la position y = 0
                    existe = True
                    print("Cube found at ground level")
                    break  # Sortir de la boucle dès qu'un cube est trouvé au niveau du sol

            if existe and not (keys[pygame.K_SPACE]):  # Si un cube est au sol et "Espace" n'est pas enfoncé
                camera.pos[2] += 0  # Aucun déplacement vers le bas
                existe = False
            else:
                camera.pos[2] += 2  # Déplacer la caméra vers le bas par défaut




        if keys[pygame.K_UP]:
            camera.pos[2]
            click = True
        if keys[pygame.K_RIGHT]:
            left = True

        if keys[pygame.K_LEFT]:
            right = True

        if keys[pygame.K_q]:
            camera.pos[0] += 2
        if keys[pygame.K_a]:
            for c in ListDesCubes:
                c.Zrotation(-3, camera.pos)
        if keys[pygame.K_e]:
            for c in ListDesCubes:
                c.Zrotation(3, camera.pos)

        """if keys[pygame.K_e]:
            for c in ListDesCubes:
                c.Zrotation(3, camera,pos)"""

        if keys[pygame.K_SPACE]:
            #print('in it')
            if jump_force == 0:
                jump_force = 7

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
                    [0, 0, cubeSize + 1])  # Ajuster la hauteur du nouveau cube
                new_cube = Cube(screen, vertices, faces, new_cube_pos, 10, image1, image2, camera)
                ListDesCubes.append(new_cube)
            else:
                # Si aucun cube n'existe à cette position, créer un nouveau cube à la position de la souris
                new_cube = Cube(screen, vertices, faces, mouse_world_pos, 10, image1, image2, camera)
                ListDesCubes.append(new_cube)

        # Vérification simultanée des touches "Espace" et "S" pour le déplacement de la caméra vers le bas
        if keys[pygame.K_SPACE] and keys[pygame.K_s]:
            camera.pos[2] -= 2  # Déplacement vers le bas si les deux touches sont enfoncées

    if camera.pos[0] > 100:
        camera.pos[0] = coordX
    jump_force = max(0, jump_force - jump_reduce)
    #camera.pos[0] = min(0, camera.pos[0] - jump_force + gravity)
    #l'inverse du saut
    camera.pos[0] = min(0, camera.pos[0] - jump_force + gravity)
    #print(camera.pos[0])

    for i in range(hauteur):
        proportion = i / hauteur

        couleurIntermediaire = (
            int(couleurBlue[0] * (1 - proportion) + couleurBlanc[0] * proportion),
            int(couleurBlue[1] * (1 - proportion) + couleurBlanc[1] * proportion),
            int(couleurBlue[2] * (1 - proportion) + couleurBlanc[2] * proportion),
        )

        pygame.draw.line(screen, couleurIntermediaire, (0, i), (largeur, i))
    draw_ground()
    for c in ListDesCubes:
        c.draw(camera.pos)
    pygame.display.set_caption('Minecraft')
    pygame.display.set_icon(icon)
    pygame.display.update()
    clock.tick(60)

pygame.quit()

"""if click:
    declageY += (cubeSize //2)
    cube3 = Cube(screen, vertices, faces, (declageY, coordX, coordZ), cubeSize2, image2, camera)
    ListDesCubes.append(cube3)
    click = False

if left:
    decalageX += (cubeSize * 2)
    cube4 = Cube(screen, vertices, faces, (coordY, decalageX, coordZ), cubeSize, image2, camera)
    ListDesCubes.append(cube4)
    left = False

if right:
    decalageXRight -= (cubeSize * 2)
    cube4 = Cube(screen, vertices, faces, (coordY, decalageXRight, coordZ), cubeSize, image2, camera)
    ListDesCubes.append(cube4)
    right = False"""
