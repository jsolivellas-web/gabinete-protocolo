"""Lleva al programa las interacciones del ejemplo «Vivo»: pulsación, avisos apilados, buscador, menú de cuenta, hoja deslizante del acto y mantener para borrar.
Uso: python fuente/herramientas/aplicar_interaccion.py   (solo se ejecuta una vez; comprueba que cada cambio encaja exactamente)."""
import io, os, re
P = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'gestor-protocolo.html')
s = io.open(P, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    assert c == n, (c, old[:90])
    s = s.replace(old, new)

# Curvas y pulsación
rep("  color-scheme:light;\n", "  color-scheme:light;\n  --e-out:cubic-bezier(.23,1,.32,1); --e-inout:cubic-bezier(.77,0,.175,1); --e-drawer:cubic-bezier(.32,.72,0,1);\n")
rep("button:hover{border-color:var(--ink-2)}", """@media (hover:hover) and (pointer:fine){button:hover{border-color:var(--ink-2)}}
button,.btn,.chip{transition:transform 160ms var(--e-out);touch-action:manipulation;-webkit-tap-highlight-color:transparent}
button:active:not(:disabled),.btn:active,.chip:active{transform:scale(.97)}""")
rep("button.ghost:hover{color:var(--ink);background:var(--paper)}", "@media (hover:hover) and (pointer:fine){button.ghost:hover{color:var(--ink);background:var(--paper)}}")
rep("button.pt{cursor:pointer;transition:transform .16s ease}\nbutton.pt:hover{transform:translateY(-2px)}", "button.pt{cursor:pointer}\nbutton.pt:active:not(:disabled){transform:scale(.985)}")
rep(".p-ql button:hover{text-decoration:underline;text-underline-offset:3px}", "@media (hover:hover) and (pointer:fine){.p-ql button:hover{text-decoration:underline;text-underline-offset:3px}}")

# Avisos apilados
s = re.sub(r"\.toast\{position:fixed;[^\n]*\n", """.ts{position:fixed;z-index:50;right:max(16px,env(safe-area-inset-right,0px));bottom:calc(16px + env(safe-area-inset-bottom,0px));width:min(340px,calc(100vw - 32px));height:60px}
.ts::before{content:"";position:absolute;inset:-130px 0 0}
.ts:empty{display:none}
.to{position:absolute;left:0;right:0;bottom:0;min-height:52px;background:var(--navy);color:var(--navy-ink);border-radius:13px;padding:10px 14px;font-size:.88rem;display:flex;align-items:center;justify-content:space-between;gap:10px;transform:translateY(calc(var(--n)*-9px)) scale(calc(1 - var(--n)*.05));transform-origin:bottom center;transition:transform 380ms ease,opacity 380ms ease;z-index:calc(10 - var(--n))}
.to.ini,.to.fin{transform:translateY(100%);opacity:0}
.to.fin{transition-duration:200ms}
.to.ocu{opacity:0}
.ts:hover .to{transform:translateY(calc(var(--n)*-62px))}
.to button{border:0;background:#ffffff1f;color:inherit;border-radius:8px;padding:4px 9px;font-size:.78rem}
""", s, count=1)
rep("function toast(msg){ const t = document.createElement('div'); t.className = 'toast'; t.textContent = msg; document.body.append(t); setTimeout(() => t.remove(), 2600); }",
r"""// Avisos apilados: se pausan al pasar el ratón o al cambiar de pestaña. accion = {label, fn} añade un botón, p. ej. Deshacer.
let avisos = [];
function capaAvisos(){
  let c = $('#ts'); if (c) return c;
  c = document.createElement('div'); c.id = 'ts'; c.className = 'ts'; c.setAttribute('aria-live', 'polite'); document.body.append(c);
  c.addEventListener('pointerenter', pausaAvisos); c.addEventListener('pointerleave', sigueAvisos);
  return c;
}
function pintaAvisos(){ avisos.forEach((t, i) => { const n = avisos.length - 1 - i; t.el.style.setProperty('--n', n); t.el.classList.toggle('ocu', n > 2); }); }
function quitaAviso(t){ clearTimeout(t.id); avisos = avisos.filter(x => x !== t); t.el.classList.add('fin'); pintaAvisos(); setTimeout(() => t.el.remove(), 220); }
function pausaAvisos(){ avisos.forEach(t => { clearTimeout(t.id); t.resta = Math.max(800, t.resta - (Date.now() - t.ini)); }); }
function sigueAvisos(){ avisos.forEach(t => { t.ini = Date.now(); t.id = setTimeout(() => quitaAviso(t), t.resta); }); }
function toast(msg, accion){
  const el = document.createElement('div'); el.className = 'to ini'; el.innerHTML = `<span>${esc(msg)}</span>${accion ? `<button>${esc(accion.label)}</button>` : ''}`;
  el.style.setProperty('--n', 0); capaAvisos().append(el);
  const t = {el, resta:accion ? 7000 : 4000, ini:Date.now(), id:0}; avisos.push(t); el.offsetHeight; el.classList.remove('ini'); pintaAvisos();
  if (accion) $('button', el).addEventListener('click', () => { quitaAviso(t); accion.fn(); });
  t.id = setTimeout(() => quitaAviso(t), t.resta);
}
document.addEventListener('visibilitychange', () => document.hidden ? pausaAvisos() : sigueAvisos());""")

# Mantener para borrar en todas las fichas
s, n = re.subn(r'class="ghost danger" data-del-(ev|acta|eval|conv)>', r'class="ghost danger hold" data-hold="Borrar" data-del-\1>', s)
assert n == 4, n
s, n = re.subn(r'function confirmBox\((\w+), (\w+)([^)]*)\)\s*\{', lambda m: m.group(0) + f' if (UI.holdOk){{ {m.group(2)}(); return; }}', s)
assert n == 1, n

CSS = """.hold{position:relative;overflow:hidden;user-select:none;-webkit-user-select:none}
.hold::after{content:attr(data-hold);position:absolute;inset:0;background:var(--bad);color:#fff;display:grid;place-items:center;clip-path:inset(0 100% 0 0);transition:clip-path 200ms var(--e-out)}
.hold.on::after{clip-path:inset(0 0 0 0);transition:clip-path 2s linear}
/* Barra: buscador y menú de cuenta */
.topbar-in{position:relative}
.find{border:0;background:var(--paper);color:var(--ink-2);border-radius:10px;padding:7px 10px;font-size:.8rem;font-weight:500}
.find kbd{font:inherit;font-size:.7rem;font-weight:600}
button.av{border:0;padding:0}
.nav-list a[data-logout]{display:none}
.pop{position:absolute;right:12px;top:calc(100% + 6px);z-index:25;width:230px;background:var(--sheet);border-radius:12px;padding:5px;box-shadow:0 10px 32px rgba(25,27,26,.16),0 0 0 1px rgba(25,27,26,.05);transform-origin:top right;opacity:0;transform:scale(.95);visibility:hidden;transition:opacity 120ms ease,transform 120ms var(--e-out),visibility 0s 120ms}
.pop.open{opacity:1;transform:none;visibility:visible;transition:opacity 180ms var(--e-out),transform 180ms var(--e-out)}
.pop div{padding:8px 10px;font-size:.78rem;color:var(--ink-2);overflow-wrap:anywhere}
.pop button{display:block;width:100%;text-align:left;border:0;background:none;border-radius:8px;padding:8px 10px;font-size:.86rem}
/* Buscador: sin animación, se abre muchas veces al día */
.cmd{position:fixed;inset:0;z-index:45;display:none;align-items:flex-start;justify-content:center;padding:12vh 12px 0;background:rgba(20,22,21,.32)}
.cmd.open{display:flex}
.cmd > div{width:min(520px,100%);background:var(--sheet);border-radius:14px;overflow:hidden;box-shadow:0 18px 50px rgba(25,27,26,.25)}
.cmd input{border:0;border-radius:0;border-bottom:1px solid var(--line);background:none;padding:14px 16px;font-size:1rem;outline:0}
.cmd ul{list-style:none;margin:0;padding:5px;max-height:320px;overflow:auto}
.cmd li{padding:9px 11px;border-radius:8px;font-size:.9rem;cursor:pointer;display:flex;justify-content:space-between;gap:12px}
.cmd li small{color:var(--ink-2)}
.cmd li.sel{background:var(--paper)}
.cmd li.no{color:var(--ink-2);cursor:default}
/* Hoja del acto */
.bk{position:fixed;inset:0;z-index:30;background:rgba(20,22,21,.42);opacity:0;visibility:hidden;transition:opacity 160ms ease,visibility 0s 160ms}
.bk.open{opacity:1;visibility:visible;transition:opacity 240ms ease}
.sh{position:fixed;z-index:31;left:50%;bottom:0;width:min(620px,100vw);max-height:min(640px,calc(100dvh - 40px));background:var(--sheet);border-radius:22px 22px 0 0;padding-bottom:env(safe-area-inset-bottom,0px);display:flex;flex-direction:column;visibility:hidden;transform:translate(-50%,100%);transition:transform 240ms var(--e-drawer),visibility 0s 240ms}
.sh.open{transform:translate(-50%,0);visibility:visible;transition:transform 420ms var(--e-drawer)}
.sh.drag{transition:none!important}
.sh:focus{outline:0}
.sh-hd{padding:10px 20px 12px;touch-action:none;user-select:none;-webkit-user-select:none;cursor:grab}
.sh-hd::before{content:"";display:block;width:40px;height:4px;border-radius:3px;background:var(--line-2);margin:0 auto 12px}
.sh-hd h3{font-size:1.35rem;letter-spacing:-.025em}
.sh-hd p{margin:3px 0 0;color:var(--ink-2);font-size:.86rem}
.sh-bd{padding:0 20px 16px;overflow:auto;flex:1;overscroll-behavior:contain}
.sh-tabs{position:relative;display:flex;gap:2px;background:var(--paper);border-radius:11px;padding:3px;margin-bottom:12px}
.sh-tabs .cp{position:absolute;inset:3px;display:flex;gap:2px;background:var(--navy);border-radius:9px;pointer-events:none;transition:clip-path 240ms var(--e-inout)}
.sh-tab{flex:1;border:0;background:none;padding:7px 6px;font-weight:600;font-size:.84rem;color:var(--ink-2);text-align:center;border-radius:9px}
.cp .sh-tab{color:var(--navy-ink)}
.sh-it{display:flex;align-items:center;gap:10px;padding:8px 0;border-top:1px solid var(--line);font-size:.9rem}
.sh-it:first-child{border-top:0}
.sh-it input{width:17px;height:17px;margin:0;flex:none;accent-color:#1f2523}
.sh-it input:checked + span{opacity:.5}
.sh-it .d{margin-left:auto;color:var(--ink-2);white-space:nowrap}
.sh-ft{display:flex;gap:8px;justify-content:flex-end;padding:12px 20px 16px;border-top:1px solid var(--line);flex-wrap:wrap}
.sh-ft .hold{margin-right:auto;color:var(--bad)}
/* Entrada del Panel y de los diálogos */
@keyframes sube{from{opacity:0;transform:translateY(8px)}}
#view.in .p-hl,#view.in .p-fe,#view.in .p-kp > *,#view.in .p-rn,#view.in .p-ac,#view.in .p-ql{animation:sube 320ms var(--e-out) backwards}
#view.in .p-fe{animation-delay:45ms}
#view.in .p-kp > :nth-child(1){animation-delay:90ms}
#view.in .p-kp > :nth-child(2){animation-delay:135ms}
#view.in .p-kp > :nth-child(3){animation-delay:180ms}
#view.in .p-kp > :nth-child(4){animation-delay:225ms}
#view.in .p-rn{animation-delay:270ms}
#view.in .p-ac{animation-delay:315ms}
#view.in .p-ql{animation-delay:360ms}
.p-row.rev .im{clip-path:inset(0 0 100% 0)}
.p-row.rev.ver .im{clip-path:inset(0 0 0 0);transition:clip-path 620ms var(--e-inout)}
.p-row.rev.ver .p-it:nth-child(2) .im{transition-delay:70ms}
.p-row.rev.ver .p-it:nth-child(3) .im{transition-delay:140ms}
.modal-bg{transition:opacity 200ms ease}
.modal{transition:opacity 200ms var(--e-out),transform 200ms var(--e-out)}
@starting-style{.modal-bg{opacity:0}.modal{opacity:0;transform:scale(.96)}}
@media (max-width:900px){
  .find{margin-left:auto}.find kbd{display:none}
  .nav-list{order:5}.subnav{order:6}
}
@media (prefers-reduced-motion:reduce){
  button:active:not(:disabled),.btn:active,.chip:active,button.pt:active:not(:disabled){transform:none}
  #view.in *{animation:none!important}
  .p-row.rev .im{clip-path:none}
  .sh{opacity:0;transform:translate(-50%,0);transition:opacity 160ms ease,visibility 0s 160ms}
  .sh.open{opacity:1;transition:opacity 160ms ease}
  .to,.to.ini,.to.fin{transform:none}
}
.verdict{"""
rep(".verdict{", CSS)

# Barra superior
rep('<div class="av" id="av" hidden></div>', '''<button class="find" id="find" aria-label="Buscar">Buscar <kbd>Ctrl K</kbd></button>
    <button class="av" id="av" aria-haspopup="menu" aria-expanded="false" aria-label="Cuenta" hidden></button>
    <div class="pop" id="pop" role="menu"></div>''')

# Panel: revelar imágenes y abrir la hoja
rep('<div class="p-row">', '''<div class="p-row${UI.revelado ? '' : ' rev'}">''')
rep("""${ico('arrow')}</button>`).join('')}</nav>`;\n}""", """${ico('arrow')}</button>`).join('')}</nav>`;\n  revela();\n}""")
rep("if (o && UI.view === 'panel'){ UI.evento = clone(Store.get('eventos', o.dataset.openEv)); go('eventos'); }", "if (o && UI.view === 'panel'){ abreFicha(o.dataset.openEv); }")
rep("  const v = $('#view'); v.onclick = null;\n", "  const v = $('#view'); v.onclick = null;\n  v.classList.remove('in');\n")
rep("[UI.view] || renderPanel)(v);\n}", "[UI.view] || renderPanel)(v);\n  if (UI.view === 'panel'){ v.offsetHeight; v.classList.add('in'); clearTimeout(UI.inT); UI.inT = setTimeout(() => v.classList.remove('in'), 900); }\n}")

JS = r"""/* ============================================================
   INTERACCIÓN: HOJA DEL ACTO, BUSCADOR, CUENTA Y BORRADO
   ============================================================ */
function revela(){
  const r = $('.p-row.rev'); if (!r) return;
  if (!window.IntersectionObserver || matchMedia('(prefers-reduced-motion: reduce)').matches){ r.classList.remove('rev'); return; }
  const io = new IntersectionObserver(es => { if (es.some(x => x.isIntersecting)){ UI.revelado = true; r.classList.add('ver'); io.disconnect(); } }, {rootMargin:'0px 0px -40px 0px'});
  io.observe(r);
}
// Borrar: al mantener pulsado se ofrece Deshacer. Con teclado sigue pidiendo confirmación.
const borraBase = Store.remove.bind(Store);
Store.remove = async (col, id) => {
  const conDeshacer = UI.holdOk, o = Store.get(col, id);
  await borraBase(col, id);
  if (conDeshacer && o) toast('Borrado', {label:'Deshacer', fn:async () => { await Store.save(col, o); render(); }});
};
let holdT = 0, holdEl = null;
const sueltaHold = () => { clearTimeout(holdT); holdEl?.classList.remove('on'); holdEl = null; };
document.addEventListener('pointerdown', e => {
  const b = e.target.closest?.('[data-hold]'); if (!b || e.button) return;
  holdEl = b; b.classList.add('on');
  holdT = setTimeout(() => { sueltaHold(); UI.trasHold = true; UI.holdOk = true; b.dataset.listo = '1'; b.click(); UI.holdOk = false; }, 2000);
});
document.addEventListener('pointerup', () => { sueltaHold(); setTimeout(() => { UI.trasHold = false; }); });
document.addEventListener('pointercancel', sueltaHold);
document.addEventListener('pointerout', e => { if (holdEl && e.target === holdEl) sueltaHold(); });
document.addEventListener('contextmenu', e => { if (e.target.closest?.('[data-hold]')) e.preventDefault(); });
document.addEventListener('click', e => {
  const b = e.target.closest?.('[data-hold]'); if (!b) return;
  if (b.dataset.listo){ delete b.dataset.listo; return; }
  if (UI.trasHold){ e.stopImmediatePropagation(); return; }
  if (e.detail > 0){ e.stopImmediatePropagation(); e.preventDefault(); toast('Mantén pulsado 2 segundos para borrar'); }
}, true);

// Hoja del acto: vista rápida desde el Panel. Las tareas se guardan al marcarlas.
document.body.insertAdjacentHTML('beforeend', `<div class="bk" id="bk"></div><section class="sh" id="sh" role="dialog" aria-modal="true" aria-labelledby="sh-t" tabindex="-1"></section>
  <div class="cmd" id="cmd"><div role="dialog" aria-label="Buscar"><input id="cmd-q" placeholder="Buscar un apartado o un acto…" aria-label="Buscar"><ul id="cmd-res"></ul></div></div>`);
const SH_TABS = ['Tareas', 'Presupuesto', 'Invitados'];
const sh = $('#sh'), bk = $('#bk');
const Ficha = {ev:null, n:0, origen:null, dr:null};
function fichaPanel(ev, n){
  if (n === 0) return (ev.checklist || []).length ? ev.checklist.map((c, i) => `<label class="sh-it"><input type="checkbox" data-c="${i}" ${c.ok ? 'checked' : ''}><span>${esc(c.t)}</span></label>`).join('') : '<p class="small muted">Este acto no tiene lista de control.</p>';
  if (n === 1){ const ps = (ev.partidas || []).filter(p => num(p.previsto) > 0); return ps.length ? ps.map(p => `<div class="sh-it"><span>${esc(p.concepto)}</span><span class="d">${eur(num(p.previsto))}</span></div>`).join('') + `<div class="sh-it"><b>Total previsto</b><b class="d">${eur(ps.reduce((s, p) => s + num(p.previsto), 0))}</b></div>` : '<p class="small muted">Aún no hay partidas con importe previsto.</p>'; }
  const inv = ev.invitados || []; return inv.length ? inv.map(p => `<div class="sh-it"><span>${esc(p.nombre || 'Sin nombre')}</span><span class="d">${esc(p.rsvp || 'Pendiente')}</span></div>`).join('') : '<p class="small muted">Aún no hay invitados.</p>';
}
function fichaTab(n){
  Ficha.n = n; $('#sh-pn').innerHTML = fichaPanel(Ficha.ev, n);
  const box = $('.sh-tabs .cp'), b = $$('.sh-tabs > .sh-tab')[n], w = box.offsetWidth;
  if (w){ const l = b.offsetLeft - box.offsetLeft; box.style.clipPath = `inset(0 ${w - l - b.offsetWidth}px 0 ${l}px round 9px)`; }
}
function abreFicha(id){
  const ev = Store.get('eventos', id); if (!ev) return;
  Ficha.ev = clone(ev); Ficha.origen = document.activeElement;
  sh.innerHTML = `<div class="sh-hd" id="sh-hd"><h3 id="sh-t">${esc(ev.nombre || 'Sin título')}</h3><p>${[fdate(ev.fecha), ev.lugar && esc(ev.lugar)].filter(Boolean).join(' · ')}</p></div>
    <div class="sh-bd"><div class="sh-tabs">${SH_TABS.map((t, i) => `<button class="sh-tab" data-sh-tab="${i}">${t}</button>`).join('')}<div class="cp" aria-hidden="true">${SH_TABS.map(t => `<span class="sh-tab">${t}</span>`).join('')}</div></div><div id="sh-pn"></div></div>
    <div class="sh-ft"><button class="ghost hold" data-hold="Mantener para borrar" id="sh-del">Mantener para borrar</button><button id="sh-x">Cerrar</button><button class="primary" id="sh-full">Abrir ficha completa</button></div>`;
  sh.style.transform = ''; sh.classList.add('open'); bk.classList.add('open'); fichaTab(0); sh.focus({preventScroll:true});
  const hd = $('#sh-hd');
  hd.addEventListener('pointerdown', e => { if (Ficha.dr || !e.isPrimary) return; Ficha.dr = {y:e.clientY, t:Date.now(), d:0, id:e.pointerId}; hd.setPointerCapture(e.pointerId); sh.classList.add('drag'); });
  hd.addEventListener('pointermove', e => { const r = Ficha.dr; if (!r || e.pointerId !== r.id) return; r.d = e.clientY - r.y; const y = r.d < 0 ? -Math.sqrt(-r.d) * 2 : r.d; sh.style.transform = `translate(-50%,${y}px)`; });
  const fin = () => { const r = Ficha.dr; if (!r) return; Ficha.dr = null; sh.classList.remove('drag'); const v = Math.abs(r.d) / Math.max(1, Date.now() - r.t); if (r.d > 140 || (r.d > 12 && v > .11)) cierraFicha(); else sh.style.transform = ''; };
  hd.addEventListener('pointerup', fin); hd.addEventListener('pointercancel', fin);
}
function cierraFicha(){ sh.style.transform = ''; sh.classList.remove('open'); bk.classList.remove('open'); Ficha.origen?.focus?.({preventScroll:true}); }
bk.addEventListener('click', cierraFicha);
sh.addEventListener('click', e => {
  const t = e.target.closest('[data-sh-tab]'); if (t) return fichaTab(+t.dataset.shTab);
  if (e.target.closest('#sh-x')) return cierraFicha();
  if (e.target.closest('#sh-full')){ UI.evento = clone(Store.get('eventos', Ficha.ev.id)); cierraFicha(); go('eventos'); return; }
  if (e.target.closest('#sh-del')) confirmBox('¿Borrar este evento? No se puede deshacer.', async () => { const id = Ficha.ev.id; cierraFicha(); await Store.remove('eventos', id); render(); });
});
sh.addEventListener('change', async e => { const c = e.target.dataset.c; if (c == null) return; const ev = clone(Store.get('eventos', Ficha.ev.id)); ev.checklist[+c].ok = e.target.checked; Ficha.ev = ev; await Store.save('eventos', ev); });
addEventListener('resize', () => { if (sh.classList.contains('open')) fichaTab(Ficha.n); });

// Buscador (Ctrl K): apartados y actos
const cmd = $('#cmd'), cmdQ = $('#cmd-q'), cmdRes = $('#cmd-res'); let cmdSel = 0, cmdVis = [];
function cmdLista(){
  const t = cmdQ.value.trim().toLowerCase();
  const it = [...VIEWS.map(v => ({l:v.label, k:'Apartado', fn:() => go(v.id)})), ...Store.data.eventos.map(e => ({l:e.nombre || 'Sin título', k:'Acto', fn:() => { UI.evento = clone(e); go('eventos'); }}))];
  cmdVis = it.filter(x => x.l.toLowerCase().includes(t)).slice(0, 12); cmdSel = Math.min(cmdSel, Math.max(0, cmdVis.length - 1));
  cmdRes.innerHTML = cmdVis.length ? cmdVis.map((x, i) => `<li class="${i === cmdSel ? 'sel' : ''}" data-i="${i}">${esc(x.l)}<small>${x.k}</small></li>`).join('') : '<li class="no">Sin resultados</li>';
}
const abreCmd = () => { cmd.classList.add('open'); cmdQ.value = ''; cmdSel = 0; cmdLista(); cmdQ.focus(); };
const cierraCmd = () => cmd.classList.remove('open');
const cmdElige = x => { cierraCmd(); x.fn(); };
$('#find').addEventListener('click', abreCmd);
cmd.addEventListener('click', e => { if (e.target === cmd) return cierraCmd(); const li = e.target.closest('[data-i]'); if (li) cmdElige(cmdVis[+li.dataset.i]); });
cmdQ.addEventListener('input', () => { cmdSel = 0; cmdLista(); });
document.addEventListener('keydown', e => {
  if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k'){ e.preventDefault(); cmd.classList.contains('open') ? cierraCmd() : abreCmd(); return; }
  if (e.key === 'Escape'){ if (cmd.classList.contains('open')) cierraCmd(); else if (sh.classList.contains('open')) cierraFicha(); else $('#pop').classList.remove('open'); return; }
  if (!cmd.classList.contains('open')) return;
  if ((e.key === 'ArrowDown' || e.key === 'ArrowUp') && cmdVis.length){ e.preventDefault(); cmdSel = (cmdSel + (e.key === 'ArrowDown' ? 1 : -1) + cmdVis.length) % cmdVis.length; cmdLista(); }
  if (e.key === 'Enter' && cmdVis[cmdSel]) cmdElige(cmdVis[cmdSel]);
});

// Menú de cuenta (solo en la web, con sesión iniciada)
$('#av').addEventListener('click', () => {
  const p = $('#pop'); let mail = ''; try { mail = SB_USER?.email || ''; } catch {}
  p.innerHTML = `<div>${esc(mail)}</div><button role="menuitem" id="pop-salir">Cerrar sesión</button>`;
  $('#av').setAttribute('aria-expanded', p.classList.toggle('open'));
  $('#pop-salir').onclick = () => $('#nav [data-logout]')?.click();
});
document.addEventListener('click', e => { if (!e.target.closest('#av,#pop')){ $('#pop').classList.remove('open'); $('#av').setAttribute('aria-expanded', 'false'); } });

"""
mark = '/* ============================================================\n   ARRANQUE'
rep(mark, JS + mark)
io.open(P, 'w', encoding='utf-8', newline='\n').write(s)
print('ok')
