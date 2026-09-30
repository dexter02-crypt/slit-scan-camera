"""Shared-by-copy local-camera helpers; each repository runs independently."""
from pathlib import Path
import json
import time
import uuid
import cv2
import numpy as np


def frame_ok(frame):
    if not isinstance(frame,np.ndarray) or frame.dtype!=np.uint8 or frame.ndim!=3 or frame.shape[2]!=3:
        raise ValueError('Expected a uint8 BGR image.')
    if min(frame.shape[:2])<16 or frame.shape[0]*frame.shape[1]>12_000_000:
        raise ValueError('Use a frame from 16 pixels to 12 megapixels.')
    return frame


def fit(frame,width=960):
    frame_ok(frame)
    if frame.shape[1]<=width:return frame.copy()
    return cv2.resize(frame,(width,round(width*frame.shape[0]/frame.shape[1])),interpolation=cv2.INTER_AREA)


def panel(frame,lines):
    bottom=np.full((90,frame.shape[1],3),(22,18,14),np.uint8)
    for i,line in enumerate(lines[:3]):
        cv2.putText(bottom,str(line)[:140],(12,24+24*i),cv2.FONT_HERSHEY_SIMPLEX,.48,(235,235,235),1,cv2.LINE_AA)
    return np.vstack([frame,bottom])


def save_image(frame,root='outputs'):
    frame_ok(frame);root=Path(root)
    if root.is_symlink():raise ValueError('Refusing a symlink output directory.')
    root.mkdir(parents=True,exist_ok=True)
    path=root/('capture-'+time.strftime('%Y%m%d-%H%M%S')+'-'+uuid.uuid4().hex[:10]+'.png')
    ok,data=cv2.imencode('.png',frame)
    if not ok:raise ValueError('PNG encoding failed.')
    with path.open('xb') as f:f.write(data.tobytes())
    print('Saved locally:',path,flush=True)
    return path


def live(processor,index=0,title='KedByte Camera',allow_snapshots=False):
    if isinstance(index,bool) or not isinstance(index,int) or not 0<=index<=8:
        raise ValueError('Use a local camera index 0..8.')
    cap=cv2.VideoCapture(index)
    if not cap.isOpened():cap.release();raise ValueError('Cannot open camera; check permission or select --camera 1.')
    cap.set(cv2.CAP_PROP_FRAME_WIDTH,1280);cap.set(cv2.CAP_PROP_FRAME_HEIGHT,720)
    current=None
    try:
        cv2.namedWindow(title,cv2.WINDOW_AUTOSIZE)
        def click(event,x,y,flags,param):
            if event==cv2.EVENT_LBUTTONDOWN and current is not None and 0<=y<current.shape[0] and 0<=x<current.shape[1]:
                if hasattr(processor,'click'):
                    try:processor.click(current,x,y)
                    except ValueError as e:print('Selection:',e,flush=True)
        cv2.setMouseCallback(title,click)
        print('Local camera only. No recording/upload. S saves one image only with --allow-snapshots.',flush=True)
        while True:
            ok,raw=cap.read()
            if not ok:raise ValueError('Camera stopped returning frames.')
            current=fit(cv2.flip(frame_ok(raw),1));image=processor.process(current,time.monotonic())
            cv2.imshow(title,panel(image,processor.help()))
            key=cv2.waitKey(1)&255
            if key in (ord('q'),27):break
            if key==ord('s'):
                if allow_snapshots:save_image(image)
                else:print('Snapshots disabled. Use --allow-snapshots to enable S.',flush=True)
            else:processor.key(key,current)
            if cv2.getWindowProperty(title,cv2.WND_PROP_VISIBLE)<1:break
    finally:cap.release();cv2.destroyAllWindows()


def demo_frame(step=0,w=640,h=360):
    yy,xx=np.mgrid[:h,:w];base=np.empty((h,w,3),np.uint8)
    base[...,0]=(xx//4+step*2)%190+30;base[...,1]=(yy//2+step)%170+25;base[...,2]=50
    for x in range(0,w,40):cv2.line(base,(x,0),(x,h-1),(100,85,80),1)
    for y in range(0,h,40):cv2.line(base,(0,y),(w-1,y),(100,85,80),1)
    cv2.circle(base,(100+(step*5)%(w-160),h//2),48,(70,210,245),-1,cv2.LINE_AA)
    return base


def cli(factory,title,demo,check):
    import argparse
    p=argparse.ArgumentParser(description=title)
    p.add_argument('command',choices=['camera','demo','check'])
    p.add_argument('--camera',type=int,default=0);p.add_argument('--allow-snapshots',action='store_true')
    a=p.parse_args()
    if a.command=='camera':live(factory(),a.camera,title,a.allow_snapshots)
    elif a.command=='check':check();print('Native synthetic check passed; live-camera behavior is a separate check.')
    else:save_image(demo());print('Synthetic demonstration, not a camera capture.')
