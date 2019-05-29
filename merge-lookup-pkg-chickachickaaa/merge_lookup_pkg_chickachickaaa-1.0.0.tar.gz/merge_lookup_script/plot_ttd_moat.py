import pandas as pd 
import matplotlib.pyplot as plt


#false_plot_ttd.xlsx upload this file to data frame in pandas

#with the df we'll show bar charts of each unique domain and their count
#x axis label is domain name
#y axis label is number count
#two bar charts one for ttd one for moat
#make clear this is for unmatched only 

def main():

df = pd.read_excel("false_plot_ttd.xlsx", encoding="utf-8")
print(df)
df.plot()
plt.show()

if __name__ == "__main__":
    main()