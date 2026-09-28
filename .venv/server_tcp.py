import socket
import sys
import threading

# Criação e configuração do socket do servidor
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

try:
    server.bind(("127.0.0.1", 4422))
    server.listen(5)
    print("[SISTEMA] Servidor aguardando conexões na porta 4422...")

    client_socket, address = server.accept()
    print(f"[SISTEMA] Cliente conectado de: {address[0]}:{address[1]}")

except Exception as error:
    print(f"[ERRO] Falha ao iniciar o servidor: {error}")
    sys.exit()


# Função executada em thread para RECEBER mensagens do cliente
def recebe_mensagens():
    with open("output.txt", "a", encoding="utf-8") as file:
        while True:
            try:
                data = client_socket.recv(1024)

                # Se recv() retornar vazio, o cliente fechou a conexão
                if not data:
                    print("\n[SISTEMA] O cliente se desconectou.")
                    break

                message = data.decode("utf-8")
                print(f"\n[CLIENTE]: {message}")

                # Salva no log
                file.write(f"[CLIENTE]: {message}\n")
                file.flush()

                # Exibe o prompt para o servidor continuar digitando
                sys.stdout.write("Servidor: ")
                sys.stdout.flush()

            except Exception:
                break

    client_socket.close()


# Inicia a thread para escutar o cliente em segundo plano
receive_thread = threading.Thread(target=recebe_mensagens, daemon=True)
receive_thread.start()

# Exibe o prompt inicial do servidor
sys.stdout.write("Servidor: ")
sys.stdout.flush()

# Loop principal para ENVIAR mensagens do servidor ao cliente
while True:
    try:
        message_to_send = sys.stdin.readline().strip()

        if message_to_send.lower() == "sair":
            client_socket.send("Servidor encerrado.".encode("utf-8"))
            print("[SISTEMA] Encerrando servidor...")
            break

        if message_to_send:
            # Envia a mensagem para o cliente
            client_socket.send(message_to_send.encode("utf-8"))
            sys.stdout.write("Servidor: ")
            sys.stdout.flush()

    except (KeyboardInterrupt, BrokenPipeError):
        print("\n[SISTEMA] Encerrando o servidor...")
        break

client_socket.close()
server.close()