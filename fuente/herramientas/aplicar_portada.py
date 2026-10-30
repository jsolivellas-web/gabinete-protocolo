"""Pone la foto de portada en el Panel y hace que generar_web.py la copie a la raíz de la web.
Uso: python fuente/herramientas/aplicar_portada.py   (solo se ejecuta una vez; comprueba que cada cambio encaja exactamente)."""
import io, os
BASE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(BASE, '..', 'gestor-protocolo.html')
G = os.path.join(BASE, 'generar_web.py')
s = io.open(P, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    assert c == n, (c, old[:90])
    s = s.replace(old, new)

rep(""".p-hl{display:flex;align-items:flex-end;justify-content:space-between;gap:20px;flex-wrap:wrap;padding:12px 4px 0}
.p-hl h1{font-size:3.5rem;letter-spacing:-.045em;line-height:1}
.p-hl p{margin:10px 0 0;color:var(--ink-2);font-size:1rem;max-width:62ch}
.p-hl .btns{display:flex;gap:8px;flex-wrap:wrap}
""", """.p-hl{position:relative;overflow:hidden;min-height:340px;border-radius:24px;background:var(--navy);color:#fff;display:flex;align-items:flex-end;justify-content:space-between;gap:20px;flex-wrap:wrap;padding:28px}
.p-hl > img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:center 42%}
.p-hl::after{content:"";position:absolute;inset:0;background:linear-gradient(90deg,rgba(20,24,23,.82) 0%,rgba(20,24,23,.5) 42%,rgba(20,24,23,.05) 72%),linear-gradient(0deg,rgba(20,24,23,.55) 0%,rgba(20,24,23,0) 45%)}
.p-hl > div{position:relative;z-index:1}
.p-hl h1{font-size:3.5rem;letter-spacing:-.045em;line-height:1;color:#fff}
.p-hl p{margin:10px 0 0;color:#ffffffe0;font-size:1rem;max-width:44ch}
.p-hl .btns{display:flex;gap:8px;flex-wrap:wrap}
.p-hl button.primary{background:#fbfaf7;border-color:#fbfaf7;color:#191b1a}
.p-hl button.ghost{background:rgba(20,24,23,.5);border-color:#ffffff66;color:#fff;backdrop-filter:blur(8px);-webkit-backdrop-filter:blur(8px)}
""")
rep(".p-gr{display:grid;grid-template-columns:repeat(12,minmax(0,1fr));gap:12px;margin-top:-8px}", ".p-gr{display:grid;grid-template-columns:repeat(12,minmax(0,1fr));gap:12px;margin-top:-10px}")
rep("  .p-hl h1{font-size:2.5rem}\n", """  .p-hl{min-height:400px;padding:22px}
  .p-hl h1{font-size:2.5rem}
  .p-hl > img{object-position:50% 50%}
  .p-hl::after{background:linear-gradient(0deg,rgba(20,24,23,.92) 0%,rgba(20,24,23,.74) 58%,rgba(20,24,23,.1) 92%)}
""")
rep('<header class="p-hl"><div><h1>', '<header class="p-hl"><img src="portada.jpg" alt="Collage de eventos: concierto, congreso, carrera popular, festival y cena de gala" width="1800" height="1004" fetchpriority="high"><div><h1>')
rep("@media (hover:hover) and (pointer:fine){button.ghost:hover{color:var(--ink);background:var(--paper)}}", "@media (hover:hover) and (pointer:fine){button.ghost:hover{color:var(--ink);background:var(--paper)}.p-hl button.ghost:hover{color:#fff;background:#ffffff33}}")
io.open(P, 'w', encoding='utf-8', newline='\n').write(s)

g = io.open(G, encoding='utf-8').read()
old = "wr('index.html', s)\n"
assert g.count(old) == 1
g = g.replace(old, old + "shutil.copyfile('fuente/portada.jpg', 'portada.jpg')\n")
assert g.startswith('import io, os, sys')
g = g.replace('import io, os, sys', 'import io, os, shutil, sys', 1)
io.open(G, 'w', encoding='utf-8', newline='\n').write(g)
print('ok')
