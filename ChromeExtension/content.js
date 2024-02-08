chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
  if (message.action === "showPopup") {
    showCustomPopup(message.text);
  } else if (message.action === "updateDescription") {
    // ポップアップの説明文を更新
    const descriptionElement = document.getElementById('description');
    if (descriptionElement) {
      descriptionElement.textContent = `解説: ${message.description}`;
    }
  }
});

function showCustomPopup(selectedText) {
  // 既存のポップアップがあれば削除
  const existingPopup = document.getElementById('custom-popup');
  if (existingPopup) {
    existingPopup.remove();
  }


  // ポップアップの作成
  const popupDiv = document.createElement('div');
  popupDiv.id = 'custom-popup';
  const imageUrl = chrome.runtime.getURL('images/google_icon.png');
  const closeButton = `<button id="closeButton" style="float: right;">&times;</button>`;
  popupDiv.innerHTML = closeButton + `
    <div id="custom-popup-content">
      <p id="question">質問: ${selectedText}</p>
      <p id="description">解説: 少々お待ちください...</p>
      <button id="searchButton">
        <img src="${imageUrl}" alt="Search" />
        Googleで検索
      </button>
    </div>`;
  document.body.appendChild(popupDiv);

  document.getElementById('closeButton').addEventListener('click', function() {
    popupDiv.remove(); // ポップアップをDOMから削除
  });

  // 検索ボタンのイベントリスナー
  document.getElementById('searchButton').addEventListener('click', function() {
    const query = selectedText;
    if (query) {
      const url = 'https://www.google.com/search?q=' + encodeURIComponent(query);
      window.open(url, '_blank');
    }
  });
}
