import socket 
import threading 
import time 

def create_server():
    print("======== ABC Customer Service Server ========")

    # create server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # Server Config
    HOST = "localhost"
    PORT = 8888
    
    try:
        # bind socket to my config
        server_socket.bind((HOST, PORT))
        # can handle 2 connection
        server_socket.listen(2)
        
        print(f"Server is up and running at {HOST}:{PORT}")
        print(f"Waiting for customer connections...")
        
        while True:
            # accept client connection
            client_socket, client_address = server_socket.accept()
            print(f"Customer connected from {client_address}")
            
            # Handle in client in thread
            client_thread = threading.Thread(
                target=handle_customer, 
                args=(client_socket, client_address)
            )
            client_thread.start()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # clean resource
        server_socket.close()
    
def handle_customer(client_socket, address):
    try:
        # send welcome message
        welcome_msg = "Welcome to ABC Customer Service! How can I help you?\n"
        client_socket.send(welcome_msg.encode('utf-8'))
        
        while True:
            # Receive message from client
            data = client_socket.recv(1024).decode('utf-8')
            if(not data or data.lower()=='bye' or  data.lower()=='exit'):
                break
            print(f"Customer form {address}: {data}")
            
            if 'order' in data.lower():
                res = "I will check your order. Please wait.... \n"
            elif 'refund' in data.lower():
                res = "I will process refund immediately....\n"
            elif 'help' in data.lower():
                res = "Available services: Order status, refund, product info"
            else:
                res = f"Thank you for message: {data}. Our team will connect soon. \n"
            client_socket.send(res.encode('utf-8'))
    except Exception as e:
        print(f"Error handling customer {address}: {e}")
    finally:
        client_socket.close()
        print(f"customer {address} disconnected")


create_server()