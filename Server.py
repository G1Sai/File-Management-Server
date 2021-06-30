import socket
import os
from _thread import *
from User import User
import userfunctions
import NewExceptions

files_location=os.getcwd() #Location of registry defaulted to current working directory.
ServerSocket = socket.socket()
host = '127.0.0.1'
port = 8088


commands=['change_folder','list','read_file','write_file','create_folder','register','login','logout']

active_users=[] #A list of all the active users.

try:
    ServerSocket.bind((host, port))
except socket.error as e:
    print(str(e))

ServerSocket.listen(5)

def server(client):
    os.chdir(files_location)
    client.send(str.encode('Enter Command:'))
    fileopen=''
    user=User('Guest',client) #If no user is logged in, the current user is defaulted to Guest
    while True:
        try:
            data = client.recv(2048).decode('utf-8').strip()
            command=data.split()
            if not command[0] in commands:
                client.send(str.encode('Invalid Input'))
            else:
                if command[0]!=commands[2] and fileopen!='':
                    fileopen=''
                    fh.close()
                if user.username!='Guest':  #If the user is logged in

                    if command[0]==commands[6] or command[0]==commands[5]:
                        client.send(str.encode('Already logged in!'))

                    elif command[0]==commands[0]:
                        user=userfunctions.change_folder(user,command[1])
                        client.send(str.encode('Folder changed to '+user.cwd))

                    elif command[0]==commands[4]:
                        user=userfunctions.create_folder(user,command[1])
                        client.send(str.encode('Folder created!'))
                    
                    elif command[0]==commands[2]:
                        fileopen, fh, read_string=userfunctions.read_file(user,fileopen,fh,command)
                        client.send(str.encode(read_string))

                    elif command[0]==commands[3]:
                        os.chdir(user.cwd)
                        if len(command)>=3:
                            fw=open(command[1],'a')
                            final_string=data.replace(commands[3],'').strip().replace(command[1]+' ','')
                            fw.write(final_string)
                            fw.close()
                            client.send(str.encode("File successfully written!"))
                            
                        elif len(command)==2:
                            open(command[1],'w').close() #Emptying the file
                            client.send(str.encode("File successfully cleared!"))
                        else:
                            client.send(str.encode("Invalid Input!"))
                    elif command[0]==commands[1]:
                        details=userfunctions.list_details(user)
                        client.send(str.encode("{:<15} {:<20} {:<25}".format('Name','Size (in Bytes)','Date & Time of Creation')))
                        for k in range(len(details)-1):
                            client.send(str.encode("{:<15} {:<20} {:<25}\n".format(details[k][0],details[k][1],details[k][2])))
                    elif command[0]==commands[7]:
                        active_users.remove(user.username)
                        exit()
                        
                        
                    
                if user.username=='Guest':   #If the user is NOT logged in
                    if command[0]==commands[6]:
                        os.chdir(files_location) #Changing directory to the location of the registry
                        if command[1] not in active_users:
                            user=userfunctions.login_user(command[1],command[2],client)
                            active_users.append(user.username)
                            client.send(str.encode("Welcome "+user.username+'!'))
                        else:
                            client.send(str.encode("User already logged in!"))
                    
                    elif command[0]==commands[5]:
                        os.chdir(files_location) #Changing directory to the location of the registry
                        user=userfunctions.register_user(command[1],command[2],client)
                        active_users.append(user.username)
                        client.send(str.encode("Welcome "+user.username+'!'))
                    else:
                        client.send(str.encode('User not logged in'))
        except IndexError as e:
            client.send(str.encode("Invalid Input"))
        except NewExceptions.LoginError as le:
            client.send(str.encode(str(le)))
        except FileNotFoundError as fe:
            client.send(str.encode("Folder not found!"))
        except FileExistsError as fee:
            client.send(str.encode("Folder already exists!"))
        except NewExceptions.RootFolderError as rfe:
            client.send(str.encode(str(rfe)))
        except ConnectionResetError as cre:
            active_users.remove(user.username)
        except NewExceptions.NoFileNameError as nfe:
            client.send(str.encode(str(rfe)))
        if not data:
            continue
    client.close()

while True:
    Client, address = ServerSocket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    start_new_thread(server, (Client,)) #Starts a new thread for every client connected.
ServerSocket.close()
    