import { raw } from './util.js';

const svg = (body, cls = '') => raw(
  `<svg class="icon ${cls}" viewBox="0 0 24 24" aria-hidden="true" focusable="false" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">${body}</svg>`,
);

const STAR = 'M12 3.4l2.65 5.37 5.93.86-4.29 4.18 1.01 5.9L12 16.93l-5.3 2.78 1.01-5.9-4.29-4.18 5.93-.86z';
const HEART = 'M12 20.3s-7.4-4.6-9.3-9.5C1.4 7.4 3.6 4.2 7 4.2c2.1 0 3.4 1.1 5 3.1 1.6-2 2.9-3.1 5-3.1 3.4 0 5.6 3.2 4.3 6.6-1.9 4.9-9.3 9.5-9.3 9.5z';

export const icon = {
  star: () => svg(`<path d="${STAR}"/>`),
  starFill: () => svg(`<path d="${STAR}" fill="currentColor"/>`),
  heart: () => svg(`<path d="${HEART}"/>`),
  heartFill: () => svg(`<path d="${HEART}" fill="currentColor"/>`),
  menu: () => svg('<path d="M4 7h16M4 12h16M4 17h16"/>'),
  close: () => svg('<path d="M6 6l12 12M18 6L6 18"/>'),
  chevronDown: () => svg('<path d="M6 9l6 6 6-6"/>'),
  chevronLeft: () => svg('<path d="M15 6l-6 6 6 6"/>'),
  chevronRight: () => svg('<path d="M9 6l6 6-6 6"/>'),
  sun: () => svg('<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>'),
  moon: () => svg('<path d="M20 14.5A8 8 0 1 1 9.5 4a6.5 6.5 0 0 0 10.5 10.5z"/>'),
  external: () => svg('<path d="M14 4h6v6M20 4l-9 9M18 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h5"/>', 'icon-sm'),
  plus: () => svg('<path d="M12 5v14M5 12h14"/>'),
  minus: () => svg('<path d="M5 12h14"/>'),
  reset: () => svg('<path d="M4 9V4h5M4.6 15a8 8 0 1 0 1.9-8.3L4 9"/>'),
  check: () => svg('<path d="M5 12.5l4.5 4.5L19 7.5"/>'),
  pin: () => svg('<path d="M12 21s-7-6.2-7-11.5a7 7 0 0 1 14 0C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/>'),
  info: () => svg('<circle cx="12" cy="12" r="9"/><path d="M12 11v6M12 7.5v.5"/>'),
  user: () => svg('<circle cx="12" cy="8" r="4"/><path d="M4 21c1.5-4 4.5-6 8-6s6.5 2 8 6"/>'),
  ballot: () => svg('<rect x="4" y="3" width="16" height="18" rx="2"/><path d="M8 12l3 3 5-6"/>'),
  arrowUp: () => svg('<path d="M12 19V5M6 11l6-6 6 6"/>', 'icon-sm'),
  arrowDown: () => svg('<path d="M12 5v14M6 13l6 6 6-6"/>', 'icon-sm'),
  table: () => svg('<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M3 10h18M9 4v16"/>', 'icon-sm'),
  dollar: () => svg('<path d="M12 3v18M16.5 7.5c-.7-1.4-2.3-2.2-4.5-2.2-2.6 0-4.3 1.3-4.3 3.2 0 4.6 9 2.4 9 7 0 2-1.9 3.3-4.7 3.3-2.3 0-4.1-.9-4.9-2.5"/>'),
  news: () => svg('<rect x="3" y="5" width="15" height="15" rx="2"/><path d="M18 9h3v9a2 2 0 0 1-2 2M7 9h7M7 13h7M7 17h4"/>'),
  globe: () => svg('<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.5 2.6 3.8 5.6 3.8 9s-1.3 6.4-3.8 9c-2.5-2.6-3.8-5.6-3.8-9S9.5 5.6 12 3z"/>'),
  upload: () => svg('<path d="M12 16V4M7 9l5-5 5 5M4 16v3a1 1 0 0 0 1 1h14a1 1 0 0 0 1-1v-3"/>'),
  trash: () => svg('<path d="M4 7h16M10 11v6M14 11v6M6 7l1 13h10l1-13M9 7V4h6v3"/>'),
};

// Each copy gets its own gradient id: a shared id breaks once the first copy is hidden.
let logoSeq = 0;
export const logo = () => { const id = `lg-logo-${logoSeq++}`; return raw(`<svg class="logo-mark" viewBox="0 0 40 40" aria-hidden="true" focusable="false">
  <defs><linearGradient id="${id}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#5b6bff"/><stop offset=".55" stop-color="#a463ff"/><stop offset="1" stop-color="#f0476a"/></linearGradient></defs>
  <rect x="2" y="2" width="36" height="36" rx="11" fill="url(#${id})"/>
  <path d="M12 9.5h16a2 2 0 0 1 2 2v17a2 2 0 0 1-2 2H12a2 2 0 0 1-2-2v-17a2 2 0 0 1 2-2z" fill="none" stroke="#fff" stroke-width="2.4" opacity=".55"/>
  <path d="M14.5 20.5l4 4 7.5-9" fill="none" stroke="#fff" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/>
</svg>`); };
