# Gabinete de Protocolo

Programa web para organizar cualquier tipo de evento: eventos y tareas, packs con contratación, actas con presupuesto (Word y PDF), invitaciones, análisis de noticias de protocolo, precedencias y colocación en mesa, tratamientos (incluida la lista oficial del Govern de les Illes Balears) y evaluación con método SMART.

- **Web:** estática, sin compilación (`index.html`, `login.html`).
- **Inicio de sesión y datos:** Supabase. Cada usuario solo ve sus registros (tabla `gabinete_registros` con RLS).
- **Publicación:** Vercel, enlazado a este repositorio; cada cambio que se sube se publica solo.

## Estructura

| Ruta | Qué es |
|---|---|
| `index.html`, `login.html`, `js/`, `icono.svg` | La web publicada en Vercel. **No editar `index.html` a mano**: se genera. |
| `fuente/gestor-protocolo.html` | **El original del programa.** Todos los cambios se hacen aquí. También es la versión que se publica en Claude (https://claude.ai/artifact/JufLkyuhWR986s4XSBnDQ5). |
| `fuente/herramientas/generar_web.py` | Convierte el original en `index.html` añadiendo el inicio de sesión y el guardado en Supabase. |
| `fuente/herramientas/leer_xlsx.py`, `proveedores.json` | Lector de Excel sin dependencias y los proveedores de Mallorca extraídos de él. |
| `fuente/propuestas-interfaz.html`, `fuente/propuestas-nuevas.html` | Las propuestas de interfaz. Se aplicó la G · Bento sereno (fusión de la A y la E, en tonos neutros) con `herramientas/aplicar_tema_g.py`. |

`fuente/` no se publica en Vercel (ver `.vercelignore`).

## Cómo hacer un cambio

1. Editar `fuente/gestor-protocolo.html`.
2. Generar la web: `python fuente/herramientas/generar_web.py`
3. Confirmar y subir (`git commit` y `git push`). Vercel publica solo en uno o dos minutos.
4. Si se quiere, volver a publicar `fuente/gestor-protocolo.html` en Claude con la misma dirección.

Si se añade una colección nueva al guardado, hay que añadirla también a la restricción `gabinete_registros_coleccion_check` en Supabase.
