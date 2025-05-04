document.addEventListener('DOMContentLoaded', function() {
    const filtersToggle = document.getElementById('filtersToggle');
    const filtersContainer = document.getElementById('filtersContainer');
    
    filtersToggle.addEventListener('click', function() {
        this.classList.toggle('active');
        filtersContainer.classList.toggle('active');
    });
    
    const priceMin = document.getElementById('priceMin');
    const priceMax = document.getElementById('priceMax');
    const priceMinInput = document.getElementById('priceMinInput');
    const priceMaxInput = document.getElementById('priceMaxInput');
    
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
    
    updatePriceInputs();
});