
import os
import sys
import csv


class Mapper:
    
    '''
    Mapper class for ETL
    static methods to map the keys and cast the values
    '''

    def __init__(self):
        
        self.__ENGINE_LOCATION__ = {
            'rear': 0,
            'front': 1
        }


        self.__NUMBER_TO_WORD__ = {
            'one': 1,
            'two': 2,
            'three': 3,
            'four': 4,
            'five': 5,
            'six': 6,
            'seven': 7,
            'eight': 8,
            'nine': 9
        }


        self.__ASPIRATION__ = {
            'std': 0,
            'turbo': 1
        }


    def __map_engine_location__(self, record):
        return int(self.__ENGINE_LOCATION__[record])
    

    def __map_num_of_cylinders__(self, record):
        return int(self.__NUMBER_TO_WORD__[record])


    def __map_engine_size__(self, record):
        return int(record)


    def __map_weight__(self, record):
        return int(record)


    def __map_horse_power__(self, record):
        return float(record.replace(',','.'))


    def __map_aspiration__(self, record):
        return int(self.__ASPIRATION__[record])


    def __map_price__(self, record):
        cents_in_euro = 0.01
        return int(record)*cents_in_euro


    def __map_make__(self, record):
        return str(record)


    def __map_to_nested_lists__(self, rows, fname=None):
        '''
        '''
        try:
            matrix_rows = []
            headers = list(rows[0].keys())
            matrix_rows.append(headers)
            
            for row in rows:
                matrix_rows.append(list(row.values()))
            
            if fname:

                with open(fname,'w', encoding='utf8', newline='') as fp:
                    writer = csv.writer(fp)
                    writer.writerows(matrix_rows)
                
                return fname


            return matrix_rows

        except Exception as ex:
            raise ex


class UtilityFunction(Mapper):

    '''
    UtilityFunction class holds the helper functions
    '''

    def __init__(self):
        super().__init__()


    def __clean_row__ (self, input_row, output_cols):
        '''

        '''
        try:
            
            filtered_rows = {}
            for _col in output_cols:
                
                if input_row[_col].strip() != '-':
                    filtered_rows[_col] = input_row[_col].strip()
                else:
                    return None
            
            return filtered_rows

        except Exception as ex:
            raise ex
    

    def __remove_file__(self, dataFile):
        '''
        input : removes the dataFile
        '''
        try:
            os.remove(dataFile)
        except Exception as ex:
            raise ex