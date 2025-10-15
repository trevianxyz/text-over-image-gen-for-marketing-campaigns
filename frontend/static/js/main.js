document.getElementById('campaignForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const form = e.target;
    const submitBtn = document.getElementById('submitBtn');
    const btnText = submitBtn.querySelector('.btn-text');
    const btnLoader = submitBtn.querySelector('.btn-loader');
    
    // Get form data
    const products = document.getElementById('products').value
        .split(',')
        .map(p => p.trim())
        .filter(p => p);
    
    const data = {
        products: products,
        region: document.getElementById('region').value,
        audience: document.getElementById('audience').value,
        message: document.getElementById('message').value
    };
    
    // Show loading state
    submitBtn.disabled = true;
    btnText.style.display = 'none';
    btnLoader.style.display = 'inline';
    document.getElementById('results').style.display = 'none';
    document.getElementById('error').style.display = 'none';
    
    try {
        const response = await fetch('/campaigns/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const result = await response.json();
        
        // Display results
        document.getElementById('campaignId').textContent = result.campaign_id;
        
        const complianceStatus = document.getElementById('complianceStatus');
        complianceStatus.textContent = result.compliance.status;
        complianceStatus.className = result.compliance.status.toLowerCase();
        
        // Load images
        document.getElementById('img11').src = `/${result.outputs['1:1']}`;
        document.getElementById('img169').src = `/${result.outputs['16:9']}`;
        document.getElementById('img916').src = `/${result.outputs['9:16']}`;
        
        // Show results
        form.style.display = 'none';
        document.getElementById('results').style.display = 'block';
        
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('errorMessage').textContent = 
            error.message || 'Failed to generate campaign. Please try again.';
        document.getElementById('error').style.display = 'block';
    } finally {
        submitBtn.disabled = false;
        btnText.style.display = 'inline';
        btnLoader.style.display = 'none';
    }
});

function hideError() {
    document.getElementById('error').style.display = 'none';
}

