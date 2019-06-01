from texttable import Texttable

def printing(data):
  t = Texttable()
  t.add_rows(data)
  print(t.draw())
  
def zeros(df,column):
  zeros=(df[column]==0).sum()
  total=df[column].count()
  return round((zeros * 100) / total,2)

def missing(df,column):
  miss = df[column].isnull().sum()
  total=df[column].count()
  return round((miss * 100) / total,2)
  
def central_tendency(df,column):
  mean=df[column].mean()
  median=df[column].median()
  mode=df[column].mode().values.tolist()
  min=df[column].min()
  max=df[column].max()
  count=df[column].count()
  zero=zeros(df,column)
  miss=missing(df,column)
  t_list= [['Colunm','Mean','Median','Mode','Min','Max','Count','Zeros %','Missing %']]
  t_list= t_list + [[column,mean,median,mode,min,max,count,(str(zero)+"%"),(str(miss)+"%")]]
  printing(t_list)

def measure_of_dispersion(df,column):
  rnge=(df[column].max()-df[column].min())
  var=df[column].var()
  sd=df[column].std()
  md=df[column].mad()
  q1=df[column].quantile(0.25)
  q3=df[column].quantile(0.75)
  iqr=(q3-q1)
  skw=df[column].skew()
  kut=df[column].kurt()
  t_list= [['Colunm','Range','Variance','STDev','Deviation','IQR','Skewness','kurtosis']]
  t_list= t_list + [[column,rnge,var,sd,md,iqr,skw,kut]]
  printing(t_list)
  
  
def continuous_analysis(df,column):
  t_list= [['Univariate analysis calculate central_tendency']]
  printing(t_list)
  central_tendency(df,column)
  t_list= [['Univariate analysis calculate measure of dispersion']]
  printing(t_list)
  measure_of_dispersion(df,column)