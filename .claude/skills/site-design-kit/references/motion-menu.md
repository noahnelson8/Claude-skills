# Motion menu

Pick **one signature move** and **at most two supporting effects**. Every effect needs a `prefers-reduced-motion` fallback that still looks designed (a static composition with depth, not a blank).

## Signature moves (pick one)
| Move | What the visitor sees | Fits | Recipe |
|---|---|---|---|
| **Transition as scroll** | The scene changes state as you scroll (clouds part, layers move, a product rotates) | Brand stories, hosting/infra, premium products | MotionSites `techniques/scroll.md`; ScrollCraft `scrub`/`reveal` devices |
| **Live 3D hero** | A real 3D object or room you can look around | Real estate, products, architecture | MotionSites `techniques/3d-and-webgl.md` (Three.js) |
| **Spatial browsing** | Products laid out in 3D space you move through | E-commerce, collections, lookbooks | MotionSites `techniques/3d-and-webgl.md` + `depth-and-interaction.md` |
| **Touchable surfaces** | Elements respond to cursor or touch (tilt, magnetism, liquid glass) | Portfolios, agencies, app launches | MotionSites `techniques/surfaces-and-buttons.md` |
| **Layered parallax hero** | Background, subject and foreground move at different speeds | Any premium marketing hero | ScrollCraft `references/hero-depth.md` |
| **Kinetic headline** | The headline assembles word by word or blurs in | Funnels (cheap, fast, readable) | MotionSites `techniques/type-and-text-motion.md` |
| **Seamless video hero** | A looping background video behind the headline | Funnels, launches | MotionSites `techniques/video-and-media.md` + its media shelf |

## Supporting effects (up to two)
- Section reveal on scroll (fade + small rise, 400–600ms, staggered).
- Smooth anchor scroll and a sticky nav that condenses.
- Hover lift on cards (transform only).
- Number counters, **only with real numbers**.
- Subtle cursor follower (desktop only, off on touch).

## Funnel rule
On a funnel page the headline, offer and CTA must be readable on a phone **before** any motion finishes. Prefer kinetic headline or video hero; avoid long pinned sections above the first CTA.
