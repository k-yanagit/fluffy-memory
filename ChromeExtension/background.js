chrome.runtime.onMessage.addListener(
    function(request, sender, sendResponse) {
      const apiUrl = 'API_ENDPOINT'; // ここにAPIのエンドポイントURLをセット
      fetch(apiUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({question: request.question})
      })
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        const description = data.text;
        chrome.storage.local.set({question: request.question, description: description});
        chrome.scripting.executeScript({
          target: {tabId: sender.tab.id},
          files: ['popup.js']
        });
      })
      .catch(error => {
        console.error('Error:', error);
        chrome.storage.local.set({description: 'Error fetching data.'});
      });
    }
  );
