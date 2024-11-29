document.getElementById('user_mail').addEventListener('input', function() {
    let query = this.value;

    if (query.length > 1) {  
        fetch(`/check_email?email=${query}`)
            .then(response => response.json())
            .then(data => {
                let suggestions = data.suggestions;
                let suggestionsList = document.getElementById('email_suggestions');
                suggestionsList.innerHTML = '';

                suggestions.forEach(suggestion => {
                    let item = document.createElement('div');
                    item.classList.add('suggestion-item');
                    item.textContent = suggestion;
                    suggestionsList.appendChild(item);
                });
            });
    } else {
        document.getElementById('email_suggestions').innerHTML = '';
    }
});