# Grimluk Backend

Questo repository contiene il **backend** dell’applicazione *Grimluk*, una piattaforma bancaria digitale progettata secondo un’architettura **a microservizi API-based ed event-driven**.
Il sistema è composto da più servizi indipendenti, containerizzati tramite Docker, che comunicano tra loro tramite **HTTP** e **Apache Kafka**.

---

## Architettura generale

Il backend è suddiviso nei seguenti microservizi:

- **BFF (Backend For Frontend)**  
- **User Service**
- **Account Service**
- **Transaction Service**

A supporto dell’architettura sono presenti:
- **PostgreSQL** come database relazionale
- **Apache Kafka** per la comunicazione asincrona
- **Zookeeper** per il coordinamento dei broker Kafka

---

## Tecnologie utilizzate

- **Linguaggio**: Python  
- **Runtime Docker**: `python:3.11-slim`
- **Framework API**: FastAPI
- **Validazione dati**: Pydantic
- **Database**: PostgreSQL
- **Message broker**: Apache Kafka
- **Containerizzazione**: Docker & Docker Compose
- **IDE consigliato**: Visual Studio Code

---

## Documentazione API

Ogni microservizio espone automaticamente la documentazione delle API tramite **Swagger (OpenAPI)**. La documentazione più curata è relativa al microservizio BFF.
Una volta avviato il sistema, la documentazione è accessibile all’indirizzo:
- http://**[host]**:**[port]**/docs

---

## Prerequisiti

Per eseguire il progetto in ambiente di sviluppo è necessario avere installato:

- **Docker Desktop** (o un’alternativa compatibile)
- **Docker Compose**
- **Git**

Non è richiesta, ma è comunque fortemente consigliata, l’installazione locale di Python, in quanto l’intero sistema è containerizzato.

---

## Avvio del progetto

1. Clonare il repository
2. Avviare l’intero stack applicativo tramite Docker Compose: **docker-compose up --build**
3. È possibile monitorare lo stato dei container e i log tramite Docker Desktop o tramite CLI.

---
## Porte esposte a runtime

| Servizio            | Porta |
| ------------------- | ----- |
| BFF                 | 8000  |
| User Service        | 8001  |
| Account Service     | 8002  |
| Transaction Service | 8003  |
| PostgreSQL          | 5432  |
| Kafka (internal)    | 29092 |
| Kafka (external)    | 9092  |
| Zookeeper           | 2181  |
