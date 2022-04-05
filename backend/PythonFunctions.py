import pandas as pd


def ReplaceWMean(df,colName):
    Mean = df[colName].mean()
    Col = df[colName].fillna(value=Mean)
    df[colName] = Col
    return(df)
  
  
  #print(ReplaceWMean(df,'ColumnA'))
  
  
  
def ReplaceWMode(df,colName):
    Mode = df[colName].mode()
    Col = df[colName].fillna(value=int(Mode))
    df[colName] = Col
    return(df)
  
  
  #print(ReplaceWMode(df,'ColumnC'))
  
  
  
  def ReplaceWMedian(df,colName):
    Median = df[colName].median()
    Col = df[colName].fillna(value=Median)
    df[colName] = Col
    return(df)

  
  print(ReplaceWMedian(df,'ColumnB'))
