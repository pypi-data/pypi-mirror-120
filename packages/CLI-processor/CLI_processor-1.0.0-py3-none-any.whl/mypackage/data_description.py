import pandas as pd
import sys

class Description:

    def __init__(self,dataset):
        self.data = dataset

    def tasks(self):
        
        while True:
            print("Tasks of Data Description: ")
            print("1. Show Dataset")                
            print("2. Show Properties of each Column")                
            print("3. Describe a specific Column")
            print()
            
            print("What do you want to do?(Press -1 to go back) :")                
            value = int(input())


            if value==1:
                self.showdata()


            elif value==2:
                self.showdescription()
                    

            elif value==3:
                self.desc_column()

            elif value==-1:
                break   


    def showdata(self):
        length = int(input("Enter the no of rows"))
        print(self.data.head(length))

    def showdescription(self):
        print(self.data.describe())
        print(self.data.info)


    def desc_column(self):
        print("Here is the list of all Columns : ")
        for i in self.data.columns:
            print(i,end=' ')
        print()    
        while True:
            print("Enter the name of the column you want to describe : ")
            col = input()
            if col in self.data.columns :
                print(self.data[col].describe())
                break
            else:
                print(col + " is not present in the data set.")
                continue
        




