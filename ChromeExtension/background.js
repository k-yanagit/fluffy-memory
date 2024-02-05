chrome.runtime.onMessage.addListener(
    function(request, sender, sendResponse) {
      // 選択されたテキストでストレージを更新
      chrome.storage.local.set({question: request.question, description: '少々お待ちください...'});

      // APIにリクエストを送る
      fetch('http://0.0.0.0:8000/chat/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({text: request.question})
      })
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        console.log('API response:', data);
        // APIからのレスポンスで 'text' キーの内容を取得
        const description = data.text;
        // 取得したdescriptionを保存
        chrome.storage.local.set({question: request.question, description: description});
      })
      .catch(error => {
        console.error('Error:', error);
        chrome.storage.local.set({description: 'エラーが発生しました。'});
      });
    }
  );
