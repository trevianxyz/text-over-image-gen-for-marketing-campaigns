// Country selector functionality
let countriesData = null;
let selectedCountry = null;

// Audience selector functionality
let audiencesData = null;

// Product tags functionality
let productsList = [];

// Load countries data on page load
document.addEventListener('DOMContentLoaded', async () => {
    try {
        console.log('Loading countries from /api/countries...');
        const response = await fetch('/api/countries');
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        countriesData = await response.json();
        console.log('Countries loaded successfully:', countriesData);
        console.log(`Loaded ${countriesData.countries.length} countries`);
        
        // Show a brief success message
        const searchInput = document.getElementById('regionSearch');
        if (searchInput) {
            searchInput.placeholder = `Search ${countriesData.countries.length} countries...`;
        }
    } catch (error) {
        console.error('Failed to load countries:', error);
        
        // Show user-friendly error message
        const searchInput = document.getElementById('regionSearch');
        if (searchInput) {
            searchInput.placeholder = 'Error loading countries - please refresh the page';
            searchInput.disabled = true;
        }
        
        // Show error in the dropdown
        const dropdown = document.getElementById('regionDropdown');
        if (dropdown) {
            dropdown.innerHTML = '<div class="no-results">Failed to load countries. Please refresh the page.</div>';
            dropdown.style.display = 'block';
        }
        
        // Fallback: Load a minimal set of countries for basic functionality
        console.log('Loading fallback countries...');
        countriesData = {
            countries: [
                { code: 'US', name: 'United States', primary_language: 'English', region: 'North America' },
                { code: 'CA', name: 'Canada', primary_language: 'English', region: 'North America' },
                { code: 'MX', name: 'Mexico', primary_language: 'Spanish', region: 'North America' },
                { code: 'GB', name: 'United Kingdom', primary_language: 'English', region: 'Europe' },
                { code: 'DE', name: 'Germany', primary_language: 'German', region: 'Europe' },
                { code: 'FR', name: 'France', primary_language: 'French', region: 'Europe' },
                { code: 'JP', name: 'Japan', primary_language: 'Japanese', region: 'Asia Pacific' },
                { code: 'AU', name: 'Australia', primary_language: 'English', region: 'Asia Pacific' }
            ]
        };
        console.log('Fallback countries loaded:', countriesData);
    }
    
    // Load audiences data
    try {
        console.log('Loading audiences from /api/audiences...');
        const response = await fetch('/api/audiences');
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        audiencesData = await response.json();
        console.log('Audiences loaded successfully:', audiencesData);
        console.log(`Loaded ${audiencesData.total_count} audiences`);
        
    } catch (error) {
        console.error('Failed to load audiences:', error);
        
        // Fallback: Load a minimal set of audiences for basic functionality
        console.log('Loading fallback audiences...');
        audiencesData = {
            audiences: [
                { id: 'construction_workers', label: 'Construction Workers', description: 'Skilled tradespeople in construction industry', category: 'Professions' },
                { id: 'healthcare_workers', label: 'Healthcare Workers', description: 'Medical professionals and healthcare staff', category: 'Professions' },
                { id: 'office_workers', label: 'Office Workers', description: 'Corporate and administrative professionals', category: 'Professions' },
                { id: 'young_adults', label: 'Young Adults (18-24)', description: 'College students and young professionals', category: 'Demographics' },
                { id: 'millennials', label: 'Millennials (25-34)', description: 'Early career professionals', category: 'Demographics' }
            ],
            total_count: 5
        };
        console.log('Fallback audiences loaded:', audiencesData);
    }
    
    // Populate profession and demographic dropdowns
    populateAudienceDropdowns();
    
    // Load campaign history
    loadCampaignHistory();
});

// Populate profession and demographic dropdowns
function populateAudienceDropdowns() {
    if (!audiencesData || !audiencesData.audiences) {
        console.warn('No audiences data available to populate dropdowns');
        return;
    }
    
    const professionSelect = document.getElementById('profession');
    const demographicSelect = document.getElementById('demographic');
    
    // Filter professions and demographics
    const professions = audiencesData.audiences.filter(a => a.category === 'Professions');
    const demographics = audiencesData.audiences.filter(a => a.category === 'Demographics');
    
    // Populate profession dropdown
    professions.forEach(profession => {
        const option = document.createElement('option');
        option.value = profession.id;
        option.textContent = profession.label;
        professionSelect.appendChild(option);
    });
    
    // Populate demographic dropdown
    demographics.forEach(demographic => {
        const option = document.createElement('option');
        option.value = demographic.id;
        option.textContent = demographic.label;
        demographicSelect.appendChild(option);
    });
    
    console.log(`Populated ${professions.length} professions and ${demographics.length} demographics`);
}

// Load campaign history from master manifest
async function loadCampaignHistory() {
    try {
        console.log('Loading campaign history from master manifest...');
        const response = await fetch('/api/master-manifest');
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const manifest = await response.json();
        console.log('Master manifest loaded:', manifest);
        
        displayCampaignHistory(manifest);
    } catch (error) {
        console.error('Failed to load campaign history:', error);
        const historyContainer = document.getElementById('campaignHistory');
        historyContainer.innerHTML = '<div class="no-history"><div class="no-history-icon">📭</div><p>No campaign history available</p></div>';
    }
}

function displayCampaignHistory(manifest) {
    const historyContainer = document.getElementById('campaignHistory');
    
    if (!manifest.campaigns || manifest.campaigns.length === 0) {
        historyContainer.innerHTML = '<div class="no-history"><div class="no-history-icon">📭</div><p>No campaigns yet. Create your first campaign above!</p></div>';
        return;
    }
    
    // Sort campaigns by timestamp (most recent first)
    const sortedCampaigns = [...manifest.campaigns].sort((a, b) => 
        new Date(b.timestamp) - new Date(a.timestamp)
    );
    
    // Limit to most recent 10 campaigns
    const recentCampaigns = sortedCampaigns.slice(0, 10);
    
    historyContainer.innerHTML = recentCampaigns.map(campaign => {
        const timestamp = new Date(campaign.timestamp).toLocaleString();
        const productCount = Object.keys(campaign.products).length;
        const productNames = Object.keys(campaign.products);
        
        return `
            <div class="history-item" onclick="viewCampaignDetails('${campaign.campaign_id}')">
                <div class="history-header">
                    <span class="history-campaign-id">${campaign.campaign_id.substring(0, 8)}...</span>
                    <span class="history-timestamp">${timestamp}</span>
                </div>
                <div class="history-details">
                    <div class="history-detail">
                        <span class="history-detail-label">Region</span>
                        <span class="history-detail-value">${campaign.region || 'N/A'}</span>
                    </div>
                    <div class="history-detail">
                        <span class="history-detail-label">Audience</span>
                        <span class="history-detail-value">${campaign.audience || 'N/A'}</span>
                    </div>
                    <div class="history-detail">
                        <span class="history-detail-label">Products</span>
                        <span class="history-detail-value">${productCount} product${productCount !== 1 ? 's' : ''}</span>
                    </div>
                    <div class="history-detail">
                        <span class="history-detail-label">Compliance</span>
                        <span class="history-compliance ${(campaign.compliance_status || 'approved').toLowerCase()}">${campaign.compliance_status || 'Approved'}</span>
                    </div>
                </div>
                <div class="history-products">
                    ${productNames.map(product => `<span class="history-product-tag">${product}</span>`).join('')}
                </div>
            </div>
        `;
    }).join('');
}

function viewCampaignDetails(campaignId) {
    console.log('View campaign details:', campaignId);
    // TODO: Implement modal or detail view for campaign
    alert(`Campaign details for ${campaignId} - Feature coming soon!`);
}

// Product tags functionality
const productInput = document.getElementById('productInput');
const productTags = document.getElementById('productTags');
const productsHidden = document.getElementById('products');

function addProduct(productName) {
    const trimmed = productName.trim();
    if (!trimmed) return;
    
    // Avoid duplicates
    if (productsList.includes(trimmed)) {
        productInput.value = '';
        return;
    }
    
    // Add to list
    productsList.push(trimmed);
    
    // Create tag element
    const tag = document.createElement('div');
    tag.className = 'product-tag';
    tag.innerHTML = `
        <span class="tag-text">${trimmed}</span>
        <span class="tag-remove" data-product="${trimmed}">×</span>
    `;
    
    productTags.appendChild(tag);
    
    // Update hidden input
    productsHidden.value = productsList.join(',');
    
    // Clear input
    productInput.value = '';
    
    console.log('Added product:', trimmed, 'Total:', productsList);
}

function removeProduct(productName) {
    productsList = productsList.filter(p => p !== productName);
    productsHidden.value = productsList.join(',');
    
    // Remove tag element
    const tags = productTags.querySelectorAll('.product-tag');
    tags.forEach(tag => {
        const tagText = tag.querySelector('.tag-text').textContent;
        if (tagText === productName) {
            tag.remove();
        }
    });
    
    console.log('Removed product:', productName, 'Remaining:', productsList);
}

// Handle Enter key
productInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
        e.preventDefault();
        addProduct(productInput.value);
    } else if (e.key === 'Backspace' && !productInput.value && productsList.length > 0) {
        // Remove last tag if input is empty and backspace is pressed
        e.preventDefault();
        removeProduct(productsList[productsList.length - 1]);
    }
});

// Handle tag removal clicks
productTags.addEventListener('click', (e) => {
    if (e.target.classList.contains('tag-remove')) {
        const productName = e.target.getAttribute('data-product');
        removeProduct(productName);
    }
});

// Country search functionality
document.getElementById('regionSearch').addEventListener('input', (e) => {
    const query = e.target.value.toLowerCase();
    const dropdown = document.getElementById('regionDropdown');
    
    console.log('Searching for:', query);
    
    if (!countriesData) {
        console.warn('Countries data not loaded yet');
        dropdown.innerHTML = '<div class="no-results">Loading countries...</div>';
        dropdown.style.display = 'block';
        return;
    }
    
    if (query.length < 2) {
        dropdown.style.display = 'none';
        return;
    }
    
    const filteredCountries = countriesData.countries.filter(country => 
        country.name.toLowerCase().includes(query) ||
        country.code.toLowerCase().includes(query) ||
        country.primary_language.toLowerCase().includes(query)
    );
    
    console.log(`Found ${filteredCountries.length} countries matching "${query}"`);
    
    if (filteredCountries.length === 0) {
        dropdown.innerHTML = '<div class="no-results">No countries found</div>';
    } else {
        dropdown.innerHTML = filteredCountries.map(country => `
            <div class="country-option" data-code="${country.code}" data-name="${country.name}">
                <div>
                    <div class="country-name">${country.name}</div>
                    <div class="country-details">${country.primary_language} • ${country.region}</div>
                </div>
            </div>
        `).join('');
    }
    
    dropdown.style.display = 'block';
});

// Handle country selection
document.addEventListener('click', (e) => {
    if (e.target.closest('.country-option')) {
        const option = e.target.closest('.country-option');
        const countryCode = option.dataset.code;
        const countryName = option.dataset.name;
        
        selectCountry(countryCode, countryName);
    } else if (!e.target.closest('.country-selector')) {
        // Close dropdown when clicking outside
        document.getElementById('regionDropdown').style.display = 'none';
    }
});

function selectCountry(code, name) {
    console.log('Selected country:', { code, name });
    selectedCountry = { code, name };
    
    // Update hidden input
    document.getElementById('region').value = code;
    console.log('Updated hidden input value:', code);
    
    // Show selected country
    document.getElementById('selectedCountryName').textContent = name;
    document.getElementById('selectedCountry').style.display = 'flex';
    
    // Hide search and dropdown
    document.getElementById('regionSearch').style.display = 'none';
    document.getElementById('regionDropdown').style.display = 'none';
    
    console.log('Country selection complete');
}

// Clear country selection
document.getElementById('clearCountry').addEventListener('click', () => {
    selectedCountry = null;
    document.getElementById('region').value = '';
    document.getElementById('selectedCountry').style.display = 'none';
    document.getElementById('regionSearch').style.display = 'block';
    document.getElementById('regionSearch').value = '';
});

// Audience search functionality
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
    
    const region = document.getElementById('region').value;
    const profession = document.getElementById('profession').value;
    const demographic = document.getElementById('demographic').value;
    const message = document.getElementById('message').value;
    
    // Combine profession and demographic for audience
    const audience = profession && demographic ? `${profession}_${demographic}` : (profession || demographic);
    
    // Client-side validation
    if (!region) {
        alert('Please select a country/region');
        return;
    }
    
    if (!profession) {
        alert('Please select a profession');
        return;
    }
    
    if (!demographic) {
        alert('Please select a demographic');
        return;
    }
    
    if (products.length === 0) {
        alert('Please enter at least one product');
        return;
    }
    
    
    if (!message.trim()) {
        alert('Please enter a campaign message');
        return;
    }
    
    const data = {
        products: products,
        region: region,
        audience: audience,
        message: message
    };
    
    console.log('Form data being submitted:', data);
    console.log('Selected country:', selectedCountry);
    
    // Show loading state
    submitBtn.disabled = true;
    btnText.style.display = 'none';
    btnLoader.style.display = 'inline';
    document.getElementById('results').style.display = 'none';
    document.getElementById('error').style.display = 'none';
    
    // Show and initialize progress bar
    const progressContainer = document.getElementById('progressContainer');
    const progressBarFill = document.getElementById('progressBarFill');
    const progressPercentage = document.getElementById('progressPercentage');
    const progressMessage = document.getElementById('progressMessage');
    
    progressContainer.style.display = 'block';
    progressBarFill.style.width = '0%';
    progressPercentage.textContent = '0%';
    
    // Simulate progress updates (since we don't have real-time updates from backend)
    const steps = [
        { id: 'step1', message: 'Checking compliance...', progress: 5 },
        { id: 'step2', message: 'Validating request...', progress: 15 },
        { id: 'step3', message: 'Generating AI images...', progress: 45 },
        { id: 'step4', message: 'Translating content...', progress: 65 },
        { id: 'step5', message: 'Adding brand overlays...', progress: 85 },
        { id: 'step6', message: 'Finalizing campaign...', progress: 95 }
    ];
    
    let currentStep = 0;
    
    function updateProgress() {
        if (currentStep < steps.length) {
            const step = steps[currentStep];
            
            // Mark previous steps as completed
            for (let i = 0; i < currentStep; i++) {
                const prevStep = document.getElementById(steps[i].id);
                prevStep.classList.remove('active');
                prevStep.classList.add('completed');
            }
            
            // Mark current step as active
            const currentStepEl = document.getElementById(step.id);
            currentStepEl.classList.add('active');
            
            // Update progress bar
            progressBarFill.style.width = step.progress + '%';
            progressPercentage.textContent = step.progress + '%';
            progressMessage.textContent = step.message;
            
            currentStep++;
        }
    }
    
    // Start progress simulation
    updateProgress();
    const progressInterval = setInterval(updateProgress, 3000); // Update every 3 seconds
    
    try {
        const response = await fetch('/campaigns/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            
            // Check if it's a compliance failure
            if (response.status === 400 && errorData.detail && errorData.detail.compliance) {
                throw new Error(`Compliance Check Failed: ${errorData.detail.compliance.message}`);
            }
            
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
        
        // Display metadata if available
        if (result.metadata) {
            document.getElementById('metadataInfo').style.display = 'block';
            document.getElementById('llmModel').textContent = result.metadata.llm_usage.model || 'N/A';
            document.getElementById('promptTokens').textContent = result.metadata.llm_usage.prompt_tokens || 0;
            document.getElementById('completionTokens').textContent = result.metadata.llm_usage.completion_tokens || 0;
            document.getElementById('totalTokens').textContent = result.metadata.llm_usage.total_tokens || 0;
            document.getElementById('totalImages').textContent = result.metadata.total_images || 0;
            
            // Format timestamp
            const generatedAt = new Date(result.metadata.generated_at);
            document.getElementById('generatedAt').textContent = generatedAt.toLocaleString();
            
            // Format cost
            const cost = result.metadata.cost_usd || 0;
            if (cost < 0.01) {
                // Show full precision for very small costs
                document.getElementById('costUsd').textContent = `$${cost.toFixed(6)}`;
            } else if (cost < 1) {
                // Show cents for costs under $1
                document.getElementById('costUsd').textContent = `$${cost.toFixed(4)}`;
            } else {
                // Show standard format for larger costs
                document.getElementById('costUsd').textContent = `$${cost.toFixed(2)}`;
            }
        }
        
        // Create product containers dynamically
        const productsContainer = document.getElementById('productsContainer');
        productsContainer.innerHTML = '';
        
        // Display all products
        for (const [productName, productOutputs] of Object.entries(result.outputs)) {
            const productDiv = document.createElement('div');
            productDiv.className = 'product-section';
            productDiv.innerHTML = `
                <h4>${productName}</h4>
                <div class="image-grid">
                    <div class="image-card">
                        <h5>Square (1:1)</h5>
                        <img src="/${productOutputs['1:1']}" alt="Square format" loading="lazy">
                        <p class="image-size">1024 x 1024</p>
                    </div>
                    <div class="image-card">
                        <h5>Landscape (16:9)</h5>
                        <img src="/${productOutputs['16:9']}" alt="Landscape format" loading="lazy">
                        <p class="image-size">1024 x 576</p>
                    </div>
                    <div class="image-card">
                        <h5>Portrait (9:16)</h5>
                        <img src="/${productOutputs['9:16']}" alt="Portrait format" loading="lazy">
                        <p class="image-size">576 x 1024</p>
                    </div>
                </div>
            `;
            
            productsContainer.appendChild(productDiv);
        }
        
        // Complete progress bar
        clearInterval(progressInterval);
        progressBarFill.style.width = '100%';
        progressPercentage.textContent = '100%';
        progressMessage.textContent = 'Campaign generated successfully!';
        
        // Mark all steps as completed
        steps.forEach(step => {
            const stepEl = document.getElementById(step.id);
            stepEl.classList.remove('active');
            stepEl.classList.add('completed');
        });
        
        // Hide progress after a brief delay and show results
        setTimeout(() => {
            progressContainer.style.display = 'none';
            form.style.display = 'none';
            document.getElementById('results').style.display = 'block';
        }, 1500);
        
    } catch (error) {
        console.error('Error:', error);
        
        // Stop progress updates
        clearInterval(progressInterval);
        progressBarFill.style.width = '0%';
        progressMessage.textContent = 'Error generating campaign';
        progressContainer.style.display = 'none';
        
        // Reset all steps
        steps.forEach(step => {
            const stepEl = document.getElementById(step.id);
            stepEl.classList.remove('active', 'completed');
        });
        
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

