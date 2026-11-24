/**
 * Flashcards, Spaced Repetition (SM-2) practice, and review rating
 */
import { state, abortActiveModeRequest } from './state.js';
import { apiFetch, checkUnauthorized } from './api.js';
import { escapeHtml, renderInteractiveWords, isMostlyRussian } from './ui.js';
import { playAudio } from './tts.js';

export async function loadStats() {
  try {
    const res = await apiFetch("/api/stats");
    if (checkUnauthorized(res)) return;
    const data = await res.json();
    document.getElementById("stat-due").innerText = data.due || 0;
    document.getElementById("stat-total").innerText = data.total || 0;
  } catch (err) {
    console.error(err);
  }
}

export async function loadNextCard() {
  abortActiveModeRequest();
  state.activeModeAbortController = new AbortController();
  const signal = state.activeModeAbortController.signal;
  const url = state.currentCategory ? `/api/cards/next?category=${state.currentCategory}` : `/api/cards/next`;
  try {
    const res = await apiFetch(url, { signal });
    if (signal.aborted || state.currentMode !== 'card') return;
    if (checkUnauthorized(res)) return;
    const data = await res.json();
    if (signal.aborted || state.currentMode !== 'card') return;

    if (!data.card) {
      document.getElementById("card-box").classList.add("hidden");
      document.getElementById("empty-state").classList.remove("hidden");
      state.currentCard = null;
      return;
    }

    document.getElementById("card-box").classList.remove("hidden");
    document.getElementById("empty-state").classList.add("hidden");

    state.currentCard = data.card;
    renderCard(state.currentCard, data.is_extra);
  } catch (err) {
    if (err.name === 'AbortError') return;
    console.error(err);
  }
}

export function renderCard(card, isExtra) {
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
    const ew1 = escapeHtml(w1);
    const ew2 = escapeHtml(w2);

    frontEl.innerHTML = `
      <div class="flex items-center justify-center space-x-2 text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
        <span class="interactive-word" data-word="${ew1}" onclick="handleInteractiveWordClick(this)">${ew1}</span>
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
        <span class="interactive-word text-slate-300" data-word="${ew1}" onclick="handleInteractiveWordClick(this)">${ew1}</span>
        <span class="text-purple-400 font-bold mx-2 select-none">↔</span>
        <span class="interactive-word text-emerald-400 underline decoration-purple-500 underline-offset-4" data-word="${ew2}" onclick="handleInteractiveWordClick(this)">${ew2}</span>
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

  if (state.autoPlayAudio) {
    // Не озвучивать автоматически при открытии, если вопрос на русском языке (например, разбор ошибок)
    const isRussianQuestion = card.type === 'correction' || isMostlyRussian(card.front);
    if (!isRussianQuestion) {
      if (state.autoPlayDelay > 0) {
        setTimeout(() => playAudio(true), state.autoPlayDelay);
      } else {
        playAudio(true);
      }
    }
  }
}

export function revealAnswer() {
  if (!state.currentCard) return;
  document.getElementById("card-back-container").classList.remove("hidden");
  document.getElementById("actions-unrevealed").classList.add("hidden");
  document.getElementById("actions-revealed").classList.remove("hidden");

  // Для карточек с русским вопросом (например, разбор ошибок) — после открытия ответа озвучиваем английский ответ!
  if (state.autoPlayAudio) {
    const isRussianQuestion = state.currentCard.type === 'correction' || isMostlyRussian(state.currentCard.front);
    if (isRussianQuestion && state.currentCard.back && !isMostlyRussian(state.currentCard.back)) {
      if (state.autoPlayDelay > 0) {
        setTimeout(() => playAudio(false), state.autoPlayDelay);
      } else {
        playAudio(false);
      }
    }
  }

  // For antonym cards, pronounce the revealed answer word!
  if (state.autoPlayAudio && (state.currentCard.type === 'antonym' || state.currentCard.front.includes('↔') || state.currentCard.front.includes('<->'))) {
    const delim = state.currentCard.front.includes('↔') ? '↔' : '<->';
    const parts = state.currentCard.front.split(delim).map(s => s.trim());
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

export async function rateCard(rating) {
  if (!state.currentCard) return;
  try {
    await apiFetch(`/api/cards/${state.currentCard.id}/review`, {
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
