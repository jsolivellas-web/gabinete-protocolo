"""Ajusta el programa para que coincida con la maqueta G: siempre en claro, menú en una sola fila y saludo con el nombre.
Uso: python fuente/herramientas/aplicar_ajustes_g.py   (solo se ejecuta una vez; comprueba que cada cambio encaja exactamente)."""
import io, os
P = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'gestor-protocolo.html')
s = io.open(P, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    assert c == n, (c, old[:90])
    s = s.replace(old, new)

# 1. Siempre en claro, como la maqueta: el modo oscuro deja de activarse solo (por el sistema o por el tema de Claude)
rep('@media (prefers-color-scheme: dark){:root:not([data-theme="light"])', '@media (prefers-color-scheme: dark){:root[data-theme="oscuro-auto"]', 4)
rep(':root[data-theme="dark"]', ':root[data-theme="oscuro"]', 4)
rep("  --r:14px; --shadow:", "  color-scheme:light;\n  --r:14px; --shadow:")

# 2. Menú en una sola fila; Eventos y Protocolo despliegan una segunda fila con sus apartados
rep(""".topbar-in{max-width:1180px;margin:0 auto;display:flex;flex-direction:column;gap:8px}""",
    """.topbar-in{max-width:1180px;margin:0 auto;display:flex;align-items:center;gap:8px 22px;flex-wrap:wrap}""")
rep(""".nav-list{display:flex;flex-wrap:wrap;gap:4px 2px;align-items:center}""",
    """.nav-list{display:flex;flex:1;min-width:0;flex-wrap:nowrap;gap:2px;align-items:center;overflow-x:auto;scrollbar-width:none}
.nav-list a[data-logout]{margin-left:auto;font-weight:500}
.subnav{flex-basis:100%;display:flex;gap:4px;overflow-x:auto;scrollbar-width:none;padding-left:2px}
.subnav:empty{display:none}
.subnav a{padding:5px 12px;border-radius:999px;font-size:.8rem;font-weight:600;color:var(--ink-2);text-decoration:none;white-space:nowrap}
.subnav a:hover{color:var(--accent)}
.subnav a.on{background:var(--accent-soft);color:var(--accent)}""")
rep(""".nav-group{font-size:.62rem;""", """.nav-group,.brand-sub,.nav-list .count{display:none!important}
.nav-group-x{font-size:.62rem;""")
rep(""".nav-list a{color:var(--ink-2);text-decoration:none;padding:6px 12px;""", """.nav-list a{color:var(--ink-2);text-decoration:none;padding:7px 14px;""")
rep("""  .nav-list{flex-wrap:nowrap;overflow-x:auto;scrollbar-width:none;margin-inline:-4px}""", """  .nav-list{flex-basis:100%;margin-inline:-4px}""")
rep("""    <div class="brand-row"><div class="brand">Gabinete de Protocolo</div><div class="brand-sub">Eventos · Actas · Precedencias</div></div>
    <nav class="nav-list" id="nav" aria-label="Apartados"></nav>""", """    <div class="brand">Gabinete de Protocolo</div>
    <nav class="nav-list" id="nav" aria-label="Apartados"></nav>
    <nav class="subnav" id="subnav" aria-label="Subapartados"></nav>""")

a = s.index("function renderNav(){"); b = s.index("  $('#nav').innerHTML = h;", a)
s = s[:a] + """// Menú principal: los apartados de Eventos y de Protocolo se agrupan y muestran una segunda fila
const MENU = [['panel','Panel'],['eventos','Eventos',['eventos','catalogo','invitaciones']],['packs','Packs'],['proveedores','Proveedores'],['convocatorias','Convocatorias'],['actas','Actas'],['protocolo','Protocolo',['noticias','precedencia','tratamientos']],['evaluacion','Evaluación'],['guia','Guía']];
function renderNav(){
  let h = '';
  const grupo = MENU.find(m => m[2] && m[2].includes(UI.view));
  MENU.forEach(([id, label, subs]) => {
    const on = subs ? subs.includes(UI.view) : UI.view === id;
    h += `<a href="#${subs ? subs[0] : id}" data-view="${subs ? subs[0] : id}" class="${on ? 'on' : ''}">${esc(label)}</a>`;
  });
  $('#subnav').innerHTML = grupo ? grupo[2].map(id => { const v = VIEWS.find(x => x.id === id); return `<a href="#${id}" data-view="${id}" class="${UI.view === id ? 'on' : ''}">${esc(v.label)}${v.count ? ` · ${v.count()}` : ''}</a>`; }).join('') : '';
""" + s[b:]
rep("""function go(view){ UI.view = view; try { history.replaceState(null, '', '#' + view); } catch {} render(); window.scrollTo(0, 0); }""",
    """function go(view){ UI.view = view; try { history.replaceState(null, '', '#' + view); } catch {} render(); window.scrollTo(0, 0); }
$('#subnav').addEventListener('click', e => { const a = e.target.closest('[data-view]'); if (a){ e.preventDefault(); go(a.dataset.view); } });""")

# 3. Saludo con el nombre de la cuenta (versión web con inicio de sesión)
rep("""  const saludo = hora < 14 ? 'Buenos días' : hora < 21 ? 'Buenas tardes' : 'Buenas noches';
  const dias = f =>""", """  let nombre = ''; try { const md = SB_USER?.user_metadata || {}; nombre = String(md.full_name || md.name || '').trim().split(/\\s+/)[0] || ''; } catch {}
  const saludo = (hora < 14 ? 'Buenos días' : hora < 21 ? 'Buenas tardes' : 'Buenas noches') + (nombre ? ', ' + esc(nombre) : '');
  const dias = f =>""")
rep("""<h1>${saludo}.</h1>""", """<h1>${saludo}.</h1>""")
io.open(P, 'w', encoding='utf-8', newline='\n').write(s)
print('ok')
