import socket 
import threading 
import time 

def create_client():
    print("======== ABC Customer Service Client ========")

    # create server socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # connet to server - localhost:8888
        client_socket.connect(('localhost',8888))
        
        # Receive welcome message from server
        welcome = client_socket.recv(1024).decode('utf-8')
        print(f"Server says: {welcome}")
        
        # Simulate customer message
        messages = [
            "Hi, I need help in order status",
            "I want to get refund soon",
            "Can you help me with product info",
            "Hi, I need help in order status",
            "I want to get refund soon",
            "Can you help me with product info",
            "exit"
        ]
        
        for message in messages:
            print(f"From client: {message}")
            client_socket.send(message.encode('utf-8'))
            
            if message.lower()=="exit":
                break
            
            res = client_socket.recv(1024).decode('utf-8')
            print(f"From server: {res}")
            time.sleep(4)
            
    except Exception as e:
        print(f"Client error: {e}")
    finally:
        client_socket.close()

create_client()