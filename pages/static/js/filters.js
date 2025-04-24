document.addEventListener('DOMContentLoaded', function() {
    const filtersToggle = document.getElementById('filtersToggle');
    const filtersContainer = document.getElementById('filtersContainer');
    
    if (filtersToggle && filtersContainer) {
        filtersToggle.addEventListener('click', function() {
            this.classList.toggle('active');
            filtersContainer.classList.toggle('active');
        });
    }

    const formatNumber = (num) => {
        return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ' ');
    };

    const priceMin = document.getElementById('priceMin');
    const priceMax = document.getElementById('priceMax');
    const priceMinInput = document.getElementById('priceMinInput');
    const priceMaxInput = document.getElementById('priceMaxInput');

    const updateInputs = () => {
        priceMinInput.value = formatNumber(priceMin.value);
        priceMaxInput.value = formatNumber(priceMax.value);
    };

    [priceMin, priceMax].forEach(slider => {
        slider.addEventListener('input', function() {
            let value = parseInt(this.value);
            
            if (this === priceMin && value > parseInt(priceMax.value)) {
                value = priceMax.value;
                this.value = value;
            }
            
            if (this === priceMax && value < parseInt(priceMin.value)) {
                value = priceMin.value;
                this.value = value;
            }
            
            updateInputs();
        });
    });

    [priceMinInput, priceMaxInput].forEach(input => {
        input.addEventListener('input', function(e) {
            let value = parseInt(this.value.replace(/\s/g, '')) || 0;
            
            if (this === priceMinInput) {
                value = Math.min(value, parseInt(priceMax.value));
                priceMin.value = value;
            } else {
                value = Math.max(value, parseInt(priceMin.value));
                priceMax.value = value;
            }
            
            this.value = formatNumber(value);
        });
    });

    updateInputs();
});