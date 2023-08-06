import pandas as pd
import sys
import os

class Download:
    def __init__(self,dataset):
        self.data = dataset

    def download(self):
        while 1:
            print("Enter the name of filename : ")
            val = input()
            file = val+".csv"

            b = os.listdir()
            print(b)
            c=0
            for i in b:
                if i==file:
                    c=1
                    print("Enter another name of file, file with this name exits")
                    break
            if c==1:
                continue    
            else:
                pd.DataFrame(self.data).to_csv(file,index=False)
                print()
                print("Everything is done, Now enjoy!!!!!!!!!!")    
                sys.exit()