import NewExceptions
import os
import User
import pickle

def register_user(username,password,client): #Register a user to registry
    username=username.lower()
    if not os.path.isfile('registry'):
        registry={}
        registry[username]=password
        fh=open('registry','wb')
        pickle.dump(registry,fh)
        fh.close()
        return User.User(username,client)
    fh=open('registry','rb') 
    registry=pickle.load(fh)
    fh.close() 
    if username in registry:
        raise NewExceptions.RegisterError("User already exists!")
    registry[username]=password
    os.mkdir(username)
    fh=open('registry','wb')
    pickle.dump(registry,fh)
    fh.close()
    return User.User(username,client)

def login_user(username,password,client): #Login a user if credentials match those in the registry. username is the username. password is the password. client is the socket object.
    username=username.lower()
    if not os.path.isfile('registry'):
        registry={}
        fh=open('registry','wb')
        pickle.dump(registry,fh)
        fh.close()
    fh=open('registry','rb') 
    registry=pickle.load(fh)   
    fh.close()
    if username not in registry:
        raise NewExceptions.LoginError("User not found!")
    if registry[username]!=password:
        raise NewExceptions.LoginError("Incorrect Password!")
    return User.User(username,client)
    
                           
def change_folder(usr,new_folder): #To change the folder of the current user. usr is User object. new_folder is name of the folder to be changed to.
    os.chdir(usr.cwd)
    if os.getcwd() == usr.root and new_folder=='..':
        raise NewExceptions.RootFolderError("Already in root folder!")
    if new_folder in os.listdir() or new_folder=='..':
        os.chdir(new_folder)
        usr.cwd=os.getcwd()
        return usr
    else:
        raise FileNotFoundError("Folder not found!")

def create_folder(usr,folder_name): #Create a folder if it does not already exist. usr if User object. folder_name is name of the folder to be created.
    os.chdir(usr.cwd)
    if folder_name in os.listdir():
        raise FileExistsError("Folder already exists!")
    os.mkdir(folder_name)
    return usr

def list_details(usr): #Lists all the folders and files in a directory. usr is a User object.
    os.chdir(usr.cwd)
    details=[]
    for i in os.listdir(os.getcwd()):
        info=os.stat(i)
        details.append([i,info.st_size,os.times.ctime(info.st_ctime)])
    return details
        

def read_file(user,fileopen,fh,command): 
    str=''
    os.chdir(user.cwd)
    if fileopen=='':
        if len(command) == 1:
            raise NewExceptions.NoFileNameError("File Name Not Entered!")
        else:
            fh=open(command[1])
            str=fh.read(100)
            fileopen=command[1]
    elif fileopen!='' and len(command)==1:
        fh.close()
        fileopen=''
    elif fileopen!='':
        if fileopen!=command[1]:
            fh.close()
            fh=open(command[1])
            fileopen=command[1]
        str=fh.read(100)
    return (fileopen,fh,str)



