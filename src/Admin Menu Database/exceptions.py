
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


INPUT_TOO_LONG_EXCEPTION = Exception(100, 'Input too long')
INPUT_TOO_SHORT_EXCEPTION = Exception(101, 'Input too short')
INPUT_NOT_A_NUMBER_EXCEPTION = Exception(102, 'Input must be a number')
INPUT_NOT_A_STRING_EXCEPTION = Exception(103, 'Input must be text')
