from kafka import KafkaConsumer, KafkaProducer
import json
from rt import criar_ticket, comentar_ticket,verificar_ou_criar_fila


def simple_producer(message):
    producer = KafkaProducer(
        bootstrap_servers=['localhost:9092'],
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    
        
    producer.send('zap', message)
    print(f'Enviada mensagem {message}')
    
    producer.close()



def simple_consumer():
    
    verificar_ou_criar_fila(
        nome="edital",
        descricao="Fila de suporte edital",
        correspond_address="suporte@example.com",
        comment_address="comentarios-suporte@example.com"
    )


    
    
    consumer = KafkaConsumer(
        'meu-topico',
        bootstrap_servers=['localhost:9092'],
        group_id='meu-grupo-consumer-2',
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        auto_offset_reset='earliest'  # Lê desde o início
    )
    
    print("Aguardando mensagens... (Ctrl+C para sair)")
    
    try:
        for message in consumer:
            print(f"Recebido: {message.value}")
            value = message.value
            id = value["id"]
            message = value["message"]
            timestamp = value["timestamp"]
            ticket_id = criar_ticket(
                subject=f"⚠️ ID Mensagem {id}",
                content=f"{message} - {timestamp}",
                queue="edital"  # Verifique se essa fila existe no seu RT
            )
            if ticket_id: 
                comentar_ticket(
                    ticket_id=ticket_id,
                    mensagem="Mensagem adicional: o problema está sendo investigado pela equipe de infraestrutura."
            )
            simple_producer(f"Tiket aberto numero: {ticket_id}")
            # Aqui você processa sua mensagem
            # Exemplo: salvar no banco, enviar email, etc.
            
    except KeyboardInterrupt:
        print("Consumer interrompido")
    finally:
        consumer.close()


if __name__ == "__main__":
    simple_consumer()
    