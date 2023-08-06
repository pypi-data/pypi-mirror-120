'''
etl.py
'''

import os
import sys
import csv
from auto1.helper.helper import UtilityFunction


class Etl:
    '''
    Methods:
        - Load : loads the source file, and prepares the file as stage for transformation
        - Transform : performs the transformation on source file
    '''

    def __init__(self, dataFile):
        
        '''
        output_cols: list of required columns as a result
        '''
        
        self.__output_cols__ = ['engine-location','num-of-cylinders','engine-size','weight','horsepower','aspiration','price','make']
        
        self.dataFile = dataFile
        self.__dir__ = os.path.splitext(dataFile)[0]

        # stage dataframe
        self.__df__ = []

        # instance to utility  
        self.__util__ = UtilityFunction()


    def load(self, dataFile=None):
        '''
        loads the source data file and filters the records

        input : source file
        output: prepared dataFile for transformation 

        '''
        try:
            
            if dataFile is None:            
                raise FileExistsError

            with open(dataFile) as fp:
                rows = csv.DictReader(fp, delimiter=";")
                for row in rows:
                    _row = self.__util__.__clean_row__(input_row=row, output_cols=self.__output_cols__)
                    if _row:
                        self.__df__.append(_row)

            fname = dataFile.split('.')[0]
            self.dataFile = self.__util__.__map_to_nested_lists__(self.__df__, fname=f'{fname}.csv')

        except Exception as ex:
            raise ex


    def transform(self, dataFile=None):
        '''
        Takes the dataFile prepared by load method, and performs transformation

        input : dataFile
        output : transformed records in nested list format
        '''
        try:

            if dataFile is None:
                raise FileExistsError

            result =  []
            with open(dataFile, encoding='utf8') as fp:
                rows = csv.DictReader(fp, delimiter=",")
                
                for row in rows:
                    temp = {}

                    if row['engine-location'] is not None:
                        temp['engine-location'] = self.__util__.__map_engine_location__(record=row['engine-location'])

                    if row['num-of-cylinders'] is not None:
                        temp['num-of-cylinders'] = self.__util__.__map_num_of_cylinders__(record=row['num-of-cylinders'])

                    if row['engine-size'] is not None:
                        temp['engine-size'] = self.__util__.__map_engine_size__(record=row['engine-size'])

                    if row['weight'] is not None:
                        temp['weight'] = self.__util__.__map_weight__(record=row['weight'])

                    if row['horsepower'] is not None:
                        temp['horsepower'] = self.__util__.__map_horse_power__(record=row['horsepower'])

                    if row['aspiration'] is not None:
                        temp['aspiration'] = self.__util__.__map_aspiration__(record=row['aspiration'])

                    if row['price'] is not None:
                        temp['price'] = self.__util__.__map_price__(record=row['price'])

                    if row['make'] is not None:
                        temp['make'] = self.__util__.__map_make__(record=row['make'])
                    
                    result.append(temp)

            self.__util__.__remove_file__(dataFile=dataFile)    
            return self.__util__.__map_to_nested_lists__(result)

        except Exception as ex:
            raise ex

