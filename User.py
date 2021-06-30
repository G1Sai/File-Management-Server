import os

class User:
    def __init__(self,username,client):
        self.username=username
        self.cwd=os.path.dirname(os.getcwd()+'\\'+username+'\\') #Current Working Directory of the user
        self.root=os.path.dirname(os.getcwd()+'\\'+username+'\\') #The root for the user. A user cannot traverse upwards beyond the root.
        self.client=client
        self.isLoggedIn=False