chrome.storage.local.get(['question', 'description'], function(result) {
    document.getElementById('question').textContent = result.question;
    document.getElementById('description').textContent = result.description;
  });

  document.getElementById('searchButton').addEventListener('click', function() {
    const query = document.getElementById('question').textContent;
    const url = 'https://www.google.com/search?q=' + encodeURIComponent(query);
    window.open(url, '_blank');
  });
