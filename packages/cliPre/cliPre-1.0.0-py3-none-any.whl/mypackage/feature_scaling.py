import pandas as pd 
import numpy as np
from sklearn.preprocessing import MinMaxScaler

from sklearn.preprocessing import StandardScaler

class Feature:
    def __init__(self,dataset):
        self.data = dataset

    def tasks(self):
        
        while True:
            print("Tasks of Feature Scaling: ")
            print("1. Perform Normalization (Min-Max Scaling)")                
            print("2. Perform Standardization (Standard Scaler)")                
            print("3. Show dataset")
            print()
            
            print("What do you want to do?(Press -1 to go back) :")                
            value = int(input())

            if value==1:
                self.normalization()

            elif value==2:
                self.standardization()

            elif value==3:
                self.showdata()

            elif value==-1:
                break    


    def normalization(self):
            while True:
                print("Tasks of Normalization: ")
                print("1. Normalization on one-column")                
                print("2. Normalization on full dataset")                
                print("3. Show dataset")
                print()

                print("Enter your choice (Press -1 to go back) : ")
                val = int(input())
                if val==1:
                    self.normOne()
                elif val==2:
                    self.normAll()
                elif val==3:
                    self.showdata()
                elif val==-1:
                    break;   

    def normOne(self):
        while True:
            print("List of all the columns with thier datatypes")
            print(self.data.dtypes)
            print()
            print("Enter the column name(Press -1 to go back) : ")
            val = input()
            if val=="-1":
                break
            else:
                if val  not in self.data.columns:
                    print("You entered wrong column name")
                    print()
                    continue     
                else:
                    scaler = MinMaxScaler()
                    self.data[[val]] = scaler.fit_transform(self.data[[val]])

                    print("Normalization of "+val+" is done.")


    def normAll(self):
        col_list = self.data.select_dtypes(exclude=['object']).columns
        scaler = MinMaxScaler()
        self.data[col_list] = scaler.fit_transform(self.data[col_list])
        print("Normalization of whole dataset is done.")


                

    def standardization(self):
            while True:
                print("Tasks of standardization: ")
                print("1. standardization on one-column")                
                print("2. standardization on full dataset")                
                print("3. Show dataset")
                print()

                print("Enter your choice (Press -1 to go back) : ")
                val = int(input())
                if val==1:
                    self.standOne()
                elif val==2:
                    self.standAll()
                elif val==3:
                    self.showdata()
                elif val==-1:
                    break;            

    def standOne(self):
        while True:
            print("List of all the columns with thier datatypes")
            print(self.data.dtypes)
            print()
            print("Enter the column name(Press -1 to go back) : ")
            val = input()
            if val=="-1":
                break
            else:
                if val  not in self.data.columns:
                    print("You entered wrong column name")
                    print()
                    continue     
                else:
                    scaler = StandardScaler()
                    self.data[[val]] = scaler.fit_transform(self.data[[val]])

                    print("Standardization of "+val+" is done.")


    def standAll(self):
        col_list = self.data.select_dtypes(exclude=['object']).columns
        scaler = StandardScaler()
        self.data[col_list] = scaler.fit_transform(self.data[col_list])
        print("Standardization of whole dataset is done.")




    def showdata(self):
        length = int(input("Enter the no of rows"))
        print(self.data.head(length))
                        

