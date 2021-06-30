# File-Management-Server
A simplified client-server solution for file management

This is a simple file manager. The server is capable of basic file operations including reading, creating and modifying files. It can also create folders and tranverse the directories.

Almost all of the operations take place in the server. Clients connect to the server to use it. The server is capable of handling multiple clients simultaneously. 

A user is required to login to use the server. New users can be registered. Each user has their own directory, which could consist of files and folders.

The server supports a subset of commands commonly found on UNIX-based systems. These commands are heavily simplified compared to their UNIX counterparts and are the services of the server.



The commands are as follow:

change_folder {name} :
Changes the current working directory. '..' in place of {name} to walk back to the previous folder.

list  :
Lists all the folders and files in the current directory.

read_file {name}  :
Reads first 100 characters from {name}. Subsequent calls return next 100 characters.

write_file {name} {input}  :
 Appends {input} to {name} file. Empty {input} clears the file of content.

create_folder {name}  :
Creates a folder with name <name>

register {username} {password} :
Registers a user {username} with password <password>

login {username} {password}  :
Logs the user {username} if {password} is correct.

logout : Logs the user out.
