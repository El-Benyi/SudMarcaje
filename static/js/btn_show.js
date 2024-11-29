document.querySelectorAll('.show_info_btn').forEach(button => {
    button.addEventListener('click', function () {
        const userId = this.dataset.id;
        const userDiv = document.getElementById(`show_info_${userId}`);
        const closeBtn = userDiv.querySelector('.close-btn');  

        document.querySelectorAll('.profile_user').forEach(profile => {
            if (profile !== userDiv) {
                profile.style.display = 'none';
            }
        });

        if (userDiv) {
            userDiv.style.display = 'block';
        }

        if (closeBtn) {
            closeBtn.addEventListener('click', function () {
                userDiv.style.display = 'none';
            });
        }
    });
});