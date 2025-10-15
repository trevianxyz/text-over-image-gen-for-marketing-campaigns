// Country selector functionality
let countriesData = null;
let selectedCountry = null;

// Audience selector functionality
let audiencesData = null;
let selectedAudience = null;

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
        
        // Show a brief success message
        const searchInput = document.getElementById('audienceSearch');
        if (searchInput) {
            searchInput.placeholder = `Search ${audiencesData.total_count} audiences...`;
        }
    } catch (error) {
        console.error('Failed to load audiences:', error);
        
        // Show user-friendly error message
        const searchInput = document.getElementById('audienceSearch');
        if (searchInput) {
            searchInput.placeholder = 'Error loading audiences - please refresh the page';
            searchInput.disabled = true;
        }
        
        // Show error in the dropdown
        const dropdown = document.getElementById('audienceDropdown');
        if (dropdown) {
            dropdown.innerHTML = '<div class="no-results">Failed to load audiences. Please refresh the page.</div>';
            dropdown.style.display = 'block';
        }
        
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
document.getElementById('audienceSearch').addEventListener('input', (e) => {
    const query = e.target.value.toLowerCase();
    const dropdown = document.getElementById('audienceDropdown');
    
    console.log('Searching audiences for:', query);
    
    if (!audiencesData) {
        console.warn('Audiences data not loaded yet');
        dropdown.innerHTML = '<div class="no-results">Loading audiences...</div>';
        dropdown.style.display = 'block';
        return;
    }
    
    if (query.length < 2) {
        dropdown.style.display = 'none';
        return;
    }
    
    const filteredAudiences = audiencesData.audiences.filter(audience => 
        audience.label.toLowerCase().includes(query) ||
        audience.description.toLowerCase().includes(query) ||
        audience.category.toLowerCase().includes(query)
    );
    
    console.log(`Found ${filteredAudiences.length} audiences matching "${query}"`);
    
    if (filteredAudiences.length === 0) {
        dropdown.innerHTML = '<div class="no-results">No audiences found</div>';
    } else {
        dropdown.innerHTML = filteredAudiences.map(audience => `
            <div class="audience-option" data-id="${audience.id}" data-label="${audience.label}">
                <div class="audience-label">${audience.label}</div>
                <div class="audience-description">${audience.description}</div>
                <div class="audience-category">${audience.category}</div>
            </div>
        `).join('');
    }
    
    dropdown.style.display = 'block';
});

// Handle audience option clicks
document.addEventListener('click', (e) => {
    if (e.target.closest('.audience-option')) {
        const option = e.target.closest('.audience-option');
        const audienceId = option.dataset.id;
        const audienceLabel = option.dataset.label;
        
        selectAudience(audienceId, audienceLabel);
    } else if (!e.target.closest('.audience-selector')) {
        // Close dropdown when clicking outside
        document.getElementById('audienceDropdown').style.display = 'none';
    }
});

function selectAudience(id, label) {
    console.log('Selected audience:', { id, label });
    selectedAudience = { id, label };
    
    // Update hidden input
    document.getElementById('audience').value = id;
    
    // Show selected audience
    document.getElementById('selectedAudienceName').textContent = label;
    document.getElementById('selectedAudience').style.display = 'flex';
    document.getElementById('audienceSearch').style.display = 'none';
    
    // Hide dropdown
    document.getElementById('audienceDropdown').style.display = 'none';
}

// Clear audience selection
document.getElementById('clearAudience').addEventListener('click', () => {
    selectedAudience = null;
    document.getElementById('audience').value = '';
    document.getElementById('selectedAudience').style.display = 'none';
    document.getElementById('audienceSearch').style.display = 'block';
    document.getElementById('audienceSearch').value = '';
});

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
    const audience = document.getElementById('audience').value;
    const message = document.getElementById('message').value;
    
    // Client-side validation
    if (!region) {
        alert('Please select a country/region');
        return;
    }
    
    if (!audience) {
        alert('Please select a target audience');
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

