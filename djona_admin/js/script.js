function performSearch(query) {
    const resultsContainer = document.getElementById('search-results');
    const loadingIndicator = document.getElementById('loading-indicator');

    if (query.trim() === '') {
        resultsContainer.innerHTML = '';
        return;
    }

    loadingIndicator.style.display = 'block';

    fetch(`/search/?q=${encodeURIComponent(query)}`)
        .then(response => response.json())
        .then(data => {
            loadingIndicator.style.display = 'none';
            const results = data.results || [];
            if (results.length === 0) {
                resultsContainer.innerHTML = '<li class="no-results">Aucun véhicule trouvé.</li>';
            } else {
                resultsContainer.innerHTML = results.map(result => `
                    <li>
                        <strong>${result.marque}</strong> - ${result.modele} - €${result.prix}
                    </li>
                `).join('');
            }
        })
        .catch(error => {
            console.error('Erreur lors de la recherche :', error);
            loadingIndicator.style.display = 'none';
        });
}

function resetSearch() {
    document.querySelector('.search-input').value = '';
    document.getElementById('search-results').innerHTML = '';
}

