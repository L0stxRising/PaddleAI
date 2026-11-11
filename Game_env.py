# import os
# os.environ["SDL_VIDEODRIVER"] = "dummy"

import pygame as pg
import random
import math
from PIL import Image

W,H=640,360
Speed=2
PaddleH,PaddleW=50,10

class PaddleGameENV():
    def __init__(self):
        self.SCREEN=pg.Surface((W,H))
        
        self.p1=PaddlePlayer(1,"tag_1",s=5)
        self.p2=PaddlePlayer(2,"tag_2",s=5)
        self.P1goal=pg.Rect((W-3,-10,3,H+20))
        self.P2goal=pg.Rect((0,-10,3,H+20))
        self.surface=pg.Surface([W,H],pg.SRCALPHA)
        pg.draw.rect(self.surface,"white",(W/2,-10,10,H+20))
        pg.draw.rect(self.surface,"red",(W-3,-10,3,H+20))
        pg.draw.rect(self.surface,"Blue",(0,-10,3,H+20))
        self.Mrect=pg.Rect(0,0,W,H)
        
        self.ball=ball(1,5,7.5)
        self.ball.startCalc()

        self.truncated=False
        
    def reward(self,win,p):
        return win[p]*2
    
    def step(self,p1C,p2C):

        self.p1.control(p1C)
        self.p2.control(p2C)
        self.ball.UpdatePos()
        self.ball.checkColl([self.p1,self.p2])
        won=self.checkwin()
        self.draw(self.SCREEN)
        
        rewardP1=self.reward(won,0)
        rewardP2=self.reward(won,1)
        
        return [self.get_obs(self.SCREEN), rewardP1, rewardP2, won, self.truncated]
            
    def checkwin(self):
        if self.P1goal.colliderect(self.ball.rect):
            self.truncated=True
            return [1,-1]
        elif self.P2goal.colliderect(self.ball.rect):
            self.truncated=True
            return [-1,1]
        else:
            return [0,0]
        
    def draw(self,SCREEN):
        SCREEN.fill("black")
        SCREEN.blit(self.surface,self.Mrect)
        self.p1.draw(SCREEN)
        self.p2.draw(SCREEN)
        self.ball.draw(SCREEN)
    
    def get_obs(self,Screen):
        im=pg.image.tobytes(Screen,"RGB")
        return Image.frombytes("RGB",Screen.get_size(),im).convert("L")

    def reset(self):
        self.truncated=False
        self.ball=ball(1,5,7.5)
        self.ball.startCalc()

class ball(pg.sprite.Sprite):
    def __init__(self,n,speed,r=5):
        super().__init__()
        self.n=n
        self.r=r
        
        self.speed=speed
        self.speedx=0
        self.speedy=0
        
        self.surface=pg.Surface((r*2,r*2),pg.SRCALPHA)
        pg.draw.circle(self.surface,"green",(r,r),self.r)
        self.mask=pg.mask.from_surface(self.surface)
        self.rect=self.mask.get_rect(center=(W/2+5,H/2))
        
        self.angle=None
    def startCalc(self):
        r1,r2=random.uniform(-45,45),random.uniform(135,225)
        self.angle=random.choice([r1,r2])
        # print(startAngle)
        rads=self.angle*(math.pi/180)
        # So Im Not so good at math so im going Basic af
        # Assuming X axis as the Base.
        smth=math.sin(rads)
        self.speedy=-smth*self.speed
        smth=math.cos(rads)
        self.speedx=smth*self.speed
        
    def checkColl(self,objs):
        collObjs=pg.sprite.spritecollide(self,objs,False,pg.sprite.collide_mask)
        if collObjs:
            # self.startCalc([self.angle-Predictability,self.angle+Predictability])
            self.speedx*=-1
            self.speedy+=collObjs[0].currentSpeed*0.2+random.uniform(-0.5,0.5)
        if self.rect.y+self.r>H:
            self.rect.bottom=H
            self.speedy*=-1
            self.speedy+=(random.uniform(-0.2,0.2)*self.speedy)
        elif self.rect.y<0:
            self.rect.top=0
            self.speedy*=-1
            self.speedy+=(random.uniform(-0.2,0.2)*self.speedy)
        if self.rect.x+self.r>W:
            self.rect.right=W
            self.speedx*=-1
        elif self.rect.x<0:
            self.rect.left=0
            self.speedx*=-1
        self.speedy=min(max(self.speedy,-7),7)
        if abs(self.speedy)<2:
            self.speedy=2
    def UpdatePos(self):
        # self.calc()
        self.rect.x+=self.speedx
        self.rect.y+=self.speedy
        
    def draw(self,s):
        s.blit(self.surface,self.rect)
        
class PaddlePlayer(pg.sprite.Sprite):
    def __init__(self,pNum,tag="Human",s=2):
        super().__init__()
        self.n=pNum
        self.pos=pg.Vector2(50,(H/2)-PaddleH/2) if pNum==1 else pg.Vector2(580,(H/2)-PaddleH/2)
        self.tag=tag
        self.color="blue" if pNum==1 else "red"
        self.s=s
        
        self.surface=pg.Surface((PaddleW,PaddleH),pg.SRCALPHA)
        pg.draw.rect(self.surface,self.color,pg.Rect(0,0,PaddleW,PaddleH),border_radius=2)
        self.mask=pg.mask.from_surface(self.surface)
        self.rect=self.mask.get_rect(topleft=(self.pos.x,self.pos.y))
        
        self.movef=0
        self.currentSpeed=0
    def control(self, keyset):
        # Keyset = [Up,Down]
        self.currentSpeed=max(min(self.s*(self.movef*0.01),self.s*1.5),self.s)
        if keyset[0]:
            self.rect.y-=self.currentSpeed
            self.movef+=1
        elif keyset[1]:
            self.rect.y+=self.currentSpeed
            self.movef+=1
        else:
            self.movef=0
            self.currentSpeed=0

        if self.rect.y+PaddleH>=H:
            self.rect.y-=self.s*(2)
        if self.rect.y<=0:
            self.rect.y+=self.s*(2)
    
    def draw(self,s):
        s.blit(self.surface,self.rect)
        

# def main():
#     R=True
#     p1=PaddleGame(1)
#     p2=PaddleGame(2)
#     k1=[pg.K_w,pg.K_s]
#     k2=[pg.K_UP,pg.K_DOWN]
#     while R:
#         for e in pg.event.get():
#             if e.type==pg.QUIT:
#                 print("Exiting")
#                 R=False
                
#         SCREEN.fill("black")
#         p1.control(k1)
#         p2.control(k2)
#         p1.draw(SCREEN)
#         p2.draw(SCREEN)
#         pg.display.flip()
#         CLOCK.tick(60)
if __name__=="__main__":
    game=PaddleGameENV()
    for _ in range(10000):
        game.step([1,0],[0,1])
    Image.Image.show(game.step([0,1],[1,0])[0])