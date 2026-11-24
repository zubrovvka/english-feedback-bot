/**
 * Central state management for the English Feedback trainer
 */

export const state = {
  currentMode: 'card', // 'card' | 'cloze' | 'quiz'
  currentCategory: null,
  currentCard: null,
  currentClozeCard: null,
  currentQuizData: null,
  quizStreak: 0,
  currentImageBase64: null,
  allCardsCache: [],
  hasGeminiKey: false,
  clozeHintIndex: 0,
  autoPlayAudio: true,
  autoPlayDelay: 0,
  activeModeAbortController: null,
};

export function abortActiveModeRequest() {
  if (state.activeModeAbortController) {
    try { state.activeModeAbortController.abort(); } catch (e) {}
    state.activeModeAbortController = null;
  }
}

export const CARD_TYPES = Object.freeze({
  VOCAB: 'vocab',
  CORRECTION: 'correction',
  GOOD_LANGUAGE: 'good_language',
  SUGGESTION: 'suggestion',
  ANTONYM: 'antonym'
});
