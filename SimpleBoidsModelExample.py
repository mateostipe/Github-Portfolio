import sys
import random
import math
import pygame
import time
from pygame.math import Vector2

# ---------- Parameters ----------
WIDTH, HEIGHT = 1200, 800
NUM_BOIDS = 50
MAX_SPEED = 2.0
MAX_FORCE = 0.05

SEPARATION_RADIUS = 25
ALIGNMENT_RADIUS = 50
COHESION_RADIUS = 75

SEPARATION_WEIGHT = 2.0
ALIGNMENT_WEIGHT = 1.0
COHESION_WEIGHT = 1.0

BOID_SIZE = 8
BG_COLOR = (30, 30, 30)
BOID_COLOR = (200, 200, 220)
FPS = 60
# --------------------------------

class Boid:
    def __init__(self, x, y):
        self.pos = Vector2(x, y)
        angle = random.uniform(0, math.tau)
        self.vel = Vector2(math.cos(angle), math.sin(angle)) * random.uniform(1.0, MAX_SPEED)
        self.acc = Vector2(0, 0)
        self.max_speed = MAX_SPEED
        self.max_force = MAX_FORCE

    def edges(self):
        # Wrap-around
        if self.pos.x > WIDTH:
            self.pos.x = 0
        elif self.pos.x < 0:
            self.pos.x = WIDTH
        if self.pos.y > HEIGHT:
            self.pos.y = 0
        elif self.pos.y < 0:
            self.pos.y = HEIGHT

    def apply_force(self, force):
        self.acc += force

    def update(self):
        self.vel += self.acc
        if self.vel.length() > self.max_speed:
            self.vel.scale_to_length(self.max_speed)
        self.pos += self.vel
        self.acc = Vector2(0, 0)

    def seek(self, target):
        desired = (target - self.pos)
        if desired.length() == 0:
            return Vector2(0, 0)
        desired.scale_to_length(self.max_speed)
        steer = desired - self.vel
        if steer.length() > self.max_force:
            steer.scale_to_length(self.max_force)
        return steer

    def behaviors(self, boids):
        sep = self.separation(boids) * SEPARATION_WEIGHT
        ali = self.alignment(boids) * ALIGNMENT_WEIGHT
        coh = self.cohesion(boids) * COHESION_WEIGHT

        self.apply_force(sep)
        self.apply_force(ali)
        self.apply_force(coh)

    def separation(self, boids):
        steer = Vector2(0, 0)
        total = 0
        for other in boids:
            if other is self:
                continue
            d = self.pos.distance_to(other.pos)
            if d < SEPARATION_RADIUS and d > 0:
                diff = (self.pos - other.pos)
                if diff.length() > 0:
                    diff /= d  # weight by distance
                steer += diff
                total += 1
        if total > 0:
            steer /= total
            if steer.length() > 0:
                steer.scale_to_length(self.max_speed)
                steer -= self.vel
                if steer.length() > self.max_force:
                    steer.scale_to_length(self.max_force)
        return steer

    def alignment(self, boids):
        avg_vel = Vector2(0, 0)
        total = 0
        for other in boids:
            if other is self:
                continue
            d = self.pos.distance_to(other.pos)
            if d < ALIGNMENT_RADIUS:
                avg_vel += other.vel
                total += 1
        if total > 0:
            avg_vel /= total
            if avg_vel.length() > 0:
                avg_vel.scale_to_length(self.max_speed)
                steer = avg_vel - self.vel
                if steer.length() > self.max_force:
                    steer.scale_to_length(self.max_force)
                return steer
        return Vector2(0, 0)

    def cohesion(self, boids):
        center = Vector2(0, 0)
        total = 0
        for other in boids:
            if other is self:
                continue
            d = self.pos.distance_to(other.pos)
            if d < COHESION_RADIUS:
                center += other.pos
                total += 1
        if total > 0:
            center /= total
            return self.seek(center)
        return Vector2(0, 0)

    def draw(self, surface):
        # Draw a triangle pointing in direction of velocity
        angle = math.atan2(self.vel.y, self.vel.x)
        p1 = Vector2(BOID_SIZE, 0).rotate_rad(angle) + self.pos
        p2 = Vector2(-BOID_SIZE * 0.6, BOID_SIZE * 0.6).rotate_rad(angle) + self.pos
        p3 = Vector2(-BOID_SIZE * 0.6, -BOID_SIZE * 0.6).rotate_rad(angle) + self.pos
        pygame.draw.polygon(surface, BOID_COLOR, [p1, p2, p3])

def create_boids(n):
    return [Boid(random.uniform(0, WIDTH), random.uniform(0, HEIGHT)) for _ in range(n)]

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Boids Simulation")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 24)
    global NUM_BOIDS

    boids = create_boids(NUM_BOIDS)
    paused = False
    running = True
    

    while running:
        dt = clock.tick(FPS) / 1000.0  # seconds per frame

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused
                elif event.key == pygame.K_r:
                    boids = create_boids(NUM_BOIDS)
                elif event.key == pygame.K_UP:
                    NUM_BOIDS += 10
                    boids.extend(create_boids(10))
                elif event.key == pygame.K_DOWN:
                    if NUM_BOIDS > 10:
                        NUM_BOIDS = max(10, NUM_BOIDS - 10)
                        boids = boids[:NUM_BOIDS]

        if not paused:
            for boid in boids:
                boid.behaviors(boids)
            for boid in boids:
                boid.update()
                boid.edges()

        screen.fill(BG_COLOR)

        for boid in boids:
            boid.draw(screen)

        # HUD
        #fps_text = font.render(f"FPS: {int(clock.get_fps())}", True, (200, 200, 200))
        #count_text = font.render(f"Boids: {len(boids)}", True, (200, 200, 200))
        #instr_text = font.render("Space pause  R reset  Up/Down change count", True, (150, 150, 150))
        #screen.blit(fps_text, (10, 10))
        #screen.blit(count_text, (10, 30))
        #screen.blit(instr_text, (10, HEIGHT - 30))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
