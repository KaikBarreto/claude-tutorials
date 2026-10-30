// www.google.com: /maps (iframe de mapa) e /s2/favicons (logo de banco/site -> selo neutro com a inicial)
import { fakeMapHtml, faviconSvg } from '../../lib/fakemap.mjs';

export default async function google({ path, query }) {
  if (path.startsWith('/maps')) {
    const q = String(query.q || query.query || 'mapa');
    return { __raw: true, type: 'text/html; charset=utf-8', body: fakeMapHtml(q, q) };
  }
  if (path.startsWith('/s2/favicons')) return { __raw: true, type: 'image/svg+xml', body: faviconSvg(query.domain || '?') };
  return { __status: 404, body: { message: 'www.google.com sem handler para ' + path } };
}
