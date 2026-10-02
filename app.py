"""Local camera time-warp experiment."""
import sys

__version__ = "0.1.0"
from common import cli,demo_frame
from core import SlitScan


def demo():
    s=SlitScan(300)
    for i in range(66):out=s.process(demo_frame(i),i/30)
    return out


def check():
    import numpy as np
    s=SlitScan(200);a=np.full((20,40,3),30,np.uint8);b=np.full_like(a,200)
    s.process(a,0);s.process(a,.1);out=s.process(b,.2)
    assert s.completed and np.all(out[:,:20]==30) and np.all(out[:,20:]==200)


if __name__=='__main__':
    try:cli(SlitScan,'KedByte Slit Scan',demo,check)
    except (ValueError,OSError,RuntimeError) as e:print('Stopped:',e,file=sys.stderr);sys.exit(2)
