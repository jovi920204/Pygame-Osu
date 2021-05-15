#!/usr/bin/env python
# coding: utf-8

# In[1]:


#!/usr/bin/env python
# coding: utf-8

# In[13]:

# !pip install pygame
# !pip install slider

# In[14]:
import os,sys
from os import path
import gc
import psutil
cd=os.getcwd()
skinDir=path.join(cd,'skin')
songsDir=path.join(cd,'songs')
process = psutil.Process(os.getpid())


# In[15]:


import slider
from datetime import timedelta

import pygame
from pygame.mixer import music
from pygame.locals import *
import numpy
import math
pygame.init()
pygame.font.init()
pygame.display.init()
pygame.fastevent.init()
pygame.display.set_caption('MusicGame')
screen=pygame.display.set_mode((1366,768),flags=DOUBLEBUF)
info=pygame.display.Info()
clock=pygame.time.Clock()
pygame.mouse.set_visible(True)


# In[16]:


import timeit
timer_time=timeit.default_timer()
def timer_clear():
    global timer_time
    timer_time=timeit.default_timer()
def timer_p(num=''):
    print(num,timeit.default_timer()-timer_time)
    timer_clear()


# In[17]:


MAPINFO=0
MAPLIST=1
EVENT_PRINT=0
FPSINFO=0
AUTO=0


# In[18]:


def imageSizeFix(imageSize,screenSize):
    if imageSize[0]>screenSize[0]:
        imageSize=(screenSize[0],imageSize[1]*screenSize[0]//imageSize[0])
    if imageSize[1]>screenSize[1]:
        imageSize=(imageSize[0]*screenSize[1]//imageSize[1],screenSize[1])
    return imageSize
def imageSizeExpandX(imageSize,screenSize):
    return (screenSize[0],imageSize[1]*screenSize[0]//imageSize[0])
def imageSizeExpandY(imageSize,screenSize):
    return (imageSize[0]*screenSize[1]//imageSize[1],screenSize[1])

def BlitToWindow(surface):
    surface=pygame.transform.scale(surface,screen.get_size())
    screen.blit(surface,(0,0))
    
def ExtensionFilter(Path,Extension):
    return [k for k in os.scandir(Path) if path.splitext(k)[-1]==Extension] 

def readMusic():
    music.load(path.join(Map.songDir,Map.songMap.audio_filename))
def assignTrace(x):
    return math.floor(x*trace['Number']/513)
def loadBackground():
    global songNowDir,cd
    try:
        imageBackground=  pygame.image.load(path.join(Map.songDir,'background.jpg')).convert()
    except:
        try:
            imageBackground=  pygame.image.load(path.join(Map.songDir,'background.png')).convert()
        except:
            imageBackground=  pygame.Surface((0,0)).convert()
    return imageBackground


# In[19]:


class Register:
    def __init__(self,pos,size=(0,0),surface=None):
        self.surface=pygame.Surface(size,flags=pygame.SRCALPHA|HWSURFACE|ASYNCBLIT).convert_alpha() if surface==None else surface.convert_alpha()
        self.rect=pygame.Rect(pos,self.surface.get_size())
        self.register=[]
    @property
    def pos(self) :return self.rect.topleft
    @pos.setter
    def pos(self,_pos):self.rect.topleft=_pos
    @property
    def size(self):return numpy.array(self.rect.size)
    @size.setter
    def size(self,_size):self.rect.size=_size
        
    def clear(self):
        self.surface.fill((0,0,0,0))
    def blit(self): 
        return self.surface.blits([(sur.surface,sur.pos,sur.surface.get_clip(),BLEND_ALPHA_SDL2) for sur in self.register])

class ScoreBoard:
    def __init__(self):
        self.rect=pygame.Rect((0,0,0,0))
        self.color=(255,255,255)
        self.content=""
        self.font=pygame.font.SysFont(pygame.font.get_default_font(),100)
        self.surface=self.font.render(self.content,1,self.color).convert_alpha()
        self.__change=False
    @property
    def font(self):
        return self.__font
    @font.setter
    def font(self,_font):
        self.__font=_font
        self.__change=1
    @property
    def pos(self) :return self.rect.topleft
    @pos.setter
    def pos(self,_pos):self.rect.topleft=_pos
    @property
    def color(self):
        return self.__color
    @color.setter
    def color(self,_color):
        self.__color=_color
        self.__change=1
    @property
    def size(self):
        return self.font.size(self.content)
    @property
    def content(self):
        return self.__content
    @content.setter
    def content(self,_content):
        self.__content=_content
        self.__change=1
    def update(self):
        if self.__change:
            self.surface=self.font.render(self.content,1,self.color).convert_alpha()
            self.rect.size=self.size
            self.__change=False
        
class Animation(Register):
    def animation(self,data,startFrame=0):
        self.__data=data#[i.convert_alpha() for i in data]
        self.__length=len(data)
        self.__time=pygame.time.get_ticks()
        self.frame=startFrame
        self.surface=data[self.__frame]
    @property
    def frame(self):return self.__frame
    @frame.setter
    def frame(self,_frame):
        self.__frame=_frame
        self.surface=self.__data[self.__frame]
    @property
    def length(self):return self.__length

    def update(self,time):
        if pygame.time.get_ticks()-self.__time>time:
            self.surface=self.__data[self.frame]
            self.frame=(self.frame+1)%self.length
            self.__time=pygame.time.get_ticks()
            return True
        return False
class AnimationMultipleEffectCenter:
    blank=pygame.Surface((1,1)).convert_alpha()
    def __init__(self,center):
        self.surface=AnimationEffect.blank
        self.rect=[]
        self.__register=[]
        self.__effect=-1
        self.__effectNow=-1
        self.__time=pygame.time.get_ticks()
        self.__once=1
        self.__frame=0
        self.__length=0
        self.center=center
    def animation(self,data):
        self.__effect+=1
        self.__register.append([i for i in data])#
        self.__once=1
        siz=numpy.array(data[0].get_size())
        self.rect.append(pygame.Rect(self.center-siz//2,siz))
        return self.__effect

    def trigger(self,effectNumber):
        self.__effectNow=effectNumber
        self.__frame=0
        self.__length=len(self.__register[self.__effectNow])
    def begin(self,effectNumber):
        if self.__once:
            self.__effectNow=effectNumber
            self.__frame=0
            self.__length=len(self.__register[self.__effectNow])
            self.__once=0
    def end(self):
        self.__once=1 

    @property
    def pos(self) :return self.rect[self.__effectNow].topleft
    @pos.setter
    def pos(self,_pos):self.rect[self.__effectNow].topleft=_pos
    @property
    def size(self):return self.rect[self.__effectNow].size
    @size.setter
    def size(self,_size):self.rect[self.__effectNow].size=_size
        
    def update(self,time):
        if pygame.time.get_ticks()-self.__time>time:
            if self.__frame<self.__length:
                self.surface=self.__register[self.__effectNow][self.__frame]
                self.__frame+=1
                self.__time=pygame.time.get_ticks()
                return 1
            else:self.surface=AnimationEffect.blank
        return 0    
class AnimationEffect:
    blank=pygame.Surface((1,1)).convert_alpha()
    def __init__(self,pos):
        self.surface=AnimationEffect.blank
        self.rect=pygame.Rect(pos,(1,1))
        self.__time=pygame.time.get_ticks()
        self.__once=1
        self.__frame=0
        self.__length=0
    def animation(self,data):
        self.__register=data#
        self.rect.size=data[0].get_size()
        self.__once=1
        self.__length=len(data)

    def trigger(self):
        self.__frame=0
        
    def begin(self):
        if self.__once:
            self.__frame=0
            self.__once=0
    def end(self):
        self.__once=1 

    @property
    def pos(self) :return self.rect.topleft
    @pos.setter
    def pos(self,_pos):self.rect.topleft=_pos
    @property
    def size(self):return self.rect.size
    @size.setter
    def size(self,_size):self.rect.size=_size
        
    def update(self,time):
        if pygame.time.get_ticks()-self.__time>time:
            if self.__frame<self.__length:
                self.surface=self.__register[self.__frame]
                self.__frame+=1
                self.__time=pygame.time.get_ticks()
                return 1
            else:self.surface=AnimationEffect.blank
        return 0    
class Page(Register):
    def __init__(self):
        Register.__init__(self,(0,0),(1366,768))
    def clear(self):
            self.surface.fill((128,128,128))

class MapManager:
    def __init__(self,Path):
        self.songDir=None
        self.songMap=None
        self.path=Path
        print("Map0",process.memory_info().rss)
        self.songs=[{'dir':i,'osu':ExtensionFilter(i,'.osu')} for i in os.scandir(songsDir)]
        self.songs=[{'dir':v['dir'],'osu':[slider.Beatmap.from_path(path.join(self.path,v['dir'],k)) for k in v['osu']]} for v in self.songs]
        self.songs.sort(key=lambda k:k['dir'].name)
        for v in self.songs:
                v['osu'].sort(key=lambda k:k.overall_difficulty)
        print("Map1",process.memory_info().rss)
        if MAPLIST:
            for i,v in enumerate(self.songs):
                for _i,_v in enumerate(v['osu']):
                    print('%d,%d\t'%(i,_i),_v)    
    def readMap(self,songIndex,osuIndex):
        self.songDir=self.songs[songIndex]['dir']
        self.songMap=self.songs[songIndex]['osu'][osuIndex]            


# In[20]:


MUSIC_END=pygame.USEREVENT
# pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP,MUSIC_END])


# In[21]:


trace={
    'Skin':[pygame.image.load_extended(path.join(skinDir,'mania-key1.png')).convert_alpha(),
            pygame.image.load_extended(path.join(skinDir,'mania-key1D.png')).convert_alpha(),
           ],
    'Number':4,
    'Width':142,
    'Judge':662,
    'Speed':1,
    'Color':numpy.array((0,0,0,255)),
    'BoxWidth':info.current_w//45+(info.current_w//45+1)%2,
    'BtnKey':{v:i for i,v in enumerate("dfjk")}
}


# In[22]:


class GameMania(Page):

            
    def do(self,argument):
        Map.readMap(argument[0],argument[1])
        readMusic()
        
        self.register=[]
        if MAPINFO:
            print(vars(Map.songMap))

        background=loadBackground()
        reg=Register((self.size-background.get_size())//2,surface=background)
        self.register.append(reg)

        trace['Width']=trace['Skin'][0].get_size()[0]
        for i in range(trace['Number']):
            if i==0:
                reg=Animation(((self.size[0]-trace['BoxWidth']*(trace['Number']-1)-trace['Number']*trace['Width'])//2,0),surface=trace['Skin'][0])
            else:
                reg=Animation((self.register[-1].rect.topright[0]+trace['BoxWidth'],0),surface=trace['Skin'][0])
            reg.animation(trace['Skin'])
            self.register.append(reg)
        TraceSkin=self.register[-trace['Number']::]

        reg=Register((TraceSkin[0].rect.topleft[0],trace['Judge']),(TraceSkin[-1].rect.topright[0]-TraceSkin[0].rect.topleft[0],5))
        reg.surface.fill(trace['Color'])
        self.register.append(reg)
        TraceJudge=self.register[-1]
        TraceJudgeLineY=TraceJudge.rect.centery

        note=pygame.image.load_extended(path.join(skinDir,'mania-note1.png')).convert_alpha()
        noteX,noteY=note.get_size()
        hnote=pygame.image.load_extended(path.join(skinDir,'mania-note1L-0.png')).convert_alpha()
        hnote=pygame.transform.scale(hnote,(TraceSkin[0].size[0]//2,1))
        noteType={
            'Hold':0,
            'Down':1,
            'Up':2
        }
        hnoteX,hnoteY=hnote.get_size()
        hnoteD=2*trace['Speed']

        area=TraceJudge.size
        reg=Register(((self.size[0]-area[0])//2,0),(area[0],self.size[1]))
        self.register.append(reg)
        Notes=self.register[-1]

        mania300=[pygame.image.load_extended(path.join(skinDir,'hit300-'+str(i)+ '.png')).convert_alpha() for i in range(30)]
        mania100=[pygame.image.load_extended(path.join(skinDir,'hit100-'+str(i)+ '.png')).convert_alpha() for i in range(30)]
        mania50=[pygame.image.load_extended(path.join(skinDir,'hit50-'+str(i)+ '.png')).convert_alpha() for i in range(30)]
        mania0=[pygame.image.load_extended(path.join(skinDir,'hit0-'+str(i)+ '.png')).convert_alpha() for i in range(35)]

        for i in range(trace['Number']):
            reg=AnimationMultipleEffectCenter((TraceSkin[i].rect.center[0],trace['Judge']))
            reg.animation(mania300)
            reg.animation(mania100)
            reg.animation(mania50)
            reg.animation(mania0)
            self.register.append(reg)
        TracePoint=self.register[-trace['Number']:]

        moveTime=1500/trace['Speed']
        music.set_volume(Map.songMap.timing_points[0].volume/100)            
        
        hit_obj=Map.songMap._hit_objects.copy()
        hit_obj.reverse()
        hit_objTime=hit_obj[-1].time.total_seconds()*1000
        
        timeBoard={'Perfect':75,'Great':150,'Good':350,'Miss':500}
        scoreBoard={'Perfect':0,'Great':0,'Good':0,'Miss':0,'Combo':[0]}
        comboBoard=ScoreBoard()
        comboBoard.color=(0,255,255)
        self.register.append(comboBoard)
        
        fpsBoard=ScoreBoard()
        fpsBoard.color=(0,255,0)
        self.register.append(fpsBoard)
        
        totalNote=ScoreBoard()
        totalNote.pos=(0,fpsBoard.font.size('0')[1])
        self.register.append(totalNote)
        
        self.KEY=[True for i in range(trace['Number'])]
        music.play()
        music.set_endevent(MUSIC_END)
        while 1:
#             timer_clear()
            time=music.get_pos()
            NotesClear=[]
            event_get=pygame.fastevent.get()
            for event in event_get:
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if not AUTO:
                        if event.unicode in trace['BtnKey']:
                            index=trace['BtnKey'][event.unicode]
                            TraceSkin[index].frame=1
                            if self.KEY[index]:
                                for i,v in enumerate(Notes.register):
                                    if v.trace != index or v.type != noteType['Down']:
                                        continue
                                    for i0,k in enumerate(timeBoard.keys()):
                                        if -timeBoard[k]<=time-v.time<=timeBoard[k]:
                                            if k!='Miss':
                                                scoreBoard['Combo'][-1]+=1
                                            else:
                                                scoreBoard['Combo'][-1]=int(scoreBoard['Combo'][-1])
                                                scoreBoard['Combo'].append(0)
                                            if scoreBoard['Combo'][-1]>0:
                                                comboBoard.content=str(int(scoreBoard['Combo'][-1]))
                                            TracePoint[index].begin(i0)
                                            scoreBoard[k]+=1
                                            NotesClear.append(i)
                                            break
                                    else:
                                        continue
                                    break
                                self.KEY[index]=False
                    if event.unicode =='\x1b':
                        music.stop()
                        return
                if event.type==KEYUP:
                    if not AUTO:
                        if event.unicode in trace['BtnKey']:
                            index=trace['BtnKey'][event.unicode]
                            TraceSkin[index].frame=0
                            self.KEY[index]=True
                            for i,v in enumerate(Notes.register):
                                if v.trace!=index : 
                                    continue
                                if v.type!=noteType['Up']:
                                    break
                                for i0,k in enumerate(timeBoard.keys()):
                                    if -timeBoard[k]<=time-v.time<=timeBoard[k]:
                                        if k!='Miss':
                                            scoreBoard['Combo'][-1]+=1
                                        else:
                                            scoreBoard['Combo'][-1]=int(scoreBoard['Combo'][-1])
                                            scoreBoard['Combo'].append(0)
                                        if scoreBoard['Combo'][-1]>0:
                                            comboBoard.content=str(int(scoreBoard['Combo'][-1]))
                                        TracePoint[index].begin(i0)
                                        scoreBoard[k]+=1
                                        NotesClear.append(i)
                                        break
                                else:
                                    continue
                                break

                            TracePoint[index].end()

                if event.type == music.get_endevent():
                    print(scoreBoard)
                    return
                if EVENT_PRINT:
                    print(event)

            def compute(dt):
                return TraceJudgeLineY*dt//moveTime

            if AUTO:
                for index in range(trace['Number']):
                    for i,v in enumerate(Notes.register):
                        k='Perfect'
                        if v.type==noteType['Hold'] and time>=v.starttime:
                            length=compute(v.endtime-time)
                            v.surface.set_clip(pygame.Rect((0,0),(v.size[0],length)))
                        if v.trace==index and time>=v.endtime:
                            scoreBoard['Combo'][-1]+=1
                            comboBoard.content=str(int(scoreBoard['Combo'][-1]))
                            TracePoint[index].trigger(0)
                            scoreBoard[k]+=1
                            NotesClear.append(i)


            if len(hit_obj)>0 and time>hit_objTime-moveTime:
                t=assignTrace(hit_obj[-1].position[0])
                length=TraceJudgeLineY-compute(hit_objTime-time)
                pos=TraceSkin[t].rect.centerx-Notes.pos[0]
                if type(hit_obj[-1]) is slider.beatmap.HoldNote:
                    endtime=eval(hit_obj[-1].addition.split(':')[0])
                    endlength=TraceJudgeLineY-compute(endtime-time)
                    totalL=int((length-endlength))
                    reg=Register((pos-hnoteX//2,totalL-hnoteY//2),surface=pygame.transform.scale(hnote,(hnoteX,totalL)))
                    reg.starttime=hit_objTime
                    reg.endtime=endtime
                    reg.time=(reg.starttime+endtime)//2
                    reg.height=reg.rect.centery
                    reg.trace=t
                    reg.type=noteType['Hold']
                    Notes.register.append(reg)
                    reg=Register((pos-noteX//2,length-noteY//2),surface=note)
                    reg.starttime=hit_objTime
                    reg.endtime=hit_objTime
                    reg.time=hit_objTime
                    reg.height=reg.rect.centery
                    reg.trace=t
                    reg.type=noteType['Down']
                    Notes.register.append(reg)
                    reg=Register((pos-noteX//2,endlength-noteY//2),surface=note)
                    reg.starttime=endtime
                    reg.endtime=endtime
                    reg.time=endtime
                    reg.height=reg.rect.centery
                    reg.trace=t
                    reg.type=noteType['Up']
                    Notes.register.append(reg)
                else:
                    reg=Register((TraceSkin[t].rect.centerx-noteX//2-Notes.pos[0],length-noteY//2),surface=note)
                    reg.starttime=hit_objTime
                    reg.endtime=hit_objTime
                    reg.time=hit_objTime
                    reg.height=reg.rect.centery
                    reg.trace=t
                    reg.type=noteType['Down']
                    Notes.register.append(reg)
                hit_obj.pop()
                try:
                    hit_objTime=hit_obj[-1].time.total_seconds()*1000
                except:
                    pass
            for index,key in enumerate(self.KEY):
                TracePoint[index].update(10)
                if not key:
                    for i,v in enumerate(Notes.register):
                        if v.trace!=index or v.type != noteType['Hold']:
                            continue
                        if v.type==noteType['Hold'] and time>=v.starttime:
                            length=TraceJudgeLineY*(v.endtime-time)//moveTime
                            v.surface.set_clip(pygame.Rect((0,0),(v.size[0],length)))
                        if time >v.endtime:
                            TracePoint[index].trigger(0)
                            NotesClear.append(i)
                            break
            for i,v in enumerate(Notes.register):
                v.rect.centery=TraceJudgeLineY-compute(v.time-time)
                if  v.rect.centery>=TraceJudge.rect.centery and time-v.endtime>timeBoard['Miss']:
                    scoreBoard['Miss']+=1
                    if scoreBoard['Combo'][-1]>0:scoreBoard['Combo'].append(0)
                    comboBoard.content=""
                    NotesClear.append(i)

#             if len(Notes.register)>1000:
#                 try:
#                     Notes.register=list(list(zip(*filter(lambda x:x[0] not in NotesClear,enumerate(Notes.register))))[1])
#                 except:
#                     Notes.register=[]
#             else:
            NotesClear.sort(reverse=1)
            for i in NotesClear:
                del Notes.register[i]

            clock.tick(480)
            if FPSINFO:
                fpsBoard.content="%3.1f"%(clock.get_fps())
                fpsBoard.update()
                totalNote.content="%d"%(len(Notes.register)) 
                totalNote.update()
            comboBoard.pos=(self.size-comboBoard.size)//2
            comboBoard.update()
            
            Notes.clear()
            Notes.blit()

            if not all(self.size-screen.get_size()):
                screen.fill((128,128,128))
                screen.blits([(sur.surface,sur.pos,sur.surface.get_clip(),BLEND_ALPHA_SDL2) for sur in self.register])
            else:
                self.clear()
                self.blit()
                BlitToWindow(self.surface)
            pygame.display.flip()


# In[2]:


# import pygame,sys
# pygame.init()
# pygame.display.init()
# size = width , height = 1366,768
# screen1 = pygame.display.set_mode(size)

image1 = pygame.image.load("page1-base.png").convert()
icon_osu = pygame.image.load("page1-pygame osu.png")
icon_play = pygame.image.load("page1-play.png")
icon_exit = pygame.image.load("page1-exit.png")
# pygame.display.set_caption("pygame")


# In[3]:


class sprite(pygame.sprite.Sprite):
    def __init__(self,pos,image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = pygame.Rect(pos,image.get_size())


# In[4]:


play = sprite((738,242),pygame.Surface((334,76),flags=pygame.SRCALPHA))
play.image.fill((0,0,0,0))

eexit = sprite((738,388),pygame.Surface((334,76),flags=pygame.SRCALPHA))
eexit.image.fill((0,0,0,0))


# In[5]:


song1 = sprite((515,225),pygame.Surface((335,75),flags=pygame.SRCALPHA))
song1.image.fill((0,0,0,0))

song2 = sprite((515,468),pygame.Surface((335,75),flags=pygame.SRCALPHA))
song2.image.fill((0,0,0,0))

back = sprite((1270,675),pygame.Surface((75,75),flags=pygame.SRCALPHA))
back.image.fill((0,0,0,0))


# In[6]:


# screen2 = pygame.display.set_mode(size)
image2 = pygame.image.load("page2-base.png").convert()
icon_song1 = pygame.image.load("page2-song1.png")
icon_song2 = pygame.image.load("page2-song2.png")
icon_back = pygame.image.load("page2-back.png")
Picksong1 = pygame.image.load("page2-pick song1.png")
Picksong2 = pygame.image.load("page2-pick song2.png")
Pickback = pygame.image.load("page2-pick back.png")


# In[7]:


#建立難易度選擇的頁面
#Degree Of Difficulty
dod = pygame.image.load("dod-base.png") #背景與第二頁相同
icon_dod = pygame.image.load("page2-dod.png") #大小 92x92
Pickdod = pygame.image.load("page2-pick dod.png")
ar1 = 0
ar2 = 0
#建立數字文字
number = ["0","1","2","3","4","5","6","7","8","9"]
font_num = pygame.font.SysFont("simhei", 56)
text_num = [ScoreBoard() for i in range (10)]
for i in range(10):
    text_num[i].font = font_num
    text_num[i].color = (0,0,0)
    text_num[i].content = number[i]
    text_num[i].update()
#     text_num[i] = font_num.render(number[i],True,(0,0,0),(255,255,255))


# In[8]:


def page1():
    
    while True:
        x,y = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and eexit.rect.collidepoint(x,y):
                pygame.quit()
                sys.exit()
            if play.rect.collidepoint(x,y) and event.type == pygame.MOUSEBUTTONDOWN:
                page2()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        screen.fill((0,0,0,0))
        screen.blit(image1,(0,0))
        screen.blit(icon_osu,(245,140))
        screen.blit(icon_play,play.rect.topleft)
        screen.blit(icon_exit,eexit.rect.topleft)
        screen.blit(play.image,play.rect.topleft)
        screen.blit(eexit.image,eexit.rect.topleft)
        pygame.display.update()
        


# In[9]:


def page2():
    global ar1,ar2
    while True:
        x,y = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if back.rect.collidepoint(x,y) and event.type == pygame.MOUSEBUTTONDOWN:
                page1()
            if song1.rect.collidepoint(x,y) and event.type == pygame.MOUSEBUTTONDOWN:
                ar1 = 2 #song1被選取時，ar1 = 0，並跳轉到page_dod，把難易度的數量一併丟過去
                page_dod(len(Map.songs[ar1]['osu']))
            if song2.rect.collidepoint(x,y) and event.type == pygame.MOUSEBUTTONDOWN:
                ar1 = 1 #song1被選取時，ar1 = 0，並跳轉到page_dod，把難易度的數量一併丟過去
                page_dod(len(Map.songs[ar1]['osu']))
        screen.fill((0,0,0,0))
        screen.blit(image2,(0,0))
        screen.blit(icon_song1,(515,225))
        screen.blit(icon_song2,(515,468))
        screen.blit(icon_back,(1270,675))
        if song1.rect.collidepoint(x,y):
            screen.blit(Picksong1,(515,225))
        elif song2.rect.collidepoint(x,y):
            screen.blit(Picksong2,(515,468))
        elif back.rect.collidepoint(x,y):
            screen.blit(Pickback,(1270,675))   
        pygame.display.update()


# In[10]:


def page_dod(dod_num):
    global ar1,ar2
    lenth = 92*dod_num + 26*(dod_num-1) #包含選取方塊長度和每個方塊的間距
    while True:
        button = [0 for i in range(dod_num)]
        for i in range(dod_num): #生成選取方塊的rect
            button[i] = sprite(((1366-lenth)/2+i*26+i*92,338),pygame.Surface((92,92),flags=pygame.SRCALPHA))
            button[i].image.fill((0,0,0,0))
        x,y = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if back.rect.collidepoint(x,y) and event.type == pygame.MOUSEBUTTONDOWN:
                page2()
            for i in range(dod_num):
                if button[i].rect.collidepoint(x,y) and event.type == pygame.MOUSEBUTTONDOWN:
                    ar2 = i
                    playsong(ar1,ar2)
        screen.fill((0,0,0,0))
        screen.blit(dod,(0,0))
        screen.blit(icon_back,(1270,675))
        if back.rect.collidepoint(x,y):
            screen.blit(Pickback,(1270,675))
        for i in range(dod_num):
            screen.blit(icon_dod,button[i].rect.topleft)
            screen.blit(button[i].image,button[i].rect.topleft)
            text_num[i].rect.center=button[i].rect.center
            screen.blit(text_num[i+1].surface,text_num[i].pos)
        pygame.display.update()


# In[11]:


def playsong(ar1,ar2):
    GameStart=GameMania()
    GameStart.do([ar1,ar2])
    del GameStart
    gc.collect()
#把我選取歌的圖示分別給予一個Index，當點選時，把那個Index值丟給playsong(Index)函數中的GameStart.do([Index])
#如此一來，就能夠簡化程式碼，讓程式不佔記憶體太多空間


# In[12]:


try:
    os.remove('/songs/.DS_Store')
except:
    pass
Map=MapManager(songsDir)
# print(len(Map.songs[0]['osu']))  列印出第0首個中，有幾個難易度可供選擇
page1()


# In[ ]:





# In[ ]:




