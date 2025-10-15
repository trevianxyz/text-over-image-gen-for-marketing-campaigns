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
        
        // Display campaign info
        document.getElementById('campaignId').textContent = result.campaign_id;
        
        const complianceStatus = document.getElementById('complianceStatus');
        complianceStatus.textContent = result.compliance.status;
        complianceStatus.className = result.compliance.status.toLowerCase();
        
        // Display campaign details
        document.getElementById('productCount').textContent = data.products.length;
        document.getElementById('campaignRegion').textContent = data.region;
        document.getElementById('campaignMessage').textContent = data.message;
        
        // Create product containers dynamically
        const productsContainer = document.getElementById('productsContainer');
        productsContainer.innerHTML = '';
        
        // For now, show the first product's images (API returns first product's outputs)
        // In a full implementation, you'd want to modify the API to return all products
        const productName = data.products[0] || 'Product';
        
        const productDiv = document.createElement('div');
        productDiv.className = 'product-section';
        productDiv.innerHTML = `
            <h4>${productName}</h4>
            <div class="image-grid">
                <div class="image-card">
                    <h5>Square (1:1)</h5>
                    <img src="/${result.outputs['1:1']}" alt="Square format" loading="lazy">
                    <p class="image-size">1024 x 1024</p>
                </div>
                <div class="image-card">
                    <h5>Landscape (16:9)</h5>
                    <img src="/${result.outputs['16:9']}" alt="Landscape format" loading="lazy">
                    <p class="image-size">1024 x 576</p>
                </div>
                <div class="image-card">
                    <h5>Portrait (9:16)</h5>
                    <img src="/${result.outputs['9:16']}" alt="Portrait format" loading="lazy">
                    <p class="image-size">576 x 1024</p>
                </div>
            </div>
        `;
        
        productsContainer.appendChild(productDiv);
        
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

