# Council: which visual design fits ACL (22 Nov 2026)

The creator: "i changed my mind about this design bro ask council what design feets to acl and then tell me the best
design that fits acl". The same question (`council_design_fit_prompt_2026-11-22.txt`) went to GPT, Gemini and DeepSeek,
each in a new chat. Opinions, not sign-off; summaries in our words.

## GPT's opinion (not sign-off): "The Living Atlas"
- A scientific atlas of a world that happens to be alive; "the world is the protagonist, its history is the artwork".
- Fixed, slightly tilted orthographic view of all 40 × 40 tiles; smooth zoom from the archipelago to one person; places
  stay put across centuries.
- Deep navy seas, desaturated green forests, warm ochre plains, slate mountains, ivory snow; fine contours and
  elevation shading; fire the brightest warm thing.
- Tiny faceless silhouettes by band; bands as soft outlines around real clusters, not villages.
- A birth adds a small point of light, a death gently puts one out; a click shows the recorded event.
- Time is the main animation: a timeline through centuries. Atlas serif headings, monospace data. Slow, restrained
  motion; one step stays one week, and smoothing must never suggest actions the world did not take.
- Never invent buildings, paths, tools, rituals, faces or relationships; never make discoveries look inevitable; never
  present a brain scan as a picture of consciousness; never turn an emergent event into a scripted scene.
- Runner-up: a minimal low-poly 3D island diorama (better for videos, but easily looks like a survival game).

## Gemini's opinion (not sign-off): "An Illustrated Field-Survey and Natural-History Atlas"
- The look of a scientific expedition's archive: warm paper (unbleached vellum) with printmaker inks; dark UIs feel like
  space or surveillance, ASCII like a terminal, pixel art like a scripted game.
- Top-down orthographic map with smooth zoom; a side margin for thoughts, brain scans and the chronicle.
- Inks: slate sea, ochre beach, sage plains, deep pine forest, sienna hills, charcoal peaks, white snow, cobalt rivers;
  contour lines and stippled elevation.
- Fire as a vermilion ember with faint smoke; heaps, stores and crops as small geometric marks sized by what is there.
- People as faceless directional pawns by band colour; kinship and speech as faint arcs only when they happen.
- A birth blooms as a soft ink ring; a death leaves a brief ash mark that fades.
- Serif for the chronicle, tabular monospace for numbers; unhurried motion, one week per beat.
- Never: buildings, clothing, faces, cinematic camera shake, emotional music, speech bubbles implying human language.
- Runner-up: a "topographic light table" (alabaster and graphite, a pure lab view).

## DeepSeek's opinion (not sign-off): "The Observatory Atlas"
- A scientific instrument for witnessing an unwritten world; "the map is the primary evidence; everything else is
  annotation".
- Full-bleed, north-up, top-down relief map; zoom and pan only, no isometric or rotating camera.
- Near-black blue-slate ground, muted biome washes from real height and biome, thin river lines, amber fire, muted band
  colours. People as tiny marks by band; a thin ring on selection opens state, thought and brain scan.
- Bands as colour and a label on hover; territories only if computed. Birth: a new mark with a brief ring; death: the
  mark fades, no skull. Generations: a timeline scrubber, population chart, chronicle of firsts, an optional "ghost"
  layer drawn only from recorded lives.
- Monospace for measurements, humanist serif for the chronicle; discrete weekly ticks, gentle crossfades, no game-like
  motion.
- Never: gamify, invent buildings, tools or faces, pixel art, 3D spectacle, dramatic birth or death symbols, labels
  that imply intention, or relations and causes the data does not hold.
- Runner-up: a light "field notebook" atlas (paper-toned map plates, chronicle notes in the margin).

## The assistant, as council
- **All three chose an atlas,** independently: map first, real terrain with contours, tiny faceless people by band,
  fire the one warm light, births and deaths as quiet marks, generations shown through time, a serif for the chronicle
  and monospace for data, slow motion, and nothing the world does not contain.
- **They differ on light or dark:** Gemini says warm paper; DeepSeek dark, with paper as its runner-up; GPT's palette
  (navy sea, ochre plains, ivory snow) reads as a printed atlas. Two of three point to paper.
- **Camera:** GPT a slight tilt; Gemini and DeepSeek straight top-down (as today's observatory).
- **Checked against the code:** every element they ask for exists in the stream (heights, biomes, bands, fires, heaps,
  stores, crops, births and deaths, what was said, thoughts, the chronicle). The viewer already plays each week as days
  from the week's real events (`acl/stage.py`), which meets GPT's rule that smoothing must not invent actions. The
  current observatory already has the bones (relief from real height, chronicle, brain scan).
- **Recommendation:** "The Living Atlas": a naturalist's printed atlas of a world nobody wrote, on warm paper, top-down,
  with the dark observatory kept as its night mode. Details in the message to the creator.
