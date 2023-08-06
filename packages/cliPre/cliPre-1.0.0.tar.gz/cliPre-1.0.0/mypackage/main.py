import sys
import pandas as pd
from data_description import Description
from imputation import Imputation
from categorical import Categorial
from feature_scaling import Feature
from download import Download

class Preprocessing:
    def __init__(self):
         if(len(sys.argv)!=2 or sys.argv[1].endswith('.csv')!=1):
             print("No of arguments are not meet its requirments.")
             return   
         else:
            print("Welcome to  machine learnig cli tool")     

    def remove_column(self):
        self.df = pd.read_csv('train.csv')
        print(self.df.head())
        print("Here is the list list of all the columns")
        for i in self.df.columns:
            print(i,end=' ')
        print()    
        while True:
            print("Enter the target column : ")
            col = input()
            print(col)

            print("Are you Sure(y/n)")
            res = input()
            if res=='y':
                if col in self.df.columns:
                    self.df.drop(col,axis=1,inplace=True)
                    print(self.df.head())
                    print(self.df.columns)
                    print("Done....")
                    break 
                else:
                    print("Entered value in not present in columns list , Re-enter the column")
                    continue   

    def tasks(self):
        while True:
            print("Tasks....")
            print("1. Data Description")                
            print("2. Handling Null Values")                
            print("3. Encoding Categorical Data")                
            print("4. Feature Scaling of the Dataset")                
            print("5. Download the modified dataset")
            print()                
            print()
            print("What do you want to do?(Press -1 to exit) : ")                
            value = int(input())
            print(value)

            if value == 1:
                print("yash") 
                obj1 = Description(self.df)
                obj1.tasks()

            elif value==2:
                obj2 = Imputation(self.df)
                obj2.tasks()

            elif value==3:
                obj3 = Categorial(self.df)
                obj3.tasks()

            elif value==4:
                obj4 = Feature(self.df)
                obj4.tasks()    

            elif value==5:
                obj5 = Download(self.df)
                obj5.download()    

            elif value == -1:
                break    

def preprocessing():
    obj = Preprocessing()
    obj.remove_column()
    obj.tasks()
