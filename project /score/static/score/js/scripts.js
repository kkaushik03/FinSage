document.addEventListener('DOMContentLoaded', async () => {
    const outputElement = document.getElementById('output');
    outputElement.innerText = 'Loading...'; // Initial loading text

    try {
        // Fetch data from the backend
        const response = await fetch('/api/hello/');
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.text(); // Expecting plain text response
        outputElement.innerText = data; // Replace "Loading..." with the fetched text
    } catch (error) {
        console.error('There was a problem with the fetch operation:', error);
        outputElement.innerText = 'Error loading data.';
    }
});