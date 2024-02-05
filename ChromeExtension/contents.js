document.getElementById('searchButton').addEventListener('click', function() {
    const query = document.getElementById('question').textContent;
    if (query) {
      const url = 'https://www.google.com/search?q=' + encodeURIComponent(query);
      window.open(url, '_blank');
    }
  });
