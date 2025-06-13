from kafka import KafkaProducer
import json
import time


duvidas = [
    {"pergunta": "Qual é a capital da Argentina?"},
    {"pergunta": "Qual é a capital do Japão?"},
    {"pergunta": "Qual é a capital do Brasil?"}
]


def simple_producer():
    producer = KafkaProducer(
        bootstrap_servers=['localhost:9092'],
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    count = 0
    # Envia 10 mensagens
    for duvida in duvidas:
        
        try:
            
            message = {
                'id': count,
                'message': duvida["pergunta"],
                'timestamp': time.time()
            }     
            print("💬 Duvida :"+duvida["pergunta"])
        except Exception as e:
            print(f"❌ Erro ao responder: {e}")
        
        producer.send('edital', message)
        print(f'Enviada mensagem {duvida}')
        time.sleep(1)
    
    producer.close()

if __name__ == "__main__":
    simple_producer()
    