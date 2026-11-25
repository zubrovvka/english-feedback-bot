/**
 * Cloze deletion (fill-in-the-blank) training mode
 */
import { state, abortActiveModeRequest } from './state.js';
import { apiFetch, checkUnauthorized } from './api.js';
import { levenshteinDistance, escapeHtml } from './ui.js';
import { loadStats } from './srs.js';

export async function loadNextCloze() {
  abortActiveModeRequest();
  state.activeModeAbortController = new AbortController();
  const signal = state.activeModeAbortController.signal;
  const url = state.currentCategory ? `/api/cards/cloze?category=${state.currentCategory}` : `/api/cards/cloze`;
  state.clozeHintIndex = 0;
  try {
    const res = await apiFetch(url, { signal });
    if (signal.aborted || state.currentMode !== 'cloze') return;
    if (checkUnauthorized(res)) return;
    const data = await res.json();
    if (signal.aborted || state.currentMode !== 'cloze') return;

    if (!data || !data.target) {
      document.getElementById("cloze-sentence").innerText = "Нет карточек для тренировки пропусков.";
      return;
    }

    state.currentClozeCard = data;
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
    if (err.name === 'AbortError') return;
    console.error(err);
  }
}

export function checkClozeAnswer(e) {
  if (e) e.preventDefault();
  if (!state.currentClozeCard) return;

  const userVal = document.getElementById("cloze-input").value.trim().toLowerCase();
  const targetVal = state.currentClozeCard.target.toLowerCase();

  const cleanUser = userVal.replace(/['’.,!?-]/g, "").trim();
  const cleanTarget = targetVal.replace(/['’.,!?-]/g, "").trim();

  const input = document.getElementById("cloze-input");
  const feedback = document.getElementById("cloze-feedback");

  const isMatch = cleanUser === cleanTarget ||
    (cleanTarget.length >= 4 && levenshteinDistance(cleanUser, cleanTarget) <= 1);

  const safeTarget = escapeHtml(state.currentClozeCard.target);
  const safeExplanation = escapeHtml(state.currentClozeCard.explanation || '');

  if (isMatch) {
    input.className = "w-full text-center py-3 px-4 bg-emerald-950/60 border-2 border-emerald-500 text-emerald-300 rounded-xl text-lg font-bold transition";
    feedback.className = "mt-3 p-3 rounded-xl bg-emerald-950/50 border border-emerald-700/60 text-emerald-200 text-xs sm:text-sm text-left";
    feedback.innerHTML = `🎉 <b>Точно в цель!</b> Правильный ответ: <code>${safeTarget}</code>`;
    feedback.classList.remove("hidden");

    apiFetch(`/api/cards/${state.currentClozeCard.card_id}/review`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ rating: 3 })
    }).then((res) => {
      if (!checkUnauthorized(res) && res.ok) loadStats();
    });

    document.getElementById("btn-cloze-check").classList.add("hidden");
    document.getElementById("btn-cloze-next").classList.remove("hidden");
    document.getElementById("btn-cloze-hint").disabled = true;
    input.disabled = true;
  } else {
    input.className = "w-full text-center py-3 px-4 bg-rose-950/60 border-2 border-rose-500 text-rose-300 rounded-xl text-lg font-bold transition";
    feedback.className = "mt-3 p-3 rounded-xl bg-rose-950/50 border border-rose-700/60 text-rose-200 text-xs sm:text-sm text-left";
    feedback.innerHTML = `❌ Правильно: <b class="text-white text-base">${safeTarget}</b><br><span class="text-xs text-slate-300 mt-1 block">${safeExplanation}</span>`;
    feedback.classList.remove("hidden");

    apiFetch(`/api/cards/${state.currentClozeCard.card_id}/review`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ rating: 1 })
    }).then((res) => {
      if (!checkUnauthorized(res) && res.ok) loadStats();
    });

    document.getElementById("btn-cloze-check").classList.add("hidden");
    document.getElementById("btn-cloze-next").classList.remove("hidden");
    document.getElementById("btn-cloze-hint").disabled = true;
    input.disabled = true;
  }
}

export function revealClozeHintLetter() {
  if (!state.currentClozeCard) return;
  const target = state.currentClozeCard.target;
  if (state.clozeHintIndex < target.length) {
    state.clozeHintIndex++;
    const hintPrefix = target.substring(0, state.clozeHintIndex);
    document.getElementById("cloze-input").value = hintPrefix;
    document.getElementById("cloze-input").focus();
  }
}
