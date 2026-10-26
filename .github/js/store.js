// Everything a visitor saves lives in this browser's localStorage and nowhere
// else: there is no server and no account. That is a deliberate privacy choice;
// political opinions are sensitive data, and a database of them is a liability.

const KEY = 'iv:v1';

const DEFAULTS = {
  countryChosen: false,
  theme: null,           // 'dark' | 'light'
  starred: [],           // race ids
  liked: [],             // candidate ids
  answers: {},           // "My views": question id -> -2..2, or 'skip'
  electionAnswers: {},   // race id -> { question id -> -2..2 | 'skip' }
  quizPos: 0,
  address: null,         // { consent, input, matched, lat, lon, state, cd, sldu, sldl, county, savedAt }
  avatar: null,          // data: URL; null shows the flag
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
let storageOk = true;

function save() {
  try {
    localStorage.setItem(KEY, JSON.stringify(state));
    storageOk = true;
  } catch (e) {
    storageOk = false; // private mode or full storage: keep working in memory
    console.warn('Informed Voter: could not save to this browser.', e);
  }
}

export const store = {
  get: () => state,
  get storageOk() { return storageOk; },
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
  // Swap ids that were renamed (map: old id -> new id), keeping the list's order.
  renameIds(listKey, map) {
    const list = state[listKey].map((id) => map.get(id) || id);
    if (list.some((id, i) => id !== state[listKey][i])) this.set({ [listKey]: [...new Set(list)] });
  },
  isStarred: (id) => state.starred.includes(id),
  isLiked: (id) => state.liked.includes(id),
  answered: (answers = state.answers) => Object.values(answers).filter((v) => v !== 'skip').length,
  clearAll() {
    state = { ...DEFAULTS, countryChosen: true, theme: state.theme };
    save();
    listeners.forEach((fn) => fn(state, {}));
  },
};
