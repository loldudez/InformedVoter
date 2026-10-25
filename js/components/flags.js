// Small inline flags for the country picker.

function usFlag() {
  // Official proportions: hoist 1, fly 1.9; canton 0.76 x 7/13; 50 stars in 9 rows.
  const H = 3900, Wd = 7410, stripe = H / 13, cw = 0.76 * H, chh = stripe * 7;
  const G = 0.063 * H, E = 0.054 * H, R = 0.0616 * H / 2;
  const star = (cx, cy) => {
    const pts = [];
    for (let i = 0; i < 10; i++) {
      const a = -Math.PI / 2 + (i * Math.PI) / 5;
      const rr = i % 2 ? R * 0.382 : R;
      pts.push(`${(cx + rr * Math.cos(a)).toFixed(0)},${(cy + rr * Math.sin(a)).toFixed(0)}`);
    }
    return `<polygon points="${pts.join(' ')}"/>`;
  };
  let stripes = '', stars = '';
  for (let i = 0; i < 13; i += 2) stripes += `<rect y="${(i * stripe).toFixed(0)}" width="${Wd}" height="${stripe.toFixed(0)}"/>`;
  for (let row = 1; row <= 9; row++) {
    const odd = row % 2 === 1;
    for (let col = odd ? 1 : 2; col <= 11; col += 2) stars += star(col * G, row * E);
  }
  return `<svg viewBox="0 0 ${Wd} ${H}" preserveAspectRatio="xMidYMid slice" aria-hidden="true"><rect width="${Wd}" height="${H}" fill="#fff"/><g fill="#b22234">${stripes}</g><rect width="${cw.toFixed(0)}" height="${chh.toFixed(0)}" fill="#3c3b6e"/><g fill="#fff">${stars}</g></svg>`;
}

const UK = `<svg viewBox="0 0 60 30" preserveAspectRatio="xMidYMid slice" aria-hidden="true"><clipPath id="ivuk-s"><path d="M0,0 v30 h60 v-30 z"/></clipPath><clipPath id="ivuk-t"><path d="M30,15 h30 v15 z v15 h-30 z h-30 v-15 z v-15 h30 z"/></clipPath><g clip-path="url(#ivuk-s)"><path d="M0,0 v30 h60 v-30 z" fill="#012169"/><path d="M0,0 L60,30 M60,0 L0,30" stroke="#fff" stroke-width="6"/><path d="M0,0 L60,30 M60,0 L0,30" clip-path="url(#ivuk-t)" stroke="#C8102E" stroke-width="4"/><path d="M30,0 v30 M0,15 h60" stroke="#fff" stroke-width="10"/><path d="M30,0 v30 M0,15 h60" stroke="#C8102E" stroke-width="6"/></g></svg>`;

const CA = `<svg viewBox="0 0 40 20" preserveAspectRatio="xMidYMid slice" aria-hidden="true"><rect width="40" height="20" fill="#fff"/><rect width="10" height="20" fill="#d80621"/><rect x="30" width="10" height="20" fill="#d80621"/><polygon fill="#d80621" points="20,2.2 21.3,4.6 22.8,4 22.3,8 24.6,5.8 25.2,7.3 27.4,6.8 26.6,9.3 27.8,10 24.2,13 24.7,14.4 20.6,13.9 20.7,17.6 19.3,17.6 19.4,13.9 15.3,14.4 15.8,13 12.2,10 13.4,9.3 12.6,6.8 14.8,7.3 15.4,5.8 17.7,8 17.2,4 18.7,4.6"/></svg>`;

const FR = `<svg viewBox="0 0 3 2" preserveAspectRatio="xMidYMid slice" aria-hidden="true"><rect width="1" height="2" fill="#002395"/><rect x="1" width="1" height="2" fill="#fff"/><rect x="2" width="1" height="2" fill="#ed2939"/></svg>`;

export const FLAGS = { us: usFlag(), uk: UK, ca: CA, fr: FR };
