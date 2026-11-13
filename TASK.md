# Tarea automática: fábrica de vídeos Hacoo (POLE14)

## >>> NOVEDAD 13 nov 2026 (noche) — CUPÓN BLACKF (200 €) <<<
- Grabación nueva de Pol: `recs/blackf_es.mp4` (12 s, ES, Gran Via 28 Madrid). Producto 70,94 €, envío 3,70 € → 0,00 € (aquí SÍ "envío gratis"). Código BLACKF: "200€ DE DESCUENTO, hasta 200,00 €, del 13.11 al 30.11.2026, para productos específicos".
- La grabación acaba en la ventana del cupón: NO se ve el total final a 0,00 €. No decir "pago 0 €" ni "gratis total"; sí "cupón de hasta 200 €" + "envío gratis".
- Pol (13 nov): usarlo en TODAS las cuentas ES (@hacoocupones, @chinahero01, @90hacoo14, @hacoorabatt, @el.ceo.de.hacoo; @codigos_hacoo_ solo si sale buenísimo). Primero llenar huecos: @hacoocupones 14-16, @chinahero01 y @90hacoo14 el 16, y todas las ES el 17. Estilo hero (TikTok Sans Bold, voz ElevenLabs seguida). Nunca sin voz.

## >>> NOVEDAD 10 nov 2026 (16:15) — ESTILO QUE POL QUIERE AHORA <<<
- Pol (10 nov): "por ahora son los mejores que has hecho" → estilo SENCILLO CON MOVIMIENTO: grabación seguida, líneas que entran con la voz, círculo/rectángulo rojo en la casilla y el botón, manita, cámara suave, billetes al bajar el precio. Motor: `engine/hero.py` (spec json) + `engine/mux3.py`; constructor `engine/specs/sb.py`.
- TIPOGRAFÍA (Pol 10 nov: "la del 1er vídeo de fable es perfecta"): SOLO la del hero → TikTok Sans Bold en MAYÚSCULAS, contorno negro, cifras/código en amarillo con brillo (`font=None` en sb.build). No variar fuentes.
- GANCHO (Pol 10 nov): la frase del gancho se ve desde el fotograma 0; lo único que entra desenfocándose es la línea del importe ("(CUPÓN 120€)").
- Idioma del fondo = idioma del vídeo: francés → scratchpad r4/rec.mp4 (Londres, £36.15→£0.00; en pantalla y en la descripción "jusqu'à 120" sin moneda); español → k120/rec.mp4 (39,17 €→3,70 €, nunca "envío gratis"); inglés → en/rec.mp4 (Alemania, 70,34 €→0,00 €).
- NUNCA subir vídeos sin voz. ElevenLabs: cuenta nueva en plan Starter (de pago, 40.000 caracteres/mes), clave en scratchpad/.el_key (no escribirla nunca). Voces usadas: Liam, Charlie, Jessica, Will, Chris (eleven_multilingual_v2).
- Tanda automática: `engine/specs/jobs.py` (guiones, ganchos, descripciones) → `gen.py tts|align|build` → `chk.py` → `run.sh ID` → `verify.py ID`. Pol quiere MUCHOS ganchos distintos para testear.
- Falta el SFX de dinero: Pol tiene que pasar su zip de SFX (no inventar sonidos).
- PROGRAMADO: 11 nov (8 cuentas, estilo nuevo), 12 nov (épicos antiguos), 13-15 nov (23 vídeos `videos/120g_*.mp4` + hero FR el 13 en @reductionsxhacoo; el 14 @hacoorabatt lleva el vídeo en inglés E01). Lo antiguo de esos días está en borrador. Del 16 nov en adelante faltan vídeos.
- Pendiente: tras 3-4 días comparar visitas/retención por tipo de gancho (tabla en el doc del proyecto `claude/plan-ganchos-13-15-nov.md`) y contárselo a Pol antes de subir a 2-3/día.

## >>> ORDEN VIGENTE (9 nov 2026, 22:20) — MANDA SOBRE TODO LO DE ABAJO <<<
- FULL CUPÓN 120 en TODAS las cuentas. NO hagas ni programes vídeos de POLE14 (no uses factory.py para crear posts).
- Cuentas activas, 1 vídeo/día cada una, en hora pico, vídeo inédito y distinto en cada cuenta:
  - ES (grabación española, "hasta 120 €", sin "envío gratis"): @codigos_hacoo_ 7992090 (LA CHETADA, mucho cuidado), @90hacoo14 7802274, @hacoocupones 7801775, @hacoorabatt 7905293. Hora ~17:30-19:10, separadas ≥20 min.
  - FR (grabación francesa, "livraison gratuite" ok): @reductionsxhacoo 7841739, @code.promo.hacoo 7801996, @desc.pole 7968754. Hora 08:20-10:10, separadas ≥20 min.
  - @chinahero01 7690746: ACTIVA otra vez (Pol 9 nov 22:42: "no pares chinahero"), 1/día como las demás ES.
- Si faltan vídeos del 120 para cubrir los próximos días, NO rellenes con otra cosa: avisa a Pol (SendUserMessage) con qué cuentas/días faltan.
- Ritmo (Pol 9 nov 22:42): ahora 1/día por cuenta. Cuando las cuentas estén más activas (más visitas/seguidores), se puede subir a 2 y luego 3 al día; avisa a Pol con datos antes de subir el ritmo.
- Música a -28 LUFS (mux3 por defecto). Descripciones cortas: frase de búsqueda + código + beneficio + CTA + 3-4 hashtags, sin #happ, en el idioma de la cuenta.
- No borres nada: lo que sobre, a borrador.

Objetivo: que todas las cuentas tengan siempre contenido programado en Metricool para los próximos 3 días, con vídeos nuevos que no repitan ninguno anterior.

## 1. Preparar
- `add_repo` Pole14/POLE-CLaude (push) y clónalo (`git clone --depth 1 https://github.com/Pole14/pole-claude`). Todo está en ese repo (es público).
- Comprueba dependencias: `python3 -c "import cv2, numpy, PIL"` y `ffmpeg -version`. Si falta algo: `pip install --break-system-packages opencv-python-headless numpy pillow`.

## 2. Ver qué falta (Metricool, timezone Europe/Madrid)
`getScheduledPosts` desde mañana 00:00 hasta dentro de 4 días, para cada cuenta. Cuenta solo las publicaciones con draft = false.

| Cuenta | blogId | Idioma(s) | Ritmo |
|---|---|---|---|
| @reductionsxhacoo | 7841739 | fr | 1/día (la más fuerte) |
| @code.promo.hacoo | 7801996 | fr | 1/día |
| @hacoorabatt | 7905293 | es + en | NO TOCAR: publica Pol |
| @chinahero01 | 7690746 | es (en días alternos en) | NO TOCAR: publica Pol |
| @hacoocupones | 7801775 | es | NO TOCAR: publica Pol |
| @codigos_hacoo_ | 7992090 | es | 1/día. LA CHETADA (cuenta top de Pol, solo 120). MUCHO CUIDADO: solo vídeos inéditos y buenísimos, nunca 2 al día, no tocar sus posts/borradores |
| @90hacoo14 | 7802274 | es | NO TOCAR NUNCA: cuenta nueva con mucho potencial (1.800 visitas en su 1er vídeo), la lleva Pol, solo cupón de 120 € |

Cualquier cuenta nueva que Pol conecte para el cupón de 120 € (8 nov: una española, @90hacoo14, y una francesa nueva): NO TOCAR, solo cupón de 120 € y la lleva Pol.

ORDEN DE POL (8 nov 2026, 22:35): las cuentas francesas (@reductionsxhacoo y @code.promo.hacoo) siguen normal (ahora 1/día, ver regla del 9 nov). En las demás publica Pol: no programes nada y no saques sus borradores. Cuando el cupón de 120 € exista de verdad (Pol pasa la grabación con el cupón aplicado y sus condiciones, y queda apuntado en `claude/receta-viral.md`), TODAS las cuentas pasan a vídeos del cupón de 120 €, 1/día. Hasta entonces, nunca hagas vídeos de cupones de 100/120/200 €.

9 NOV 2026 (16:35) ACTUALIZACIÓN: Hacoo (EricPoa) confirmó por WhatsApp el cupón 120HACOO (120 € de descuento). Pol da permiso para usar TODAS las cuentas. Vídeos de 120 válidos: solo los hechos con la grabación v3 CON EL TELÉFONO DIFUMINADO (Pol, 9 nov 19:36: "difumina mi número"; usa siempre los videos/120hacoo_*_v2.mp4, nunca los sin _v2). Pol 9 nov 20:16: solo vídeos de la tanda NUEVA (épicos con manita, zooms y rectángulos: d,e,f,g,w1,w2,x,y,z); nada de la tanda antigua (a_1a1, b_liam, c_charlie). Vídeo distinto en cada cuenta. @hacoorabatt vuelve a tener permiso. Nueva cuenta FR del 120: @desc.pole (7968754), conectada 9 nov. Pol 9 nov 20:32: @chinahero01 NO subir nada (sus posts del 120 en borrador). @90hacoo14 el 9 nov nada más. (videos/120hacoo_*.mp4, voz Liam/Charlie). En el texto: "hasta 120 €", nunca "envío gratis" (la grabación muestra 3,70 € de envío). Programados el 9 y 10 nov en @90hacoo14, @chinahero01 y @hacoocupones. @hacoorabatt: NO SUBIR NADA (Pol, 9 nov 16:42); sus 3 posts del 120 quedaron en borrador. La "Cuenta FRANCES 120" (7968754) aún no tiene TikTok conectado en Metricool. Las cuentas francesas siguen con POLE14 hasta que haya vídeos de 120 en francés.
(Nota antigua, ya superada) 9 NOV 2026 (12:55) CORRECCIÓN: la grabación "120HACOO" NO sirve. Es la misma pantalla que el vídeo de -200 € con 18BOSS (misma hora 11:39, misma dirección, mismos productos, mismo total 18,92 €) con solo la cifra cambiada, y las cuentas no cuadran (228,69 − 120 − 76,78 − 122,99 ≠ 18,92). No hagas ni programes vídeos de 120 €. Los 4 posts de 120 del 9 nov quedan en borrador. Sigue solo con POLE14.

Si `getBrandSettings` muestra una marca nueva, no programes nada en ella hasta que Pol diga para qué es. REGLA DE POL (9 nov 2026, 20:34, sustituye a TODAS las anteriores de ritmo): 1 vídeo BUENÍSIMO al día por cuenta y listo, en hora pico (ES: 17:30-19:00, el pico de Metricool es 18 h; FR: 07:30-10:00, que es lo que mejor les va). Nunca 2 al día en una cuenta (Pol: "si no, las vamos a shadowbanear"; la cuenta que más visitas pilló llevaba 3 días sin publicar). Solo vídeos de calidad épica (manita, zooms, rectángulos, voz seguida), vídeo distinto en cada cuenta y escalona las cuentas. Antes de programar un día, mira si Pol ya ha subido algo ese día (analytics TKPO02): si sí, ese día nada.
Revisión del finde (8 nov 2026): gana el gancho -90 % (bienvenida) y "code promo + mes" publicados por la mañana (6-9 h): 923, 818 y 1.346 visitas. Por la tarde-noche rinden menos en FR (344-787). Carrusel EN (239) y haul (344) flojos. En FR el vídeo diario va entre 7:30 y 10 h y, cuando haya grabación de -90 %, prioriza ese gancho.
Para cada día de los próximos 3 que tenga menos publicaciones de las que marca el ritmo, apunta un hueco.

## 2b. Estrategia
Lee `ESTRATEGIA.md` del repo (algoritmo + plan por cuenta, 9 nov 2026) y síguelo: descripción corta (frase de búsqueda + código + beneficio + 3-4 hashtags, sin #happ), gancho con número grande verdadero, vídeo único por cuenta, cuentas separadas ≥20-30 min.


GRABACIONES 120 (9 nov 21:15): hay 2. (1) ES: scratchpad k120/rec.mp4 (Gua 82, La Rioja, 39,17€→3,70€, envío 3,70 → nunca "envío gratis"). (2) FR: grabada en el móvil francés ("actif"), dirección Maisons-Alfort, 70,48€→0,00€ con envío 0,00 (aquí SÍ "livraison gratuite"), teléfono difuminado; vídeos videos/120hacoo_fr_*.mp4. La FR solo para cuentas francesas (@desc.pole); la ES solo para las españolas. @desc.pole: 1/día por la mañana (08:30-10:00), programado 10-12 nov.

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
   - FR: 1 al día entre 07:30 y 10:00.
   - ES/EN: entre 13:00 y 15:00 o entre 18:00 y 21:00.
   - La gente compra sobre todo de 20 a 23 h, así que el vídeo de la tarde, antes de las 20 h.
   - Máximo 1 por día por cuenta, contando las que ya había.
4. En el mismo commit sube used.json y out/*.meta.json. Los mp4 de out/ no se suben (están en .gitignore); solo los de videos/.

## 6. Avisar
- Añade una línea por vídeo en la sección "Fábrica" al final de `claude/log-metricas.md`: fecha, cuenta, formato, gancho y hora (lee el doc, añade y reescríbelo entero).
- Manda a Pol (SendUserMessage) 2–4 líneas: cuántos vídeos se han hecho, para qué cuentas y hasta qué día hay contenido.

## Reglas
- No borres nada en Metricool.
- No toques publicaciones que ya existen.
- "Envío gratis" solo aparece porque todas las grabaciones del catálogo muestran envío 0,00 €. Si añades una grabación nueva, compruébalo.
- El -90% es la oferta de bienvenida de Hacoo para cuentas nuevas, no del código.
