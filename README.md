# Flask Banking App

A simple banking application built with Flask. This app allows users to register, log in, and manage their bank accounts, including viewing balances and transaction histories.

## Features

- User Registration and Authentication
- View Account Balance
- View Transaction History
- Transfer Money Between Accounts

## Requirements

- Python 3.x
- Flask
- SQLite (or any other database you prefer)
- Gunicorn (for deployment)
- Nginx (for deployment)

## Installation

1. **Clone the repository:**

    ```sh
    git clone https://github.com/vvksrma/Flask-Banking-App.git
    cd Flask-Banking-App
    ```

2. **Create a virtual environment and activate it:**

    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install the required packages:**

    ```sh
    pip install -r requirements.txt
    ```

4. **Set up the database:**

    ```sh
    flask db init
    flask db migrate -m "Initial migration."
    flask db upgrade
    ```

5. **Run the application:**

    ```sh
    flask run
    ```

## Deployment

### Using Gunicorn and Nginx

1. **Install Gunicorn:**

    ```sh
    pip install gunicorn
    ```

2. **Start Gunicorn:**

    ```sh
    gunicorn --bind 0.0.0.0:8000 wsgi:app
    ```

3. **Set up Nginx:**

    - Create an Nginx configuration file:

        ```sh
        sudo nano /etc/nginx/sites-available/flask_banking_app
        ```

    - Add the following configuration:

        ```nginx
        server {
            listen 80;
            server_name yourdomain.com;

            location / {
                proxy_pass http://127.0.0.1:8000;
                proxy_set_header Host $host;
                proxy_set_header X-Real-IP $remote_addr;
                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                proxy_set_header X-Forwarded-Proto $scheme;
            }

            location /static {
                alias /path/to/your/project/static;
            }
        }
        ```

    - Enable the configuration and restart Nginx:

        ```sh
        sudo ln -s /etc/nginx/sites-available/flask_banking_app /etc/nginx/sites-enabled
        sudo nginx -t
        sudo systemctl restart nginx
        ```

## Usage

- Visit `http://yourdomain.com` to access the application.
- Register a new user account.
- Log in with your credentials.
- Use the dashboard to view your account balance, transaction history, and perform transfers.

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add some feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Open a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any questions or suggestions, please open an issue or contact the repository owner at [your_email@example.com].
