import json 
import os

class Storage :
    @staticmethod
    def load_data(filename):
        try:
            with open(filename , 'r')as file:
                data = json.load(file)
            if not isinstance(data, list):
                print(f"Invalid data format in '{filename}'. Expected a list.")
                return None
                
            return data 
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            print("Sorry Json File is currupted")
            return None


    @staticmethod
    def save_data(filename,data):
        if not isinstance(data,list):
            print("Invalid data format. Expected a list.")
            return False

        temp_file = filename + '.tmp'

        try:
            with open(temp_file, 'w') as file:
                json.dump(data,file,indent=4)
            os.replace(temp_file,filename)
            return True
        except (OSError,TypeError,ValueError)as e:
            print(f"Error saving data: {e}")
            return False
    
       