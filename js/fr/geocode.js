// French address -> commune, department and region, through the Géoplateforme's
// public geocoding service (IGN; it replaced api-adresse.data.gouv.fr). The address is
// sent only there, only after the visitor ticks the consent box, and the result is
// kept in this browser (js/fr/store.js). It answers CORS requests, so no proxy is needed.

import { fetchJSON } from '../util.js';
import { loadDepartements } from './data.js';

const URL_BASE = 'https://data.geopf.fr/geocodage/search';

// INSEE commune code -> department code: two characters, three overseas (971-976).
export const depOf = (citycode) => (/^97/.test(citycode) ? citycode.slice(0, 3) : citycode.slice(0, 2));

export async function geocodeFr(text) {
  const url = `${URL_BASE}?${new URLSearchParams({ q: text, index: 'address', limit: '5' })}`;
  const [res, deps] = await Promise.all([fetchJSON(url), loadDepartements()]);
  const regOf = new Map((deps?.features || []).map((f) => [f.id, f.properties.reg]));
  const depName = new Map((deps?.features || []).map((f) => [f.id, f.properties.name]));
  return (res.features || []).filter((f) => f.properties?.citycode).map((f) => {
    const p = f.properties;
    const dep = depOf(p.citycode);
    return {
      label: p.label, city: p.city, citycode: p.citycode, postcode: p.postcode, type: p.type,
      dep, depName: depName.get(dep) || null, reg: regOf.get(dep) || null,
      lon: f.geometry?.coordinates?.[0], lat: f.geometry?.coordinates?.[1], score: p.score,
    };
  });
}
