# Simple Pass 🔐

A simple yet secure password manager built with Flask and Streamlit. This application allows you to securely store and manage your passwords with encryption.

## Features

- 🔒 Secure password storage with Fernet encryption
- 👥 User-friendly Streamlit interface
- 🔑 Master password protection
- ✨ Add, view, edit, and delete passwords
- 🔄 Automatic database creation
- 🌐 RESTful API backend

## Installation

1. Clone the repository:

bash
git clone https://github.com/Pratik-uzi/simple-pass.git
cd simple-pass

2. Create a virtual environment and activate it:

bash
python -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate

3. Install dependencies:

bash
pip install -e .


## Usage

1. Start the application:

bash
python start.py


This will:
- Start the Flask backend server on http://localhost:5000
- Launch the Streamlit frontend on http://localhost:8501
- Open your default web browser automatically

2. Default master password: `omfo1234`

## API Endpoints

- `GET /` - Check if API is running
- `POST /add` - Add new password
- `GET /view` - View all passwords
- `GET /view/<id>` - View specific password (requires master password)
- `PUT /update/<id>` - Update password (requires master password)
- `DELETE /delete/<id>` - Delete password (requires master password)

## Security Features

- Passwords are encrypted using Fernet (symmetric encryption)
- Master password required for sensitive operations
- Environment variables for secure key storage
- SQLite database with secure file permissions

## Development

To run only the backend server during development:

bash:simple-pass/README.md
python run.py


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request