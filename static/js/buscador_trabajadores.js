document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.getElementById('exampleDataList');
    const workers = document.querySelectorAll('.workers');

    searchInput.addEventListener('input', () => {
        const searchValue = searchInput.value.toLowerCase();

        workers.forEach(worker => {
            const workerName = worker.querySelector('span').textContent.toLowerCase();
            if (workerName.includes(searchValue)) {
                worker.style.display = ''; 
            } else {
                worker.style.display = 'none'; 
            }
        });
    });
});