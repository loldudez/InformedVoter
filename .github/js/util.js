// Small shared helpers: escaping HTML templates, formatting, deterministic randomness.

export const $ = (sel, root = document) => root.querySelector(sel);
export const $$ = (sel, root = document) => [...root.querySelectorAll(sel)];

const ESC = { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' };
export const esc = (s) => String(s ?? '').replace(/[&<>"']/g, (c) => ESC[c]);

// html`...` escapes every interpolated value unless it is already Raw (another
// html`` result or an explicit raw()). News headlines and other outside text
// therefore can't inject markup by accident.
export class Raw {
  constructor(s) { this.s = s; }
  toString() { return this.s; }
}
export const raw = (s) => new Raw(String(s));
const part = (v) => {
  if (v == null || v === false) return '';
  if (v === true) return 'true';
  if (v instanceof Raw) return v.s;
  if (Array.isArray(v)) return v.map(part).join('');
  return esc(v);
};
export function html(strings, ...vals) {
  let out = strings[0];
  for (let i = 0; i < vals.length; i++) out += part(vals[i]) + strings[i + 1];
  return new Raw(out);
}

// Formatting ----------------------------------------------------------------

export const clamp = (x, lo, hi) => Math.min(hi, Math.max(lo, x));
export const fmtInt = (n) => Math.round(n).toLocaleString('en-US');
export const fmtPct = (x, d = 1) => `${Number(x).toFixed(d)}%`;
export const fmtProb = (p) => {
  const pct = p * 100;
  if (pct > 99) return '>99%';
  if (pct < 1) return '<1%';
  return `${Math.round(pct)}%`;
};
export function fmtMoney(n, { exact = false } = {}) {
  if (exact) return '$' + fmtInt(n);
  const a = Math.abs(n);
  if (a >= 1e9) return `$${(n / 1e9).toFixed(1)}B`;
  if (a >= 1e6) return `$${(n / 1e6).toFixed(a >= 1e7 ? 0 : 1)}M`;
  if (a >= 1e3) return `$${(n / 1e3).toFixed(a >= 1e5 ? 0 : 1)}K`;
  return `$${Math.round(n)}`;
}
export function fmtCompact(n) {
  const a = Math.abs(n);
  if (a >= 1e6) return `${(n / 1e6).toFixed(a >= 1e7 ? 1 : 2)}M`;
  if (a >= 1e3) return `${Math.round(n / 1e3)}K`;
  return fmtInt(n);
}
// Margins are stored as first-named minus second-named share, in points.
export const fmtLead = (party, pts, d = 1) => `${party} +${Math.abs(pts).toFixed(d)}`;
export function fmtDR(dr, d = 1) {
  if (dr == null) return '—';
  if (Math.abs(dr) < 0.05) return 'Even';
  return dr > 0 ? `D +${dr.toFixed(d)}` : `R +${(-dr).toFixed(d)}`;
}
export const signed = (x, d = 1, unit = '') => `${x > 0 ? '+' : x < 0 ? '−' : '±'}${Math.abs(x).toFixed(d)}${unit}`;

const MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
// "2026-07-21" means that calendar day where the voter is. new Date() would read it
// as UTC midnight, which shows as the day before anywhere in the Americas.
const toDate = (d) => {
  const m = typeof d === 'string' && d.match(/^(\d{4})-(\d{2})-(\d{2})$/);
  return m ? new Date(+m[1], +m[2] - 1, +m[3]) : new Date(d);
};
export const fmtDate = (d) => { d = toDate(d); return `${MONTHS[d.getMonth()]} ${d.getDate()}, ${d.getFullYear()}`; };
export const fmtShortDate = (d) => { d = toDate(d); return `${MONTHS[d.getMonth()]} ${d.getDate()}`; };
export function timeAgo(d, now = new Date()) {
  const s = (now - new Date(d)) / 1000;
  if (s < 90) return 'just now';
  if (s < 3600) return `${Math.round(s / 60)} min ago`;
  if (s < 86400) return `${Math.round(s / 3600)} hr ago`;
  const days = Math.round(s / 86400);
  return days === 1 ? 'yesterday' : `${days} days ago`;
}
export const isoDay = (d) => new Date(d).toISOString().slice(0, 10);
export const addDays = (d, n) => new Date(new Date(d).getTime() + n * 864e5);

export function initials(name) {
  return name.split(/\s+/).filter(Boolean).map((w) => w[0]).slice(0, 2).join('').toUpperCase();
}
export const ordinal = (n) => {
  const s = ['th', 'st', 'nd', 'rd'], v = n % 100;
  return n + (s[(v - 20) % 10] || s[v] || s[0]);
};

// Deterministic randomness, so demo data is identical on every visit ---------

export function hashStr(str) {
  let h = 2166136261;
  for (let i = 0; i < str.length; i++) {
    h ^= str.charCodeAt(i);
    h = Math.imul(h, 16777619);
  }
  return h >>> 0;
}
export function rng(seed) {
  let a = typeof seed === 'string' ? hashStr(seed) : seed >>> 0;
  return () => {
    a = (a + 0x6d2b79f5) >>> 0;
    let t = a;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}
export function gauss(r) {
  let u = 0, v = 0;
  while (u === 0) u = r();
  while (v === 0) v = r();
  return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v);
}
export const pick = (r, arr) => arr[Math.floor(r() * arr.length)];

export function debounce(fn, ms = 150) {
  let t;
  return (...a) => { clearTimeout(t); t = setTimeout(() => fn(...a), ms); };
}

export async function fetchJSON(url) {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`${res.status} ${url}`);
  return res.json();
}
