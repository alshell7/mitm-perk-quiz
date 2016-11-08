#    MIT Copyright (c) 2016 alshell7.
#    Permission is hereby granted, free of charge, to any person obtaining
#    a copy of this software and associated documentation files (the "Software"),
#    to deal in the Software without restriction, including without limitation
#    the rights to use, copy, modify, merge, publish, distribute, sublicense,
#    and/or sell copies of the Software, and to permit persons to whom the Software
#    is furnished to do so, subject to the following conditions:
#    The above copyright notice and this permission notice shall be included in
#    all copies or substantial portions of the Software.
#    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#    EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
#    OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#    IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
#    CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
#    TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE
#    OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import json        
import hashlib 
import warnings
import argparse
from winsound import *

def_auth_token = None
commandLine = argparse.ArgumentParser(prog='mitm-perk-quiz', description="Simple program to extract the Perk Pop Quiz Answers")
commandLine.add_argument('-jf','--jsonfile', nargs='?', help="The JSON file to process that contains the Quiz http response")
commandLine.add_argument('-at', '--authtoken', nargs ='?', help="Authentication token, to process the json data and find correct answers")
commandLine.add_argument('-v', '--version', action='version', version='%(prog)s 1.0')

def myMessage():    
    print("\n-----------------------Welcome to MITM#PerkQuiz-----------------------")
    print("-----------------------Developed by alshell7-----------------------\n")
    

#http://code.activestate.com/recipes/391367-deprecated/
def deprecated(func):
    """This is a decorator marking this function
    as deprecated. It will result in a warning being emmitted
    when this function is used."""
    def newFunc(*args, **kwargs):
        warnings.warn("Call to deprecated function %s." % func.__name__,
                      category=DeprecationWarning)
        return func(*args, **kwargs)
    newFunc.__name__ = func.__name__
    newFunc.__doc__ = func.__doc__
    newFunc.__dict__.update(func.__dict__)
    return newFunc

class HashUtil(object):
    def __init__(self):
        self.HEX_CHARS = "0123456789abcdef"    
    @deprecated
    def asHex(buf):
        chars = []        
        chars.count = len(bytes(buf)) * 2        
        for i in range(0, len(buf)):
            chars[i * 2] = HEX_CHARS[(buf[i] & 240) >> 4]
            chars[(i * 2) + 1] = HEX_CHARS[buf[i] & 15]; 
        return str(chars)
        
    def sha1Hash(toHash):
        try:
            messageDigest = hashlib.sha1()
            stringM = str(toHash)
            byteM = bytes(stringM, encoding='utf')
            messageDigest.update(byteM)
            return messageDigest.hexdigest()
        except TypeError:
            raise "String to be hashed was not compatible"    
    
def verifyRightAnswer(answer_id, correct_sha, authentication_token):
    """
    Actual function that checks whether the given option is the right answer or not.
    """
    h = HashUtil.sha1Hash
    right_answer_id = str(answer_id)
    auth_token = str(authentication_token)
    auth_correction = auth_token + right_answer_id
    result = h(auth_correction)
    #print(result)
    return (result == correct_sha)

def stripJsonToCurly(complete_response):
    """
    Removes the extra (like HTTP headers) data from the response, strips it to JSON string    
    """
    data = str(complete_response)
    start = data.find('{')
    end = data.find("}}}")
    json_len = end + 3
    if (json_len > 1):
        return data[start:json_len]

def processResponseFinal(json_response, auth_token):
    try:
        print("\n-----------------------STARTING TO DECODE-----------------------\n")
        short_data = []        
        parsed_json = json.loads(json_response)
        questions = parsed_json['data']['questions']    
        for question in questions:
            #print("ID : {0}, Question : {1}".format(question["id"], question["question_text"]))
            print(question["question_text"])            
            correct_sha = question["correct"]
            print("Options are:")
            options = question["answers"]        
            for option in options:            
                correct = verifyRightAnswer(option["id"], correct_sha, auth_token)
                optionEdited = "\t\t" + option["answer_text"]
                if correct:
                    short_data.append(optionEdited)
                    print(optionEdited + " ---CORRECT")
                #You can uncomment the below two lines in order to the display the options and mark the answer as correct too    
                #else:
                   # print(optionEdited)
        if len(short_data) > 0:
            print("\nPRINTING ANSWERS FROM LAST TO FIRST\n")
            lifoAnswers = short_data[::-1]
            del short_data                              
            for ans in lifoAnswers:
                print(ans)
                        
        else:
            print("\nCould not get the answers? Your auth_token is wrong probably.")                        
        print("\n-----------------------COMPLETED DECODING-----------------------\n")
            
    except:        
        raise TypeError("Improper JSON data provided")

def reProcessExternalFile(dataLocation, authenticationToken ):
    try:
        #print("File Location: " + dataLocation)
        #print("Authentication Token: " + authenticationToken)
        with open(dataLocation, mode='r') as extFile:            
            json_data = stripJsonToCurly(extFile.read())            
            processResponseFinal(json_data, authenticationToken)
    except FileNotFoundError as fileNot:
        print("Could not locate/process the specified JSON file!\n" + str(fileNot))                
        exit()        
    except TypeError as invalid:
        print(str(invalid))
        exit()    
    finally:        
        MessageBeep(MB_ICONASTERISK)

#Entry point for the program
if __name__ == '__main__':
    #MessageBeep(MB_ICONEXCLAMATION)

    commands = vars(commandLine.parse_args())            
    if commands.get("jsonfile") is not None:
        jsonFile = str(commands.get("jsonfile")).replace('\\\\', '\\')                
        if commands.get("authtoken") is not None:
            reProcessExternalFile(jsonFile, str(commands.get("authtoken")))
        else:
            if def_auth_token is None:
                print("Authentication Token (def_auth_token) was not feeded to the program")
            else:
                reProcessExternalFile(jsonFile, def_auth_token)
    else:
        myMessage()
        
        print("Optionally you can utilise the program by providing the JSON file and auth_token as arguments")
        commandLine.print_usage()
        print('\n')

        #Getting the authentication token of the user...
        authenticationToken = str(input("Specify the Authentication Token: "))
        if authenticationToken == "":
            MessageBeep(MB_ICONEXCLAMATION)
            print("Authentication Token cannot be Null!")
            exit()

        #Getting the location of file to decrypt where the GET RESPONSE of PerPopQuiz sent by the server is captured...
        dataLocation = str(input("Specify the Location of JSON file to process: "))
        if dataLocation == "":     
            MessageBeep(MB_ICONEXCLAMATION)       
            print("File to process has to be specified!")
            exit()                        
                        
        reProcessExternalFile(dataLocation, authenticationToken)  

        #If wish to re work on the same file with different data... 
        while True:
            choice = str(input("Do you wish to re-process the data?\n('y' for yes)"))
            if choice == 'y':
                reProcessExternalFile(dataLocation, authenticationToken)            
            else:
                break
        print("\n-----------------------Exiting MITM#Perk-----------------------\n")
        exit()


@deprecated
def processFile(location):
    import re, sys
    data = ""
    with open(location, mode='r') as f:
        for line in f:
            line = re.sub(r',\s+d:\s+.*?(?= })', r'', line)
            data.join(line)
    return data

@deprecated
def startFinalProcessInbackground():
    from threading import Thread
    myProcessThread = Thread(target = processResponseFinal, args = (def_json_data, def_auth_token))
    myProcessThread.daemon = True
    myProcessThread.start()

@deprecated
def test(dataLocation):
        print(processFile(dataLocation))
        response_content = file.read()
        temp = response_content
        grp = json_data[285:-1]
        complete = grp[0:len(grp)- 2]
        return complete