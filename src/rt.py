import requests

# Configurações
RT_BASE_URL = "http://localhost:80/REST/2.0"  # Altere se necessário
RT_USERNAME = "root"
RT_PASSWORD = "password"

# Autenticação básica
session = requests.Session()
session.auth = (RT_USERNAME, RT_PASSWORD)
session.headers.update({"Content-Type": "application/json"})

def verificar_ou_criar_fila(nome: str, descricao: str = "", correspond_address: str = "", comment_address: str = "") -> int:
    """
    Verifica se uma fila existe no RT. Se não existir, cria a fila.
    Retorna o ID da fila.
    """
    # 1. Tenta obter a fila pelo nome
    url_get = f"{RT_BASE_URL}/queue/{nome}"
    response_get = session.get(url_get)

    if response_get.status_code == 200:
        queue_data = response_get.json()
        print(f"✅ Fila '{nome}' já existe. ID: {queue_data.get('id')}")
        return queue_data.get("id")

    elif response_get.status_code == 404:
        print(f"ℹ️ Fila '{nome}' não encontrada. Criando nova...")

        # 2. Cria a fila
        url_create = f"{RT_BASE_URL}/queue"
        payload = {
            "Name": nome,
            "Description": descricao,
            "CorrespondAddress": correspond_address,
            "CommentAddress": comment_address
        }

        response_create = session.post(url_create, json=payload)

        if response_create.status_code == 201:
            queue_id = response_create.json().get("id")
            print(f"✅ Fila '{nome}' criada com sucesso. ID: {queue_id}")
            return queue_id
        else:
            print(f"❌ Erro ao criar fila '{nome}'")
            print("Status:", response_create.status_code)
            print("Resposta:", response_create.text)
            return None

    else:
        print(f"❌ Erro ao verificar existência da fila '{nome}'")
        print("Status:", response_get.status_code)
        print("Resposta:", response_get.text)
        return None



def criar_ticket(subject: str, content: str, queue: str = "General") -> int:
    url = f"{RT_BASE_URL}/ticket"
    payload = {
        "Subject": subject,
        "Text": content,
        "Queue": queue,
        "Requestor": "usuario@example.com"  # pode ser um email real
    }

    response = session.post(url, json=payload)

    if response.status_code == 201:
        ticket_id = response.json().get("id")
        print("✅ Ticket criado com sucesso!")
        print("Ticket ID:", ticket_id)
        return ticket_id
    else:
        print("❌ Erro ao criar ticket")
        print("Status:", response.status_code)
        print("Resposta:", response.text)
        return None

def comentar_ticket(ticket_id: int, mensagem: str):
    url = f"{RT_BASE_URL}/ticket/{ticket_id}/comment"
    payload = {
        "Content": mensagem,
        "ContentType": "text/plain"
    }

    response = session.post(url, json=payload)

    if response.status_code != 500:
        print(f"✅ Comentário adicionado ao ticket #{ticket_id}")
    else:
        print(f"❌ Erro ao comentar no ticket #{ticket_id}")
        print("Status:", response.status_code)
        print("Resposta:", response.text)

def criar_fila(nome: str, descricao: str = "", correspond_address: str = "", comment_address: str = "") -> int:
    """
    Cria uma nova fila (queue) no Request Tracker.
    """
    url = f"{RT_BASE_URL}/queue"
    payload = {
        "Name": nome,
        "Description": descricao,
        "CorrespondAddress": correspond_address,
        "CommentAddress": comment_address
    }

    response = session.post(url, json=payload)

    if response.status_code == 201:
        queue_id = response.json().get("id")
        print(f"✅ Fila '{nome}' criada com sucesso! ID: {queue_id}")
        return queue_id
    else:
        print(f"❌ Erro ao criar fila '{nome}'")
        print("Status:", response.status_code)
        print("Resposta:", response.text)
        return None

# 🚀 Exemplo de uso
#ticket_id = criar_ticket(
#    subject="⚠️ Problema na integração Kafka + RT",
#    content="Detectamos falha na comunicação entre Kafka e Request Tracker ao processar eventos.",
#    queue="General"  # Verifique se essa fila existe no seu RT
#)

#if ticket_id:
#    comentar_ticket(
#        ticket_id=ticket_id,
#        mensagem="Mensagem adicional: o problema está sendo investigado pela equipe de infraestrutura."
#    )
