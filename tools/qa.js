// QA automático de una corrida tienda-express. Pegar en javascript_tool (panel del navegador, tienda ya desbloqueada)
// estando en: https://<tienda>.myshopify.com/products/<handle>?preview_theme_id=<id>
// Devuelve un objeto; "ok" = true solo si todo pasa.
(async () => {
  document.querySelector('[data-hk-pop]')?.classList.remove('is-open');
  document.querySelectorAll('img[loading=lazy]').forEach(i => (i.loading = 'eager'));
  await new Promise(r => setTimeout(r, 2500));
  const theme = new URL(location.href).searchParams.get('preview_theme_id');
  const imgs = [...document.querySelectorAll('.hk img')];
  const links = [...new Set([...document.querySelectorAll('a[href]')].map(a => a.getAttribute('href'))
    .filter(h => h && h.startsWith('/') && !h.startsWith('//')))];
  const malos = [];
  for (const h of links) {
    const u = new URL(h, location.origin); if (theme) u.searchParams.set('preview_theme_id', theme);
    const r = await fetch(u); if (r.status >= 400) malos.push([h, r.status]);
  }
  const r = {
    secciones_hk: document.querySelectorAll('.hk').length,
    placeholders: [...document.querySelectorAll('.hk-ph')].map(p => p.textContent.trim()).filter(Boolean),
    imagenes: imgs.length,
    imagenes_rotas: imgs.filter(i => i.complete && i.naturalWidth === 0).map(i => i.src.split('/').pop()),
    enlaces: links.length, enlaces_rotos: malos,
    boton_cod_app: !!document.querySelector('[class*=rsi_]'),
    boton_propio_oculto: document.querySelector('[data-hk-submit]')?.hidden ?? null,
    variantes: JSON.parse(document.querySelector('[data-hk-variants]')?.textContent || '[]').length,
    textos_en_ingles: [...document.body.innerText.matchAll(/\b(Add to cart|Buy it now|Shipping|Free|Sold out|Search)\b/g)].map(m => m[0]).slice(0, 10),
  };
  r.ok = !r.placeholders.length && !r.imagenes_rotas.length && !r.enlaces_rotos.length && r.boton_cod_app && r.variantes > 0;
  return r;
})();
