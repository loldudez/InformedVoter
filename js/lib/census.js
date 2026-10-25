// Address -> districts, using the U.S. Census Bureau's free public geocoder.
//
// The geocoder sends no CORS headers, so a browser can't fetch() it; it does
// support JSONP, which loads the answer as a <script> from census.gov. The
// address goes to the Census Bureau and nowhere else.
//
// The "Current" vintage already carries the 120th Congress districts and the 2026
// state legislative districts, so mid-decade redistricting is reflected.

let seq = 0;
const ENDPOINT = 'https://geocoding.geo.census.gov/geocoder/geographies/onelineaddress';

export function geocode(address, { timeoutMs = 25000 } = {}) {
  return new Promise((resolve, reject) => {
    const cb = `__ivGeocode${Date.now()}${seq++}`;
    const params = new URLSearchParams({
      address,
      benchmark: 'Public_AR_Current',
      vintage: 'Current_Current',
      layers: 'all',
      format: 'jsonp',
      callback: cb,
    });
    const script = document.createElement('script');
    const timer = setTimeout(() => {
      cleanup();
      reject(new Error('The Census Bureau geocoder took too long to answer. Please try again.'));
    }, timeoutMs);
    function cleanup() {
      clearTimeout(timer);
      delete window[cb];
      script.remove();
    }
    window[cb] = (data) => {
      cleanup();
      try { resolve(parse(data)); } catch (e) { reject(e); }
    };
    script.onerror = () => {
      cleanup();
      reject(new Error('Could not reach the Census Bureau geocoder. Check your connection and try again.'));
    };
    script.src = `${ENDPOINT}?${params}`;
    document.head.appendChild(script);
  });
}

// Pick the newest layer of a kind: "120th Congressional Districts" beats "119th".
function newest(geos, re) {
  const keys = Object.keys(geos).filter((k) => re.test(k));
  keys.sort((a, b) => parseInt(b, 10) - parseInt(a, 10));
  return keys.length ? { key: keys[0], value: (geos[keys[0]] || [])[0] || null } : { key: null, value: null };
}

function parse(data) {
  const matches = data?.result?.addressMatches || [];
  return matches.map((m) => {
    const g = m.geographies || {};
    const st = (g.States || [])[0] || null;
    const cd = newest(g, /Congressional Districts/);
    const up = newest(g, /State Legislative Districts - Upper/);
    const lo = newest(g, /State Legislative Districts - Lower/);
    return {
      matched: m.matchedAddress,
      lon: m.coordinates?.x,
      lat: m.coordinates?.y,
      state: st?.STUSAB || null,
      cd: cd.value ? cd.value.GEOID.slice(2) : null,
      cdLayer: cd.key,
      sldu: up.value ? (up.value.SLDU || up.value.BASENAME) : null,
      sldl: lo.value ? (lo.value.SLDL || lo.value.BASENAME) : null,
      sldLayer: up.key || lo.key,
      county: (g.Counties || [])[0]?.NAME || null,
      place: (g['Incorporated Places'] || [])[0]?.NAME || null,
    };
  });
}
