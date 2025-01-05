# Decentralized Web Authentication Using Blockchain

This project demonstrates a decentralized authentication system using the Ethereum blockchain and MetaMask for a web application built with Flask. It showcases how blockchain technology can be leveraged to enhance security and user experience by decentralizing user authentication.

## Features

- **Blockchain Authentication**: Utilizes Ethereum for secure and transparent user authentication.
- **MetaMask Integration**: Allows users to authenticate using their MetaMask wallet, ensuring security and ease of use.
- **Flask Web Application**: A simple yet powerful backend built with Flask to handle requests and serve the frontend.
- **Decentralized File Storage**: Allows users to upload and retrieve files using IPFS, providing decentralized storage solutions.
- **Machine Learning Integration for Security Vulnerability Detection**: Incorporates a Random Forest-based machine learning model to analyze and predict security vulnerabilities from event logs, enhancing the system's overall security posture.


## Prerequisites

Before you can run this project, you'll need the following installed:
- [Python 3](https://www.python.org/downloads/)
- [Node.js and npm](https://nodejs.org/en/download/) (for any potential frontend JavaScript libraries you might use)
- [MetaMask](https://metamask.io/) browser extension installed and configured
- IPFS node: Ensure you have an IPFS node running locally or connect to a remote node. You can install IPFS from [IPFS Installation Guide](https://docs.ipfs.io/install/).

### Setup
- Ensure `MetaMask` is connected to the appropriate Ethereum network.
- Configure your environment variables for connecting to Ethereum and IPFS if necessary.

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
   
   *Create a .env file in the root directory and update it with your specific variables:*
   ```bash
   SECRET_KEY=your_secret_key_here
   WEB3_PROVIDER=https://mainnet.infura.io/v3/your_infura_project_id
   ```
### Running the Application

   **Start IPFS Daemon:**
   ```bash
   ipfs init    #Once after installation
   ipfs daemon
   ```
   **Start the server:**
   ```bash
   python3 app.py
   ```
