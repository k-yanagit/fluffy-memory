document.addEventListener('mouseup', function(e) {
  const selectedText = window.getSelection().toString().trim();
  console.log(selectedText)
  if (selectedText.length > 0) {
    chrome.runtime.sendMessage({question: selectedText});

    // カスタムポップアップHTMLを挿入する
    const existingPopup = document.getElementById('custom-popup');
    if (existingPopup) {
      existingPopup.remove();
    }

    const popupDiv = document.createElement('div');
    popupDiv.id = 'custom-popup';
    popupDiv.innerHTML = `
      <div id="custom-popup-content">
        <p id="question">質問: ${selectedText}</p>
        <p id="description">解説: 少々お待ちください...</p>
        <button id="searchButton">
          <img src="images/google_icon.png" alt="Search" />
          Googleで検索
        </button>
      </div>`;
    document.body.appendChild(popupDiv);

    // イベントリスナーを追加
    document.getElementById('searchButton').addEventListener('click', function() {
      const query = document.getElementById('question').textContent;
      if (query) {
        const url = 'https://www.google.com/search?q=' + encodeURIComponent(query);
        window.open(url, '_blank');
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
