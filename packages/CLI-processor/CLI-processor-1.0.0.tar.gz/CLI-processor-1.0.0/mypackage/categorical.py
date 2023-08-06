import pandas as pd

class Categorial:
    def __init__(self,dataset):
        self.data = dataset
        self.col_list = self.data.select_dtypes(include=['object']).columns

    def tasks(self):

        while True:
            print("Tasks for Categorial encoding : ")
            print("1. Show the categorial columns")
            print("2. Perform ordinal encoding")
            print("3. Perform one hot encoding")
            print("4. Perform Dummy variable encoding")
            print("5. Show the data set")
            print()
            print("Enter your choice (press -1 to go back) : ")    
            val = int(input())

            if val==-1:
                break;

            elif val==2:
                self.ordinal()
            elif val==1:
                self.showCol()
            elif val==3:
                self.one_hot()
            elif val==4:
                self.dummy_encoding()
            elif val==5:
                self.showdata()
    

    def showCol(self):
        print("Here is the list of category columns:-")
        print()
        print("Category   Unique Values",end='')
        
        for i in self.col_list:
            print()
            print(i, "  ",self.data[i].nunique() ,end='')
        print()
    

    def ordinal(self):
        while True:    
            print("Here is the list of columns on which  you can perform ordinal encoding:-")
            for i in self.col_list:
                print(i)
            print()

            print("Enter the name of column on which  you can perform ordinal encoding(press -1 to go back):-")
            val = input()

            if val=='-1':
                break   

            elif val not in self.col_list:
                print(val + " is not present in the upper list, please enter from above list.")

            
            else:
                col_unique = self.data[val].unique()
                print(col_unique)
                dict_list = {}
                for i in range(len(col_unique)):
                    print("Enter the value for "+col_unique[i] )
                    value = int(input())
                    dict_list[col_unique[i]] = value
                self.data[val] = self.data[val].replace(dict_list)    
                print(self.data[val].head())


    def one_hot(self):
       while True:    
            print("Here is the list of columns on which  you can perform one hot encoding:-")
            for i in self.col_list:
                print(i)
            print()

            print("Enter the name of column on which  you can perform one hot encoding(press -1 to go back):-")
            val = input()

            if val=='-1':
                break   

            elif val not in self.col_list:
                print(val + " is not present in the above list, please enter from above list.")

            
            else:
                    df = pd.get_dummies(self.data[val])
                    print(df)
                    self.data = pd.concat([self.data , df],axis='columns')
                    self.data.drop([val],axis=1,inplace=True)
                    print(" One Hot Encoding is done...")
                    print(self.data.head())

    def dummy_encoding(self):
            while True:    
                print("Here is the list of columns on which  you can perform dummy encoding:-")
                for i in self.data.select_dtypes(include=['object']).columns:
                    print(i)
                print()

                print("Enter the name of column on which  you can perform dummy encoding(press -1 to go back):-")
                val = input()

                if val=='-1':
                    break   

                elif val not in self.col_list:
                    print(val + " is not present in the above list, please enter from above list.")

            
                else:
                    df = pd.get_dummies(self.data[val])
                    print(df)
                    self.data = pd.concat([self.data , df],axis='columns')
                    self.data.drop([val],axis=1,inplace=True)
                    while True:
                        for i in df.columns:
                            print(i)
                        print("Enter the name of column for removal : ")    
                        col = input()    
                        if col not in df.columns:
                            continue
                        else:
                            self.data.drop([col],axis=1,inplace=True)
                            break
                    print(" Dummy Encoding is done...")
                    print(self.data.head())
     


    def showdata(self):
            length = int(input("Enter the no of rows"))
            print(self.data.head(length))
