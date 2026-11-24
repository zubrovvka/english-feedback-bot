/**
 * UI components, navigation, helpers, and gestures
 */
import { state, abortActiveModeRequest } from './state.js';
import { apiFetch, checkUnauthorized } from './api.js';

export function levenshteinDistance(s1, s2) {
  if (s1 === s2) return 0;
  if (!s1.length) return s2.length;
  if (!s2.length) return s1.length;
  const d = [];
  for (let i = 0; i <= s1.length; i++) d[i] = [i];
  for (let j = 0; j <= s2.length; j++) d[0][j] = j;
  for (let i = 1; i <= s1.length; i++) {
    for (let j = 1; j <= s2.length; j++) {
      const cost = s1[i - 1] === s2[j - 1] ? 0 : 1;
      d[i][j] = Math.min(d[i - 1][j] + 1, d[i][j - 1] + 1, d[i - 1][j - 1] + cost);
    }
  }
  return d[s1.length][s2.length];
}

export function isMostlyRussian(text) {
  if (!text) return false;
  const cyrillic = (text.match(/[а-яА-ЯёЁ]/g) || []).length;
  const latin = (text.match(/[a-zA-Z]/g) || []).length;
  return cyrillic > latin;
}

export function escapeHtml(str) {
  if (!str) return '';
  return String(str).replace(/[&<>"']/g, m => ({
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#39;'
  }[m]));
}

export function updatePinBadgeUI(hasPin) {
  const pinBadge = document.getElementById("cfg-pin-status-badge");
  if (!pinBadge) return;
  if (hasPin) {
    pinBadge.innerText = "🔒 PIN активен";
    pinBadge.className = "text-[10px] px-2 py-0.5 rounded font-bold bg-emerald-900/60 text-emerald-300 border border-emerald-700/50";
  } else {
    pinBadge.innerText = "⚠️ Открыт";
    pinBadge.className = "text-[10px] px-2 py-0.5 rounded font-bold bg-amber-900/60 text-amber-300 border border-amber-700/50";
  }
}

export function showToast(msg) {
  const toast = document.getElementById("toast-notify");
  const toastText = document.getElementById("toast-text");
  if (!toast || !toastText) return;
  toastText.innerText = msg;
  toast.classList.remove("hidden");
  setTimeout(() => {
    toast.classList.add("hidden");
  }, 3000);
}

export function renderInteractiveWords(text, contextSentence) {
  if (!text) return '';
  const context = escapeHtml(contextSentence || text);
  const tokens = text.split(/(\s+|[.,!?;:()«»""—–\/\n]+)/);
  return tokens.map(token => {
    if (/^[a-zA-Z][a-zA-Z'-]*[a-zA-Z]$/.test(token) || /^[a-zA-Z]{2,}$/.test(token)) {
      const escapedToken = escapeHtml(token);
      return `<span class="interactive-word" data-word="${escapedToken}" data-sentence="${context}" onclick="handleInteractiveWordClick(this)">${escapedToken}</span>`;
    }
    return escapeHtml(token);
  }).join('');
}

export function handleInteractiveWordClick(el) {
  const word = el.getAttribute("data-word");
  const sentence = el.getAttribute("data-sentence");
  openQuickAdd(word, sentence);
}

export function openQuickAdd(word, sentence) {
  const clean = word.replace(/^[^\w]+|[^\w]+$/g, "").trim();
  document.getElementById("qa-word").value = clean;
  document.getElementById("qa-example").value = sentence || '';
  document.getElementById("qa-translation").value = '';
  document.getElementById("modal-quick-add").classList.remove("hidden");

  autoTranslateQuickAdd();
}

export function closeQuickAddModal() {
  document.getElementById("modal-quick-add").classList.add("hidden");
}

export async function autoTranslateQuickAdd() {
  const word = document.getElementById("qa-word").value.trim();
  const sentence = document.getElementById("qa-example").value.trim();
  if (!word) return;

  const aiBtn = document.getElementById("qa-btn-ai");
  aiBtn.innerText = "⏳...";
  try {
    const res = await apiFetch("/api/translate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: word, sentence: sentence })
    });
    const data = await res.json();
    if (data.translation) {
      document.getElementById("qa-translation").value = data.translation;
    }
  } catch (e) {
    console.error(e);
  } finally {
    aiBtn.innerHTML = "<span>✨</span><span>AI</span>";
  }
}

export async function submitQuickAdd(onAdded) {
  const word = document.getElementById("qa-word").value.trim();
  const translation = document.getElementById("qa-translation").value.trim();
  const example = document.getElementById("qa-example").value.trim();

  if (!word) {
    alert("Укажи слово");
    return;
  }

  try {
    const res = await apiFetch("/api/cards/quick-add", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        word: word,
        translation: translation,
        sentence: example
      })
    });
    const data = await res.json();
    if (data.success) {
      closeQuickAddModal();
      showToast(`Слово "${word}" добавлено в тренажер!`);
      if (onAdded) onAdded();
    }
  } catch (err) {
    alert("Ошибка при добавлении: " + err.message);
  }
}

// Touch & Swipe gestures for Mobile
let touchStartX = 0;
let touchStartY = 0;
let touchEndX = 0;
let touchEndY = 0;

export function setupTouchGestures(handlers = {}) {
  const cardBox = document.getElementById("card-box");
  if (!cardBox) return;

  cardBox.addEventListener("touchstart", (e) => {
    touchStartX = e.changedTouches[0].screenX;
    touchStartY = e.changedTouches[0].screenY;
  }, { passive: true });

  cardBox.addEventListener("touchend", (e) => {
    touchEndX = e.changedTouches[0].screenX;
    touchEndY = e.changedTouches[0].screenY;
    handleCardSwipe(handlers);
  }, { passive: true });
}

export function handleCardSwipe(handlers = {}) {
  const dx = touchEndX - touchStartX;
  const dy = touchEndY - touchStartY;
  
  if (Math.abs(dy) > Math.abs(dx) && Math.abs(dy) > 35) return;
  
  const unrevealed = document.getElementById("actions-unrevealed");
  const isUnrevealed = unrevealed && !unrevealed.classList.contains("hidden");

  if (Math.abs(dx) > 60) {
    if (dx > 0) {
      if (handlers.rateCard) handlers.rateCard(3); // Swipe Right -> Easy
    } else {
      if (handlers.rateCard) handlers.rateCard(1); // Swipe Left -> Forgot
    }
  } else if (Math.abs(dx) < 15 && Math.abs(dy) < 15) {
    if (isUnrevealed && handlers.revealAnswer) handlers.revealAnswer(); // Tap to flip
  }
}
