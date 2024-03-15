## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/aS4meone/parser
    ```

2. Navigate to the project directory:

    ```bash
    cd parser
    ```

3. Configure your .env file:

4. Run docker-compose:

    ```bash
    docker compose up -d
    ```

5. Upgrade database
    ```bash
    docker exec -it parser-back-1 /bin/bash
    ```
   then do
   ```bash
    alembic upgrade heads
    ```
      ```bash
    exit
    ```
   
## Usage
After completing all the steps higher - go to 127.0.0.1:8000/docs and use the API