# similation of the orbits of planets around the sun
# use real astronomical values (real mass of the sun, real distance from the earth to the sun, etc.)
# apply the force of gravity between all the different planets to get an accurate eliptical orbit
# shows the distance of the planet to the sun from for each planet (it's actually not circular and is consistently changing as they orbit around)

import pygame
import math

pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1600, 950
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Planet Simulation")

# Color constants
WHITE = (167, 185, 214)
YELLOW = (255, 255, 0)
BLUE = (100, 149, 237)
RED = (188, 39, 50)
DARK_GREY = (80, 78, 81)
ORANGE = (227, 149, 59)
GOLD = (227, 180, 98)
LIGHT_BLUE = (116, 182, 227)
DARK_BLUE = (55, 93, 173)

# Font for displaying planet distances
FONT = pygame.font.SysFont("comicsans", 16)

# Planet class for simulation
class Planet:
    # Constants for astronomical calculations
    AU = 149.6e6 * 1000  # Astronomical Unit in meters
    G = 6.67430e-11  # Gravitational constant in m^3/kg/s^2

    # Scale factor for converting meters to pixels and time step (1 day in seconds)
    SCALE = 150 / AU
    TIMESTEP = 3600 * 24

    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass
        self.velocity = [0, 0]

        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0

    def draw(self, win):
        # Convert planet's position from meters to screen pixels
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2

        # Draw the planet's orbit if available
        if len(self.orbit) > 2:
            updated_points = [(p[0] * self.SCALE + WIDTH / 2, p[1] * self.SCALE + HEIGHT / 2) for p in self.orbit]
            pygame.draw.lines(win, self.color, False, updated_points, 2)

        # Draw the planet as a circle
        pygame.draw.circle(win, self.color, (int(x), int(y)), self.radius)

        # Display the distance to the sun (if not the sun itself)
        if not self.sun:
            distance_text = FONT.render(f"{round(self.distance_to_sun / 1000, 1)} km", 1, (255,255,255))
            win.blit(distance_text, (x - distance_text.get_width() / 2, y - distance_text.get_height() / 2))

    def attraction(self, other):
        # Calculate the gravitational force between two planets
        dx = other.x - self.x
        dy = other.y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        if other.sun:
            self.distance_to_sun = distance

        force = (self.G * self.mass * other.mass) / (distance ** 2)
        angle = math.atan2(dy, dx)
        force_x = force * math.cos(angle)
        force_y = force * math.sin(angle)
        return force_x, force_y

    def update_position(self, planets):
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue

            # Calculate the gravitational forces on the planet from other planets
            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy

        # Calculate acceleration due to the net force
        acceleration_x = total_fx / self.mass
        acceleration_y = total_fy / self.mass

        # Update the planet's velocity based on acceleration and time step
        self.velocity[0] += acceleration_x * self.TIMESTEP
        self.velocity[1] += acceleration_y * self.TIMESTEP

        # Update the planet's position based on velocity and time step
        self.x += self.velocity[0] * self.TIMESTEP
        self.y += self.velocity[1] * self.TIMESTEP

        # Add the current position to the orbit history
        self.orbit.append((self.x, self.y))

# Main simulation function
def main():
    run = True
    clock = pygame.time.Clock() # keep the simulation the same speed no matter the speed of the computer

    # Create the Sun and planets with initial positions and velocities
    sun = Planet(0, 0, 30, YELLOW, 1.98892e30)
    sun.sun = True

    mercury = Planet(0.387 * Planet.AU, 0, 8, DARK_GREY, 3.30e23)
    mercury.velocity[1] = -47.4 * 1000  # Initial velocity for Mercury

    venus = Planet(0.723 * Planet.AU, 0, 14, WHITE, 4.8685e24)
    venus.velocity[1] = -35.02 * 1000  # Initial velocity for Venus

    earth = Planet(-1 * Planet.AU, 0, 16, BLUE, 5.9742e24)
    earth.velocity[1] = 29.783 * 1000  # Initial velocity for Earth

    mars = Planet(-1.524 * Planet.AU, 0, 12, RED, 6.39e23)
    mars.velocity[1] = 24.077 * 1000  # Initial velocity for Mars

    jupiter = Planet(5.203 * Planet.AU, 0, 40, ORANGE, 1.898e27)
    jupiter.velocity[1] = 13.07 * 1000  # Initial velocity for Jupiter

    saturn = Planet(9.583 * Planet.AU, 0, 35, GOLD, 5.683e26)
    saturn.velocity[1] = 9.69 * 1000  # Initial velocity for Saturn

    uranus = Planet(19.22 * Planet.AU, 0, 25, LIGHT_BLUE, 8.681e25)
    uranus.velocity[1] = 6.81 * 1000  # Initial velocity for Uranus

    neptune = Planet(30.05 * Planet.AU, 0, 24, DARK_BLUE, 1.024e26)
    neptune.velocity[1] = 5.43 * 1000  # Initial velocity for Neptune

    # Add all planets to the list
    planets = [sun, mercury, venus, earth, mars, jupiter, saturn, uranus, neptune]

    while run:
        clock.tick(60)
        WIN.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for planet in planets:
            planet.update_position(planets)
            planet.draw(WIN)

        pygame.display.update()

    pygame.quit()

# Run the simulation
if __name__ == "__main__":
    main()
