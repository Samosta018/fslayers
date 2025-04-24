document.addEventListener('DOMContentLoaded', function() {
    // Toggle filters
    const filtersToggle = document.getElementById('filtersToggle');
    const filtersContainer = document.getElementById('filtersContainer');
    
    filtersToggle.addEventListener('click', function() {
        this.classList.toggle('active');
        filtersContainer.classList.toggle('active');
    });
    
    // Price range slider
    const priceMin = document.getElementById('priceMin');
    const priceMax = document.getElementById('priceMax');
    const priceMinInput = document.getElementById('priceMinInput');
    const priceMaxInput = document.getElementById('priceMaxInput');
    const priceRangeContainer = document.getElementById('priceRangeContainer');
    const negotiableCheckbox = document.getElementById('negotiableCheckbox');
    
    function formatPrice(price) {
        return new Intl.NumberFormat('ru-RU').format(price) + ' ₽';
    }
    
    function updatePriceInputs() {
        priceMinInput.value = formatPrice(priceMin.value);
        priceMaxInput.value = formatPrice(priceMax.value);
    }
    
    priceMin.addEventListener('input', function() {
        if (parseInt(priceMin.value) > parseInt(priceMax.value)) {
            priceMax.value = priceMin.value;
        }
        updatePriceInputs();
    });
    
    priceMax.addEventListener('input', function() {
        if (parseInt(priceMax.value) < parseInt(priceMin.value)) {
            priceMin.value = priceMax.value;
        }
        updatePriceInputs();
    });
    
    // Parse price input and update slider
    priceMinInput.addEventListener('change', function() {
        const value = parseInt(this.value.replace(/\D/g, ''));
        if (!isNaN(value)) {
            priceMin.value = Math.min(value, parseInt(priceMax.value));
            updatePriceInputs();
        }
    });
    
    priceMaxInput.addEventListener('change', function() {
        const value = parseInt(this.value.replace(/\D/g, ''));
        if (!isNaN(value)) {
            priceMax.value = Math.max(value, parseInt(priceMin.value));
            updatePriceInputs();
        }
    });
    
    // Negotiable checkbox
    negotiableCheckbox.addEventListener('change', function() {
        if (this.checked) {
            priceRangeContainer.classList.add('disabled');
        } else {
            priceRangeContainer.classList.remove('disabled');
        }
    });
    
    // Initialize
    updatePriceInputs();
});