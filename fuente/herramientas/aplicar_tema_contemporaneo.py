"""Aplica la interfaz «Sereno contemporáneo» a fuente/gestor-protocolo.html: una sola tipografía, bloques claros sobre gris cálido y un bloque oscuro para el próximo acto.
Uso: python fuente/herramientas/aplicar_tema_contemporaneo.py   (solo se ejecuta una vez; comprueba que cada cambio encaja exactamente)."""
import io, os
P = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'gestor-protocolo.html')
s = io.open(P, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    assert c == n, (c, old[:90])
    s = s.replace(old, new)
def between(a, b, new):
    global s
    i = s.index(a); j = s.index(b, i)
    s = s[:i] + new + s[j:]

# Tipografía y paleta
rep("family=Fraunces:opsz,wght@9..144,500;9..144,600;9..144,700&family=Manrope:wght@400;500;600;700&family=IBM+Plex+Mono", "family=Instrument+Sans:wght@400;500;600;700&family=IBM+Plex+Mono")
between(':root{\n  --paper:', '  --f-display:', """:root{
  --paper:#ecebe6; --sheet:#fbfaf7; --ink:#191b1a; --ink-2:#5c605d; --line:#e2e0d9; --line-2:#cfcdc5;
  --accent:#1f2523; --accent-soft:#e4e3dc; --gold:#7a6340; --gold-soft:#ece6d9; --sun:#bfa97f;
  --navy:#1f2523; --navy-ink:#f4f2ec; --sea-2:#1f2523; --sea-3:#1f2523; --terra:#8d7a63; --sand:#e4e3dc; --sage:#e4e3dc;
  --ok:#2f6b4f; --ok-soft:#e0e7e0; --warn:#8a5c14; --warn-soft:#efe6d3; --bad:#a63a32; --bad-soft:#f3e0dc;
""")
rep('--f-display:"Fraunces", Georgia, "Times New Roman", serif;', '--f-display:"Instrument Sans", system-ui, -apple-system, "Segoe UI", sans-serif;')
rep('--f-body:"Manrope", system-ui, -apple-system, "Segoe UI", sans-serif;', '--f-body:"Instrument Sans", system-ui, -apple-system, "Segoe UI", sans-serif;')
rep("--r:14px; --shadow:0 1px 2px rgba(36,48,47,.04), 0 6px 20px rgba(36,48,47,.05);", "--r:14px; --shadow:none;")
rep("h1,h2,h3{font-family:var(--f-display);text-wrap:balance;margin:0;font-weight:600;line-height:1.2}", "h1,h2,h3{font-family:var(--f-display);text-wrap:balance;margin:0;font-weight:500;line-height:1.15;letter-spacing:-.02em}")
rep("h1{font-size:2.2rem;font-weight:500;letter-spacing:-.01em}", "h1{font-size:2.5rem;letter-spacing:-.04em;line-height:1.05}")
rep(".card{background:var(--sheet);border:1px solid var(--line);border-radius:var(--r);padding:20px", ".card{background:var(--sheet);border:1px solid transparent;border-radius:20px;padding:20px")
rep("padding:8px 16px;border-radius:999px;font-weight:600;", "padding:9px 16px;border-radius:12px;font-weight:600;")
rep(".kpi .v{font-family:var(--f-display);font-size:2.1rem;font-weight:500;", ".kpi .v{font-family:var(--f-display);font-size:2.4rem;font-weight:400;letter-spacing:-.04em;")
rep(".bar > i{display:block;height:100%;background:linear-gradient(90deg,var(--sea-2),var(--sea-3))}", ".bar > i{display:block;height:100%;background:var(--navy)}")
rep(".pack-img svg,.pack-img img{display:block;width:100%;height:100%;object-fit:cover}", ".pack-img svg,.pack-img img{display:block;width:100%;height:100%;object-fit:cover}\n.pack-img svg{filter:saturate(.5)}")
# Las invitaciones son papelería: conservan una letra con serifas
rep("padding:34px 30px;font-family:var(--f-display);", 'padding:34px 30px;font-family:Georgia,"Times New Roman",serif;')

# Barra superior flotante
between('.topbar{', '.topbar-in{', """.topbar{position:sticky;top:env(safe-area-inset-top,0px);z-index:20;padding-block:12px 0;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
""")
rep(".topbar-in{max-width:1180px;margin:0 auto;display:flex;align-items:center;gap:8px 22px;flex-wrap:wrap}", ".topbar-in{max-width:1180px;margin:0 auto;display:flex;align-items:center;gap:6px 22px;flex-wrap:wrap;background:var(--sheet);border-radius:14px;padding:9px 12px 9px 18px;box-shadow:0 1px 0 rgba(25,27,26,.05)}")
rep(".brand{font-family:var(--f-display);font-size:1.3rem;font-weight:600;line-height:1.15;color:var(--accent);margin:0}", ".brand{font-size:1.05rem;font-weight:600;letter-spacing:-.02em;line-height:1.15;color:var(--ink);margin:0}\n.av{width:32px;height:32px;flex:none;border-radius:10px;background:var(--navy);color:var(--navy-ink);display:grid;place-items:center;font-weight:600;font-size:.74rem}")
rep(".nav-list{display:flex;flex:1;min-width:0;flex-wrap:nowrap;gap:2px;align-items:center;overflow-x:auto;scrollbar-width:none}", ".nav-list{display:flex;flex:1;min-width:0;flex-wrap:nowrap;gap:4px;align-items:center;justify-content:safe center;overflow-x:auto;scrollbar-width:none}")
rep(".nav-list a:hover{background:var(--accent-soft);color:var(--accent)}", ".nav-list a:hover{color:var(--ink)}")
rep(".nav-list a.on{background:var(--accent);color:#fff}", ".nav-list a.on{color:var(--ink);font-weight:700}")
rep(".guide{border:1px solid var(--line);border-left:4px solid var(--sun);", ".guide{border:1px solid transparent;border-left:4px solid var(--sun);")
rep('<div class="brand">Gabinete de Protocolo</div>\n    <nav class="nav-list" id="nav" aria-label="Apartados"></nav>', '<div class="brand">Gabinete</div>\n    <nav class="nav-list" id="nav" aria-label="Apartados"></nav>\n    <div class="av" id="av" hidden></div>')
rep("  $('#subnav').innerHTML = grupo ?", "  try { const md = SB_USER?.user_metadata || {}; const ini = String(md.full_name || md.name || SB_USER?.email || '').split(/\\s+/).filter(Boolean).slice(0, 2).map(w => w[0].toUpperCase()).join(''); $('#av').textContent = ini; $('#av').hidden = !ini; } catch {}\n  $('#subnav').innerHTML = grupo ?")

# Panel
between('.bento{display:grid;', '.verdict{', """.p-hl{display:flex;align-items:flex-end;justify-content:space-between;gap:20px;flex-wrap:wrap;padding:12px 4px 0}
.p-hl h1{font-size:3.5rem;letter-spacing:-.045em;line-height:1}
.p-hl p{margin:10px 0 0;color:var(--ink-2);font-size:1rem;max-width:62ch}
.p-hl .btns{display:flex;gap:8px;flex-wrap:wrap}
.p-gr{display:grid;grid-template-columns:repeat(12,minmax(0,1fr));gap:12px;margin-top:-8px}
.pt{background:var(--sheet);border:0;border-radius:20px;padding:18px;min-width:0;position:relative;overflow:hidden;display:flex;flex-direction:column;align-items:stretch;gap:0;text-align:left;white-space:normal;font-weight:400;color:var(--ink);font-size:inherit}
button.pt{cursor:pointer;transition:transform .16s ease}
button.pt:hover{transform:translateY(-2px)}
.pt .lb{font-size:.82rem;color:var(--ink-2);font-weight:500}
.p-fe{grid-column:span 7;min-height:326px;background:var(--navy);color:#f4f2ec;justify-content:space-between;padding:24px}
.p-fe .im{position:absolute;inset:0 0 0 34%;filter:saturate(.35) brightness(.9)}
.p-fe .im svg{display:block;width:100%;height:100%}
.p-fe::after{content:"";position:absolute;inset:0;background:linear-gradient(90deg,#1f2523 34%,#1f252300 78%)}
.p-fe > div:not(.im){position:relative;z-index:1}
.p-fe .lb{color:#b9bdb8}
.p-dd{font-size:6.2rem;font-weight:500;letter-spacing:-.06em;line-height:.9;margin-top:10px}
.p-dd small{font-size:1.1rem;letter-spacing:-.01em;margin-left:8px;color:#b9bdb8}
.p-fe h3{font-size:1.45rem;letter-spacing:-.025em;max-width:22ch}
.p-fe p{margin:6px 0 12px;color:#b9bdb8;font-size:.86rem}
.p-ln{height:3px;max-width:260px;border-radius:2px;background:#ffffff2e}
.p-ln i{display:block;height:100%;background:#f4f2ec;border-radius:2px}
.p-empty{background:var(--sheet);color:var(--ink);justify-content:flex-end;gap:10px}
.p-empty::after{display:none}
.p-empty .lb{color:var(--ink-2)}
.p-empty h3{max-width:20ch}
.p-kp{grid-column:span 5;display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:12px}
.p-kp .pt{justify-content:space-between;gap:18px}
.p-kp b{font-size:3.1rem;font-weight:400;letter-spacing:-.05em;line-height:1}
.p-kp b.m{font-size:2.2rem}
.p-rn{grid-column:span 4;gap:10px}
.p-rn h3{font-size:1.3rem;letter-spacing:-.025em}
.p-rn ol{margin:auto 0 0;padding:0;list-style:none;font-size:.84rem;color:var(--ink-2)}
.p-rn li{padding:7px 0;border-top:1px solid var(--line)}
.p-ac{grid-column:span 8}
.p-row{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px;margin-top:12px}
.p-it{background:none;border:0;padding:0;display:block;text-align:left;white-space:normal;font-weight:400;min-width:0;color:var(--ink)}
.p-it .im{height:128px;border-radius:12px;overflow:hidden;filter:saturate(.45)}
.p-it .im svg{display:block;width:100%;height:100%}
.p-it b{display:block;margin-top:9px;font-size:.92rem;font-weight:600;letter-spacing:-.01em}
.p-it span{font-size:.8rem;color:var(--ink-2)}
.p-ql{display:flex;flex-wrap:wrap;gap:6px 26px;padding:6px 4px 0}
.p-ql button{background:none;border:0;padding:4px 0;font-size:.9rem;font-weight:500;color:var(--ink)}
.p-ql button:hover{text-decoration:underline;text-underline-offset:3px}
.p-ql svg{width:13px;height:13px;fill:none;stroke:var(--ink-2);stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round}
@media (max-width:900px){
  .p-hl h1{font-size:2.5rem}
  .p-fe,.p-kp,.p-rn,.p-ac{grid-column:1/-1}
  .p-fe .im{inset:0 0 0 20%}
  .p-fe::after{background:linear-gradient(0deg,#1f2523 42%,#1f252300 88%),linear-gradient(90deg,#1f2523 22%,#1f252300 70%)}
  .p-empty::after{display:none}
}
@media (max-width:600px){.p-row{grid-template-columns:minmax(0,1fr)}.p-it .im{height:150px}}
""")
between("function renderPanel(v){", "document.addEventListener('click', e => {\n  const g = e.target.closest('[data-view-go]')", r"""function renderPanel(v){
  const evs = Store.data.eventos;
  const now = today();
  const prox = evs.filter(e => e.fecha && e.fecha >= now && e.estado !== 'Cancelado').sort((a, b) => a.fecha.localeCompare(b.fecha));
  const pend = evs.reduce((s, e) => s + (e.checklist || []).filter(c => !c.ok).length, 0);
  const evals = Store.data.evaluaciones.map(calcEval).filter(r => r.indice > 0);
  const media = evals.length ? evals.reduce((s, r) => s + r.indice, 0) / evals.length : 0;
  const hora = new Date().getHours();
  let nombre = ''; try { const md = SB_USER?.user_metadata || {}; nombre = String(md.full_name || md.name || '').trim().split(/\s+/)[0] || ''; } catch {}
  const saludo = (hora < 14 ? 'Buenos días' : hora < 21 ? 'Buenas tardes' : 'Buenas noches') + (nombre ? ', ' + esc(nombre) : '');
  const dias = f => Math.round((new Date(f + 'T00:00') - new Date(now + 'T00:00')) / 864e5);
  const cuando = f => { const d = dias(f); return d === 0 ? 'hoy' : d === 1 ? 'mañana' : `en ${d} días`; };
  const avance = e => { const ch = e.checklist || []; return ch.length ? Math.round(ch.filter(c => c.ok).length / ch.length * 100) : 0; };
  const fmes = (f, m) => new Date(f + 'T00:00').toLocaleDateString('es-ES', {month:m}).replace('.', '');
  const sig = prox[0];
  const conv = Store.data.convocatorias.filter(c => c.fecha && c.fecha >= now).sort((a, b) => a.fecha.localeCompare(b.fecha))[0];
  const resumen = prox.length ? `${prox.length} ${prox.length === 1 ? 'acto' : 'actos'} en marcha y ${pend === 1 ? '1 tarea' : pend + ' tareas'} por cerrar.` : 'Empieza por un pack o crea un evento desde cero.';
  const tot = sig ? (sig.partidas || []).reduce((s, p) => s + num(p.previsto), 0) : 0;
  const provs = provTodos();
  const pz = conv ? plazoInfo(conv) : null;
  const orden = conv ? (conv.orden || '').split('\n').map(x => x.trim()).filter(Boolean).slice(0, 3) : [];
  const mas = prox.slice(1, 4);
  const tile = (go, lb, val, cls = '') => `<button class="pt" data-view-go="${go}"><span class="lb">${lb}</span><b class="${cls}">${val}</b></button>`;
  v.innerHTML = `
  <header class="p-hl"><div><h1>${saludo}.</h1><p>${resumen}</p></div>
    <div class="btns"><button class="ghost" data-view-go="packs">Contratar un pack</button><button class="primary" data-act="new-ev">+ Nuevo evento</button></div></header>
  <div class="p-gr">
    ${sig ? `<button class="pt p-fe" data-open-ev="${sig.id}"><div class="im">${sceneSVG(escenaDe(sig.tipo))}</div><div><div class="lb">Próximo acto</div><div class="p-dd">${+sig.fecha.slice(8, 10)}<small>${fmes(sig.fecha, 'long')}</small></div></div>
      <div><h3>${esc(sig.nombre || 'Sin título')}</h3><p>${sig.lugar ? esc(sig.lugar) + ' · ' : ''}${cuando(sig.fecha)} · ${avance(sig)} % preparado</p><div class="p-ln"><i style="width:${avance(sig)}%"></i></div></div></button>`
    : `<div class="pt p-fe p-empty"><div class="lb">Próximo acto</div><h3>Aún no hay actos con fecha futura.</h3><div><button class="primary" data-act="new-ev">Crear el primero</button></div></div>`}
    <div class="p-kp">
      ${tile('eventos', pend === 1 ? 'Tarea pendiente' : 'Tareas pendientes', pend)}
      ${tile('evaluacion', 'Éxito medio', evals.length ? pct(media) : '—')}
      ${tile('proveedores', 'Proveedores en Mallorca', provs.length)}
      ${sig && tot ? `<button class="pt" data-open-ev="${sig.id}"><span class="lb">Presupuesto del próximo acto</span><b class="m">${new Intl.NumberFormat('es-ES', {style:'currency', currency:'EUR', maximumFractionDigits:0}).format(tot)}</b></button>` : tile('packs', 'Presupuesto del próximo acto', '—')}
    </div>
    ${conv ? `<button class="pt p-rn" data-view-go="convocatorias"><span class="lb">Próxima reunión · ${fdate(conv.fecha)}</span><h3>${esc(conv.organo || 'Reunión')}${conv.entidad ? ' · ' + esc(conv.entidad) : ''}</h3>${pz && pz.estado ? `<span class="pill ${pz.estado}" style="align-self:flex-start">${pz.estado === 'ok' ? 'Plazo legal cumplido' : pz.estado === 'bad' ? 'Fuera de plazo' : 'Revisa el plazo'}</span>` : ''}${orden.length ? `<ol>${orden.map(o => `<li>${esc(o)}</li>`).join('')}</ol>` : ''}</button>`
    : `<button class="pt p-rn" data-view-go="convocatorias"><span class="lb">Próxima reunión</span><h3>No hay reuniones convocadas.</h3><span class="small muted">Prepara una convocatoria con el plazo legal de cada órgano.</span></button>`}
    <section class="pt p-ac"><div class="row between"><span class="lb">${mas.length ? 'Más actos en marcha' : 'Packs para empezar'}</span><button class="small ghost" data-view-go="${mas.length ? 'eventos' : 'packs'}">Ver todos</button></div><div class="p-row">
      ${mas.length ? mas.map(e => `<button class="p-it" data-open-ev="${e.id}"><div class="im">${sceneSVG(escenaDe(e.tipo))}</div><b>${esc(e.nombre || 'Sin título')}</b><span>${+e.fecha.slice(8, 10)} ${fmes(e.fecha, 'short')} · ${esc(e.estado || 'Idea')}</span></button>`).join('')
      : ['boda-premium', 'cena-gala', 'congreso'].map(id => PACKS.find(p => p.id === id)).map(p => `<button class="p-it" data-view-go="packs"><div class="im">${sceneSVG(p.escena)}</div><b>${esc(p.nombre)}</b><span>${esc(p.tipo)}</span></button>`).join('')}
    </div></section>
  </div>
  <nav class="p-ql" aria-label="Accesos rápidos">${[['precedencia','Precedencias y mesas'],['invitaciones','Invitaciones'],['actas','Actas y presupuestos'],['tratamientos','Tratamientos'],['noticias','Analizar noticia'],['evaluacion','Evaluar un acto'],['guia','Guía y ejemplos']].map(([id, l]) => `<button data-view-go="${id}">${l}${ico('arrow')}</button>`).join('')}</nav>`;
}
""")
io.open(P, 'w', encoding='utf-8', newline='\n').write(s)
print('ok')
