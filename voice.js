function setLang(lang) {
  window.selectedLang = lang;
}

function speak() {
  const msg = new SpeechSynthesisUtterance();
  msg.text = document.querySelector("textarea[name='message']").value;
  msg.lang = window.selectedLang || "hi-IN";
  window.speechSynthesis.speak(msg);
}
