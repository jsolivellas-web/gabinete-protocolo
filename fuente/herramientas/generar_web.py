import io, os, shutil, sys
# Uso (desde cualquier sitio): python fuente/herramientas/generar_web.py
# Lee fuente/gestor-protocolo.html y escribe index.html (versión web con Supabase) en la raíz del repositorio.
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
rd = lambda p: io.open(p, encoding='utf-8').read()
def wr(p, s):
    with io.open(p, 'w', encoding='utf-8', newline='\n') as f: f.write(s)

s = rd('fuente/gestor-protocolo.html')
def rep(old, new):
    global s
    assert old in s, old[:80]
    s = s.replace(old, new, 1)

rep('<meta charset="utf-8">', '<!doctype html>\n<html lang="es">\n<head>\n<meta charset="utf-8">')
rep('<meta name="claude:viewport-fit-sides" content="cover">\n', '<link rel="icon" href="icono.svg">\n')
rep('</style>\n', '</style>\n<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2.45.4/dist/umd/supabase.min.js"></script>\n<script src="js/supabase-config.js"></script>\n<script>document.documentElement.style.visibility="hidden";setTimeout(function(){document.documentElement.style.visibility="";},6000);</script>\n</head>\n<body>\n')
s = s.rstrip() + '\n</body>\n</html>\n'
rep('html,body{height:100%}', 'html,body{height:100%;margin:0}\nimg{max-width:100%}')
rep("if (!dl){ if (text) copyText(data, 'Contenido copiado (la descarga no está disponible aquí)'); else toast('La descarga de archivos solo funciona al abrir el programa en Claude.'); return; }",
    "if (!dl){ try { const a = document.createElement('a'); a.href = URL.createObjectURL(data instanceof Blob ? data : new Blob([data])); a.download = filename; document.body.append(a); a.click(); setTimeout(() => { URL.revokeObjectURL(a.href); a.remove(); }, 1500); } catch { if (text) copyText(data, 'No se pudo descargar; contenido copiado'); else toast('No se pudo descargar el archivo.'); } return; }")
rep("    $('#storage-note').innerHTML = this.mode === 'db'",
    "    if (this.mode === 'cloud'){ $('#storage-note').innerHTML = `<b>Guardado en tu cuenta.</b> ${esc(SB_USER.email)}<br>Tus datos están en la nube y los verás desde cualquier ordenador.`; return; }\n    $('#storage-note').innerHTML = this.mode === 'db'")
rep("    const plain = clone(obj);\n",
    "    const plain = clone(obj);\n"
    "    if (this.mode === 'cloud'){\n"
    "      const {error} = await SB.from('gabinete_registros').upsert({user_id:SB_USER.id, coleccion:col, id:obj.id, data:plain, updated_at:obj.actualizado});\n"
    "      if (error){ toast('No se pudo guardar en la nube: ' + error.message); return false; }\n"
    "      const arr = this.data[col]; const i = arr.findIndex(x => x.id === obj.id);\n"
    "      if (i >= 0) arr[i] = plain; else arr.push(plain);\n"
    "      refreshLists(); return true;\n"
    "    }\n")
rep("  async remove(col, id){\n",
    "  async remove(col, id){\n"
    "    if (this.mode === 'cloud'){\n"
    "      const {error} = await SB.from('gabinete_registros').delete().match({coleccion:col, id});\n"
    "      if (error){ toast('No se pudo borrar: ' + error.message); return; }\n"
    "      this.data[col] = this.data[col].filter(x => x.id !== id); refreshLists(); return;\n"
    "    }\n")
rep("  $('#nav').innerHTML = h;",
    "  if (SB_USER) h += `<div class=\"nav-group\">Cuenta</div><a href=\"#\" data-logout title=\"${esc(SB_USER.email)}\">Cerrar sesión</a>`;\n  $('#nav').innerHTML = h;")
rep("$('#nav').addEventListener('click', e => { const a",
    "$('#nav').addEventListener('click', e => { if (e.target.closest('[data-logout]')){ e.preventDefault(); SB.auth.signOut().finally(() => location.replace('login.html')); return; } const a")
cloud = r'''/* ============================================================
   NUBE: inicio de sesión y datos de cada usuario en Supabase (tabla gabinete_registros, con RLS)
   ============================================================ */
const SB = window.supabase && window.SUPABASE_URL ? window.supabase.createClient(window.SUPABASE_URL, window.SUPABASE_KEY) : null;
let SB_USER = null;
async function startCloud(){
  const show = () => { document.documentElement.style.visibility = ''; };
  if (!SB){ show(); toast('No se pudo conectar con la nube: los datos se guardan solo en este navegador.'); return; }
  const {data:{session}} = await SB.auth.getSession();
  if (!session){ location.replace('login.html?next=index.html'); return; }
  SB_USER = session.user;
  const {data, error} = await SB.from('gabinete_registros').select('coleccion,id,data');
  if (error){ show(); toast('No se pudieron cargar tus datos: ' + error.message); return; }
  Store.mode = 'cloud';
  COLS.forEach(c => Store.data[c] = []);
  (data || []).forEach(r => Store.data[r.coleccion]?.push({...r.data, id:r.id}));
  // Lo que se guardó antes solo en este navegador se sube a la cuenta.
  const subir = [];
  COLS.forEach(c => lsGet('gp_' + c, []).forEach(o => { if (o?.id && !Store.get(c, o.id)) subir.push([c, o]); }));
  for (const [c, o] of subir) await Store.save(c, o);
  if (subir.length){ COLS.forEach(c => { try { localStorage.removeItem('gp_' + c); } catch {} }); toast(`Se han subido a tu cuenta ${subir.length} registros guardados en este navegador.`); }
  Store.noteMode(); render(); show();
  SB.auth.onAuthStateChange(ev => { if (ev === 'SIGNED_OUT') location.replace('login.html'); });
}

'''
mark = '/* ============================================================\n   ARRANQUE'
rep(mark, cloud + mark)
rep('render();\ninitCaps();', 'render();\ninitCaps();\nstartCloud();')
wr('index.html', s)
shutil.copyfile('fuente/portada.jpg', 'portada.jpg')

print('ok: index.html generado')
