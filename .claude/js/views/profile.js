import { html, raw, fmtDate } from '../util.js';
import { icon } from '../icons.js';
import { store } from '../store.js';
import { STATE_BY_ABBR } from '../data/states.js';
import { CATEGORIES, QUESTIONS, SCALE_LABEL } from '../data/questions.js';
import { geocode } from '../lib/census.js';
import { avatarSrc } from '../components/shell.js';

const ordinalCd = (cd) => (cd === '00' ? 'At-large district' : cd === '98' ? 'Delegate district' : `District ${parseInt(cd, 10)}`);

function head() {
  const st = store.get();
  const answered = store.answered();
  return html`<div class="card profile-head">
    <div class="profile-avatar"><img class="avatar" src="${avatarSrc()}" alt="Your profile picture"></div>
    <div style="flex:1;min-width:220px">
      <div class="eyebrow">My profile</div>
      <h1 style="font-size:clamp(28px,3.4vw,40px);margin:4px 0 6px">Your voter profile</h1>
      <div class="row small muted"><span>${answered} of ${QUESTIONS.length} questions answered</span><span>·</span><span>${st.starred.length} starred elections</span><span>·</span><span>${st.liked.length} liked candidates</span></div>
    </div>
    <div class="row">
      <label class="btn btn-sm" for="avatar-file">${icon.upload()} Change picture</label>
      <input id="avatar-file" type="file" accept="image/*" class="sr-only">
      ${st.avatar ? html`<button type="button" class="btn btn-sm btn-ghost" id="avatar-reset">Use the flag</button>` : ''}
    </div>
  </div>`;
}

function viewsTab() {
  const a = store.get().answers;
  const answered = store.answered();
  const touched = Object.keys(a).length;
  return html`<div class="stack">
    <div class="card">
      <div class="row between">
        <div><h2 style="margin:0">My views</h2><p class="muted" style="margin:4px 0 0">${QUESTIONS.length} agree-or-disagree questions in ${CATEGORIES.length} topics, one at a time. Skip any you like.</p></div>
        <a class="btn btn-primary" href="#/views">${touched === 0 ? 'Start the questionnaire' : touched >= QUESTIONS.length ? 'Review from the start' : 'Continue where you left off'}</a>
      </div>
      <div class="progress" style="margin:16px 0 6px"><span style="width:${(touched / QUESTIONS.length) * 100}%"></span></div>
      <p class="small faint" style="margin:0">${answered} answered, ${touched - answered} skipped. Your answers never leave this browser.</p>
    </div>
    <div class="card">
      <h3>By topic</h3>
      ${CATEGORIES.map((c) => {
        const done = c.questions.filter((q) => a[q.id] != null).length;
        const first = QUESTIONS.indexOf(c.questions.find((q) => a[q.id] == null) || c.questions[0]);
        return html`<div class="cat-progress"><a href="#/views?q=${first}">${c.title}</a><div class="progress"><span style="width:${(done / c.questions.length) * 100}%"></span></div><span class="small faint num">${done}/${c.questions.length}</span></div>`;
      })}
    </div>
    ${touched ? html`<details class="card"><summary style="cursor:pointer;font-weight:650">Review and edit my answers</summary>
      <div class="stack" style="margin-top:14px">${CATEGORIES.map((c) => html`<div><div class="eyebrow" style="margin-bottom:6px">${c.title}</div><div class="answer-list">${c.questions.filter((q) => a[q.id] != null).map((q) => html`<a class="answer-row" href="#/views?q=${QUESTIONS.indexOf(q)}"><span>${q.text}</span><span class="answer-tag">${a[q.id] === 'skip' ? 'Skipped' : SCALE_LABEL[a[q.id]]}</span></a>`)}</div></div>`)}</div>
      <button type="button" class="btn btn-sm btn-ghost" id="clear-answers" style="margin-top:16px">${icon.trash()} Clear all my answers</button>
    </details>` : ''}
  </div>`;
}

function districtsList(ad) {
  const s = STATE_BY_ABBR[ad.state];
  return html`<dl class="kv">
    <dt>State</dt><dd>${s ? s.name : ad.state}</dd>
    ${ad.county ? html`<dt>County</dt><dd>${ad.county}</dd>` : ''}
    <dt>U.S. House</dt><dd>${ad.cd ? ordinalCd(ad.cd) : 'Not found'}</dd>
    ${s && !s.noLegislature ? html`<dt>${s.unicameral ? 'Legislature' : s.upper.name}</dt><dd>${ad.sldu ? `District ${ad.sldu.replace(/^0+/, '')}` : 'Not found'}</dd>` : ''}
    ${s && s.lower ? html`<dt>${s.lower.name}</dt><dd>${ad.sldl ? `District ${ad.sldl.replace(/^0+/, '')}` : 'Not found'}</dd>` : ''}
  </dl>`;
}

function locationTab() {
  const ad = store.get().address;
  if (ad && ad.matched) {
    return html`<div class="stack">
      <div class="card">
        <div class="row between"><div><div class="eyebrow">Saved address</div><h2 style="margin:4px 0 0;font-size:22px">${ad.matched}</h2></div>
          <a class="btn btn-primary" href="#/elections">${icon.ballot()} See my elections</a></div>
        <p class="small faint" style="margin:6px 0 16px">Matched by the U.S. Census Bureau on ${fmtDate(ad.savedAt)}. Stored only in this browser.</p>
        ${districtsList(ad)}
        <div class="row" style="margin-top:18px"><button type="button" class="btn btn-sm" id="change-address">Change address</button><button type="button" class="btn btn-sm btn-ghost" id="remove-address">${icon.trash()} Remove my address</button></div>
      </div>
      <div id="address-form-slot" hidden>${addressForm()}</div>
    </div>`;
  }
  return addressForm();
}

function addressForm() {
  const ad = store.get().address;
  return html`<form class="card stack" id="address-form" novalidate>
    <div><h2 style="margin:0">My location</h2><p class="muted" style="margin:4px 0 0">Your full street address tells us exactly which districts you vote in. ZIP codes alone can’t: many span more than one congressional district.</p></div>
    <div class="notice">${icon.info()}<div><b>How your address is used.</b> It is sent only to the U.S. Census Bureau’s free public geocoder to find your districts, then saved in this browser so you don’t have to retype it. Informed Voter has no server and never receives it. It is used only to show the elections you can vote in.</div></div>
    <label class="check"><input type="checkbox" id="consent" ${ad?.consent ? 'checked' : ''}> <span>I agree to let Informed Voter use my address only to find the elections on my ballot.</span></label>
    <div class="field"><label for="addr">Home street address</label><input class="input" id="addr" name="addr" autocomplete="street-address" placeholder="123 Main St, Baton Rouge, LA 70802" value="${ad?.input || ''}"></div>
    <div class="row"><button class="btn btn-primary" type="submit" id="find-btn">${icon.pin()} Find my address</button><span class="small faint" id="addr-status" role="status"></span></div>
    <div id="suggestions" class="stack-sm"></div>
  </form>`;
}

async function shrinkImage(file) {
  const url = URL.createObjectURL(file);
  try {
    const img = await new Promise((res, rej) => { const i = new Image(); i.onload = () => res(i); i.onerror = rej; i.src = url; });
    const size = 256;
    const c = document.createElement('canvas');
    c.width = c.height = size;
    const s = Math.min(img.width, img.height);
    c.getContext('2d').drawImage(img, (img.width - s) / 2, (img.height - s) / 2, s, s, 0, 0, size, size);
    return c.toDataURL('image/jpeg', 0.86);
  } finally {
    URL.revokeObjectURL(url);
  }
}

export const profile = {
  title: () => 'My profile',
  render(ctx) {
    const tab = ctx.query.tab === 'location' ? 'location' : 'views';
    return html`<div class="wrap page stack" style="max-width:960px">
      ${head()}
      <nav class="seg" aria-label="Profile sections"><a href="#/profile?tab=views" ${raw(tab === 'views' ? 'aria-current="page"' : '')}>My views</a><a href="#/profile?tab=location" ${raw(tab === 'location' ? 'aria-current="page"' : '')}>My location</a></nav>
      ${tab === 'views' ? viewsTab() : locationTab()}
    </div>`;
  },
  mount(root, ctx) {
    const file = root.querySelector('#avatar-file');
    file?.addEventListener('change', async () => {
      const f = file.files?.[0];
      if (!f || !f.type.startsWith('image/') || f.size > 15e6) return;
      try {
        store.set({ avatar: await shrinkImage(f) });
        window.dispatchEvent(new Event('iv:rerender'));
      } catch {
        alert('That image could not be read. Try a JPG or PNG.');
      }
    });
    root.querySelector('#avatar-reset')?.addEventListener('click', () => { store.set({ avatar: null }); window.dispatchEvent(new Event('iv:rerender')); });
    root.querySelector('#clear-answers')?.addEventListener('click', () => {
      if (confirm('Clear all of your My views answers? This cannot be undone.')) { store.set({ answers: {}, quizPos: 0 }); window.dispatchEvent(new Event('iv:rerender')); }
    });
    root.querySelector('#remove-address')?.addEventListener('click', () => {
      if (confirm('Remove your saved address from this browser?')) { store.set({ address: null }); window.dispatchEvent(new Event('iv:rerender')); }
    });
    root.querySelector('#change-address')?.addEventListener('click', () => {
      const slot = root.querySelector('#address-form-slot');
      slot.hidden = false;
      slot.querySelector('#addr')?.focus();
    });

    const form = root.querySelector('#address-form');
    if (!form) return;
    const status = form.querySelector('#addr-status');
    const sugg = form.querySelector('#suggestions');
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const consent = form.querySelector('#consent').checked;
      const input = form.querySelector('#addr').value.trim();
      sugg.innerHTML = '';
      if (!consent) { status.textContent = 'Please tick the consent box first.'; return; }
      if (input.length < 8) { status.textContent = 'Enter your full street address, including city and state or ZIP code.'; return; }
      status.innerHTML = '<span class="spinner"></span> Asking the U.S. Census Bureau…';
      try {
        const matches = (await geocode(input)).filter((m) => m.state && STATE_BY_ABBR[m.state]);
        if (!matches.length) {
          status.textContent = '';
          sugg.innerHTML = String(html`<div class="notice warn">${icon.info()}<div><b>No match found.</b> Check the spelling, include the city and state (or ZIP), and leave out apartment or unit numbers. P.O. boxes can’t be matched to a district.</div></div>`);
          return;
        }
        status.textContent = matches.length === 1 ? 'We found this address. Is it yours?' : `We found ${matches.length} possible addresses. Pick yours:`;
        sugg.innerHTML = matches.map((m, i) => String(html`<button type="button" class="suggestion" data-i="${i}">${icon.pin()}<span><b>${m.matched}</b><br><span class="small faint">${m.county || ''}${m.cd ? ` · ${ordinalCd(m.cd)}` : ''}</span></span><span class="btn btn-sm" style="margin-left:auto">Use this</span></button>`)).join('');
        sugg.querySelectorAll('[data-i]').forEach((b) => b.addEventListener('click', () => {
          const m = matches[+b.dataset.i];
          store.set({ address: { ...m, consent: true, input, savedAt: new Date().toISOString() } });
          if (location.hash !== '#/profile?tab=location') location.hash = '#/profile?tab=location';
          else window.dispatchEvent(new Event('iv:rerender'));
        }));
      } catch (err) {
        status.textContent = err.message;
      }
    });
  },
};
