import pandas as pd
import sys

df = pd.read_csv(sys.argv[1], header = None, sep = ",")
df_s = df.sample(int(sys.argv[2]))
df_s.to_csv(sys.argv[3], header = False, index = False)
