# CUSTOM EXCEPTION HANDLING


import os
import sys

# Func to define error more clearly
def error_message_detail(error, error_detail:sys): # error_detail:sys is the sys module of Python
    _, _, exc_tb = error_detail.exc_info() # Return Error type, Error value, traceback -> exc_tb show a "map" to the Error
    file_name = exc_tb.tb_frame.f_code.co_filename # Traceback to find the Error file
    line_number = exc_tb.tb_lineno # Traceback to find Error line
    
    error_message = "Error occurred python script name [{0}] line number [{1}] error message [{2}]".format(file_name, line_number, str(error))
    
    return error_message

class USvisaException(Exception): # Class USvisaException inheritance Class Exception
    # Constructor, "self" is to receive the "object" that python automatic add in a method 
    def __init__(self, error_message, error_detail): # "self" is like "this" in java 
        '''
        param erro_message: error message in string format
        '''
        super().__init__(error_message) # Pass error message to parent class by calling parent Constructor
        self.error_message = error_message_detail(error_message, error_detail=error_detail) # Call above func to define error message more clearly
        
    # Magic method "__"
    def __str__(self): # == public String toString() in java, when use print(obj) or str(obj) it call to this func. Without it print(obj) will print out hex text 
        return self.error_message 