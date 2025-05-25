import socket
import json
import base64
import logging
import os

server_address = ('172.16.16.101', 9999)

def send_command(command_str=""):
    global server_address
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_address)
    logging.warning(f"connecting to {server_address}")
    try:
        logging.warning(f"sending message ")
        sock.sendall(command_str.encode())
        data_received = ""
        while True:
            data = sock.recv(16)
            if data:
                data_received += data.decode()
                if "\r\n\r\n" in data_received:
                    break
            else:
                break
        hasil = json.loads(data_received)
        logging.warning("data received from server:")
        return hasil
    except Exception as e:
        logging.warning(f"error during data receiving: {str(e)}")
        return False
    finally:
        sock.close()

def remote_list():
    command_str = "LIST"
    hasil = send_command(command_str)
    if (hasil['status']=='OK'):
        print("daftar file : ")
        for nmfile in hasil['data']:
            print(f"- {nmfile}")
        return True
    else:
        print("Gagal")
        return False

def remote_get(filename=""):
    command_str = f"GET {filename}"
    hasil = send_command(command_str)
    if (hasil['status']=='OK'):
        namafile = hasil['data_namafile']
        isifile = base64.b64decode(hasil['data_file'])
        with open(namafile, 'wb+') as fp:
            fp.write(isifile)
        print(f"File {namafile} downloaded successfully")
        return True
    else:
        print("Gagal:", hasil['data'])
        return False

def remote_put(filename=""):
    if not os.path.exists(filename):
        print("File not found locally")
        return False
    
    with open(filename, 'rb') as f:
        file_content = base64.b64encode(f.read()).decode()
    
    command_str = f"PUT {filename} {file_content}"
    hasil = send_command(command_str)
    if (hasil['status']=='OK'):
        print(hasil['data'])
        return True
    else:
        print("Gagal:", hasil['data'])
        return False

def remote_delete(filename=""):
    command_str = f"DELETE {filename}"
    hasil = send_command(command_str)
    if (hasil['status']=='OK'):
        print(hasil['data'])
        return True
    else:
        print("Gagal:", hasil['data'])
        return False

def show_menu():
    print("\nAvailable commands:")
    print("1. LIST - List files on server")
    print("2. GET <filename> - Download file")
    print("3. PUT <filename> - Upload file")
    print("4. DELETE <filename> - Delete file")
    print("5. EXIT - Exit program")

if __name__=='__main__':
    logging.basicConfig(level=logging.INFO)
    while True:
        show_menu()
        command = input("Enter command: ").strip().split()
        
        if not command:
            continue
            
        cmd = command[0].upper()
        
        if cmd == "EXIT":
            break
        elif cmd == "LIST":
            remote_list()
        elif cmd == "GET" and len(command) == 2:
            remote_get(command[1])
        elif cmd == "PUT" and len(command) == 2:
            remote_put(command[1])
        elif cmd == "DELETE" and len(command) == 2:
            remote_delete(command[1])
        else:
            print("Invalid command")