import socket
import sys
import threading

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client.connect(("127.0.0.1", 4422))
    client.send(b"Conexao aberta, pode enviar dados.")
    print("[SISTEMA] Conectado ao servidor.")
except Exception as e:
    print(f"[ERRO] Não foi possível conectar ao servidor: {e}")
    sys.exit()


def recebe_mensagens():
    while True:
        try:
            data = client.recv(1024)
            # Se recv() retornar 0 bytes, a conexão foi encerrada pelo servidor
            if not data:
                print("\n[SISTEMA] Conexão encerrada pelo servidor.")
                client.close()
                sys.exit()

            message = data.decode("utf-8")
            print(f"\n[RECEBIDO] {message}")
            sys.stdout.write("Você: ")
            sys.stdout.flush()
        except Exception:
            break


# Thread como daemon para não travar o encerramento do script
receive_thread = threading.Thread(target=recebe_mensagens, daemon=True)
receive_thread.start()

# Exibe o primeiro prompt na tela
sys.stdout.write("Você: ")
sys.stdout.flush()

while True:
    try:
        message_to_send = sys.stdin.readline().strip()

        if message_to_send.lower() == "sair":
            client.send("Cliente desconectado.".encode("utf-8"))
            client.close()
            print("[SISTEMA] Você foi desconectado.")
            break

        if message_to_send:
            client.send(message_to_send.encode("utf-8"))
            sys.stdout.write("Você: ")
            sys.stdout.flush()

    except (KeyboardInterrupt, BrokenPipeError, Exception) as e:
        print(f"\n[SISTEMA] Encerrando o cliente... {e}")
        client.close()
        break