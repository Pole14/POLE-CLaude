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
| @code.promo.hacoo | 7801996 | fr | 2/día |
| @hacoorabatt | 7905293 | es + en | NO TOCAR: publica Pol |
| @chinahero01 | 7690746 | es (en días alternos en) | NO TOCAR: publica Pol |
| @hacoocupones | 7801775 | es | NO TOCAR: publica Pol |
| @90hacoo14 | 7802274 | es | NO TOCAR NUNCA: cuenta nueva con mucho potencial (1.800 visitas en su 1er vídeo), la lleva Pol, solo cupón de 120 € |

Cualquier cuenta nueva que Pol conecte para el cupón de 120 € (8 nov: una española, @90hacoo14, y una francesa nueva): NO TOCAR, solo cupón de 120 € y la lleva Pol.

ORDEN DE POL (8 nov 2026, 22:35): las cuentas francesas (@reductionsxhacoo y @code.promo.hacoo) siguen normal, 2/día. En las demás publica Pol: no programes nada y no saques sus borradores. Cuando el cupón de 120 € exista de verdad (Pol pasa la grabación con el cupón aplicado y sus condiciones, y queda apuntado en `claude/receta-viral.md`), TODAS las cuentas pasan a vídeos del cupón de 120 €, 2/día. Hasta entonces, nunca hagas vídeos de cupones de 100/120/200 €.

9 NOV 2026 (16:35) ACTUALIZACIÓN: Hacoo (EricPoa) confirmó por WhatsApp el cupón 120HACOO (120 € de descuento). Pol da permiso para usar TODAS las cuentas. Vídeos de 120 válidos: solo los hechos con la grabación v3 (videos/120hacoo_*.mp4, voz Liam/Charlie). En el texto: "hasta 120 €", nunca "envío gratis" (la grabación muestra 3,70 € de envío). Programados el 9 y 10 nov en @90hacoo14, @chinahero01 y @hacoocupones. @hacoorabatt: NO SUBIR NADA (Pol, 9 nov 16:42); sus 3 posts del 120 quedaron en borrador. La "Cuenta FRANCES 120" (7968754) aún no tiene TikTok conectado en Metricool. Las cuentas francesas siguen con POLE14 hasta que haya vídeos de 120 en francés.
(Nota antigua, ya superada) 9 NOV 2026 (12:55) CORRECCIÓN: la grabación "120HACOO" NO sirve. Es la misma pantalla que el vídeo de -200 € con 18BOSS (misma hora 11:39, misma dirección, mismos productos, mismo total 18,92 €) con solo la cifra cambiada, y las cuentas no cuadran (228,69 − 120 − 76,78 − 122,99 ≠ 18,92). No hagas ni programes vídeos de 120 €. Los 4 posts de 120 del 9 nov quedan en borrador. Sigue solo con POLE14.

Si `getBrandSettings` muestra una marca nueva, no programes nada en ella hasta que Pol diga para qué es. Regla de Pol (8 nov 2026): ninguna cuenta publica solo 1 vídeo al día; mínimo 2/día, con horas distintas y vídeos siempre distintos.
Revisión del finde (8 nov 2026): gana el gancho -90 % (bienvenida) y "code promo + mes" publicados por la mañana (6-9 h): 923, 818 y 1.346 visitas. Por la tarde-noche rinden menos en FR (344-787). Carrusel EN (239) y haul (344) flojos. En cada cuenta, 1 de los 2 vídeos diarios va entre 6 y 9 h y, cuando haya grabación de -90 %, prioriza ese gancho.
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
