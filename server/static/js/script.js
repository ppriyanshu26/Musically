document.getElementById('uploadForm').addEventListener('submit', async function(event) {
    event.preventDefault();
    const fileInput = document.querySelector('input[type="file"]');
    const file = fileInput.files[0];
    
    // Check if file size is more than 5MB
    if (file.size > 5 * 1024 * 1024) {
        alert('File size exceeds 5MB limit.');
        return; // Prevent further execution
    }
    
    const formData = new FormData(this);
    const response = await fetch('/file', {
        method: 'POST',
        body: formData
    });
    const result = await response.json();
    if (response.ok) {
        alert(result.message);
        window.location.href = 'http://127.0.0.1:3000'; // Redirect to specified URL
    } else {
        alert('Upload failed: ' + result.message);
    }
});