"""Time-slice compositing: each strip comes from a different camera instant."""
import math
import numpy as np
from common import frame_ok


class SlitScan:
    def __init__(self,speed=120):
        if not math.isfinite(speed) or not 10<=speed<=600:raise ValueError('Speed must be 10..600 pixels per second.')
        self.speed=speed;self.axis=1;self.paused=False;self.canvas=None;self.cursor=0.;self.last=None;self.completed=False

    def reset(self):self.canvas=None;self.cursor=0.;self.last=None;self.completed=False

    def process(self,frame,t):
        frame_ok(frame)
        if not math.isfinite(t) or t<0 or (self.last is not None and t<self.last):raise ValueError('Time must not go backward.')
        if self.canvas is None or self.canvas.shape!=frame.shape:
            self.canvas=np.zeros_like(frame);self.cursor=0.;self.last=t;self.completed=False
        dt=min(.1,t-self.last);self.last=t
        if not self.paused and not self.completed:
            extent=frame.shape[self.axis];old=int(self.cursor)
            self.cursor=min(float(extent),self.cursor+dt*self.speed);new=int(self.cursor)
            if new>old:
                if self.axis==1:self.canvas[:,old:new]=frame[:,old:new]
                else:self.canvas[old:new,:]=frame[old:new,:]
            self.completed=new>=extent
        image=self.canvas.copy()
        if not self.completed:
            k=min(frame.shape[self.axis]-1,int(self.cursor))
            if self.axis==1:image[:,k:]=frame[:,k:];image[:,k:k+2]=(230,240,60)
            else:image[k:,:]=frame[k:,:];image[k:k+2,:]=(230,240,60)
        return image

    def key(self,key,frame=None):
        if key==ord('r'):self.reset()
        if key==32:self.paused=not self.paused
        if key in (ord('h'),ord('v')):
            self.axis=0 if key==ord('h') else 1;self.reset()

    def help(self):
        return ['SLIT SCAN | time slices, not object recognition',
                'R new scan | H horizontal sweep | V vertical sweep | SPACE pause | Q exit',
                'Scan complete: press R' if self.completed else 'Move while the line sweeps; S saves only with --allow-snapshots']
