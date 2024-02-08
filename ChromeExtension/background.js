chrome.runtime.onInstalled.addListener(() => {
  chrome.contextMenus.create({
    id: "showCustomPopup",
    title: "このテキストについて詳しく",
    contexts: ["selection"]
  });
});

// Processing when a context menu item is clicked
chrome.contextMenus.onClicked.addListener((info, tab) => {
  if (info.menuItemId === "showCustomPopup") {
    // Send message to content script to display popup
    chrome.tabs.sendMessage(tab.id, {
      action: "showPopup",
      text: info.selectionText
    });

    // Make API request
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
      // Get the contents of the 'text' key in the response from the API and send it to the content script to update the contents
      chrome.tabs.sendMessage(tab.id, {action: "updateDescription", description: data.text});
    })
    .catch(error => {
      console.error('Error:', error);
      // Send error messages to content scripts
      chrome.tabs.sendMessage(tab.id, {action: "updateDescription", description: 'エラーが発生しました。'});
    });
  }
});
