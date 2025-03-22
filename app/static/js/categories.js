document.addEventListener('DOMContentLoaded', function() {
    // Busca de categorias
    const searchInput = document.getElementById('search-input');
    const categoriasList = document.getElementById('categorias-list');

    searchInput.addEventListener('input', function(e) {
        const searchTerm = e.target.value.toLowerCase();
        const categorias = categoriasList.getElementsByTagName('li');

        Array.from(categorias).forEach(categoria => {
            const nome = categoria.querySelector('.font-medium').textContent.toLowerCase();
            if (nome.includes(searchTerm)) {
                categoria.style.display = '';
            } else {
                categoria.style.display = 'none';
            }
        });
    });

    // Atualize a URL
    const deleteUrl = "{{ url_for('main.delete_category', category_id=':id') }}".replace(':id', categoryId);
});