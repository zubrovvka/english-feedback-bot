/**
 * Express 4-choice quiz practice mode
 */
import { state, abortActiveModeRequest } from './state.js';
import { apiFetch, checkUnauthorized } from './api.js';
import { renderInteractiveWords, isMostlyRussian, escapeHtml } from './ui.js';
import { playQuizAudio } from './tts.js';

export async function loadNextQuiz() {
  abortActiveModeRequest();
  state.activeModeAbortController = new AbortController();
  const signal = state.activeModeAbortController.signal;
  const url = state.currentCategory ? `/api/cards/quiz?category=${state.currentCategory}` : `/api/cards/quiz`;
  try {
    const res = await apiFetch(url, { signal });
    if (signal.aborted || state.currentMode !== 'quiz') return;
    if (checkUnauthorized(res)) return;
    const data = await res.json();
    if (signal.aborted || state.currentMode !== 'quiz') return;

    if (data.error || !data.options) {
      document.getElementById("quiz-question").innerText = "Недостаточно карточек для квиза.";
      return;
    }

    state.currentQuizData = data;
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
      <button data-idx="${idx}" onclick="handleQuizAnswer(${idx}, this)" class="quiz-opt-btn p-3 bg-slate-950 hover:bg-slate-800 border border-slate-800 hover:border-indigo-500/60 rounded-xl text-left text-xs sm:text-sm font-medium text-slate-200 transition flex items-center space-x-2 group">
        <span class="w-6 h-6 rounded-lg bg-slate-800 group-hover:bg-indigo-600 group-hover:text-white flex items-center justify-center font-mono text-xs text-slate-400 font-bold transition">${idx + 1}</span>
        <span class="flex-1">${escapeHtml(opt)}</span>
      </button>
    `).join("");

    if (state.autoPlayAudio) {
      // Не озвучивать автоматически русский вопрос квиза
      const isRussianQuestion = isMostlyRussian(data.question);
      if (!isRussianQuestion) {
        if (state.autoPlayDelay > 0) {
          state.autoPlayTimer = setTimeout(() => playQuizAudio(true), state.autoPlayDelay);
        } else {
          playQuizAudio(true);
        }
      }
    }

  } catch (err) {
    if (err.name === 'AbortError') return;
    console.error(err);
  }
}

export function handleQuizAnswer(selectedOrIdx, btnEl) {
  if (!state.currentQuizData) return;
  const options = state.currentQuizData.options || [];
  const selected = typeof selectedOrIdx === 'number' ? options[selectedOrIdx] : selectedOrIdx;
  const correct = state.currentQuizData.correct_answer;
  const allBtns = document.querySelectorAll(".quiz-opt-btn");
  allBtns.forEach(b => b.disabled = true);

  const fBox = document.getElementById("quiz-feedback-box");
  const fText = document.getElementById("quiz-feedback-text");
  const fEx = document.getElementById("quiz-feedback-example");

  if (selected === correct) {
    btnEl.className = "quiz-opt-btn p-3 bg-emerald-950/70 border-2 border-emerald-500 rounded-xl text-left text-xs sm:text-sm font-bold text-emerald-200 flex items-center space-x-2";
    state.quizStreak++;
    fText.innerHTML = "🎉 <span class='text-emerald-400'>Отлично! Правильный ответ!</span>";
  } else {
    btnEl.className = "quiz-opt-btn p-3 bg-rose-950/70 border-2 border-rose-500 rounded-xl text-left text-xs sm:text-sm font-bold text-rose-200 flex items-center space-x-2";
    state.quizStreak = 0;
    allBtns.forEach(b => {
      const idx = parseInt(b.getAttribute("data-idx"), 10);
      if (!Number.isNaN(idx) && options[idx] === correct) {
        b.className = "quiz-opt-btn p-3 bg-emerald-950/70 border-2 border-emerald-500 rounded-xl text-left text-xs sm:text-sm font-bold text-emerald-200 flex items-center space-x-2";
      }
    });
    fText.innerHTML = `❌ Правильный ответ: <span class='text-emerald-400'>${escapeHtml(correct)}</span>`;
  }

  document.getElementById("quiz-streak-display").innerText = `${state.quizStreak} подряд`;
  document.getElementById("stat-streak").innerText = state.quizStreak;

  if (state.currentQuizData.example) {
    fEx.innerHTML = `Пример: ${renderInteractiveWords(state.currentQuizData.example)}`;
  } else {
    fEx.innerText = state.currentQuizData.explanation || '';
  }
  fBox.classList.remove("hidden");

  if (state.quizNextTimer) clearTimeout(state.quizNextTimer);
  state.quizNextTimer = setTimeout(() => {
    state.quizNextTimer = null;
    if (state.currentMode === 'quiz') {
      loadNextQuiz();
    }
  }, 1400);
}
