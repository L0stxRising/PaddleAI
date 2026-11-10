import pygame as pg
import random
import math

pg.init()
W,H=640,360
SCREEN=pg.display.set_mode((W,H))
CLOCK=pg.time.Clock()
Speed=2
PaddleH,PaddleW=50,10
WIN=7
GAME_C=0
# TODO : Make Level System with Multiple Balls
# TODO : Make Power ups obtained by hitting em from ball
# TODO : Hit streak Higher gives Benfits like faster ball hit (fire ball)
# def DrawPaddleAndScore();
class PaddleGame():
    def __init__(self):
        self.p1=PaddlePlayer(1,"tag_1")
        self.p2=PaddlePlayer(2,"tag_2")
        self.k1=[pg.K_w,pg.K_s]
        self.k2=[pg.K_UP,pg.K_DOWN]
        self.R=True
        self.P1goal=pg.Rect((W-3,-10,3,H+20))
        self.P2goal=pg.Rect((0,-10,3,H+20))
        self.ball=ball(1,5,7.5)
        self.ball.startCalc()
        
    def main(self):
        while self.R:
            for e in pg.event.get():
                if e.type==pg.QUIT:
                    print("Exiting")
                    self.R=False
                         
            self.p1.control(self.k1)
            self.p2.control(self.k2)
            self.ball.UpdatePos()
            self.ball.checkColl([self.p1,self.p2])
            self.draw()
            pg.display.flip()
            CLOCK.tick(60)
            
    def draw(self):
        SCREEN.fill("black")
        self.p1.draw(SCREEN)
        self.p2.draw(SCREEN)
        pg.draw.rect(SCREEN,"white",(W/2,-10,10,H+20))
        pg.draw.rect(SCREEN,"red",self.P1goal)
        pg.draw.rect(SCREEN,"Blue",self.P2goal)
        self.ball.draw(SCREEN)
        
    def reset(self):
        GAME_C+=1
        self.__init__()

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
    def startCalc(self,ran=[0,359]):
        self.angle=random.uniform(ran[0],ran[1])
        # print(startAngle)
        rads=self.angle*(math.pi/180)
        # So Im Not so good at math so im going Basic af
        # Assuming X axis as the Base.
        smth=math.sin(rads)
        self.speedy=-smth*self.speed
        smth=math.cos(rads)
        self.speedx=smth*self.speed
        
    def checkColl(self,objs,Predictability=3):
        collObjs=pg.sprite.spritecollide(self,objs,False,pg.sprite.collide_mask)
        if collObjs:
            self.speedx*=-1
            self.speedy*=-1
            self.startCalc([self.angle-Predictability,self.angle+Predictability])
        if self.rect.y>=H or self.rect.y<=0:
            self.speedy*=-1
        if self.rect.x>=W or self.rect.x<=0:
            self.speedx*=-1
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
        self.score=0
        self.pos=pg.Vector2(50,(H/2)-PaddleH/2) if pNum==1 else pg.Vector2(580,(H/2)-PaddleH/2)
        self.tag=tag
        self.color="blue" if pNum==1 else "red"
        self.font=pg.font.Font(None,30)
        self.textc=W/4 if self.n==1 else W-(W/4)
        self.s=s
        
        self.surface=pg.Surface((PaddleW,PaddleH),pg.SRCALPHA)
        pg.draw.rect(self.surface,self.color,pg.Rect(0,0,PaddleW,PaddleH),border_radius=2)
        self.mask=pg.mask.from_surface(self.surface)
        self.rect=self.mask.get_rect(topleft=(self.pos.x,self.pos.y))
        
    def control(self, keyset):
        keys=pg.key.get_pressed()
        if keys[keyset[0]]:
            self.rect.y-=self.s
        elif keys[keyset[1]]:
            self.rect.y+=self.s
        # So I wanted a Bit of a Recoil or smt on walls
        if self.rect.y+PaddleH>=H:
            self.rect.y-=self.s*(2)
        if self.rect.y+PaddleH<=0:
            self.rect.y+=self.s*(2)
    
    def draw(self,s):
        s.blit(self.surface,self.rect)
        
        self.text=self.font.render(f"Player_{self.n} : {self.score}",True,self.color)
        self.tpos=self.text.get_rect(centerx=self.textc,y=10)
        s.blit(self.text,self.tpos)

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
        
game=PaddleGame()
game.main()
pg.quit()