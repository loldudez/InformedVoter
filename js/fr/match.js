// Alignment between a visitor's answers to the French questionnaire and a 2027
// candidate's sourced positions (data/fr/positions.json), by the U.S. section's rule
// (js/model/match.js): a question counts only when the visitor answered it AND the
// candidate's position is documented; anything else is "non documentée" and is
// listed, never guessed. Each counted question scores 1 - |difference| / 4, and below
// MIN_COMPARED compared questions no percentage is shown.

import { MIN_COMPARED } from '../model/match.js';
import { FR_QUESTIONS } from './questions.js';

export { MIN_COMPARED };

export function compareFr(answers, positions = {}) {
  const similarities = [], differences = [], unclear = [];
  let sum = 0, n = 0, userAnswered = 0;
  for (const q of FR_QUESTIONS) {
    const user = answers[q.id];
    if (user == null || user === 'skip') continue;
    userAnswered++;
    const pos = positions[q.id];
    if (!pos || pos.stance == null) {
      unclear.push({ q, user });
      continue;
    }
    const gap = Math.abs(user - pos.stance);
    const score = 1 - gap / 4;
    sum += score;
    n++;
    (gap <= 1 ? similarities : differences).push({ q, user, pos, score });
  }
  similarities.sort((a, b) => b.score - a.score);
  differences.sort((a, b) => a.score - b.score);
  return {
    score: n >= MIN_COMPARED ? Math.round((sum / n) * 100) : null,
    compared: n,
    userAnswered,
    similarities,
    differences,
    unclear,
  };
}

// Every researched candidate, best match first; candidates without a score (fewer
// than MIN_COMPARED shared questions) come last, by how many questions they share.
export function rankFr(answers, candidates, positionsById) {
  return candidates
    .map((c) => ({ cand: c, ...compareFr(answers, positionsById[c.id]) }))
    .sort((a, b) => (b.score ?? -1) - (a.score ?? -1) || b.compared - a.compared);
}
