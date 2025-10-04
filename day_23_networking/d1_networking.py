import socket 
import platform

def explore_network_basics():
    print("========Networking========")
    
    hostname = socket.gethostname()
    # local_ip = socket.gethostbyname(hostname)

    print(f"Computer name: ",hostname)
    # print(f"Local IP:",local_ip)
    print(f"Operating System: ", platform.system())    
    
    # wait for exception to happen and catch
    try:
        # website info - https://www.flipkart.com/
        flipkart_ip = socket.gethostbyname("flipkart.com")
        print(f"Flipkart IP:",flipkart_ip)

        # website info - IRCTC
        irctc_ip = socket.gethostbyname("irctc.co.in")
        print(f"IRCTC IP:",irctc_ip)

        # website info - google
        google_ip = socket.gethostbyname("google.com")
        print(f"Google IP:",google_ip)
    except Exception as e:
        print(f"Error resolving domain: ",e)

explore_network_basics()

