import gc 

class Train:
    def __init__(self):
        print("Train is started")
    
    def check(self):
        print(f"Train is running")
        
    def __del__(self):
        print(f"Train is stopped")


def find_train():
    rajdhani = Train() # train created
    rajdhani.check()


find_train()
print("ByeBye")

# Train started 
# Train is running 
# Train is stopped
# ByeBye
