##################################################################
#                                                                #
#    Exception class for holding information about exceptions    #
#    --------------------------------------------------------    #
#                                                                #
#    To import use:                                              #
#        from exceptions import *                                #
#                                                                #
#        Alternatively use:                                      #
#            from exceptions import INPUT_TOO_LONG_EXCEPTION     #
#        to use only that specific exception                     #
#                                                                #
#    To add more exceptions add lines below the constants        #
#    defined below                                               #
#                                                                #
#    Exception codes defined as:                                 #
#        1xx - Database exception                                #
#                                                                #
##################################################################

class Exception:
    def __init__(self, code, message):
        self.code = code
        self.message = message

    def get_code(self):
        return self.code

    def get_message(self):
        return self.message


INPUT_TOO_LONG_EXCEPTION = Exception(100, 'Input too long')
INPUT_TOO_SHORT_EXCEPTION = Exception(101, 'Input too short')
INPUT_NOT_A_NUMBER_EXCEPTION = Exception(102, 'Input must be a number')
INPUT_NOT_A_STRING_EXCEPTION = Exception(103, 'Input must be text')
DUPLICATE_VALUE_EXCEPTION = Exception(104, 'Duplicate unique value in database')
NO_UPDATE_EXCEPTION = Exception(105, 'No values were updated')
EMPTY_INPUT_EXCEPTION = Exception(106, 'Empty input value')
INVALID_DECIMAL_VALUE = Exception(107, 'Invalid decimal value')
INVALID_TYPE_EXCEPTION = Exception(107, 'Invalid data type')
UNKKNOWN_REFERENCE_EXCEPTION = Exception(108, 'Trying to refer to a value that do not exists')