/**
 * English Feedback & Active Recall Trainer - Client Application
 */

// ==========================================================
// 1. STATE & INITIALIZATION
// ==========================================================
let currentMode = 'card'; // 'card' | 'cloze' | 'quiz'
let currentCategory = null;
let currentCard = null;
let currentClozeCard = null;
let currentQuizData = null;
let quizStreak = 0;
let currentImageBase64 = null;
let allCardsCache = [];
let hasGeminiKey = false;
let clozeHintIndex = 0;
let autoPlayAudio = true;
let autoPlayDelay = 0;

document.addEventListener("DOMContentLoaded", () => {
  initAutoPlaySetting();
  loadStats();
  loadNextCard();
  loadConfig();
  setupPasteListener();
  setupTouchGestures();
});

// ==========================================================
// 2. NAVIGATION & MOBILE GESTURES
// ==========================================================
function switchTab(tabId) {
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
    if (currentMode === 'card' && !currentCard) loadNextCard();
    else if (currentMode === 'cloze' && !currentClozeCard) loadNextCloze();
    else if (currentMode === 'quiz' && !currentQuizData) loadNextQuiz();
  } else if (tabId === 'cards') {
    loadCardsTable();
  } else if (tabId === 'settings') {
    updateAutoPlayUI();
  }
}

// Touch & Swipe gestures for Mobile
let touchStartX = 0;
let touchStartY = 0;
let touchEndX = 0;
let touchEndY = 0;

function setupTouchGestures() {
  const cardBox = document.getElementById("card-box");
  if (!cardBox) return;

  cardBox.addEventListener("touchstart", (e) => {
    touchStartX = e.changedTouches[0].screenX;
    touchStartY = e.changedTouches[0].screenY;
  }, { passive: true });

  cardBox.addEventListener("touchend", (e) => {
    touchEndX = e.changedTouches[0].screenX;
    touchEndY = e.changedTouches[0].screenY;
    handleCardSwipe();
  }, { passive: true });
}

function handleCardSwipe() {
  const dx = touchEndX - touchStartX;
  const dy = touchEndY - touchStartY;
  
  if (Math.abs(dy) > Math.abs(dx) && Math.abs(dy) > 35) return;
  
  const unrevealed = document.getElementById("actions-unrevealed");
  const isUnrevealed = unrevealed && !unrevealed.classList.contains("hidden");

  if (Math.abs(dx) > 60) {
    if (dx > 0) {
      if (currentCard) rateCard(3); // Swipe Right -> Easy
    } else {
      if (currentCard) rateCard(1); // Swipe Left -> Forgot
    }
  } else if (Math.abs(dx) < 15 && Math.abs(dy) < 15) {
    if (isUnrevealed) revealAnswer(); // Tap to flip
  }
}

function setPracticeMode(mode) {
  currentMode = mode;
  
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
    if (!currentCard) loadNextCard();
  } else if (mode === 'cloze') {
    loadNextCloze();
  } else if (mode === 'quiz') {
    loadNextQuiz();
  }
}

function setCategory(cat) {
  currentCategory = cat;
  document.querySelectorAll(".cat-pill").forEach(pill => {
    const pCat = pill.getAttribute("data-cat");
    if ((!cat && pCat === 'all') || pCat === cat) {
      pill.className = "cat-pill active px-3 py-1 rounded-full text-xs font-medium border border-indigo-500 bg-indigo-500/20 text-indigo-300";
    } else {
      pill.className = "cat-pill px-3 py-1 rounded-full text-xs font-medium border border-slate-700 bg-slate-900 text-slate-400 hover:border-slate-500";
    }
  });

  if (currentMode === 'card') loadNextCard();
  else if (currentMode === 'cloze') loadNextCloze();
  else if (currentMode === 'quiz') loadNextQuiz();
}

async function loadStats() {
  try {
    const res = await fetch("/api/stats");
    const data = await res.json();
    document.getElementById("stat-due").innerText = data.due || 0;
    document.getElementById("stat-total").innerText = data.total || 0;
  } catch (err) {
    console.error(err);
  }
}

function escapeHtml(str) {
  if (!str) return '';
  return String(str).replace(/[&<>"']/g, m => ({
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#39;'
  }[m]));
}

function renderInteractiveWords(text, contextSentence) {
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

function handleInteractiveWordClick(el) {
  const word = el.getAttribute("data-word");
  const sentence = el.getAttribute("data-sentence");
  openQuickAdd(word, sentence);
}

// ==========================================================
// 3. PRACTICE MODE 1: FLASHCARDS & SRS
// ==========================================================
async function loadNextCard(force = false) {
  const url = currentCategory ? `/api/cards/next?category=${currentCategory}` : `/api/cards/next`;
  try {
    const res = await fetch(url);
    const data = await res.json();

    if (!data.card) {
      document.getElementById("card-box").classList.add("hidden");
      document.getElementById("empty-state").classList.remove("hidden");
      currentCard = null;
      return;
    }

    document.getElementById("card-box").classList.remove("hidden");
    document.getElementById("empty-state").classList.add("hidden");

    currentCard = data.card;
    renderCard(currentCard, data.is_extra);
  } catch (err) {
    console.error(err);
  }
}

function renderCard(card, isExtra) {
  const badgeMap = {
    'vocab': { text: '🔤 Слово из урока', color: 'bg-indigo-900/60 text-indigo-300 border-indigo-700/50' },
    'correction': { text: '❌ Разбор ошибки', color: 'bg-rose-900/60 text-rose-300 border-rose-700/50' },
    'good_language': { text: '⭐ Закрепление лексики', color: 'bg-amber-900/60 text-amber-300 border-amber-700/50' },
    'suggestion': { text: '💡 Level Up / Синоним', color: 'bg-cyan-900/60 text-cyan-300 border-cyan-700/50' },
    'antonym': { text: '⚡ Назови антоним', color: 'bg-purple-900/60 text-purple-300 border-purple-700/50' }
  };

  const b = badgeMap[card.type] || { text: card.type, color: 'bg-slate-800 text-slate-300' };
  const badgeEl = document.getElementById("card-badge");
  badgeEl.innerText = b.text;
  badgeEl.className = `px-2.5 py-0.5 rounded text-xs font-semibold tracking-wider border ${b.color}`;

  const extraEl = document.getElementById("extra-indicator");
  if (isExtra) extraEl.classList.remove("hidden");
  else extraEl.classList.add("hidden");

  const frontEl = document.getElementById("card-front");
  const transEl = document.getElementById("card-transcription");
  const promptEl = document.getElementById("card-prompt");
  const backEl = document.getElementById("card-back");

  const isAntonym = card.type === 'antonym' || card.front.includes('↔') || card.front.includes('<->');

  if (isAntonym) {
    const delim = card.front.includes('↔') ? '↔' : '<->';
    const parts = card.front.split(delim).map(s => s.trim());
    const w1 = parts[0] || card.front;
    const w2 = parts[1] || '';

    frontEl.innerHTML = `
      <div class="flex items-center justify-center space-x-2 text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
        <span class="interactive-word" data-word="${w1}" onclick="handleInteractiveWordClick(this)">${w1}</span>
        <span class="text-purple-400 font-bold mx-2 select-none">↔</span>
        <span class="px-3 py-1 bg-purple-950/80 border-2 border-dashed border-purple-500/70 rounded-xl text-purple-300 font-mono text-xl sm:text-2xl font-bold tracking-widest shadow-inner">? ? ?</span>
      </div>
    `;

    if (card.transcription) {
      const tParts = card.transcription.split(delim);
      transEl.innerText = tParts[0].trim() + " ↔ ...";
      transEl.classList.remove("hidden");
    } else {
      transEl.classList.add("hidden");
    }

    badgeEl.innerText = "⚡ Назови антоним";
    badgeEl.className = "px-2.5 py-0.5 rounded text-xs font-semibold tracking-wider border bg-purple-900/60 text-purple-300 border-purple-700/50";
    promptEl.innerText = "Вспомни противоположное слово (антоним) и нажми «Показать ответ»";

    backEl.innerHTML = `
      <div class="text-xl sm:text-2xl font-extrabold text-white">
        <span class="interactive-word text-slate-300" data-word="${w1}" onclick="handleInteractiveWordClick(this)">${w1}</span>
        <span class="text-purple-400 font-bold mx-2 select-none">↔</span>
        <span class="interactive-word text-emerald-400 underline decoration-purple-500 underline-offset-4" data-word="${w2}" onclick="handleInteractiveWordClick(this)">${w2}</span>
      </div>
    `;
  } else {
    if (/[a-zA-Z]{2,}/.test(card.front)) {
      frontEl.innerHTML = renderInteractiveWords(card.front, card.front);
    } else {
      frontEl.innerText = card.front;
    }
    if (card.transcription) {
      transEl.innerText = card.transcription;
      transEl.classList.remove("hidden");
    } else {
      transEl.classList.add("hidden");
    }

    if (card.type === 'correction') promptEl.innerText = "Подумай, как сказать правильно, и нажми «Показать ответ»";
    else if (card.type === 'good_language') promptEl.innerText = "Вспомни точную фразу с урока и нажми «Показать ответ»";
    else if (card.type === 'suggestion') promptEl.innerText = "Вспомни продвинутый синоним и нажми «Показать ответ»";
    else promptEl.innerText = "Вспомни перевод и нажми «Показать ответ»";

    if (/[a-zA-Z]{2,}/.test(card.back)) {
      backEl.innerHTML = renderInteractiveWords(card.back, card.back);
    } else {
      backEl.innerText = card.back;
    }
  }

  // Full Russian translation of sentence / phrase
  const transBox = document.getElementById("card-translation-box");
  const transTextEl = document.getElementById("card-translation");
  if (card.translation && card.translation.trim()) {
    transTextEl.innerText = card.translation.trim();
    transBox.classList.remove("hidden");
  } else {
    transBox.classList.add("hidden");
  }

  const expBox = document.getElementById("card-explanation-box");
  const expEl = document.getElementById("card-explanation");
  if (card.explanation) {
    expEl.innerText = card.explanation;
    expBox.classList.remove("hidden");
  } else {
    expBox.classList.add("hidden");
  }

  const exBox = document.getElementById("card-example-box");
  const exEl = document.getElementById("card-example");
  if (card.example) {
    exEl.innerHTML = renderInteractiveWords(card.example, card.example);
    exBox.classList.remove("hidden");
  } else {
    exBox.classList.add("hidden");
  }

  document.getElementById("card-back-container").classList.add("hidden");
  document.getElementById("actions-unrevealed").classList.remove("hidden");
  document.getElementById("actions-revealed").classList.add("hidden");

  if (autoPlayAudio) {
    if (autoPlayDelay > 0) {
      setTimeout(() => playAudio(true), autoPlayDelay);
    } else {
      playAudio(true);
    }
  }
}

function revealAnswer() {
  if (!currentCard) return;
  document.getElementById("card-back-container").classList.remove("hidden");
  document.getElementById("actions-unrevealed").classList.add("hidden");
  document.getElementById("actions-revealed").classList.remove("hidden");

  // For antonym cards, pronounce the revealed answer word!
  if (autoPlayAudio && (currentCard.type === 'antonym' || currentCard.front.includes('↔') || currentCard.front.includes('<->'))) {
    const delim = currentCard.front.includes('↔') ? '↔' : '<->';
    const parts = currentCard.front.split(delim).map(s => s.trim());
    if (parts.length >= 2 && parts[1]) {
      if ('speechSynthesis' in window) {
        try {
          window.speechSynthesis.cancel();
          const u = new SpeechSynthesisUtterance(parts[1]);
          u.lang = 'en-US';
          window.speechSynthesis.speak(u);
        } catch (e) {}
      }
    }
  }
}

async function rateCard(rating) {
  if (!currentCard) return;
  try {
    await fetch(`/api/cards/${currentCard.id}/review`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ rating: rating })
    });
    loadStats();
    loadNextCard();
  } catch (err) {
    console.error(err);
  }
}

// ==========================================================
// 4. PRACTICE MODE 2: CLOZE DELETION (ВСТАВЬ ПРОПУСК)
// ==========================================================
async function loadNextCloze() {
  const url = currentCategory ? `/api/cards/cloze?category=${currentCategory}` : `/api/cards/cloze`;
  clozeHintIndex = 0;
  try {
    const res = await fetch(url);
    const data = await res.json();
    if (!data || !data.target) {
      document.getElementById("cloze-sentence").innerText = "Нет карточек для тренировки пропусков.";
      return;
    }

    currentClozeCard = data;
    document.getElementById("cloze-sentence").innerText = data.masked_sentence;
    document.getElementById("cloze-hint").innerText = data.hint || "Вспомни правильное слово";

    const input = document.getElementById("cloze-input");
    input.value = "";
    input.className = "w-full text-center py-3 px-4 bg-slate-950 border-2 border-indigo-500/60 focus:border-indigo-400 rounded-xl text-lg font-bold text-white focus:outline-none focus:ring-2 focus:ring-indigo-500/30 transition shadow-inner";
    input.disabled = false;
    setTimeout(() => input.focus(), 50);

    document.getElementById("cloze-feedback").classList.add("hidden");
    document.getElementById("btn-cloze-check").classList.remove("hidden");
    document.getElementById("btn-cloze-next").classList.add("hidden");
    document.getElementById("btn-cloze-hint").disabled = false;
  } catch (err) {
    console.error(err);
  }
}

function checkClozeAnswer(e) {
  if (e) e.preventDefault();
  if (!currentClozeCard) return;

  const userVal = document.getElementById("cloze-input").value.trim().toLowerCase();
  const targetVal = currentClozeCard.target.toLowerCase();

  const cleanUser = userVal.replace(/['’.,!?-]/g, "").trim();
  const cleanTarget = targetVal.replace(/['’.,!?-]/g, "").trim();

  const input = document.getElementById("cloze-input");
  const feedback = document.getElementById("cloze-feedback");

  if (cleanUser === cleanTarget || (cleanTarget.includes(cleanUser) && cleanUser.length >= 4)) {
    input.className = "w-full text-center py-3 px-4 bg-emerald-950/60 border-2 border-emerald-500 text-emerald-300 rounded-xl text-lg font-bold transition";
    feedback.className = "mt-3 p-3 rounded-xl bg-emerald-950/50 border border-emerald-700/60 text-emerald-200 text-xs sm:text-sm text-left";
    feedback.innerHTML = `🎉 <b>Точно в цель!</b> Правильный ответ: <code>${currentClozeCard.target}</code>`;
    feedback.classList.remove("hidden");

    fetch(`/api/cards/${currentClozeCard.card_id}/review`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ rating: 3 })
    }).then(() => loadStats());

    document.getElementById("btn-cloze-check").classList.add("hidden");
    document.getElementById("btn-cloze-next").classList.remove("hidden");
    input.disabled = true;
  } else {
    input.className = "w-full text-center py-3 px-4 bg-rose-950/60 border-2 border-rose-500 text-rose-300 rounded-xl text-lg font-bold transition";
    feedback.className = "mt-3 p-3 rounded-xl bg-rose-950/50 border border-rose-700/60 text-rose-200 text-xs sm:text-sm text-left";
    feedback.innerHTML = `❌ Правильно: <b class="text-white text-base">${currentClozeCard.target}</b><br><span class="text-xs text-slate-300 mt-1 block">${currentClozeCard.explanation || ''}</span>`;
    feedback.classList.remove("hidden");

    fetch(`/api/cards/${currentClozeCard.card_id}/review`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ rating: 1 })
    }).then(() => loadStats());

    document.getElementById("btn-cloze-check").classList.add("hidden");
    document.getElementById("btn-cloze-next").classList.remove("hidden");
  }
}

function revealClozeHintLetter() {
  if (!currentClozeCard) return;
  const target = currentClozeCard.target;
  if (clozeHintIndex < target.length) {
    clozeHintIndex++;
    const hintPrefix = target.substring(0, clozeHintIndex);
    document.getElementById("cloze-input").value = hintPrefix;
    document.getElementById("cloze-input").focus();
  }
}

// ==========================================================
// 5. PRACTICE MODE 3: QUIZ 4 CHOICES (ЭКСПРЕСС-КВИЗ)
// ==========================================================
async function loadNextQuiz() {
  const url = currentCategory ? `/api/cards/quiz?category=${currentCategory}` : `/api/cards/quiz`;
  try {
    const res = await fetch(url);
    const data = await res.json();
    if (data.error || !data.options) {
      document.getElementById("quiz-question").innerText = "Недостаточно карточек для квиза.";
      return;
    }

    currentQuizData = data;
    document.getElementById("quiz-question").innerText = data.question;
    const transEl = document.getElementById("quiz-transcription");
    if (data.transcription) {
      transEl.innerText = data.transcription;
      transEl.classList.remove("hidden");
    } else {
      transEl.classList.add("hidden");
    }

    document.getElementById("quiz-feedback-box").classList.add("hidden");

    const container = document.getElementById("quiz-options-container");
    container.innerHTML = data.options.map((opt, idx) => `
      <button onclick="handleQuizAnswer('${opt.replace(/'/g, "\\'")}', this)" class="quiz-opt-btn p-3 bg-slate-950 hover:bg-slate-800 border border-slate-800 hover:border-indigo-500/60 rounded-xl text-left text-xs sm:text-sm font-medium text-slate-200 transition flex items-center space-x-2 group">
        <span class="w-6 h-6 rounded-lg bg-slate-800 group-hover:bg-indigo-600 group-hover:text-white flex items-center justify-center font-mono text-xs text-slate-400 font-bold transition">${idx + 1}</span>
        <span class="flex-1">${opt}</span>
      </button>
    `).join("");

    if (autoPlayAudio) {
      if (autoPlayDelay > 0) {
        setTimeout(() => playQuizAudio(true), autoPlayDelay);
      } else {
        playQuizAudio(true);
      }
    }

  } catch (err) {
    console.error(err);
  }
}

function handleQuizAnswer(selected, btnEl) {
  if (!currentQuizData) return;
  const correct = currentQuizData.correct_answer;
  const allBtns = document.querySelectorAll(".quiz-opt-btn");
  allBtns.forEach(b => b.disabled = true);

  const fBox = document.getElementById("quiz-feedback-box");
  const fText = document.getElementById("quiz-feedback-text");
  const fEx = document.getElementById("quiz-feedback-example");

  if (selected === correct) {
    btnEl.className = "quiz-opt-btn p-3 bg-emerald-950/70 border-2 border-emerald-500 rounded-xl text-left text-xs sm:text-sm font-bold text-emerald-200 flex items-center space-x-2";
    quizStreak++;
    fText.innerHTML = "🎉 <span class='text-emerald-400'>Отлично! Правильный ответ!</span>";
  } else {
    btnEl.className = "quiz-opt-btn p-3 bg-rose-950/70 border-2 border-rose-500 rounded-xl text-left text-xs sm:text-sm font-bold text-rose-200 flex items-center space-x-2";
    quizStreak = 0;
    allBtns.forEach(b => {
      if (b.innerText.includes(correct)) {
        b.className = "quiz-opt-btn p-3 bg-emerald-950/70 border-2 border-emerald-500 rounded-xl text-left text-xs sm:text-sm font-bold text-emerald-200 flex items-center space-x-2";
      }
    });
    fText.innerHTML = `❌ Правильный ответ: <span class='text-emerald-400'>${correct}</span>`;
  }

  document.getElementById("quiz-streak-display").innerText = `${quizStreak} подряд`;
  document.getElementById("stat-streak").innerText = quizStreak;

  if (currentQuizData.example) {
    fEx.innerHTML = `Пример: ${renderInteractiveWords(currentQuizData.example)}`;
  } else {
    fEx.innerHTML = currentQuizData.explanation || '';
  }
  fBox.classList.remove("hidden");

  setTimeout(() => {
    loadNextQuiz();
  }, 1400);
}

// ==========================================================
// 6. AUDIO & SPEECH (TTS + NATIVE SPEECH SYNTHESIS FALLBACK)
// ==========================================================
function initAutoPlaySetting() {
  const stored = localStorage.getItem("autoplay_audio");
  autoPlayAudio = stored === null ? true : stored === "true";

  const storedDelay = localStorage.getItem("autoplay_delay");
  autoPlayDelay = storedDelay !== null ? parseInt(storedDelay, 10) : 0;

  updateAutoPlayUI();
}

function updateAutoPlayUI() {
  const toggleCheckbox = document.getElementById("cfg-autoplay-audio");
  if (toggleCheckbox) toggleCheckbox.checked = autoPlayAudio;

  const delaySelect = document.getElementById("cfg-autoplay-delay");
  if (delaySelect) delaySelect.value = autoPlayDelay.toString();

  const quickBtn = document.getElementById("btn-quick-autoplay");
  const quickIcon = document.getElementById("quick-autoplay-icon");
  const quickText = document.getElementById("quick-autoplay-text");

  if (quickBtn && quickIcon && quickText) {
    if (autoPlayAudio) {
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

function setAutoPlaySetting(enabled) {
  autoPlayAudio = Boolean(enabled);
  localStorage.setItem("autoplay_audio", autoPlayAudio ? "true" : "false");
  updateAutoPlayUI();
}

function setAutoPlayDelay(delayVal) {
  autoPlayDelay = parseInt(delayVal, 10) || 0;
  localStorage.setItem("autoplay_delay", autoPlayDelay.toString());
}

function toggleAutoPlayQuick() {
  setAutoPlaySetting(!autoPlayAudio);
  showToast(autoPlayAudio ? "🔊 Авто-озвучка включена" : "🔇 Авто-озвучка выключена");
}

function playAudio(isAuto = false) {
  if (!currentCard) return;
  const btn = document.getElementById("btn-audio");
  if (btn) {
    btn.classList.add("ring-2", "ring-indigo-400", "scale-105");
    setTimeout(() => btn.classList.remove("ring-2", "ring-indigo-400", "scale-105"), 300);
  }
  const player = document.getElementById("audio-player");
  player.src = `/api/tts/${currentCard.id}`;
  player.currentTime = 0;
  player.play().catch(e => {
    if ('speechSynthesis' in window) {
      try {
        window.speechSynthesis.cancel();
        const u = new SpeechSynthesisUtterance(currentCard.front);
        u.lang = 'en-US';
        window.speechSynthesis.speak(u);
      } catch (err) {}
    }
  });
}

function playClozeAudio() {
  if (!currentClozeCard) return;
  const player = document.getElementById("audio-player");
  player.src = `/api/tts/${currentClozeCard.card_id}`;
  player.currentTime = 0;
  player.play().catch(e => {
    if ('speechSynthesis' in window) {
      try {
        window.speechSynthesis.cancel();
        const u = new SpeechSynthesisUtterance(currentClozeCard.target);
        u.lang = 'en-US';
        window.speechSynthesis.speak(u);
      } catch (err) {}
    }
  });
}

function playQuizAudio(isAuto = false) {
  if (!currentQuizData || !currentQuizData.card_id) return;
  const player = document.getElementById("audio-player");
  player.src = `/api/tts/${currentQuizData.card_id}`;
  player.currentTime = 0;
  player.play().catch(e => {
    if ('speechSynthesis' in window) {
      try {
        window.speechSynthesis.cancel();
        const u = new SpeechSynthesisUtterance(currentQuizData.question);
        u.lang = 'en-US';
        window.speechSynthesis.speak(u);
      } catch (err) {}
    }
  });
}

function playCardAudioDirect(cardId) {
  const card = allCardsCache.find(c => c.id === cardId);
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

// ==========================================================
// 7. QUICK-ADD WORD (IN-CONTEXT MODAL)
// ==========================================================
function openQuickAdd(word, sentence) {
  const clean = word.replace(/^[^\w]+|[^\w]+$/g, "").trim();
  document.getElementById("qa-word").value = clean;
  document.getElementById("qa-example").value = sentence || '';
  document.getElementById("qa-translation").value = '';
  document.getElementById("modal-quick-add").classList.remove("hidden");

  // Always auto-translate clicked word immediately
  autoTranslateQuickAdd();
}

function closeQuickAddModal() {
  document.getElementById("modal-quick-add").classList.add("hidden");
}

async function autoTranslateQuickAdd() {
  const word = document.getElementById("qa-word").value.trim();
  const sentence = document.getElementById("qa-example").value.trim();
  if (!word) return;

  const aiBtn = document.getElementById("qa-btn-ai");
  aiBtn.innerText = "⏳...";
  try {
    const res = await fetch("/api/translate", {
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

async function submitQuickAdd() {
  const word = document.getElementById("qa-word").value.trim();
  const translation = document.getElementById("qa-translation").value.trim();
  const example = document.getElementById("qa-example").value.trim();

  if (!word) {
    alert("Укажи слово");
    return;
  }

  try {
    const res = await fetch("/api/cards/quick-add", {
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
      loadStats();
    }
  } catch (err) {
    alert("Ошибка при добавлении: " + err.message);
  }
}

function showToast(msg) {
  const toast = document.getElementById("toast-notify");
  document.getElementById("toast-text").innerText = msg;
  toast.classList.remove("hidden");
  setTimeout(() => {
    toast.classList.add("hidden");
  }, 3000);
}

// ==========================================================
// 8. GLOBAL KEYBOARD SHORTCUTS
// ==========================================================
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
    if (currentMode === 'card') playAudio();
    else if (currentMode === 'cloze') playClozeAudio();
    else if (currentMode === 'quiz') playQuizAudio();
    return;
  }

  if (currentMode === 'card') {
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
  } else if (currentMode === 'cloze') {
    if (e.code === "Space") {
      const nextBtn = document.getElementById("btn-cloze-next");
      if (!nextBtn.classList.contains("hidden")) {
        e.preventDefault();
        loadNextCloze();
      }
    }
  } else if (currentMode === 'quiz') {
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

// ==========================================================
// 9. UPLOAD SCREENSHOT LOGIC (CTRL+V & DRAG-N-DROP)
// ==========================================================
function setupPasteListener() {
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

function handleFileSelect(e) {
  const file = e.target.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = (event) => {
      showImagePreview(event.target.result, file.name);
    };
    reader.readAsDataURL(file);
  }
}

function showImagePreview(base64Data, filename) {
  currentImageBase64 = base64Data;
  document.getElementById("preview-img").src = base64Data;
  document.getElementById("preview-info").innerText = filename;
  document.getElementById("dropzone-prompt").classList.add("hidden");
  document.getElementById("dropzone-preview").classList.remove("hidden");
  document.getElementById("btn-parse").disabled = false;
  document.getElementById("upload-result").classList.add("hidden");
}

function resetUpload() {
  currentImageBase64 = null;
  document.getElementById("preview-img").src = "";
  document.getElementById("dropzone-prompt").classList.remove("hidden");
  document.getElementById("dropzone-preview").classList.add("hidden");
  document.getElementById("btn-parse").disabled = true;
  document.getElementById("file-input").value = "";
}

function prepareImageBlob(dataUrl) {
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

async function processImage() {
  if (!currentImageBase64) return;

  if (!hasGeminiKey) {
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
    const imageBlob = await prepareImageBlob(currentImageBase64);
    let res;
    if (imageBlob) {
      const formData = new FormData();
      formData.append("file", imageBlob, "screenshot.jpg");
      res = await fetch("/api/upload", {
        method: "POST",
        body: formData
      });
    } else {
      res = await fetch("/api/upload", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ image_b64: currentImageBase64 })
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
      ? "Сервер не отвечает. Убедись, что файл run_web.bat запущен!"
      : err.message;
    alert("Ошибка: " + msg);
  } finally {
    btn.disabled = false;
    btnText.innerText = "Распознать скриншот через Gemini";
  }
}

// ==========================================================
// 10. CARDS LIBRARY TABLE
// ==========================================================
async function loadCardsTable() {
  try {
    const res = await fetch("/api/cards");
    const data = await res.json();
    allCardsCache = data.cards || [];
    renderCardsTable(allCardsCache);
  } catch (err) {
    console.error(err);
  }
}

function renderCardsTable(cards) {
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

function filterCardsTable() {
  const query = document.getElementById("cards-search").value.toLowerCase();
  const filtered = allCardsCache.filter(c => 
    (c.front && c.front.toLowerCase().includes(query)) ||
    (c.back && c.back.toLowerCase().includes(query)) ||
    (c.type && c.type.toLowerCase().includes(query))
  );
  renderCardsTable(filtered);
}

async function deleteCardRow(cardId) {
  if (!confirm("Удалить эту карточку?")) return;
  try {
    await fetch(`/api/cards/${cardId}`, { method: "DELETE" });
    loadCardsTable();
    loadStats();
  } catch (err) {
    console.error(err);
  }
}

// ==========================================================
// 11. SETTINGS & CONFIG
// ==========================================================
async function loadConfig() {
  try {
    const res = await fetch("/api/config");
    const data = await res.json();
    hasGeminiKey = Boolean(data.has_gemini_key);
    const banner = document.getElementById("missing-key-banner");
    if (banner) {
      if (!hasGeminiKey) banner.classList.remove("hidden");
      else banner.classList.add("hidden");
    }
    if (data.tts_voice) {
      document.getElementById("cfg-tts-voice").value = data.tts_voice;
    }
    const pinBadge = document.getElementById("cfg-pin-status-badge");
    if (pinBadge) {
      if (data.has_pin) {
        pinBadge.innerText = "🔒 PIN активен";
        pinBadge.className = "text-[10px] px-2 py-0.5 rounded font-bold bg-emerald-900/60 text-emerald-300 border border-emerald-700/50";
      } else {
        pinBadge.innerText = "⚠️ Открыт";
        pinBadge.className = "text-[10px] px-2 py-0.5 rounded font-bold bg-amber-900/60 text-amber-300 border border-amber-700/50";
      }
    }
  } catch (err) {
    console.error(err);
  }
}

async function saveSettings() {
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

    const res = await fetch("/api/config", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
    const data = await res.json();
    if (data.success) {
      hasGeminiKey = Boolean(data.has_gemini_key);
      const banner = document.getElementById("missing-key-banner");
      if (banner) {
        if (hasGeminiKey) banner.classList.add("hidden");
        else banner.classList.remove("hidden");
      }
      const pinBadge = document.getElementById("cfg-pin-status-badge");
      if (pinBadge) {
        if (data.has_pin) {
          pinBadge.innerText = "🔒 PIN активен";
          pinBadge.className = "text-[10px] px-2 py-0.5 rounded font-bold bg-emerald-900/60 text-emerald-300 border border-emerald-700/50";
        } else {
          pinBadge.innerText = "⚠️ Открыт";
          pinBadge.className = "text-[10px] px-2 py-0.5 rounded font-bold bg-amber-900/60 text-amber-300 border border-amber-700/50";
        }
      }
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
