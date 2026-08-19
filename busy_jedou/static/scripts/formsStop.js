document.getElementById('FormStop').addEventListener('submit', async function(e) {
            e.preventDefault(); // Stop page reload

        const formData = new FormData(this);

        // Send POST request
        const response = await fetch('/get/stop', {
            method: 'POST',
            body: formData
    });

        // Display response on the page
        const data = await response.text();
        document.getElementById('outputStop').innerHTML = `<strong>Result:</strong><br /> ${data}`;
});