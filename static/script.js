function startListening() {
    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = 'en-US';
  
    recognition.onstart = () => console.log("Listening...");
    
    recognition.onresult = async (event) => {
      const transcript = event.results[0][0].transcript;
      document.getElementById("userText").textContent = "You: " + transcript;
  
      const res = await fetch("/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ message: transcript })
      });
  
      const data = await res.json();
      document.getElementById("botReply").textContent = data.response;
  
      const speech = new SpeechSynthesisUtterance(data.response);
      speech.lang = "en-US";
      window.speechSynthesis.speak(speech);
    };
  
    recognition.onerror = (e) => {
      console.error("Speech recognition error", e.error);
    };
  
    recognition.start();
  }
  