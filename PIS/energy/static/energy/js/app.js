const swith = document.querySelector('.switch');

swith.addEventListener('click', () => {
    document.body.classList.toggle('dark');
    swith.classList.toggle('active');
    // Guardamos el modo en localstorage.
    if (document.body.classList.contains('dark')) {
        localStorage.setItem('dark-mode', 'true');
    } else {
        localStorage.setItem('dark-mode', 'false');
    }
})