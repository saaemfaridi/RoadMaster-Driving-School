// Main JavaScript for RoadMaster Application

document.addEventListener('DOMContentLoaded', function() {
    console.log('RoadMaster application loaded');
    
    // Initialize tooltips if Bootstrap is available
    if (typeof bootstrap !== 'undefined') {
        var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }
    
    // Example function for API data fetching
    function fetchData() {
        fetch('/api/data')
            .then(response => response.json())
            .then(data => {
                console.log('Data fetched:', data);
                // Process data here
            })
            .catch(error => console.error('Error fetching data:', error));
    }
    
    // Example function for form submission
    function setupForms() {
        const forms = document.querySelectorAll('.needs-validation');
        
        Array.from(forms).forEach(form => {
            form.addEventListener('submit', event => {
                if (!form.checkValidity()) {
                    event.preventDefault();
                    event.stopPropagation();
                }
                
                form.classList.add('was-validated');
            }, false);
        });
    }
    
    // Initialize components
    setupForms();
    
    // Uncomment to fetch data on page load
    // fetchData();
}); 