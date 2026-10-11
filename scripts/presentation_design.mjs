// Shared visual contract for the 2026 LLMOps slide builder.
// Content lives in course_deck_content.mjs; this file owns reusable design
// decisions and guards. New weeks should add concepts, not duplicate UI boxes.
export const C = Object.freeze({
  ink: '#17191B', black: '#0A0B0C', white: '#FFFFFF',
  paper: '#F7F7F5', navy: '#17283B', green: '#006B4F',
  blue: '#284B72', soft: '#EDF3EF', gray: '#52606B',
  line: '#CFD5D3', muted: '#BDC7C4',
});

// AppleGothic is the only installed Korean family verified to preserve all
// weights in the PPTX -> LibreOffice PDF path on this host. Other candidates
// introduced script/serif fallback in table cells and regular text.
export const FONT = 'AppleGothic';
export const MONO = 'Menlo';
export const CANVAS = Object.freeze({width: 1280, height: 720, margin: 64});

// The labels are pedagogical intent, not a component-grid vocabulary. A
// content author may still choose a concrete `kind` for atypical evidence.
export const intentToLayout = Object.freeze({
  premise: 'statement', distinction: 'compare', sequence: 'steps',
  mechanism: 'flow', evidence: 'table', specimen: 'annotated',
  decision: 'focus', boundary: 'section', practice: 'steps',
});

export function resolveLayout(slide) {
  return slide.kind ?? intentToLayout[slide.intent];
}

export function auditDeck(deck, renderers) {
  const warnings = [];
  if (!deck?.slides?.length) throw Error('Deck has no slides');
  let prior = null;
  let run = 0;
  const titles = new Set();
  deck.slides.forEach((slide, index) => {
    const kind = resolveLayout(slide);
    if (!renderers[kind]) throw Error(`Unknown layout on slide ${index + 1}: ${kind}`);
    if (!slide.title?.trim()) throw Error(`Missing title on slide ${index + 1}`);
    if (slide.title.endsWith('.')) warnings.push(`s${index + 1}: heading ends with a period`);
    if (titles.has(slide.title) && kind !== 'section') warnings.push(`s${index + 1}: repeated title ${slide.title}`);
    titles.add(slide.title);
    run = prior === kind ? run + 1 : 1;
    if (run === 3 && !['table', 'chart'].includes(kind)) warnings.push(`s${index - 1}–${index + 1}: three identical layouts`);
    prior = kind;
  });
  return warnings;
}
