import numpy as np
import pandas as pd
print(np.random.randint(0,4))
df = pd.DataFrame(columns=["i","name"])
df.loc[0,["i","name"]] = [0,"peter"]
print(df)