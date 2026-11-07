# Tarea automática: fábrica de vídeos Hacoo (POLE14)

Objetivo: que todas las cuentas tengan siempre contenido programado en Metricool para los próximos 3 días, con vídeos nuevos que no repitan ninguno anterior.

## 1. Preparar
- `add_repo` Pole14/POLE-CLaude (push) y clónalo (`git clone --depth 1 https://github.com/Pole14/pole-claude`). Todo está en ese repo (es público).
- Comprueba dependencias: `python3 -c "import cv2, numpy, PIL"` y `ffmpeg -version`. Si falta algo: `pip install --break-system-packages opencv-python-headless numpy pillow`.

## 2. Ver qué falta (Metricool, timezone Europe/Madrid)
`getScheduledPosts` desde mañana 00:00 hasta dentro de 4 días, para cada cuenta. Cuenta solo las publicaciones con draft = false.

| Cuenta | blogId | Idioma(s) | Ritmo |
|---|---|---|---|
| @reductionsxhacoo | 7841739 | fr | 2/día (la más fuerte) |
| @hacoorabatt | 7905293 | es + en | 2/día: 1 es y 1 en |
| @chinahero01 | 7690746 | es (en días alternos en) | 1/día |
| @code.promo.hacoo | 7801996 | fr | 1 cada 2 días |
| @hacoocupones | 7801775 | es | 1 cada 2 días |

Si `getBrandSettings` muestra una marca nueva con TikTok y nombre UK, trátala como `en`, 2/día.
Para cada día de los próximos 3 que tenga menos publicaciones de las que marca el ritmo, apunta un hueco.

## 3. Elegir formato
Lee el doc del proyecto `claude/log-metricas.md` (herramienta Projects).
- Si una revisión dice claramente que gana el formato A (gancho pequeño de 2 líneas) o el B (gancho grande de 3 líneas en el centro), usa ese en el 75 % de los huecos y el otro en el 25 %, para seguir comparando.
- Si no hay veredicto, alterna A/B.

## 4. Fabricar
Para cada hueco: `python3 factory.py --lang <fr|es|en> --fmt <A|B> --n 1 --date <AAAA-MM-DD del hueco>`.
- Saca un mp4 en out/ y un `.meta.json` con la descripción (`caption`) lista. Tarda unos 40 s por vídeo.
- `factory.py` nunca repite una combinación (grabación + gancho + formato) ya usada: está apuntada en used.json. Si dice "sin combinaciones nuevas", para y avisa a Pol de que hacen falta grabaciones o voces nuevas.
- Revisa 1 fotograma de cada vídeo (segundo 1,2: el gancho se lee y no se sale de la pantalla) antes de subirlo.

## 5. Subir y programar
1. Copia cada mp4 a `videos/` del repo, haz commit y push a main (antes `git fetch origin main` y rebase si hace falta). URL pública: `https://raw.githubusercontent.com/Pole14/pole-claude/main/videos/<archivo>.mp4`. Comprueba con `curl -sI` que responde 200.
2. `createScheduledPost` en el blogId del hueco:
   - `media` = esa URL (Metricool la descarga y la aloja él).
   - `text` y `tiktokData.title` = la `caption` del `.meta.json`.
   - `tiktokData` = `{"privacyOption":"PUBLIC_TO_EVERYONE","commercialContentThirdParty":true,"title":...,"photoCoverIndex":0}`.
   - `autoPublish` true y `draft` false.
3. Horas: elige minutos que no sean redondos y no repitas hora exacta en la misma cuenta.
   - FR: una entre 08:00 y 11:00 y otra entre 18:00 y 21:00.
   - ES/EN: entre 13:00 y 15:00 o entre 18:00 y 21:00.
   - La gente compra sobre todo de 20 a 23 h, así que el vídeo de la tarde, antes de las 20 h.
   - Máximo 2 por día por cuenta, contando las que ya había.
4. En el mismo commit sube used.json y out/*.meta.json. Los mp4 de out/ no se suben (están en .gitignore); solo los de videos/.

## 6. Avisar
- Añade una línea por vídeo en la sección "Fábrica" al final de `claude/log-metricas.md`: fecha, cuenta, formato, gancho y hora (lee el doc, añade y reescríbelo entero).
- Manda a Pol (SendUserMessage) 2–4 líneas: cuántos vídeos se han hecho, para qué cuentas y hasta qué día hay contenido.

## Reglas
- No borres nada en Metricool.
- No toques publicaciones que ya existen.
- "Envío gratis" solo aparece porque todas las grabaciones del catálogo muestran envío 0,00 €. Si añades una grabación nueva, compruébalo.
- El -90% es la oferta de bienvenida de Hacoo para cuentas nuevas, no del código.
