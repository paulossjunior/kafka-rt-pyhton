# 📦 Request Tracker + Kafka Integration

Ambiente completo com:

* 🎫 [Request Tracker (RT)](https://requesttracker.com/)
* 🐘 PostgreSQL
* 🐳 Kafka + Zookeeper
* 👀 Kafka UI
* 🐍 Scripts Python de Producer e Consumer integrados com RT

---

## 🚀 Subir o ambiente

```bash
make up
```

Acesse:

* RT: [http://localhost](http://localhost)
* Kafka UI: [http://localhost:8080](http://localhost:8080)

---

## 🛑 Parar o ambiente

```bash
make down
```

---

## 🐍 Scripts Kafka

### Producer (envia mensagens)

```bash
make producer
```

### Consumer (ouve mensagens e cria tickets no RT)

```bash
make consumer
```

---

## 🧱 Estrutura dos Serviços

```yaml
services:
  db: PostgreSQL 13
  rt: Request Tracker 6
  rt-init: Inicializa usuários
  kafka: Kafka 7.4.0
  zookeeper: Necessário para Kafka
  kafka-ui: Interface web para monitorar tópicos
```

---

## 🧰 Makefile

Comandos disponíveis:

```bash
make install      # Instala dependências Python
make up           # Sobe todos os serviços
make down         # Para os serviços
make producer     # Executa producer Kafka
make consumer     # Executa consumer Kafka
```

---

## 📬 Integração RT + Kafka

O *consumer* recebe mensagens Kafka no tópico `meu-topico` e cria tickets no RT automaticamente:

```python
ticket_id = criar_ticket(
    subject=f"⚠️ ID Mensagem {id}",
    content=f"{message} - {timestamp}",
    queue="General"
)

verificar_ou_criar_fila(
        nome="edital",
        descricao="Fila de suporte edital",
        correspond_address="suporte@example.com",
        comment_address="comentarios-suporte@example.com"
)




```




## 📬 Variáveis de Ambiente

```
GEMINI_API_KEY= <KEY>
MODEL=<Model>
```
---

## 📂 Requisitos

* Docker + Docker Compose
* Python 3.10+
* Kafka Python: `pip install kafka-python`

---

## ✅ Inicialização de Usuários no RT

Adicione seu script em `create-users.sh` para configurar usuários no primeiro start.

---

## 📁 Volumes

* `pgdata`, `rt-data`: dados persistentes do RT e PostgreSQL
* `kafka-data`, `zookeeper-data`, `zookeeper-logs`: dados Kafka
