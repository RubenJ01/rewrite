import random as r
from PIL import Image as Im
from pathlib import Path


def coin_flip():
	heads_or_tails = r.choice(['heads','tails']) 
	coinHT = heads_or_tails'.png'
	NAMEFILE = Path('artwork') / coinHT
	print(heads_or_tails,NAMEFILE)
	with Im.open(NAMEFILE) as img:
		return img
