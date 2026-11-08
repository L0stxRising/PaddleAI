import pygame as pg

pg.init()
W,H=640,360
SCREEN=pg.display.set_mode((W,H))
CLOCK=pg.time.Clock()
Speed=2
PaddleH,PaddleW=50,10
WIN=7
# TODO : Make Level System with Multiple Balls
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
        
    def main(self):
        while self.R:
            for e in pg.event.get():
                if e.type==pg.QUIT:
                    print("Exiting")
                    self.R=False
                         
            self.p1.control(self.k1)
            self.p2.control(self.k2)
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


class PaddlePlayer():
    def __init__(self,pNum,tag="Human"):
        self.n=pNum
        self.startPos=pg.Vector2(75,(H/2)-PaddleH/2) if pNum==1 else pg.Vector2(565,(H/2)-PaddleH/2)
        self.score=0
        self.pos=self.startPos
        self.tag=tag
        self.color="blue" if pNum==1 else "red"
        self.font=pg.font.Font(None,30)
        self.textc=W/4 if self.n==1 else W-(W/4)
        
    def control(self, keyset):
        keys=pg.key.get_pressed()
        if keys[keyset[0]]:
            self.pos.y-=Speed
        elif keys[keyset[1]]:
            self.pos.y+=Speed
        # So I wanted a Bit of a Recoil or smt on walls
        if self.pos.y+PaddleH>=H:
            self.pos.y-=Speed*(2)
        if self.pos.y+PaddleH<=0:
            self.pos.y+=Speed*(2)
    
    def draw(self,s):
        r=pg.Rect(self.pos.x,self.pos.y,PaddleW,PaddleH)
        pg.draw.rect(s,self.color,r,5,border_radius=2)
        self.text=self.font.render(f"Player_{self.n} : {self.score}",True,self.color)
        self.tpos=self.text.get_rect(centerx=self.textc,y=10)
        SCREEN.blit(self.text,self.tpos)

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