import matplotlib.pyplot as plt
import numpy as np

#data = [[df1, column1, low_limit1, high_limit1, label1, linestyle, color], ...]
def plot_numeric_cdf(data, x_label, xlim = None, ylim = None):
    for item in data:
        df = item[0]
        column_name = item[1]
        low_limit = item[2]
        high_limit = item[3]
        label = item[4]
        linestyle = item[5]
        color = item[6]
        if low_limit == None and high_limit == None:
            df_l = df
        elif low_limit == None:
            df_l = df[df[column_name] <= high_limit]
        elif high_limit == None:
            df_l = df[df[column_name] >= low_limit]
        else:
            df_l = df[(df[column_name] >= low_limit) & (df[column_name] <= high_limit)]
            
        df_g = df_l.groupby([column_name]).size().reset_index(name = "count")
        cdf = np.cumsum(df_g['count']/np.sum(df_g['count']))
        plt.plot(df_g[column_name], cdf, linestyle = linestyle, color = color, label = label)
    if ylim == None:
        plt.ylim((0,1))
    else:
        plt.ylim(ylim)
    
    if xlim != None:
        plt.xlim(xlim)
    plt.ylabel("CDF")
    plt.xlabel(x_label)
    plt.grid(True)
    plt.legend()
    plt.show()

def plot_pie(categories, values):
    fig = plt.figure()
    ax = fig.add_axes([0,0,1,1])
    ax.axis('equal')
    ax.pie(values, labels = categories,autopct='%1.2f%%')
    plt.show()
