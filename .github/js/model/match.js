// Alignment between a voter's answers and a candidate's stated positions.
//
// Both sit on the same five-point scale (-2 strongly disagree .. +2 strongly
// agree). A question counts only when the voter answered it AND the candidate's
// position is documented; anything else is "unclear" and is listed, never guessed.
// Each counted question scores 1 - |difference| / 4, so identical answers score
// 100% and opposite extremes score 0%.

import { QUESTION_BY_ID } from '../data/questions.js';

export const MIN_COMPARED = 5; // below this, show no percentage at all

export function compare(answers, positions, questionIds) {
  const similarities = [], differences = [], unclear = [];
  let sum = 0, n = 0, userAnswered = 0;
  for (const qid of questionIds) {
    const user = answers[qid];
    if (user == null || user === 'skip') continue;
    userAnswered++;
    const q = QUESTION_BY_ID[qid];
    const pos = positions[qid];
    if (!pos || pos.stance == null) {
      unclear.push({ q, user });
      continue;
    }
    const gap = Math.abs(user - pos.stance);
    const score = 1 - gap / 4;
    sum += score;
    n++;
    const item = { q, user, stance: pos.stance, source: pos.source, score };
    (gap <= 1 ? similarities : differences).push(item);
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

export function rank(answers, candidates, positionsFor, questionIds) {
  return candidates
    .map((c) => ({ cand: c, ...compare(answers, positionsFor(c), questionIds) }))
    .sort((a, b) => (b.score ?? -1) - (a.score ?? -1) || b.compared - a.compared);
}
