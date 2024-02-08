chrome.runtime.onInstalled.addListener(() => {
  chrome.contextMenus.create({
    id: "showCustomPopup",
    title: "このテキストについて詳しく",
    contexts: ["selection"]
  });
});

// コンテキストメニュー項目がクリックされたときの処理
chrome.contextMenus.onClicked.addListener((info, tab) => {
  if (info.menuItemId === "showCustomPopup") {
    // コンテンツスクリプトにメッセージを送信してポップアップを表示
    chrome.tabs.sendMessage(tab.id, {
      action: "showPopup",
      text: info.selectionText
    });

    // ここでAPIリクエストを行う
    fetch('http://0.0.0.0:8000/chat/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({text: info.selectionText})
    })
    .then(response => {
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return response.json();
    })
    .then(data => {
      // APIからのレスポンスで 'text' キーの内容を取得し、コンテンツスクリプトに送信して内容を更新
      chrome.tabs.sendMessage(tab.id, {action: "updateDescription", description: data.text});
    })
    .catch(error => {
      console.error('Error:', error);
      // エラーメッセージをコンテンツスクリプトに送信
      chrome.tabs.sendMessage(tab.id, {action: "updateDescription", description: 'エラーが発生しました。'});
    });
  }
});
