# Transaction System | Backend
`v1.x.x`

### Description

This backend system is connected to a microservice.
The purpose of this whole system, is to :
- Create transactions
- Connect user's to websocket channel
- Microservice will process data
- Microservice will send state changes to backend using webhook
- The state update will be sent from backend to connected User
<br></br>

### Spinning up the server using Docker
1. The following command will start the django server.
    ```
    docker-compose up --build
    ```
2. It will also create a new network called `realtime-transaction-nextwork`, to which the microservice will connect (`network bridge` created so that this backend container can accept requests from other containers, locally).
<br></br>

### Creating Resources on the server
3. Run the [service-01](https://github.com/hardikambati/transaction-service01) microservice to process the transaction request.
4. Head over to [http://localhost:8000/swagger/](http://localhost:8000/swagger/).
5. `/auth/registration/` : Create a User
6. `/auth/login/` : Login
7. Listen to websocket channel here
    ```
    ws://localhost:8001/ws/transaction/?token=<authorization_token>
    ```
7. `/api/transaction/` : Create a transaction.
8. Status updates will be received on the connected websocket channel.


<br></br>
### Architecture that describes everything!

![Architecture](utils/docs/images/architecture.png)


### Read what's going on in the system in detail :

1. Once a transaction is created at the backend, a message is sent to a queue.
2. Parallely, the User who has created the transaction, will be connected to a websocket channel, to the backend.
3. The microservice will be listening to this queue.
4. Microservice picks one message at a time, validates it.
5. Then, it imitates a set of multiple processes (states), which might take variable amount of time.

    ```txt
    These are sample tags, that imitates a process
    (Could be a heavy computation task, or another microservice task)

    (task_name, time_in_sec)

    ('scheduled'   , 5)
    ('started'     , 2)
    ('verifying'   , 3)
    ('transacting' , 5)
    ('completed'   , 2)
    ('closed'      , 0)
    ('failed'      , 0)
    ```

6. After the control is passed through every single state, depending on the data, the microservice will send a `webhook` message to the backend.
7. This `webhook` message will have details regarding the current state.
8. The user, who is connected to the websocket through backend, will receive live updates, regarding current state or state changes.
9. Once all the processing is completed, the microservice sends the last process state, and the backend will close the websocket connection.
10. If any process fails, a failure message with error details will be sent to the websocket.



