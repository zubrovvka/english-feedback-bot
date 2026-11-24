/**
 * Audio playback, Edge-TTS API, Web Speech API fallback, and auto-play configuration
 */
import { state } from './state.js';
import { isMostlyRussian, showToast } from './ui.js';

export function initAutoPlaySetting() {
  const stored = localStorage.getItem("autoplay_audio");
  state.autoPlayAudio = stored === null ? true : stored === "true";

  const storedDelay = localStorage.getItem("autoplay_delay");
  state.autoPlayDelay = storedDelay !== null ? parseInt(storedDelay, 10) : 0;

  updateAutoPlayUI();
}

export function updateAutoPlayUI() {
  const toggleCheckbox = document.getElementById("cfg-autoplay-audio");
  if (toggleCheckbox) toggleCheckbox.checked = state.autoPlayAudio;

  const delaySelect = document.getElementById("cfg-autoplay-delay");
  if (delaySelect) delaySelect.value = state.autoPlayDelay.toString();

  const quickBtn = document.getElementById("btn-quick-autoplay");
  const quickIcon = document.getElementById("quick-autoplay-icon");
  const quickText = document.getElementById("quick-autoplay-text");

  if (quickBtn && quickIcon && quickText) {
    if (state.autoPlayAudio) {
      quickBtn.className = "px-2.5 py-1 rounded-full text-xs font-medium border transition flex items-center space-x-1 border-indigo-500/60 bg-indigo-500/20 text-indigo-300 hover:bg-indigo-500/30";
      quickIcon.innerText = "🔊";
      quickText.innerText = "Авто: Вкл";
    } else {
      quickBtn.className = "px-2.5 py-1 rounded-full text-xs font-medium border transition flex items-center space-x-1 border-slate-700 bg-slate-800/80 text-slate-400 hover:text-slate-200";
      quickIcon.innerText = "🔇";
      quickText.innerText = "Авто: Выкл";
    }
  }
}

export function setAutoPlaySetting(enabled) {
  state.autoPlayAudio = Boolean(enabled);
  localStorage.setItem("autoplay_audio", state.autoPlayAudio ? "true" : "false");
  updateAutoPlayUI();
}

export function setAutoPlayDelay(delayVal) {
  state.autoPlayDelay = parseInt(delayVal, 10) || 0;
  localStorage.setItem("autoplay_delay", state.autoPlayDelay.toString());
}

export function toggleAutoPlayQuick() {
  setAutoPlaySetting(!state.autoPlayAudio);
  showToast(state.autoPlayAudio ? "🔊 Авто-озвучка включена" : "🔇 Авто-озвучка выключена");
}

export function playAudio(isAuto = false) {
  if (!state.currentCard) return;
  const backContainer = document.getElementById("card-back-container");
  const isAnswerRevealed = backContainer && !backContainer.classList.contains("hidden");

  // Не озвучивать автоматически при открытии карточки, если вопрос на русском (например, разбор ошибок)
  if (isAuto && !isAnswerRevealed && (state.currentCard.type === 'correction' || isMostlyRussian(state.currentCard.front))) {
    return;
  }

  const btn = document.getElementById("btn-audio");
  if (btn) {
    btn.classList.add("ring-2", "ring-indigo-400", "scale-105");
    setTimeout(() => btn.classList.remove("ring-2", "ring-indigo-400", "scale-105"), 300);
  }
  const player = document.getElementById("audio-player");
  player.src = `/api/tts/${state.currentCard.id}`;
  player.currentTime = 0;
  player.play().catch(e => {
    if ('speechSynthesis' in window) {
      try {
        window.speechSynthesis.cancel();
        const textToSpeak = isAnswerRevealed ? (state.currentCard.back || state.currentCard.front) : state.currentCard.front;
        if (textToSpeak && !isMostlyRussian(textToSpeak)) {
          const cleanText = textToSpeak.replace(/[а-яА-ЯёЁ«»—–➔\->❌✅💡⭐🔤]+/g, " ").trim();
          if (cleanText) {
            const u = new SpeechSynthesisUtterance(cleanText);
            u.lang = 'en-US';
            window.speechSynthesis.speak(u);
          }
        }
      } catch (err) {}
    }
  });
}

export function playClozeAudio() {
  if (!state.currentClozeCard) return;
  const player = document.getElementById("audio-player");
  player.src = `/api/tts/${state.currentClozeCard.card_id}`;
  player.currentTime = 0;
  player.play().catch(e => {
    if ('speechSynthesis' in window) {
      try {
        window.speechSynthesis.cancel();
        const u = new SpeechSynthesisUtterance(state.currentClozeCard.target);
        u.lang = 'en-US';
        window.speechSynthesis.speak(u);
      } catch (err) {}
    }
  });
}

export function playQuizAudio(isAuto = false) {
  if (!state.currentQuizData || !state.currentQuizData.card_id) return;
  // Не озвучивать русские вопросы квиза
  if (isMostlyRussian(state.currentQuizData.question)) return;

  const player = document.getElementById("audio-player");
  player.src = `/api/tts/${state.currentQuizData.card_id}`;
  player.currentTime = 0;
  player.play().catch(e => {
    if ('speechSynthesis' in window) {
      try {
        window.speechSynthesis.cancel();
        if (!isMostlyRussian(state.currentQuizData.question)) {
          const u = new SpeechSynthesisUtterance(state.currentQuizData.question);
          u.lang = 'en-US';
          window.speechSynthesis.speak(u);
        }
      } catch (err) {}
    }
  });
}

export function playCardAudioDirect(cardId) {
  const card = state.allCardsCache.find(c => c.id === cardId);
  const player = document.getElementById("audio-player");
  player.src = `/api/tts/${cardId}?t=${Date.now()}`;
  player.play().catch(e => {
    if ('speechSynthesis' in window && card) {
      const u = new SpeechSynthesisUtterance(card.front);
      u.lang = 'en-US';
      window.speechSynthesis.speak(u);
    }
  });
}
