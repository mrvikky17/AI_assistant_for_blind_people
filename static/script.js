function addMessage(text, sender) {
  const box = document.getElementById("chat-box");
  const msg = document.createElement("div");
  msg.className = sender;
  msg.textContent = text;
  box.appendChild(msg);
  box.scrollTop = box.scrollHeight;
}

async function sendMessage() {
  const input = document.getElementById("user-input");
  const message = input.value.trim();
  if (!message) return;

  addMessage("You: " + message, "user");
  input.value = "";

  const res = await fetch("/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message }),
  });

  const data = await res.json();
  if (data.reply) {
    addMessage("AI: " + data.reply, "bot");
    speakText(data.reply);
  }
}

function speakText(text) {
  const synth = window.speechSynthesis;
  const utter = new SpeechSynthesisUtterance(text);
  synth.speak(utter);
}

function startSpeech() {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  const recognition = new SpeechRecognition();
  recognition.lang = "en-US";
  recognition.start();

  recognition.onresult = function(event) {
    const result = event.results[0][0].transcript;
    document.getElementById("user-input").value = result;
    sendMessage();
  };

  recognition.onerror = function() {
    alert("🎤 Could not recognize your voice. Try again.");
  };
}
