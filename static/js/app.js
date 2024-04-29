document.addEventListener('DOMContentLoaded', function() {
    const connectButton = document.getElementById('connectButton');
    
    // Check if MetaMask is installed in the user's browser
    if (!window.ethereum) {
        alert('MetaMask is not installed! Please install MetaMask to use this application.');
        return; // Stop further execution if MetaMask is not installed
    }

    connectButton.addEventListener('click', async () => {
        try {
            // Request account access from MetaMask
            const accounts = await ethereum.request({ method: 'eth_requestAccounts' });
            const account = accounts[0];
            console.log('Connected account:', account);

            // Message that the user will sign to authenticate
            const message = "Please sign this message to confirm your identity.";
            const signature = await ethereum.request({
                method: 'personal_sign',
                params: [message, account],
            });
            console.log('Signature:', signature);

            // Send the user's address and signature to the backend for verification
            fetch('/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ address: account, signature: signature, message: message })
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok.');
                }
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    console.log('Authentication successful');
                    window.location.href = '/dashboard'; // Redirect to the dashboard upon successful authentication
                } else {
                    throw new Error('Authentication failed.'); // Throw an error if authentication fails
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
