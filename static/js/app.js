document.addEventListener('DOMContentLoaded', () => {
    const connectButton = document.getElementById('connectButton');
    
    if (!window.ethereum) {
        alert('MetaMask is not installed! Please install MetaMask to use this application.');
        return;
    }

    connectButton.addEventListener('click', async () => {
        try {
            // Request account access if needed
            const accounts = await ethereum.request({ method: 'eth_requestAccounts' });
            const account = accounts[0];
            console.log('Connected account:', account);

            // Sign a message to authenticate
            const message = "Please sign this message to confirm your identity.";
            const signature = await ethereum.request({
                method: 'personal_sign',
                params: [message, account],
            });
            console.log('Signature:', signature);

            // Send the signature and address to the backend for verification
            fetch('/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ address: account, signature: signature, message: message })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    console.log('Authentication successful');
                    window.location.href = '/dashboard'; // Redirect to dashboard on success
                } else {
                    throw new Error('Authentication failed.');
                }
            })
            .catch(error => {
                console.error('Error during authentication:', error);
                alert('Authentication failed. Please try again.');
            });
        } catch (error) {
            console.error('Error connecting to MetaMask:', error);
            alert('Failed to connect to MetaMask. Please ensure it is installed and try again.');
        }
    });
});
