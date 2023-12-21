import numpy as np

class Camera:
    def __init__(self, alpha, beta, u0, v0, f, pos):
        self.alpha = alpha
        self.beta = beta
        self.u0 = u0
        self.v0 = v0
        self.pos = pos
        self.f = f

    def rotate_x(self, angle_speed):
        rotation_matrix = np.array([
            [1, 0, 0],
            [0, np.cos(angle_speed), -np.sin(angle_speed)],
            [0, np.sin(angle_speed), np.cos(angle_speed)]
        ])
        self.pos = np.dot(self.pos, rotation_matrix)

    def rotate_y(self, angle):
        rotation_matrix = np.array([
            [np.cos(angle), 0, np.sin(angle)],
            [0, 1, 0],
            [-np.sin(angle), 0, np.cos(angle)]
        ])
        self.pos = np.dot(self.pos, rotation_matrix)

    def rotate_z(self, angle):
        rotation_matrix = np.array([
            [np.cos(angle), -np.sin(angle), 0],
            [np.sin(angle), np.cos(angle), 0],
            [0, 0, 1]
        ])
        self.pos = np.dot(self.pos, rotation_matrix)

    """def screenToWorldCoordinates(self, screen_coords):
        u, v = screen_coords  # Coordonnées de l'écran (position de la souris)

        # Calcul des coordonnées mondiales à partir des coordonnées de l'écran (projection perspective)
        x = abs((u - self.u0) * self.f / (self.f + v - self.v0))
        y = abs((v - self.v0) * self.f / (self.f + v - self.v0))
        print(x, y)
        z = self.f  # Ou tout autre valeur que vous souhaitez attribuer pour la coordonnée z

        # Ajout des coordonnées de la caméra pour obtenir les coordonnées mondiales finales
        world_x = self.pos[0] + x
        world_y = self.pos[1] + y
        world_z = self.pos[2] - z  # Négatif pour simuler une profondeur dans l'espace 3D

        return np.array([world_x, world_y, world_z])"""

    def screenToWorldCoordinates(self, screen_coords):
        u, v = screen_coords  # Coordonnées de l'écran (position de la souris)

        # (projection perspective)
        x = (u - self.u0) * self.f / (self.f + (v - self.v0) * np.tan(self.alpha))
        y = (v - self.v0) * self.f / (self.f + (v - self.v0) * np.tan(self.beta))
        z = self.f

        # Ajout des coordonnées de la caméra pour obtenir les coordonnées mondiales finales
        world_x = abs(self.pos[0] + x)
        world_y = abs(self.pos[1] + y)
        world_z = abs(self.pos[2] - z)
        print(world_x, world_y, world_z)
        return np.array([world_x, world_y, world_z])

    """def screenToWorldCoordinates(self, screen_coords):
        u, v = screen_coords  # Coordonnées de l'écran (position de la souris)

        # Calcul des coordonnées mondiales à partir des coordonnées de l'écran
        x = (u - self.u0) / self.f
        y = (v - self.v0) / self.f

        # Ajout des coordonnées de la caméra pour obtenir les coordonnées mondiales finales
        world_x = self.pos[0] + x
        world_y = self.pos[1] + y
        world_z = self.pos[2]  # Ou tout autre valeur que vous souhaitez attribuer pour la coordonnée z

        return np.array([world_x, world_y, world_z])"""


