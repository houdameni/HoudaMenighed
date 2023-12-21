import numpy as np
import pygame


class Cube:

    def __init__(self, screen, points, faces, pos, size, side, otherSides, camera, test):
        self.screen = screen
        self.pos = pos
        self.size = size
        self.vertices = points * size + self.pos
        self.faces = faces
        self.test = test
        self.angleX = 0
        self.angleY = 0
        self.angleZ = 0
        self.dx = 0
        self.dy = 0
        self.dz = 0
        self.camera = camera
        self.sides = {
            'f': [(0, 1, 2, 3), side],
            'bl': [(4, 5, 6, 7), side],
            'l': [(0, 1, 5, 4), side],
            'r': [(3, 2, 6, 7), side],
            't': [(0, 3, 7, 4), otherSides],
            'b': [(1, 2, 6, 5), otherSides]
        }

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


    def project_point(self, point, camera):
        pts = point - camera
        x, y, z = pts[0], pts[1], pts[2]

        # Calcul des coordonnées 2D (u, v) à partir des coordonnées 3D (coordX, coordY, coordZ)
        u = self.camera.u0 + self.camera.alpha * (self.camera.f * x / z)
        v = self.camera.v0 + self.camera.beta * (self.camera.f * y / z)

        return np.array([int(u), int(v)])

    def projection(self, points, camera):
        f = self.camera.f
        new_points = points - camera
        pX = np.take(new_points, 0, axis=1)
        pY = np.take(new_points, 1, axis=1)
        pZZ = np.take(new_points, 2, axis=1)

        pZ = np.take(new_points, 2, axis=1)

        pZ[pZ < 1] = 1
        projected_points = np.vstack((pX / pZ, pY / pZ, np.ones(len(new_points))))

        # Matrice de projection
        projected_matrix = [
            [0, f * self.camera.beta, self.camera.u0],
            [f * self.camera.alpha, 0, self.camera.v0],
            [0, 0, 1]
        ]

        # Application de la matrice de projection
        projected_points = np.dot(projected_matrix, projected_points)
        projected_points = np.transpose(projected_points)
        return projected_points

    def centre(self, side, camera):
        vertices = self.sides[side][0]
        sum_distance = sum(np.linalg.norm(np.array(self.vertices[i]) - np.array(camera)) for i in vertices)
        return sum_distance / len(vertices)

    def draw(self, camera):
        rotated_vertices = self.projection(self.vertices, camera)
        sorted_sides = sorted(self.sides.items(), key=lambda x: self.centre(x[0], camera), reverse=True)
        for side, (indices, texture) in sorted_sides[3:6]:
            vertices = [rotated_vertices[i] for i in indices]

            self.textureMapping(self.screen, vertices, texture)

    def linear_interpolation(self, i, j, facteur):
        return i + facteur * (j - i)

    def textureMapping(self, screen, face, texture):
        widthTex, heightTex = texture.get_size()

        # Création d'un tableau pour stocker les points projetés
        vertexs = np.zeros((widthTex + 1, heightTex + 1, 2))  # Tableau 3D pour stocker les coordonnées coordX et coordY

        for i in range(heightTex + 1):
            firstInterpolation = np.array(
                [self.linear_interpolation(face[1][d], face[2][d], i / heightTex) for d in range(2)])
            secondInterpolation = np.array(
                [self.linear_interpolation(face[0][d], face[3][d], i / heightTex) for d in range(2)])

            for k in range(widthTex + 1):
                p = np.array(
                    [self.linear_interpolation(firstInterpolation[d], secondInterpolation[d], k / widthTex) for d in
                     range(2)])
                vertexs[k, i] = p  # Stockage du resultat dans le tableau

        for x in range(widthTex):
            for y in range(heightTex):
                # Dessin du polygone texturé en utilisant les valeurs du tableau

                pygame.draw.polygon(screen, texture.get_at((x, y)), [
                    vertexs[x, y],
                    vertexs[x, y + 1],
                    vertexs[x + 1, y + 1],
                    vertexs[x + 1, y]
                ])
