# Decentralized Web Authentication Using Blockchain

This project demonstrates a decentralized authentication system using the Ethereum blockchain and MetaMask for a web application built with Flask. It showcases how blockchain technology can be leveraged to enhance security and user experience by decentralizing user authentication.

## Features

- **Blockchain Authentication**: Utilizes Ethereum for secure and transparent user authentication.
- **MetaMask Integration**: Allows users to authenticate using their MetaMask wallet, ensuring security and ease of use.
- **Flask Web Application**: A simple yet powerful backend built with Flask to handle requests and serve the frontend.
- **Smart Contract Interaction**: Implements smart contracts for managing authentication logic.

## Prerequisites

Before you can run this project, you'll need the following installed:
- [Python 3](https://www.python.org/downloads/)
- [Node.js and npm](https://nodejs.org/en/download/) (for any potential frontend JavaScript libraries you might use)
- [MetaMask](https://metamask.io/) browser extension installed and configured

## Installation

Follow these steps to get your development environment set up:

1. **Clone the repository**
   ```bash
   git clone https://github.com/atulvinod01/DecentralizedWebAuthentication.git
   cd DecentralizedWebAuthentication
   ```
2. **Virtual Environment(optional)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. **Install required packages**
   ```bash
   pip install -r requirements.txt
   ```
4. **Configure your environment variables**
   Create a .env file in the root directory and update it with your specific variables:
   ```bash
   SECRET_KEY=your_secret_key_here
   WEB3_PROVIDER=https://mainnet.infura.io/v3/your_infura_project_id
   ```
