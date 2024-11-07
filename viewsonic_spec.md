## High-Throughput Task Processing System

Implement a high-throughput task processing system using asynchronous APIs to send and consume tasks from a message queue, ensuring scalability, performance and reliability.

### System Requirements

The content of the task is unrestricted, but it is required that each task be **persisted in the database**, and its `status` must be updated accordingly during processing.

Specify that each task is independent and should be processed in a `disorderly` manner, meaning there is no dependency or sequence between tasks.

1. **API for Sending Messages**:
    - Develop two APIs about message-sending using **FastAPI**.
        - First API will receive a message payload and enqueue it into a message queue (e.g., Redis, RabbitMQ, Kafka).
            - Create a new `task` in the database.
            - Set the `status` of the `task` to `pending`.
        - Second API will cancel this task.
            - If the task is canceled, its status should be set to `canceled`.
            - A task can only be canceled if its status is still `pending` or `processing`. Once the task has been marked as `completed`, cancellation is not allowed.
2. **Consumer for Processing Messages**:
    - Develop a message-consuming component that reads messages from the queue.
    - Upon receiving a task, the consumer should:
        - Update the task's `status` to `processing`.
        - Sleep for 3 seconds to simulate task processing.
        - After 3 seconds, update the corresponding task in the database to set its status to `completed`.
    - Ensure that any business logic necessary for message processing is executed asynchronously to maintain scalability.

### Testing Requirements

1. **Unit Testing**:
    - Write unit tests for both the message-sending and consuming logic.
    - Ensure proper handling of edge cases such as message queue failures, invalid message payloads, and database connection issues.

### Technical Specifications

- Use **FastAPI** for both the message-sending API and the consumer processing logic.
- Implement **async/await** functionality to ensure non-blocking operations.
- Deploy the system using **Docker** for easier environment setup.
- **Message Queue**:
    - Choose a message queue system such as **Redis**, **RabbitMQ**, and **Kafka** to handle message transmission.
    - Configure the queue to handle high throughput with minimal latency.

### **Bonus**:

- Add performance-enhancing features such as caching, batch processing, or optimized database queries.
- Implement logging and monitoring tools to observe system performance and message flow.
- Include performance testing.

### Submission Instructions

1. Push the source code to a GitHub or GitLab repository.
2. Include a simple **README** file that details:
    - Project architecture
    - How to run the application using Docker or Docker Compose
    - How to execute tests
    - Any assumptions or additional design decisions
3. Provide the source code for the system, including FastAPI implementation, message queue integration, and database setup.
