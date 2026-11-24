/**
 * Main application entry point: ES Module bundle
 */
import { state, abortActiveModeRequest, CARD_TYPES } from './modules/state.js';
import { apiFetch, checkUnauthorized, submitPinAuth as apiSubmitPinAuth } from './modules/api.js';
import {
  escapeHtml,
  isMostlyRussian,
  updatePinBadgeUI,
  showToast,
  renderInteractiveWords,
  handleInteractiveWordClick,
  openQuickAdd,
  closeQuickAddModal,
  autoTranslateQuickAdd,
  submitQuickAdd as uiSubmitQuickAdd,
  setupTouchGestures
} from './modules/ui.js';
import {
  initAutoPlaySetting,
  updateAutoPlayUI,
  setAutoPlaySetting,
  setAutoPlayDelay,
  toggleAutoPlayQuick,
  playAudio,
  playClozeAudio,
  playQuizAudio,
  playCardAudioDirect
} from './modules/tts.js';
import { loadStats, loadNextCard, renderCard, revealAnswer, rateCard } from './modules/srs.js';
import { loadNextCloze, checkClozeAnswer, revealClozeHintLetter } from './modules/cloze.js';
import { loadNextQuiz, handleQuizAnswer } from './modules/quiz.js';

// ==========================================================
// 1. NAVIGATION & TABS
// ==========================================================
export function switchTab(tabId) {
  document.querySelectorAll(".tab-pane").forEach(el => el.classList.add("hidden"));
  const targetTab = document.getElementById(`tab-${tabId}`);
  if (targetTab) targetTab.classList.remove("hidden");

  ['practice', 'upload', 'cards', 'settings'].forEach(id => {
    const btn = document.getElementById(`nav-${id}`);
    const mobBtn = document.getElementById(`mob-nav-${id}`);
    if (id === tabId) {
      if (btn) btn.className = "px-3 py-1.5 rounded-lg text-sm font-medium transition bg-indigo-600 text-white flex items-center space-x-1";
      if (mobBtn) mobBtn.className = "flex flex-col items-center py-1 px-3 text-indigo-400 font-semibold text-xs transition";
    } else {
      if (btn) btn.className = "px-3 py-1.5 rounded-lg text-sm font-medium transition text-slate-300 hover:bg-slate-800 hover:text-white flex items-center space-x-1";
      if (mobBtn) mobBtn.className = "flex flex-col items-center py-1 px-3 text-slate-400 hover:text-white font-medium text-xs transition";
    }
  });

  if (tabId === 'practice') {
    loadStats();
    if (state.currentMode === 'card' && !state.currentCard) loadNextCard();
    else if (state.currentMode === 'cloze' && !state.currentClozeCard) loadNextCloze();
    else if (state.currentMode === 'quiz' && !state.currentQuizData) loadNextQuiz();
  } else if (tabId === 'cards') {
    loadCardsTable();
  } else if (tabId === 'settings') {
    updateAutoPlayUI();
  }
}

export function setPracticeMode(mode) {
  abortActiveModeRequest();
  state.currentMode = mode;
  
  ['card', 'cloze', 'quiz'].forEach(m => {
    const btn = document.getElementById(`mode-btn-${m}`);
    const box = document.getElementById(`${m}-box`);
    if (m === mode) {
      btn.className = "flex-1 py-1.5 px-3 rounded-lg text-xs sm:text-sm font-semibold transition bg-indigo-600 text-white flex items-center justify-center space-x-1.5";
      box.classList.remove("hidden");
    } else {
      btn.className = "flex-1 py-1.5 px-3 rounded-lg text-xs sm:text-sm font-semibold transition text-slate-400 hover:text-white flex items-center justify-center space-x-1.5";
      box.classList.add("hidden");
    }
  });

  const streakIndicator = document.getElementById("streak-indicator");
  if (mode === 'quiz') streakIndicator.classList.remove("hidden");
  else streakIndicator.classList.add("hidden");

  if (mode === 'card') {
    if (!state.currentCard) loadNextCard();
  } else if (mode === 'cloze') {
    loadNextCloze();
  } else if (mode === 'quiz') {
    loadNextQuiz();
  }
}

export function setCategory(cat) {
  state.currentCategory = cat;
  document.querySelectorAll(".cat-pill").forEach(pill => {
    const pCat = pill.getAttribute("data-cat");
    if ((!cat && pCat === 'all') || pCat === cat) {
      pill.className = "cat-pill active px-3 py-1 rounded-full text-xs font-medium border border-indigo-500 bg-indigo-500/20 text-indigo-300";
    } else {
      pill.className = "cat-pill px-3 py-1 rounded-full text-xs font-medium border border-slate-700 bg-slate-900 text-slate-400 hover:border-slate-500";
    }
  });

  if (state.currentMode === 'card') loadNextCard();
  else if (state.currentMode === 'cloze') loadNextCloze();
  else if (state.currentMode === 'quiz') loadNextQuiz();
}

export function submitPinAuth(e) {
  return apiSubmitPinAuth(e, {
    onSuccess: () => {
      loadStats();
      if (state.currentMode === 'card') loadNextCard();
      else if (state.currentMode === 'cloze') loadNextCloze();
      else if (state.currentMode === 'quiz') loadNextQuiz();
      loadConfig();
    }
  });
}

export function submitQuickAdd() {
  return uiSubmitQuickAdd(() => loadStats());
}

// ==========================================================
// 2. CARDS LIBRARY TABLE
// ==========================================================
export async function loadCardsTable() {
  try {
    const res = await apiFetch("/api/cards");
    if (checkUnauthorized(res)) return;
    const data = await res.json();
    state.allCardsCache = data.cards || [];
    renderCardsTable(state.allCardsCache);
  } catch (err) {
    console.error(err);
  }
}

export function renderCardsTable(cards) {
  const tbody = document.getElementById("cards-table-body");
  if (!cards.length) {
    tbody.innerHTML = `<tr><td colspan="5" class="py-6 text-center text-slate-500">Пока нет карточек в базе</td></tr>`;
    return;
  }

  tbody.innerHTML = cards.map(c => `
    <tr class="hover:bg-slate-800/40 transition">
      <td class="py-3 px-4 font-mono text-xs text-indigo-400">${escapeHtml(c.type)}</td>
      <td class="py-3 px-4 font-semibold text-white">${escapeHtml(c.front)}</td>
      <td class="py-3 px-4 text-slate-300">${escapeHtml(c.back)}</td>
      <td class="py-3 px-4 text-xs text-slate-400">${c.interval} дн. (повт: ${c.repetition})</td>
      <td class="py-3 px-4 text-right space-x-2">
        <button onclick="playCardAudioDirect(${c.id})" class="p-1.5 hover:bg-slate-800 rounded text-slate-400 hover:text-white" title="Послушать">🔊</button>
        <button onclick="deleteCardRow(${c.id})" class="p-1.5 hover:bg-rose-950/60 rounded text-slate-500 hover:text-rose-400" title="Удалить">🗑</button>
      </td>
    </tr>
  `).join("");
}

export function filterCardsTable() {
  const query = document.getElementById("cards-search").value.toLowerCase();
  const filtered = state.allCardsCache.filter(c => 
    (c.front && c.front.toLowerCase().includes(query)) ||
    (c.back && c.back.toLowerCase().includes(query)) ||
    (c.type && c.type.toLowerCase().includes(query))
  );
  renderCardsTable(filtered);
}

export async function deleteCardRow(cardId) {
  if (!confirm("Удалить эту карточку?")) return;
  try {
    const res = await apiFetch(`/api/cards/${cardId}`, { method: "DELETE" });
    if (checkUnauthorized(res)) return;
    if (!res.ok) {
      const data = await res.json().catch(() => ({}));
      showToast(data.error || "Ошибка при удалении карточки");
      return;
    }
    showToast("✓ Карточка удалена");
    loadCardsTable();
    loadStats();
  } catch (err) {
    console.error(err);
    showToast("Ошибка соединения при удалении");
  }
}

// ==========================================================
// 3. SETTINGS & CONFIG
// ==========================================================
export async function loadConfig() {
  try {
    const res = await apiFetch("/api/config");
    const data = await res.json();
    state.hasGeminiKey = Boolean(data.has_gemini_key);
    const banner = document.getElementById("missing-key-banner");
    if (banner) {
      if (!state.hasGeminiKey) banner.classList.remove("hidden");
      else banner.classList.add("hidden");
    }
    if (data.tts_voice) {
      document.getElementById("cfg-tts-voice").value = data.tts_voice;
    }
    updatePinBadgeUI(data.has_pin);
  } catch (err) {
    console.error(err);
  }
}

export async function saveSettings() {
  const geminiKey = document.getElementById("cfg-gemini-key").value.trim();
  const ttsVoice = document.getElementById("cfg-tts-voice").value;
  const accessPinInput = document.getElementById("cfg-access-pin");
  const accessPin = accessPinInput ? accessPinInput.value.trim() : "";
  const statusEl = document.getElementById("cfg-status");

  try {
    const payload = {
      gemini_api_key: geminiKey,
      tts_voice: ttsVoice
    };
    if (accessPinInput) {
      payload.access_pin = accessPin;
    }

    const res = await apiFetch("/api/config", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
    const data = await res.json();
    if (data.success) {
      if (accessPinInput) {
        if (accessPin) localStorage.setItem("auth_pin", accessPin);
        else localStorage.removeItem("auth_pin");
      }
      state.hasGeminiKey = Boolean(data.has_gemini_key);
      const banner = document.getElementById("missing-key-banner");
      if (banner) {
        if (state.hasGeminiKey) banner.classList.add("hidden");
        else banner.classList.remove("hidden");
      }
      updatePinBadgeUI(data.has_pin);
      statusEl.innerText = "✓ Настройки успешно сохранены!";
      statusEl.className = "text-xs text-center font-medium mt-2 text-emerald-400";
      statusEl.classList.remove("hidden");
      setTimeout(() => statusEl.classList.add("hidden"), 3000);
    } else {
      statusEl.innerText = data.error || "Ошибка сохранения";
      statusEl.className = "text-xs text-center font-medium mt-2 text-rose-400";
      statusEl.classList.remove("hidden");
    }
  } catch (err) {
    statusEl.innerText = "Ошибка сохранения: " + err.message;
    statusEl.className = "text-xs text-center font-medium mt-2 text-rose-400";
    statusEl.classList.remove("hidden");
  }
}

// ==========================================================
// 4. SCREENSHOT UPLOAD & PROCESSING
// ==========================================================
export function setupPasteListener() {
  window.addEventListener("paste", (e) => {
    const items = (e.clipboardData || e.originalEvent.clipboardData).items;
    for (let item of items) {
      if (item.type.indexOf("image") !== -1) {
        const blob = item.getAsFile();
        const reader = new FileReader();
        reader.onload = (event) => {
          showImagePreview(event.target.result, "Скриншот из буфера обмена (Ctrl+V)");
        };
        reader.readAsDataURL(blob);
        switchTab("upload");
        e.preventDefault();
        break;
      }
    }
  });

  const dropzone = document.getElementById("dropzone");
  if (!dropzone) return;

  ['dragenter', 'dragover'].forEach(eventName => {
    dropzone.addEventListener(eventName, (e) => {
      e.preventDefault();
      dropzone.classList.add("border-indigo-400", "bg-slate-900");
    });
  });

  ['dragleave', 'drop'].forEach(eventName => {
    dropzone.addEventListener(eventName, (e) => {
      e.preventDefault();
      dropzone.classList.remove("border-indigo-400", "bg-slate-900");
    });
  });

  dropzone.addEventListener("drop", (e) => {
    const dt = e.dataTransfer;
    const files = dt.files;
    if (files && files.length > 0) {
      const file = files[0];
      if (file.type.startsWith("image/")) {
        const reader = new FileReader();
        reader.onload = (event) => {
          showImagePreview(event.target.result, file.name);
        };
        reader.readAsDataURL(file);
      }
    }
  });
}

export function handleFileSelect(e) {
  const file = e.target.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = (event) => {
      showImagePreview(event.target.result, file.name);
    };
    reader.readAsDataURL(file);
  }
}

export function showImagePreview(base64Data, filename) {
  state.currentImageBase64 = base64Data;
  document.getElementById("preview-img").src = base64Data;
  document.getElementById("preview-info").innerText = filename;
  document.getElementById("dropzone-prompt").classList.add("hidden");
  document.getElementById("dropzone-preview").classList.remove("hidden");
  document.getElementById("btn-parse").disabled = false;
  document.getElementById("upload-result").classList.add("hidden");
}

export function resetUpload() {
  state.currentImageBase64 = null;
  document.getElementById("preview-img").src = "";
  document.getElementById("dropzone-prompt").classList.remove("hidden");
  document.getElementById("dropzone-preview").classList.add("hidden");
  document.getElementById("btn-parse").disabled = true;
  document.getElementById("file-input").value = "";
}

export function prepareImageBlob(dataUrl) {
  return new Promise((resolve) => {
    const img = new Image();
    img.onload = () => {
      const maxDim = 1920;
      let w = img.width;
      let h = img.height;
      if (w > maxDim || h > maxDim) {
        if (w > h) {
          h = Math.round((h * maxDim) / w);
          w = maxDim;
        } else {
          w = Math.round((w * maxDim) / h);
          h = maxDim;
        }
      }
      const canvas = document.createElement("canvas");
      canvas.width = w;
      canvas.height = h;
      const ctx = canvas.getContext("2d");
      ctx.drawImage(img, 0, 0, w, h);
      canvas.toBlob((blob) => resolve(blob), "image/jpeg", 0.85);
    };
    img.onerror = () => resolve(null);
    img.src = dataUrl;
  });
}

export async function processImage() {
  if (!state.currentImageBase64) return;

  if (!state.hasGeminiKey) {
    alert("⚠️ Сначала укажи ключ Gemini API во вкладке «Настройки ⚙️»!\n\nБесплатный ключ создаётся за 1 минуту на https://aistudio.google.com/app/apikey");
    switchTab("settings");
    return;
  }

  const btn = document.getElementById("btn-parse");
  const btnText = document.getElementById("btn-parse-text");
  const statusBox = document.getElementById("upload-status");
  const resultBox = document.getElementById("upload-result");

  btn.disabled = true;
  btnText.innerText = "Сканирую и распознаю...";
  statusBox.classList.remove("hidden");
  resultBox.classList.add("hidden");

  try {
    const imageBlob = await prepareImageBlob(state.currentImageBase64);
    let res;
    if (imageBlob) {
      const formData = new FormData();
      formData.append("file", imageBlob, "screenshot.jpg");
      res = await apiFetch("/api/upload", {
        method: "POST",
        body: formData
      });
    } else {
      res = await apiFetch("/api/upload", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ image_b64: state.currentImageBase64 })
      });
    }

    const data = await res.json();
    if (!res.ok) throw new Error(data.error || "Ошибка распознавания");

    statusBox.classList.add("hidden");
    resultBox.classList.remove("hidden");
    document.getElementById("result-summary").innerHTML = `
      Добавлено карточек: <b>${data.total_added}</b><br>
      • 🔤 Новых слов: <b>${data.counts.vocab}</b><br>
      • ❌ Исправлений: <b>${data.counts.correction}</b><br>
      • ⭐ Удачных выражений: <b>${data.counts.good_language}</b><br>
      • 💡 Синонимов: <b>${data.counts.suggestion}</b>
    `;
    resetUpload();
  } catch (err) {
    statusBox.classList.add("hidden");
    const msg = (err.message && err.message.includes("Failed to fetch"))
      ? "Сервер не отвечает. Убедись, что файл run.bat запущен!"
      : err.message;
    alert("Ошибка: " + msg);
  } finally {
    btn.disabled = false;
    btnText.innerText = "Распознать скриншот через Gemini";
  }
}

// ==========================================================
// 5. GLOBAL KEYBOARD SHORTCUTS
// ==========================================================
function setupKeyboardShortcuts() {
  document.addEventListener("keydown", (e) => {
    if (['INPUT', 'TEXTAREA', 'SELECT'].includes(document.activeElement.tagName)) {
      if (e.key === "Escape") closeQuickAddModal();
      return;
    }

    const tabPractice = !document.getElementById("tab-practice").classList.contains("hidden");
    if (!tabPractice) return;

    const isAudioKey = (
      e.code === "KeyP" || 
      e.code === "KeyR" || 
      (e.key && ["p", "P", "з", "З", "r", "R", "к", "К"].includes(e.key))
    );

    if (isAudioKey) {
      e.preventDefault();
      if (state.currentMode === 'card') playAudio();
      else if (state.currentMode === 'cloze') playClozeAudio();
      else if (state.currentMode === 'quiz') playQuizAudio();
      return;
    }

    if (state.currentMode === 'card') {
      if (e.code === "Space" || e.code === "Enter") {
        e.preventDefault();
        const isRevealed = !document.getElementById("card-back-container").classList.contains("hidden");
        if (!isRevealed) revealAnswer();
      } else if (e.code === "Digit1" || e.code === "Numpad1" || e.key === "1") {
        rateCard(1);
      } else if (e.code === "Digit2" || e.code === "Numpad2" || e.key === "2") {
        rateCard(2);
      } else if (e.code === "Digit3" || e.code === "Numpad3" || e.key === "3") {
        rateCard(3);
      }
    } else if (state.currentMode === 'cloze') {
      if (e.code === "Space") {
        const nextBtn = document.getElementById("btn-cloze-next");
        if (!nextBtn.classList.contains("hidden")) {
          e.preventDefault();
          loadNextCloze();
        }
      }
    } else if (state.currentMode === 'quiz') {
      let selectedIdx = -1;
      if (e.code === "Digit1" || e.code === "Numpad1" || e.key === "1") selectedIdx = 0;
      else if (e.code === "Digit2" || e.code === "Numpad2" || e.key === "2") selectedIdx = 1;
      else if (e.code === "Digit3" || e.code === "Numpad3" || e.key === "3") selectedIdx = 2;
      else if (e.code === "Digit4" || e.code === "Numpad4" || e.key === "4") selectedIdx = 3;

      if (selectedIdx !== -1) {
        const btns = document.querySelectorAll(".quiz-opt-btn");
        if (btns[selectedIdx] && !btns[selectedIdx].disabled) {
          btns[selectedIdx].click();
        }
      }
    }
  });
}

// ==========================================================
// 6. INITIALIZATION & EXPOSING TO WINDOW FOR HTML ONCLICK
// ==========================================================
document.addEventListener("DOMContentLoaded", () => {
  initAutoPlaySetting();
  loadStats();
  loadNextCard();
  loadConfig();
  setupPasteListener();
  setupTouchGestures({ rateCard, revealAnswer });
  setupKeyboardShortcuts();
});

// Expose functions globally for inline HTML event handlers
window.switchTab = switchTab;
window.setPracticeMode = setPracticeMode;
window.setCategory = setCategory;
window.submitPinAuth = submitPinAuth;
window.loadStats = loadStats;
window.loadNextCard = loadNextCard;
window.revealAnswer = revealAnswer;
window.rateCard = rateCard;
window.playAudio = playAudio;
window.checkClozeAnswer = checkClozeAnswer;
window.loadNextCloze = loadNextCloze;
window.revealClozeHintLetter = revealClozeHintLetter;
window.playClozeAudio = playClozeAudio;
window.loadNextQuiz = loadNextQuiz;
window.handleQuizAnswer = handleQuizAnswer;
window.playQuizAudio = playQuizAudio;
window.toggleAutoPlayQuick = toggleAutoPlayQuick;
window.setAutoPlaySetting = setAutoPlaySetting;
window.setAutoPlayDelay = setAutoPlayDelay;
window.playCardAudioDirect = playCardAudioDirect;
window.openQuickAdd = openQuickAdd;
window.closeQuickAddModal = closeQuickAddModal;
window.autoTranslateQuickAdd = autoTranslateQuickAdd;
window.submitQuickAdd = submitQuickAdd;
window.handleInteractiveWordClick = handleInteractiveWordClick;
window.resetUpload = resetUpload;
window.processImage = processImage;
window.filterCardsTable = filterCardsTable;
window.deleteCardRow = deleteCardRow;
window.saveSettings = saveSettings;
window.handleFileSelect = handleFileSelect;
