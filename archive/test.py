import numpy as np
import pandas as pd
print(np.random.randint(0,4))
df = pd.DataFrame(columns=["i","name"])
df.loc[0,["i","name"]] = [0,"peter"]
print(df)

on = False
if not on:
	print("not on currently")

StimInfo = "Hello"
print(StimInfo)
def fl():
	LoG = globals()
	StimInfo = LoG["StimInfo"]
	StimInfo = "Pleasure to meet you!"
	LoG["StimInfo"] = StimInfo
fl()
print(StimInfo)

n = np.array(["a","i","o","p","u"])
random.shuffle(n)
print(n)