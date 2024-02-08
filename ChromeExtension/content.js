/*
This program is about custom popup.
*/

document.addEventListener('mouseup', function(e) {
  const selectedText = window.getSelection().toString().trim();
  if (selectedText.length > 0) {
    chrome.runtime.sendMessage({question: selectedText});

    // Inset HTML of custom popup
    const existingPopup = document.getElementById('custom-popup');
    if (existingPopup) {
      existingPopup.remove();
    }

    const popupDiv = document.createElement('div');
    popupDiv.id = 'custom-popup';
    const imageUrl = chrome.runtime.getURL('images/google_icon.png')
    popupDiv.innerHTML = `
      <div id="custom-popup-content">
        <p id="question">質問: ${selectedText}</p>
        <p id="description">解説: 少々お待ちください...</p>
        <button id="searchButton">
          <img src="${imageUrl}" alt="Search" />
          Googleで検索
        </button>
      </div>`;
    document.body.appendChild(popupDiv);

    // Add Event Listener
    document.getElementById('searchButton').addEventListener('click', function() {
      const query = document.getElementById('question').textContent;
      if (query) {
        const url = 'https://www.google.com/search?q=' + encodeURIComponent(query);
      }
    });
  }
});

chrome.storage.onChanged.addListener(function(changes, namespace) {
  for (let [key, { oldValue, newValue }] of Object.entries(changes)) {
    if (key === 'description') {
      document.getElementById('description').textContent = newValue;
    }
  }
});
