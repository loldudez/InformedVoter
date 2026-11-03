// What a visitor saves in the France section: their answers to the French
// questionnaire, their French address, starred elections, liked candidates and
// reminder choices. It lives in its own localStorage key, apart from the U.S.
// section's (js/store.js), so neither section can disturb the other. Like the U.S.
// data it never leaves the browser: political opinions are special-category data
// under the GDPR, and a server copy of them would be a liability.

const KEY = 'iv:fr:v1';

const DEFAULTS = {
  answers: {},     // question id -> -2..2, or 'skip'
  quizPos: 0,
  address: null,   // { consent, input, label, citycode, city, postcode, dep, reg, lat, lon, savedAt }
  starred: [],     // election ids
  liked: [],       // candidate ids
  reminders: {},   // election id -> { leads: ['30', '14', '7'], savedAt }
};

function load() {
  try {
    return { ...DEFAULTS, ...JSON.parse(localStorage.getItem(KEY) || '{}') };
  } catch {
    return { ...DEFAULTS };
  }
}

let state = load();
const listeners = new Set();

function save() {
  try {
    localStorage.setItem(KEY, JSON.stringify(state));
  } catch (e) {
    console.warn('Informed Voter: could not save to this browser.', e);
  }
}

export const frStore = {
  get: () => state,
  set(patch) {
    state = { ...state, ...patch };
    save();
    listeners.forEach((fn) => fn(state, patch));
  },
  subscribe(fn) {
    listeners.add(fn);
    return () => listeners.delete(fn);
  },
  toggle(listKey, id) {
    const list = new Set(state[listKey]);
    const on = !list.has(id);
    on ? list.add(id) : list.delete(id);
    this.set({ [listKey]: [...list] });
    return on;
  },
  answered: (answers = state.answers) => Object.values(answers).filter((v) => v !== 'skip').length,
};
