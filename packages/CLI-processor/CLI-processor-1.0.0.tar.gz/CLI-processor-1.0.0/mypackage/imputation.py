import pandas as pd
import numpy as np

class Imputation:
    def __init__(self,dataset):
        self.data = dataset

    def tasks(self):
        
        while True:
            print("Tasks of Imputation: ")
            print("1. Show number of NULL values")                
            print("2. Remove Columns")                
            print("3. Fill Null Values with Mean")
            print("4. Fill Null Values with Median")
            print("5. Fill Null Values with Mode")
            print("6. Deleting rows with Null Values")
            print("7. Show the dataset")
            print()
            
            print("What do you want to do?(Press -1 to go back) :")                
            value = int(input())


            if value==1:
                self.showNull()

            elif value==2:
                self.removeColumn()
                    
            elif value==3:
                self.changeWithMean()

            elif value==4:
                self.changeWithMedian()

            elif value==5:
                self.changeWithMode()

            elif value==6:
                self.removeRows()

            elif value==7:
                self.showdata()

            elif value==-1:
                break   


    def showNull(self):
        print(self.data.isnull().sum())

    def removeColumn(self):
        while True:
            print("Here is the list of all Columns : ")
            for i in self.data.columns:
                print(i,end=' ')
            print()
            while True:
                print("Enter the name of the column you want to delete(Press q to back) : ")
                col = input()
                if col in self.data.columns :
                    self.data.drop(col,inplace=True,axis=1)
                    print("Column "+col+" is removed from the dataset.")
                    break
                 
                else:
                    print(col + " is not present in the data set.")
                    continue    
            print("If you want to delete more press 1 else 0 : ")
            val = int(input())
            if val==1:
                continue
            else:
                break        

    def removeRows(self):
        print("Shape of dataset before deleting : ",self.data.shape)
        self.data.dropna(inplace=True)
        print("Shape of dataset after deleting : ",self.data.shape)

    def changeWithMean(self):    
                while True:
                    print("Here is the list of all Columns : ")
                    for i in self.data.columns:
                        print(i,end=' ')
                    print()
                    while True:
                        print("Enter the name of the column  : ")
                        col = input()
                        if col in self.data.columns :
                            if self.data.dtypes[col] == np.object:
                                print(col+" has not a numeric data type")
                                break
                            self.data[col] = self.data[col].replace(np.nan,self.data[col].mean())
                            print("Null values of Column "+ col +" is replaced with mean.")
                            break
                        else:
                            print(col + " is not present in the data set.")
                            continue    
                    print("If you want to do more press 1 else 0 : ")
                    val = int(input())
                    if val==1:
                        continue
                    else:
                        break        

    def changeWithMedian(self):
                while True:
                    print("Here is the list of all Columns : ")
                    for i in self.data.columns:
                        print(i,end=' ')
                    print()
                    while True:
                        print("Enter the name of the column  : ")
                        col = input()
                        if col in self.data.columns :
                            if self.data.dtypes[col] == np.object:
                                print(col+" has not a numeric data type")
                                break
                            self.data[col] = self.data[col].replace(np.nan,self.data[col].median())
                            print("Null values of Column "+ col +" is replaced with median.")
                            break
                        else:
                            print(col + " is not present in the data set.")
                            continue    
                    print("If you want to do more press 1 else 0 : ")
                    val = int(input())
                    if val==1:
                        continue
                    else:
                        break            
            
    def changeWithMode(self):
    
            while True:
                    print("Here is the list of all Columns : ")
                    for i in self.data.columns:
                        print(i,end=' ')
                    print()
                    while True:
                        print("Enter the name of the column  : ")
                        col = input()
                        if col in self.data.columns :
                            # if self.data.dtypes[col] == np.object:
                            #     print(col+" has not a numeric data type")
                            #     break
                            self.data[col] = self.data[col].replace(np.nan,self.data[col].mode()[0])
                            print("Null values of Column "+ col +" is replaced with mode.")
                            break
                        else:
                            print(col + " is not present in the data set.")
                            continue    
                    print("If you want to do more press 1 else 0 : ")
                    val = int(input())
                    if val==1:
                        continue
                    else:
                        break


    def showdata(self):
        length = int(input("Enter the no of rows"))
        print(self.data.head(length))
                        

