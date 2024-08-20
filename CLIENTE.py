import socket
import threading

# Função para ouvir conexões de entrada e receber mensagens diretas
def listen_for_messages(port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", port))
    server.listen(5)
    print(f"Cliente ouvindo para mensagens diretas na porta {port}")

    while True:
        client_socket, addr = server.accept()
        mensagem = client_socket.recv(1024).decode('utf-8')
        print(f"Mensagem recebida de {addr[0]}:{addr[1]}: {mensagem}")
        client_socket.close()

# Função para enviar mensagem direta
def enviar_mensagem_direta(ip, porta, mensagem):
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((ip, porta))
        client.send(mensagem.encode('utf-8'))
        client.close()
    except Exception as e:
        print(f"Erro ao enviar mensagem: {e}")

def main():
    # Trocar Host IP para Ip do servidor 
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("127.0.0.1", 9999))

    nome = input("Digite seu nome: ")
    client.send(nome.encode('utf-8'))

    # Escolhe uma porta disponível automaticamente
    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_socket.bind(("0.0.0.0", 0))
    listen_port = listen_socket.getsockname()[1]
    listen_socket.close()

    # Envia a porta de escuta ao servidor
    client.send(str(listen_port).encode('utf-8'))

    # Inicia a thread para ouvir mensagens diretas
    threading.Thread(target=listen_for_messages, args=(listen_port,), daemon=True).start()

    while True:
        comando = input("Digite 'LIST' para obter a lista de clientes conectados, 'MSG' para enviar mensagem direta ou 'EXIT' para sair: ")
        if comando == "LIST":
            client.send(comando.encode('utf-8'))
            lista_clientes = client.recv(4096).decode('utf-8')
            print("Clientes conectados:\n", lista_clientes)
            
            # Atualiza a lista de clientes
            clientes = []
            for linha in lista_clientes.split("\n"):
                if linha.strip():
                    nome_cliente, endereco = linha.split(" - ")
                    ip, porta = endereco.split(":")
                    clientes.append((nome_cliente, (ip, int(porta))))
                    
        elif comando.startswith("MSG"):
            partes = comando.split(" ", 2)
            if len(partes) < 3:
                print("Formato inválido. Use 'MSG <nome_cliente> <mensagem>'.")
                continue
            cliente_destino, mensagem = partes[1], partes[2]
            if cliente_destino == "ALL":
                # Envia a mensagem para todos os clientes
                for nome_cliente, (ip, porta) in clientes:
                    if nome_cliente != nome:  # Não envia para o próprio cliente
                        enviar_mensagem_direta(ip, porta, f"Mensagem de {nome}: {mensagem}")
            else:
                # Envia a mensagem para um cliente específico
                for nome_cliente, (ip, porta) in clientes:
                    if nome_cliente == cliente_destino:
                        enviar_mensagem_direta(ip, porta, f"Mensagem de {nome}: {mensagem}")
                        break
                else:
                    print("Cliente não encontrado.")
        elif comando == "EXIT":
            break

    client.close()

if __name__ == "__main__":
    main()
