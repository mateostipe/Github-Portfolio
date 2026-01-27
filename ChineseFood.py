import pygame
import numpy as np
pygame.init()

n = 30
separation_force = 10
separation_range = 50
alignment_force = 0.05
alignment_range = 100
cohesion_force = 0.005
cohesion_range = 200

class boidsobj:
    def __init__(self,posx,posy):
        self.x = posx
        self.y = posy
        self.vx = 1
        self.vy = -1
        self.v = 0
        self.vxseparate = 0
        self.vyseparate = 0
        self.vxalign = 0
        self.vyalign = 0
        self.boidsnearmealignment = 0
        self.vxcohesion = 0
        self.vycohesion = 0
        self.boidsnearmecohesion = 0
        self.speedlimit = 80
    def velcap(self):
        self.v = np.sqrt((self.vx*self.vx)+(self.vy*self.vy))
        if self.v > self.speedlimit:
            tempx1 = (1+((self.vy*self.vy)/(self.vx*self.vx)))
            tempx2 = np.sqrt(((self.speedlimit*self.speedlimit)/tempx1))
            tempy = ((self.vy/self.vx)*tempx2)
            if self.vx > 0:
                self.vx = tempx2
            else:
                self.vx = -tempx2
            self.vy = tempy
            self.v = np.sqrt((self.vx*self.vx)+(self.vy*self.vy))

def getRadius(posx,posy):
    pythag = (posx*posx) + (posy*posy)
    return(np.sqrt(pythag))

boid = [boidsobj((50*i*i),30*i) for i in range(n)] #Creates each boid

boid[0].x = 350
boid[0].y = 100
boid[0].vx = 30

boid[1].x = 400
boid[1].y = 210

boid[2].x = 500
boid[2].y = 200


screensize = [1200, 700] #x and then y
boidcolor = (255, 255, 255)#white
rate = 60
dt = (1/rate)


#Creates screen that everything goes on
screen = pygame.display.set_mode(screensize)
clock = pygame.time.Clock()

# Run until you click the 'x' in top right
running = True
while running: #################################################################

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Make the background BLACK
    screen.fill((0, 0, 0))

    # Draws Circle
    for i in range(n):
        vxsum = 0
        vysum = 0
        xsum = 0
        ysum = 0
        xsumdiff = 0
        ysumdiff = 0
        for j in range(n):#checks boid relative to other boids
            if i != j:#so boid doesnt check itself
                xdiff = (boid[i].x - boid[j].x)
                ydiff = (boid[i].y - boid[j].y)
                radius = getRadius(xdiff,ydiff)
                #print(i,end=" ")
                #print(j,end=" - ")
                #print(boid[i].vxseparate)

                if (radius < separation_range) and (radius > 0):########################################## Separation Logic
                    boid[i].vxseparate = ((separation_force*xdiff)/(radius-1))
                    boid[i].vyseparate = ((separation_force*ydiff)/(radius-1))
                else:
                    boid[i].vxseparate = 0
                    boid[i].vyseparate = 0
                    
        
                if radius < alignment_range and radius > 0:############################################ Alignment Logic
                    boid[i].boidsnearmealignment = boid[i].boidsnearmealignment + 1 
                    vxsum = vxsum + boid[j].vx
                    vysum = vysum + boid[j].vy
                    vxsum = vxsum/boid[i].boidsnearmealignment
                    vysum = vysum/boid[i].boidsnearmealignment
                    boid[i].vxalign = (vxsum*alignment_force / radius)
                    boid[i].vyalign = (vysum*alignment_force / radius)
                else:
                    boid[i].vxalign = 0
                    boid[i].vyalign = 0
                
                if radius < cohesion_range and radius > 20:############################################ Cohesion Logic
                    boid[i].boidsnearmecohesion = boid[i].boidsnearmecohesion + 1
                    xsum = xsum + xdiff
                    ysum = ysum + ydiff 
                    xsum = xsum/boid[i].boidsnearmecohesion
                    ysum = ysum/boid[i].boidsnearmecohesion
                    boid[i].vxcohesion = -(xsum*cohesion_force)
                    boid[i].vycohesion = -(ysum*cohesion_force)
                    #xsumdiff = boid[i].x - xsum
                    #ysumdiff = boid[i].y - ysum
                else:
                    boid[i].vxcohesion = 0
                    boid[i].vycohesion = 0
                
                boid[i].vx = boid[i].vx + boid[i].vxseparate + boid[i].vxalign + boid[i].vxcohesion
                boid[i].vy = boid[i].vy + boid[i].vyseparate + boid[i].vyalign + boid[i].vycohesion
                
                if radius < 10:
                    print(i,end='.')
                    print(j,end=':: ')
                    print(boid[i].vyseparate,end=' | ')
                    print(boid[i].vyalign,end=' | ')
                    print(boid[i].vycohesion)
                    
                
            
        
        boid[i].boidsnearmealignment = 0
        boid[i].boidsnearmecohesion = 0

        #Velocity Cap
        boid[i].velcap()

        boid[i].x = boid[i].x + boid[i].vx*dt
        boid[i].y = boid[i].y + boid[i].vy*dt        
    
        if boid[i].x > screensize[0]:
            boid[i].x = boid[i].x - screensize[0]
        if boid[i].x < 0:
            boid[i].x = boid[i].x + screensize[0]

        if boid[i].y > screensize[1]:
            boid[i].y = boid[i].y - screensize[1]
        if boid[i].y < 0:
            boid[i].y = boid[i].y + screensize[1]
        if i == 0:
            pygame.draw.circle(screen, (200,0,0), (boid[i].x, boid[i].y), 8)
        else:
            pygame.draw.circle(screen, boidcolor, (boid[i].x, boid[i].y), 8)
    
    # Updates the Screen 
    pygame.display.flip()

    clock.tick(rate)

# Done!
pygame.quit()