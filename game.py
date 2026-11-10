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

P1=1
P2=0
class PaddleGame():
    def __init__(self):
        self.p1=PaddlePlayer(1,"tag_1",win=P1)
        self.p2=PaddlePlayer(2,"tag_2",win=P2)
        self.k1=[pg.K_w,pg.K_s]
        self.k2=[pg.K_UP,pg.K_DOWN]
        self.R=True
        self.P1goal=pg.Rect((W-3,-10,3,H+20))
        self.P2goal=pg.Rect((0,-10,3,H+20))
        self.surface=pg.Surface([W,H],pg.SRCALPHA)
        pg.draw.rect(self.surface,"white",(W/2,-10,10,H+20))
        pg.draw.rect(self.surface,"red",(W-3,-10,3,H+20))
        pg.draw.rect(self.surface,"Blue",(0,-10,3,H+20))
        self.Mrect=pg.Rect(0,0,W,H)
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
            self.checkwin()
            self.draw()
            pg.display.flip()
            CLOCK.tick(100000)
            
    def checkwin(self):
        global P1 ,P2
        # if P2>11:
        #     P2+=1
        #     self.reset()
        # elif P1>11:
        #     P1+=1
        #     self.reset()
        if self.P1goal.colliderect(self.ball.rect):
            P1+=1
            self.reset()
        elif self.P2goal.colliderect(self.ball.rect):
            P2+=1
            self.reset()
    def draw(self):
        SCREEN.fill("black")
        SCREEN.blit(self.surface,self.Mrect)
        self.p1.draw(SCREEN)
        self.p2.draw(SCREEN)
        self.ball.draw(SCREEN)
        
    def reset(self):
        global GAME_C
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
    def startCalc(self,ran=[30,330]):
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
        
    def checkColl(self,objs,Predictability=1):
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
        self.speedy=min(max(self.speedy,-8),8)
        if abs(self.speedy)<2:
            self.speedy=2
    def UpdatePos(self):
        # self.calc()
        self.rect.x+=self.speedx
        self.rect.y+=self.speedy
        
    def draw(self,s):
        s.blit(self.surface,self.rect)
        
class PaddlePlayer(pg.sprite.Sprite):
    def __init__(self,pNum,tag="Human",s=2,win=0):
        super().__init__()
        self.n=pNum
        self.score=win
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
        
        self.movef=0
        self.currentSpeed=0
    def control(self, keyset):
        keys=pg.key.get_pressed()
        self.currentSpeed=max(min(self.s*(self.movef*0.01),self.s*1.5),self.s)
        if keys[keyset[0]]:
            self.rect.y-=self.currentSpeed
            self.movef+=1
        elif keys[keyset[1]]:
            self.rect.y+=self.currentSpeed
            self.movef+=1
        else:
            self.movef=0
            self.currentSpeed=0
        # So I wanted a Bit of a Recoil or smt on walls
        if self.rect.y+PaddleH>=H:
            self.rect.y-=self.s*(2)
        if self.rect.y<=0:
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