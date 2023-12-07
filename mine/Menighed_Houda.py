import pygame
import numpy as np

class Cube:

    def __init__(self, screen,points,faces, pos, size, texture):
        self.screen = screen
        self.pos = pos
        self.size = size
        self.vertices = points * size + self.pos
        self.f = 3
        self.alpha = 50
        self.beta = 50
        self.u0 = 500
        self.v0 = 300
        self.texture = texture
        self.faces = faces
        self.angleX = 0
        self.angleY = 0
        self.angleZ = 0
        self.dx = 0
        self.dy = 0
        self.dz = 0
        self.light_dir = np.asarray([0, -1, -1])
        self.light_dir = self.light_dir/np.linalg.norm(self.light_dir) # pour le rend un vecteur unitaire
        self.normales = []

    def Zrotation(self, angle, camera):
        angle = np.radians(angle)
        rotation_matrix = np.array([
            [np.cos(angle), -np.sin(angle), 0],
            [np.sin(angle), np.cos(angle), 0],
            [0, 0, 1]
        ])
        self.vertices = np.dot((self.vertices - camera), rotation_matrix) + camera

    def Xrotation(self, angle, camera):
        angle = np.radians(angle)
        rotation_matrix = np.array([
            [1, 0, 0],
            [0, np.cos(angle), -np.sin(angle)],
            [0, np.sin(angle), np.cos(angle)]
        ])
        self.vertices = np.dot((self.vertices - camera), rotation_matrix.T) + camera

    def Yrotation(self, angle, camera):
        angle = np.radians(angle)
        rotation_matrix = np.array([
            [np.cos(angle), 0, np.sin(angle)],
            [0, 1, 0],
            [-np.sin(angle), 0, np.cos(angle)]
        ])
        self.vertices = np.dot((self.vertices - camera), rotation_matrix.T) + camera

    def jump(self):
        if not self.dy:
            key = pygame.key.get_pressed()
            if key[pygame.K_F1]:
                self.dy = 100
            else:
                self.dy = 4

    def project_point(self, point, camera):
        pts = point - camera
        x, y, z = pts[0], pts[1], pts[2]

        # Calcul des coordonnées 2D (u, v) à partir des coordonnées 3D (coordX, coordY, coordZ)
        u = self.u0 + self.alpha * (self.f * x / z)
        v = self.v0 + self.beta * (self.f * y / z)

        return np.array([int(u), int(v)])

    def projection(self, points, camera):
        f = self.f
        new_points = points - camera

        pX, pY, pZ = np.take(new_points, 0, axis=1) , np.take(new_points, 1, axis=1), np.take(new_points, 2,axis=1)

        # Calcul direct des coordonnées projetées sans utiliser column_stack
        projected_points = np.vstack((pX / pZ, pY / pZ, np.ones(len(new_points))))

        # Matrice de projection
        projected_matrix = [
            [0, f * self.beta, self.u0],
            [f * self.alpha, 0, self.v0],
            [0, 0, 1]
        ]

        # Application de la matrice de projection
        projected_points = np.dot(projected_matrix, projected_points)
        projected_points = np.transpose(projected_points)
        return projected_points

    def draw(self, camera):
        rotated_vertices = self.projection(self.vertices, camera)
        #rotated_vertices = [self.project_point(point) for point in self.vertices]
        self.faces.sort(key=lambda x: min(x))

        for indices in self.faces:
            points = [rotated_vertices[i] for i in indices]
            self.textureMapping(self.screen, points)

    # pour calculet le vecteur scalaire
    def dot_3d(self, arr1, arr2):
        return arr1[0] * arr2 + arr1[1] * arr2 + arr1[2] * arr2

    def linear_interpolation(self, i, j, facteur):
        return i + facteur * (j - i)

    def calculer_normales(self):
        self.normales = []

        for face in self.faces:
            # Obtention des points pour cette face du cube
            p1 = self.vertices[face[0]]
            p2 = self.vertices[face[1]]
            p3 = self.vertices[face[2]]

            # Calcul des vecteurs pour les côtés de la face
            v1 = p2 - p1
            v2 = p3 - p1

            # Calcul du produit vectoriel pour obtenir le vecteur normal de la face
            normal = np.cross(v1, v2)
            self.normales.append(normal / np.linalg.norm(normal))  # Normalisation du vecteur normal

    def textureMapping(self, screen, face):
        widthTex, heightTex = self.texture.get_size()
        self.calculer_normales()

        # Création d'un tableau pour stocker les points projetés
        vertexs = np.zeros((widthTex + 1, heightTex + 1, 2))  # Tableau 3D pour stocker les coordonnées coordX et coordY

        for i in range(heightTex + 1):
            firstInterpolation = np.array([self.linear_interpolation(face[1][d], face[2][d], i / heightTex) for d in range(2)])
            secondInterpolation = np.array([self.linear_interpolation(face[0][d], face[3][d], i / heightTex) for d in range(2)])

            for k in range(widthTex + 1):
                p = np.array([self.linear_interpolation(firstInterpolation[d], secondInterpolation[d],k / widthTex) for d in range(2)])
                vertexs[k, i] = p  # Stockage du resultat dans le tableau

        for x in range(widthTex):
            for y in range(heightTex):
                # Dessin du polygone texturé en utilisant les valeurs du tableau
                for normal in self.normales:
                    dot_product = np.dot(normal, self.light_dir)

                    # Définir la couleur en fonction du produit scalaire
                    brightness = max(0, dot_product)  # S'assurer que la luminosité est au moins égale à zéro
                    color = tuple(int(c * brightness) for c in
                                  self.texture.get_at((x, y)))  # Utilisation de la couleur de la texture

                pygame.draw.polygon(screen, self.texture.get_at((x, y)), [
                    vertexs[x, y],
                    vertexs[x, y + 1],
                    vertexs[x + 1, y + 1],
                    vertexs[x + 1, y]
                ])


couleurBlue = (135, 206, 235)
couleurBlanc = (255, 255, 255)
hauteur = 600
largeur = 1000

pygame.init()
screen = pygame.display.set_mode((1000, 600))
clock = pygame.time.Clock()
cubeSize = 7

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
(coordX, coordY, coordZ) = (0, 60, 50)

image1 = pygame.image.load('textures\\blocks\\tbs\\grass b.png')

image2 = pygame.image.load('textures\\blocks\\tbs\\grass b.png')
icon = pygame.image.load('textures\\blocks\\tbs\\grass s.png')

camera = np.array([coordX, coordY, 0])

cube = Cube(screen, vertices, faces, (coordY, coordX, coordZ), cubeSize, image1)
coordY2 = coordY - (cubeSize * 2)
cube2 = Cube(screen, vertices, faces, (coordY2, coordX, coordZ), cubeSize, image1)
coordX = 0
declageY = coordY - (cubeSize * 2)
decalageX = 0
decalageXRight = 0
click = False
left = False
right = False
ListDesCubes = []
ListDesCubes.append(cube)
ListDesCubes.append(cube2)
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            camera[1] -= 2
        if keys[pygame.K_d]:
            camera[1] += 2
        if keys[pygame.K_w]:
            camera[2] += 2
        if keys[pygame.K_s]:
            camera[2] -= 2
        if keys[pygame.K_UP]:
            click = True
        if keys[pygame.K_RIGHT]:
            left = True

        if keys[pygame.K_LEFT]:
            right = True

        if keys[pygame.K_q]:
            camera[0] += 2
        if keys[pygame.K_a]:
            for c in ListDesCubes:
                c.Zrotation(-3, camera)
        if keys[pygame.K_e]:
            for c in ListDesCubes:
                c.Zrotation(3, camera)

        if keys[pygame.K_e]:
            for c in ListDesCubes:
                c.Zrotation(3, camera)

        if keys[pygame.K_SPACE]:
            for c in ListDesCubes:
                c.Zrotation(3, camera)

    for i in range(hauteur):
        proportion = i / hauteur

        couleurIntermediaire = (
            int(couleurBlue[0] * (1 - proportion) + couleurBlanc[0] * proportion),
            int(couleurBlue[1] * (1 - proportion) + couleurBlanc[1] * proportion),
            int(couleurBlue[2] * (1 - proportion) + couleurBlanc[2] * proportion),
        )

        pygame.draw.line(screen, couleurIntermediaire, (0, i), (largeur, i))

    if click:
        declageY -= (cubeSize * 2)
        cube3 = Cube(screen, vertices, faces, (declageY, coordX, coordZ), cubeSize, image2)
        ListDesCubes.append(cube3)
        click = False

    if left:
        decalageX += (cubeSize * 2)
        cube4 = Cube(screen, vertices, faces, (coordY, decalageX, coordZ), cubeSize, image2)
        ListDesCubes.append(cube4)
        left = False

    if right:
        decalageXRight -= (cubeSize * 2)
        cube4 = Cube(screen, vertices, faces, (coordY, decalageXRight, coordZ), cubeSize, image2)
        ListDesCubes.append(cube4)
        right = False

    for c in ListDesCubes:
        c.draw(camera)
    pygame.display.set_caption('Minecraft')
    pygame.display.set_icon(icon)
    pygame.display.update()
    clock.tick(60)

pygame.quit()
