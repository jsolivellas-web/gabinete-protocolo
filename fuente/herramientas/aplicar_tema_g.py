"""Aplica la interfaz G · Bento sereno (fusión de A · Mediterránea y E · Bento, en tonos neutros) a fuente/gestor-protocolo.html.
Uso: python fuente/herramientas/aplicar_tema_g.py   (solo se ejecuta una vez; comprueba que cada cambio encaja exactamente)."""
import io, os
P = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'gestor-protocolo.html')
s = io.open(P, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    assert c == n, (c, old[:90])
    s = s.replace(old, new)
def between(a, b, new, include_end=False):
    global s
    i = s.index(a); j = s.index(b, i)
    if include_end: j += len(b)
    s = s[:i] + new + s[j:]

# Paleta neutra: blanco roto, arena, piedra y salvia, con un verde mar apagado como color principal
between(':root{\n  --paper:', '  --f-display:', """:root{
  --paper:#f5f3ee; --sheet:#ffffff; --ink:#24302f; --ink-2:#5f6b69; --line:#e8e3d9; --line-2:#d9d2c4;
  --accent:#3f6266; --accent-soft:#dfe9e6; --gold:#8a6a45; --gold-soft:#efe4d3; --sun:#f1e6d2;
  --navy:#4b6e71; --navy-ink:#ffffff; --sea-2:#5f8483; --sea-3:#7a9a96; --terra:#b48a6e; --sand:#ece6da; --sage:#e3ebe8;
  --ok:#2f6b4f; --ok-soft:#dfe9e3; --warn:#946116; --warn-soft:#f6ecd8; --bad:#a63a32; --bad-soft:#f6e1de;
""")
DARK = """  --paper:#131816; --sheet:#1a211f; --ink:#e4e9e6; --ink-2:#a0aca9; --line:#29322f; --line-2:#36413e;
  --accent:#8fb7b2; --accent-soft:#223a37; --gold:#d4b48a; --gold-soft:#342b20; --sun:#d9c9a8;
  --navy:#2c4547; --navy-ink:#e4e9e6; --sea-2:#3a5a5a; --sea-3:#4f7370; --terra:#c49a7f; --sand:#27261f; --sage:#1d2a27;
  --ok:#7cc29a; --ok-soft:#1b3127; --warn:#e0ad5f; --warn-soft:#382c16; --bad:#ec8a80; --bad-soft:#3a1f1c; --shadow:none; color-scheme:dark}"""
for head in ['@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){\n', ':root[data-theme="dark"]{\n']:
    i = s.index(head) + len(head); j = s.index('color-scheme:dark}', i) + len('color-scheme:dark}')
    s = s[:i] + DARK + s[j:]
rep("--r:14px; --shadow:0 1px 2px rgba(22,52,58,.05), 0 8px 24px rgba(22,52,58,.06);", "--r:14px; --shadow:0 1px 2px rgba(36,48,47,.04), 0 6px 20px rgba(36,48,47,.05);")
rep(':root[data-theme="dark"] button.primary{color:#0b2226}', ':root[data-theme="dark"] button.primary{color:#13201e}')
rep('@media (prefers-color-scheme: dark){:root:not([data-theme="light"]) button.primary{color:#0b2226}}', '@media (prefers-color-scheme: dark){:root:not([data-theme="light"]) button.primary{color:#13201e}}')
rep(':root[data-theme="dark"] .nav-list a.on{color:#0b2226}', ':root[data-theme="dark"] .nav-list a.on{color:#13201e}')
rep('@media (prefers-color-scheme: dark){:root:not([data-theme="light"]) .nav-list a.on{color:#0b2226}}', '@media (prefers-color-scheme: dark){:root:not([data-theme="light"]) .nav-list a.on{color:#13201e}}')
rep(".brand{font-family:var(--f-display);font-size:1.3rem;font-weight:700;", ".brand{font-family:var(--f-display);font-size:1.3rem;font-weight:600;")

# Portada en bloques (bento): sustituye la portada de la A
between('.hero{position:relative;', '.verdict{', """.bento{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));grid-auto-rows:minmax(150px,auto);gap:14px;grid-template-areas:"hero hero next next" "hero hero task succ" "bud bud prov conv" "quick quick quick conv"}
.bx{border-radius:24px;padding:20px;position:relative;overflow:hidden;min-width:0;background:var(--sheet);border:1px solid var(--line);box-shadow:var(--shadow);display:flex;flex-direction:column;gap:6px;align-items:stretch;text-align:left;white-space:normal;font-weight:400;color:var(--ink)}
button.bx:hover{border-color:var(--accent)}
.bx .num{font-family:var(--f-display);font-weight:500;letter-spacing:-.02em;line-height:1}
.bx .lbl{font-weight:600;font-size:.84rem;color:var(--ink-2)}
.hero{grid-area:hero;position:relative;overflow:hidden;border-radius:24px;padding:28px 28px 56px;color:#fff;background:linear-gradient(150deg,var(--navy) 0%,var(--sea-2) 60%,var(--sea-3) 100%);display:flex;flex-direction:column;justify-content:space-between;gap:16px}
.hero .eyebrow{color:#ffffffbf}
.hero h1{color:#fff;font-size:2.5rem;font-weight:500;max-width:13ch;line-height:1.05;margin-top:6px}
.hero p{margin:12px 0 0;opacity:.9;max-width:40ch;line-height:1.5}
.hero .btns{display:flex;gap:8px;flex-wrap:wrap;position:relative;z-index:1}
.hero button{border:1px solid #ffffff55;background:#ffffff1f;color:#fff}
.hero button.sun{background:var(--sun);border-color:var(--sun);color:#3a3226}
.hero .wave{position:absolute;left:0;right:0;bottom:-1px;width:100%;height:42px;display:block;pointer-events:none}
.b-next{grid-area:next;padding:0;border:0;color:#fff;cursor:pointer;background:var(--navy)}
.b-next .img{position:absolute;inset:0;filter:saturate(.7)}
.b-next .img svg{width:100%;height:100%;display:block}
.b-next .ov{position:absolute;inset:0;background:linear-gradient(90deg,rgba(24,32,31,.76),rgba(24,32,31,.06) 78%);padding:20px;display:flex;flex-direction:column;justify-content:space-between;gap:10px}
.date-chip{align-self:flex-start;background:#fff;color:#3f6266;border-radius:14px;padding:6px 12px;text-align:center;font-family:var(--f-display);font-size:1.5rem;font-weight:600;line-height:1}
.date-chip small{display:block;font-family:var(--f-body);font-size:.62rem;letter-spacing:.1em;text-transform:uppercase;color:#7a8583;margin-top:3px}
.b-next b{font-size:1.05rem;display:block;max-width:26ch}
.b-next .meta{font-size:.8rem;opacity:.88}
.b-next .bar{height:5px;border:0;background:#ffffff33;max-width:260px;margin-top:8px}
.b-next .bar > i{background:#f1e6d2!important}
.b-empty{grid-area:next;justify-content:center;align-items:flex-start;background:var(--sand);border-color:transparent}
.b-task{grid-area:task;background:var(--sand);border-color:transparent;cursor:pointer}
.b-task .num{font-size:3.6rem;color:var(--gold)}
.b-arrow{position:absolute;right:14px;bottom:14px;width:34px;height:34px;border-radius:50%;background:var(--sheet);color:var(--gold);display:grid;place-items:center}
.b-arrow svg,.qchip svg{width:15px;height:15px;fill:none;stroke:currentColor;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round}
.b-succ{grid-area:succ;align-items:center;justify-content:center;text-align:center}
.b-succ svg{width:84px;height:84px}
.b-bud{grid-area:bud;background:var(--sage);border-color:transparent;justify-content:space-between;gap:12px;cursor:pointer}
.b-bud .num{font-size:2.3rem;color:var(--accent)}
.stack{display:flex;height:22px;border-radius:8px;overflow:hidden;gap:3px;background:var(--sheet)}
.stack i{display:block;height:100%}
.leg{display:flex;gap:12px;flex-wrap:wrap;font-size:.74rem;font-weight:600;color:var(--ink-2);margin-top:8px}
.leg i{display:inline-block;width:9px;height:9px;border-radius:3px;margin-right:5px;vertical-align:middle}
.b-prov{grid-area:prov;cursor:pointer}
.b-prov .num{font-size:2.8rem;color:var(--accent)}
.avs{display:flex;margin-top:auto;padding-top:8px}
.avs span{width:30px;height:30px;border-radius:50%;border:3px solid var(--sheet);margin-right:-8px;display:grid;place-items:center;font-size:.6rem;font-weight:800}
.b-conv{grid-area:conv;background:var(--gold-soft);border-color:transparent;gap:10px;cursor:pointer}
.calx{background:var(--sheet);border-radius:16px;text-align:center;padding:0 0 10px;width:88px;overflow:hidden;border:1px solid var(--line)}
.calx small{display:block;background:var(--terra);color:#fff;font-weight:800;font-size:.68rem;letter-spacing:.1em;padding:4px 0;margin-bottom:6px}
.calx .num{font-size:2.2rem;color:var(--gold)}
.b-conv b{font-size:.92rem}
.b-conv ol{margin:0;padding-left:18px;font-size:.8rem;line-height:1.55;color:var(--ink-2)}
.b-quick{grid-area:quick;flex-direction:row;flex-wrap:wrap;align-items:center;align-content:center;gap:8px}
.b-quick h2{width:100%;font-size:1.2rem;font-weight:500;margin-bottom:4px}
.qchip{display:flex;align-items:center;gap:8px;padding:7px 14px 7px 7px;border-radius:999px;background:var(--paper);font-weight:600;font-size:.83rem;border:1px solid var(--line);color:var(--ink)}
.qchip span{width:28px;height:28px;border-radius:50%;display:grid;place-items:center}
.ev-cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:14px;margin-top:12px}
.ev-card{background:var(--sheet);border:1px solid var(--line);border-radius:20px;overflow:hidden;cursor:pointer;text-align:left;padding:0;display:flex;flex-direction:column;align-items:stretch;white-space:normal;font-weight:400;box-shadow:var(--shadow)}
.ev-card:hover{border-color:var(--accent)}
.ev-card .img{height:118px;position:relative;overflow:hidden;filter:saturate(.75)}
.ev-card .img svg,.ev-card .img img{width:100%;height:100%;display:block;object-fit:cover}
.ev-card .date-chip{position:absolute;left:10px;top:10px;font-size:1.05rem;padding:4px 10px}
.ev-card .body{padding:12px 14px 14px;display:flex;flex-direction:column;gap:6px}
.ev-card h3{font-family:var(--f-body);font-size:.95rem;font-weight:700}
.ev-card .bar{height:6px;border:0}
@media (max-width:900px){
  .bento{grid-template-columns:repeat(2,minmax(0,1fr));grid-auto-rows:minmax(140px,auto);grid-template-areas:"hero hero" "next next" "task succ" "bud bud" "prov conv" "quick quick"}
  .hero{padding:24px 22px 52px}.hero h1{font-size:2rem}
}
""")

# Panel nuevo
between("const ICO = {", "const ico = k =>", """const ICO = {
  flag:'<path d="M5 21V4M5 4h11l-2 4 2 4H5"/>', mail:'<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>',
  users:'<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20a6.5 6.5 0 0 1 13 0"/><circle cx="17" cy="9" r="2.5"/><path d="M16 14.5a5 5 0 0 1 5.5 5"/>',
  chart:'<path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/>', cal:'<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/>',
  doc:'<path d="M6 3h9l4 4v14H6z"/><path d="M14 3v5h5M9 13h7M9 17h7"/>', box:'<path d="M3 7l9-4 9 4-9 4-9-4z"/><path d="M3 7v10l9 4 9-4V7"/>',
  search:'<circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/>', star:'<path d="M12 3l2.8 5.7 6.2.9-4.5 4.4 1 6.2L12 17.3 6.5 20.2l1-6.2L3 9.6l6.2-.9z"/>',
  arrow:'<path d="M7 17L17 7M9 7h8v8"/>', news:'<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M7 8h10M7 12h10M7 16h6"/>'
};
""")
between("function renderPanel(v){", "document.addEventListener('click', e => {\n  const g = e.target.closest('[data-view-go]')", r"""function renderPanel(v){
  const evs = Store.data.eventos;
  const now = today();
  const prox = evs.filter(e => e.fecha && e.fecha >= now && e.estado !== 'Cancelado').sort((a, b) => a.fecha.localeCompare(b.fecha));
  const pend = evs.reduce((s, e) => s + (e.checklist || []).filter(c => !c.ok).length, 0);
  const evals = Store.data.evaluaciones.map(calcEval).filter(r => r.indice > 0);
  const media = evals.length ? evals.reduce((s, r) => s + r.indice, 0) / evals.length : 0;
  const hora = new Date().getHours();
  const saludo = hora < 14 ? 'Buenos días' : hora < 21 ? 'Buenas tardes' : 'Buenas noches';
  const dias = f => Math.round((new Date(f + 'T00:00') - new Date(now + 'T00:00')) / 864e5);
  const cuando = f => { const d = dias(f); return d === 0 ? 'hoy' : d === 1 ? 'mañana' : `en ${d} días`; };
  const mes = f => new Date(f + 'T00:00').toLocaleDateString('es-ES', {month:'short'}).replace('.', '');
  const avance = e => { const ch = e.checklist || []; return ch.length ? Math.round(ch.filter(c => c.ok).length / ch.length * 100) : 0; };
  const sig = prox[0];
  const conv = Store.data.convocatorias.filter(c => c.fecha && c.fecha >= now).sort((a, b) => a.fecha.localeCompare(b.fecha))[0];
  const tareas = n => n === 1 ? '1 tarea' : `${n} tareas`;
  const resumen = [
    prox.length ? `Tienes ${prox.length} ${prox.length === 1 ? 'acto' : 'actos'} en marcha y ${tareas(pend)} por cerrar.` : 'Empieza por un pack o crea un evento desde cero.',
    conv ? `${esc(conv.organo || 'La reunión')} se reúne ${cuando(conv.fecha)}.` : ''
  ].join(' ');
  const ring = (p, txt) => `<svg viewBox="0 0 42 42" aria-hidden="true"><circle cx="21" cy="21" r="16" fill="none" stroke="var(--line)" stroke-width="5"/><circle cx="21" cy="21" r="16" fill="none" stroke="var(--sea-2)" stroke-width="5" stroke-linecap="round" stroke-dasharray="${p * 1.005} 100.5" transform="rotate(-90 21 21)"/><text x="21" y="23.5" text-anchor="middle" font-size="8" font-weight="800" fill="currentColor" font-family="Manrope, sans-serif">${txt}</text></svg>`;
  // Presupuesto del próximo acto: las tres partidas mayores y el resto
  let bud = '';
  if (sig){
    const ps = (sig.partidas || []).map(p => ({c:p.concepto, v:num(p.previsto)})).filter(p => p.v > 0).sort((a, b) => b.v - a.v);
    const tot = ps.reduce((s, p) => s + p.v, 0);
    const seg = ps.slice(0, 3); const resto = tot - seg.reduce((s, p) => s + p.v, 0); if (resto > 0) seg.push({c:'Resto', v:resto});
    const cols = ['var(--navy)', 'var(--sea-3)', '#c9b48f', 'var(--line-2)'];
    bud = tot ? `<button class="bx b-bud" data-open-ev="${sig.id}"><div><div class="lbl">Presupuesto de «${esc(sig.nombre || 'Sin título')}»</div><div class="num">${new Intl.NumberFormat('es-ES', {style:'currency', currency:'EUR', maximumFractionDigits:0}).format(tot)}</div></div>
      <div><div class="stack">${seg.map((p, i) => `<i style="width:${p.v / tot * 100}%;background:${cols[i]}" title="${esc(p.c)}: ${eur(p.v)}"></i>`).join('')}</div>
      <div class="leg">${seg.map((p, i) => `<span><i style="background:${cols[i]}"></i>${esc(p.c)}</span>`).join('')}</div></div></button>`
    : `<button class="bx b-bud" data-open-ev="${sig.id}"><div class="lbl">Presupuesto</div><div class="num">—</div><span class="small muted">Añade las partidas previstas en «${esc(sig.nombre || 'el evento')}» para verlas aquí.</span></button>`;
  } else bud = `<button class="bx b-bud" data-view-go="packs"><div class="lbl">Presupuesto</div><div class="num">—</div><span class="small muted">Elige un pack para tener un presupuesto de partida.</span></button>`;
  const provs = provTodos();
  const top = [...provs].sort((a, b) => (b.val || 0) - (a.val || 0)).slice(0, 4);
  const avc = [['#dfe9e6','#3f6266'],['#efe4d3','#6b5236'],['#e6e3ef','#4f4a73'],['#e3ebe0','#3f6a45']];
  const ini = n => String(n || '').replace(/[^\p{L}\s&]/gu, '').split(/\s+/).filter(Boolean).slice(0, 2).map(w => w[0].toUpperCase()).join('');
  const pz = conv ? plazoInfo(conv) : null;
  const orden = conv ? (conv.orden || '').split('\n').map(x => x.trim()).filter(Boolean).slice(0, 4) : [];
  v.innerHTML = `
  <div class="bento">
    <section class="hero"><div><div class="eyebrow">Panel de control</div><h1>${saludo}.</h1><p>${resumen}</p></div>
      <div class="btns"><button class="sun" data-act="new-ev">+ Nuevo evento</button><button data-view-go="packs">Contratar un pack</button><button data-view-go="guia">Guía y ejemplos</button></div>
      <svg class="wave" viewBox="0 0 1200 42" preserveAspectRatio="none" aria-hidden="true"><path d="M0 26 C200 0 400 42 600 22 S1000 6 1200 24 V42 H0z" fill="#ffffff14"/><path d="M0 34 C240 14 460 42 700 30 S1040 18 1200 32 V42 H0z" fill="#ffffff1f"/></svg></section>
    ${sig ? `<button class="bx b-next" data-open-ev="${sig.id}"><div class="img">${sceneSVG(escenaDe(sig.tipo))}</div><div class="ov"><div class="date-chip">${+sig.fecha.slice(8, 10)}<small>${mes(sig.fecha)}</small></div>
      <div><b>${esc(sig.nombre || 'Sin título')}</b><span class="meta">${esc(sig.lugar || sig.tipo || '')}${sig.lugar || sig.tipo ? ' · ' : ''}${cuando(sig.fecha)} · ${avance(sig)} % preparado</span><div class="bar"><i style="width:${avance(sig)}%"></i></div></div></div></button>`
    : `<div class="bx b-empty"><div class="lbl">Próximo acto</div><b>Aún no hay actos con fecha futura.</b><span class="small muted">Crea el primero o elige un pack del catálogo.</span><button class="small primary" data-act="new-ev" style="margin-top:8px">Nuevo evento</button></div>`}
    <button class="bx b-task" data-view-go="eventos"><div class="num">${pend}</div><div class="lbl">${pend === 1 ? 'tarea pendiente' : 'tareas pendientes'}</div><span class="b-arrow">${ico('arrow')}</span></button>
    <button class="bx b-succ" data-view-go="evaluacion">${ring(evals.length ? media : 0, evals.length ? pct(media) : '—')}<div class="lbl">éxito medio${evals.length ? ` · ${evals.length} ${evals.length === 1 ? 'acto' : 'actos'}` : ''}</div></button>
    ${bud}
    <button class="bx b-prov" data-view-go="proveedores"><div class="num">${provs.length}</div><div class="lbl">proveedores en Mallorca</div><div class="avs">${top.map((p, i) => `<span style="background:${avc[i][0]};color:${avc[i][1]}" title="${esc(p.n)}">${esc(ini(p.n))}</span>`).join('')}</div></button>
    ${conv ? `<button class="bx b-conv" data-view-go="convocatorias"><div class="lbl">Próxima reunión</div><div class="calx"><small>${mes(conv.fecha).toUpperCase()}</small><div class="num">${+conv.fecha.slice(8, 10)}</div></div>
      <b>${esc(conv.organo || 'Reunión')}${conv.entidad ? ' · ' + esc(conv.entidad) : ''}</b>${pz && pz.estado ? `<span class="pill ${pz.estado}" style="align-self:flex-start">${pz.estado === 'ok' ? '✓ Plazo legal cumplido' : pz.estado === 'bad' ? 'Fuera de plazo' : 'Revisa el plazo'}</span>` : ''}
      ${orden.length ? `<ol>${orden.map(o => `<li>${esc(o)}</li>`).join('')}</ol>` : ''}</button>`
    : `<button class="bx b-conv" data-view-go="convocatorias"><div class="lbl">Próxima reunión</div><b>No hay reuniones convocadas.</b><span class="small muted">Prepara una convocatoria con el plazo legal de cada órgano.</span></button>`}
    <section class="bx b-quick"><h2>Accesos rápidos</h2>${[['precedencia','flag','Precedencias y mesas',0],['invitaciones','mail','Invitaciones',1],['actas','doc','Actas y presupuestos',2],['tratamientos','star','Tratamientos',1],['noticias','news','Analizar noticia',0],['evaluacion','chart','Evaluar un acto',3],['catalogo','box','Tipos de evento',2]].map(([id, i, l, c]) => `<button class="qchip" data-view-go="${id}"><span style="background:${avc[c][0]};color:${avc[c][1]}">${ico(i)}</span>${l}</button>`).join('')}</section>
  </div>
  ${prox.length > 1 ? `<section><div class="row between"><h2>Más actos en marcha</h2><button class="small" data-view-go="eventos">Ver todos</button></div><div class="ev-cards">${prox.slice(1, 7).map(e => `<button class="ev-card" data-open-ev="${e.id}"><div class="img">${sceneSVG(escenaDe(e.tipo))}<div class="date-chip">${+e.fecha.slice(8, 10)}<small>${mes(e.fecha)}</small></div></div>
      <div class="body"><h3>${esc(e.nombre || 'Sin título')}</h3><span class="small muted">${esc(e.lugar || e.tipo || '')} · ${esc(e.estado || 'Idea')}</span><div class="bar" title="Lista de control: ${avance(e)}%"><i style="width:${avance(e)}%"></i></div></div></button>`).join('')}</div></section>` : ''}`;
}
""")
io.open(P, 'w', encoding='utf-8', newline='\n').write(s)
print('ok')
