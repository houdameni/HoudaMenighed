import pygame, math
import numpy as np

class Camera:
    class Camera:
        def __init__(self, alpha, beta, u0, v0):
            self.alpha = alpha
            self.beta = beta
            self.u0 = u0
            self.v0 = v0

        def rotate_x(self, angle):
            rotation_matrix = np.array([
                [1, 0, 0],
                [0, np.cos(angle), -np.sin(angle)],
                [0, np.sin(angle), np.cos(angle)]
            ])
            self.camera_position = np.dot(self.camera_position, rotation_matrix)

        def rotate_y(self, angle):
            rotation_matrix = np.array([
                [np.cos(angle), 0, np.sin(angle)],
                [0, 1, 0],
                [-np.sin(angle), 0, np.cos(angle)]
            ])
            self.camera_position = np.dot(self.camera_position, rotation_matrix)

        def rotate_z(self, angle):
            rotation_matrix = np.array([
                [np.cos(angle), -np.sin(angle), 0],
                [np.sin(angle), np.cos(angle), 0],
                [0, 0, 1]
            ])
            self.camera_position = np.dot(self.camera_position, rotation_matrix)


