# Gabinete de Protocolo

Programa web para organizar cualquier tipo de evento: eventos y tareas, packs con contratación, actas con presupuesto (Word y PDF), invitaciones, análisis de noticias de protocolo, precedencias y colocación en mesa, tratamientos (incluida la lista oficial del Govern de les Illes Balears) y evaluación con método SMART.

- **Web:** estática, sin compilación (`index.html`, `login.html`).
- **Inicio de sesión y datos:** Supabase. Cada usuario solo ve sus registros (tabla `gabinete_registros` con RLS).
- **Publicación:** Vercel, enlazado a este repositorio; cada cambio que se sube se publica solo.
