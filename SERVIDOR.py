import socket
import threading

# Armazena os dados dos clientes conectados
clientes = []

def handle_client(client_socket, addr):
    try:
        # Recebe o nome do cliente
        nome = client_socket.recv(1024).decode('utf-8')
        # Recebe a porta de escuta do cliente
        porta_escuta = int(client_socket.recv(1024).decode('utf-8'))
        # Armazena as informações do cliente na lista de clientes
        clientes.append((nome, addr[0], porta_escuta))
        print(f"{nome} se conectou do IP {addr[0]} e porta {addr[1]}, escutando na porta {porta_escuta}")
        
        while True:
            # Recebe uma mensagem do cliente
            mensagem = client_socket.recv(1024)
            if not mensagem:
                break
            mensagem = mensagem.decode('utf-8')
            if mensagem == "LIST":
                # Envia a lista de clientes conectados
                lista_clientes = "\n".join([f"{nome} - {ip}:{porta}" for nome, ip, porta in clientes])
                client_socket.send(lista_clientes.encode('utf-8'))
    finally:
        client_socket.close()
        # Remove o cliente da lista ao desconectar
        clientes.remove((nome, addr[0], porta_escuta))
        print(f"{nome} se desconectou")

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 9999))
    server.listen(5)
    print("Servidor ouvindo na porta 9999")
    
    while True:
        client_socket, addr = server.accept()
        client_handler = threading.Thread(target=handle_client, args=(client_socket, addr))
        client_handler.start()

if __name__ == "__main__":
    main()
