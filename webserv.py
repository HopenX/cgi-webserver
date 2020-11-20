import sys
import socket
import os
import configparser

base_dir = os.getcwd()


def response(path, conn, staticfiles):
    if path == '/':
        path = '/index.html'
        type = 'index'
    else:
        try:
            type = path.split('.')[1]
        except:
            head = "HTTP/1.1 404 File not found\r\nContent-Type:text/html\r\n\r\n"
            conn.sendall(head.encode())
            return

    try:
        if type == 'py':
            head = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n"
            file_path = base_dir + path
            content = os.popen('python ' + file_path).read()
            conn.sendall((head + content).encode('utf-8'))
        elif type == 'html':
            head = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n"
            file_path = staticfiles + path
            content = ''
            with open(file_path) as f:
                for line in f:
                    content += line
            conn.sendall((head + content).encode('utf-8'))
        elif type == 'index':
            head = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n"
            file_path = staticfiles + path
            content = ''
            with open(file_path) as f:
                for line in f:
                    content += line
            conn.sendall((head + content).encode('utf-8'))
        elif type == 'js':
            head = "HTTP/1.1 200 OK\r\nContent-Type: application/x-javascript\r\n\r\n"
            file_path = staticfiles + path
            content = ''
            with open(file_path) as f:
                for line in f:
                    content += line
            conn.sendall((head + content).encode('utf-8'))
        elif type == 'ico':
            pass
    except FileNotFoundError:
        head = "HTTP/1.1 404 File not found\r\nContent-Type:text/html\r\n\r\n"
        conn.sendall(head.encode())


def handle_request(request, conn, staticfiles):
    first_line = request.splitlines()[0]  # Get the first line of the HTTP request packet
    first_line = first_line.rstrip('\r\n')
    # print('first_line:', first_line)
    # Save the method, path, version of the request
    req_method, req_path, req_version = first_line.split()
    # Respond to the request path
    response(req_path, conn, staticfiles)


def main():
    HOST = '127.0.0.1'
    conf_dic = dict()
    try:
        with open(sys.argv[1]) as f:
            for line in f:
                conf_dic[line.split('=')[0]] = line.split('=')[1]

    except FileNotFoundError:
        print('Unable To Load Configuration File')
        return
    except IndexError:
        print('Missing Configuration Argument')
        return

    try:
        PORT = int(conf_dic['port'])
        staticfiles = conf_dic["staticfiles"]
        cgibin = conf_dic["cgibin"]
        exec = conf_dic["exec"]
    except:
        print('Missing Field From Configuration File')
        return

    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    my_socket.bind((HOST, PORT))
    my_socket.listen(1)

    while True:
        # print('listenning at %s..' % PORT)
        conn, addr = my_socket.accept()
        request = conn.recv(1024).decode()
        if not request:  # If the request is null, continues to listen
            continue
            conn.close()
        handle_request(request, conn, staticfiles)  # Handle the request
        conn.close()  # Close the connection


if __name__ == '__main__':
    main()
