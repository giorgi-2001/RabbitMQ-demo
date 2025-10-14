# RabbitMQ Demo

This mini project demonstrates how to utilize **RabbitMQ** as a message queuing system.

## Problem Overview
RabbitMQ is a classic messaging broker that enables **decoupling of software components**. A simplified architecture of decoupled services looks like this:
- **Producer → Messaging Broker (RabbitMQ) → Consumer**


The goal of this project is to illustrate how a producer can send messages to RabbitMQ and consumers can process them concurrently.

---

## Solution

### Producer
The producer is implemented as a **FastAPI REST API**. Its responsibilities include:

- Accepting a file and a `copies` parameter via API routes.  
- Publishing messages to RabbitMQ. The `copies` parameter determines how many messages are sent, which allows testing **concurrency** in the consumer.  

---

### Consumer
Two solutions were provided for the consumer:

1. **Celery**
   - Celery is a widely used Python library for **background task processing**.  
   - It provides built-in concurrency, worker management, and automatic handling of message acknowledgment.  
   - Integration with FastAPI is straightforward. Celery automatically manages communication with RabbitMQ and ensures reliable task execution.

2. **Plain Pika Consumer**
   - Implemented a plain Python consumer using the **Pika** library.  
   - Handled concurrency with **multiprocessing** to mimic Celery’s behavior.  
   - Required manually implementing message acknowledgment, prefetch limits, and task submission logic.  
   - The FastAPI producer had to directly interact with RabbitMQ using Pika.

---

## Conclusion

For most real-world use cases, **Celery** is the preferred choice for consumers:

- Easy to set up  
- Built-in concurrency and retries  
- Automatically manages RabbitMQ communication  

However, knowing **Pika** is valuable for situations requiring **direct, low-level control** over RabbitMQ, such as:

- Custom routing or exchanges  
- Manual acknowledgment strategies  
- Fine-tuned concurrency control  

Overall, this project demonstrates both **high-level (Celery)** and **low-level (Pika)** approaches to working with RabbitMQ, providing a solid foundation for building scalable producer-consumer systems in Python.
