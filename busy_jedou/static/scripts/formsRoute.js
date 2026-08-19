document.getElementById('FormRoute').addEventListener('submit', async function (f) {
    f.preventDefault(); // Stop page reload

    const formData = new FormData(this);

    // Send POST request
    const response = await fetch('/get/route', {
        method: 'POST',
        body: formData
    });

    // Display response on the page
    const data = await response.text();
    document.getElementById('outputRoute').innerHTML = `<strong>Result:</strong><br /> ${data}`;
});
