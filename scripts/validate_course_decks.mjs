import {decks} from './course_deck_content.mjs';
import {auditDeck, resolveLayout} from './presentation_design.mjs';

const layouts = Object.fromEntries([
  'cover','section','statement','focus','annotated','compare','steps',
  'timeline','flow','swimlane','table','case','code','formula','windows',
  'dates','rank','funnel','citation','ideas','roadmap','chart','notebook',
  'links','image','tokenmap','lora-paths',
].map(kind => [kind, true]));

let failed = false;
for (const [week, deck] of Object.entries(decks)) {
  const warnings = auditDeck(deck, layouts);
  const missingSources = deck.slides.filter(slide => !slide.sources?.length).map(slide => slide.n);
  if (missingSources.length) {
    failed = true;
    console.error(`W${week}: missing source notes on slides ${missingSources.join(', ')}`);
  }
  if (Number(week) === 6) {
    const invalid = deck.slides.filter(slide => slide.sources.some(source => source.includes('course_labs/retrieval.py')));
    if (invalid.length) {
      failed = true;
      console.error(`W06: unrelated retrieval sources on slides ${invalid.map(slide => slide.n).join(', ')}`);
    }
  }
  console.log(`W${week}: ${deck.slides.length} slides, ${new Set(deck.slides.map(resolveLayout)).size} layouts`);
  warnings.forEach(warning => console.warn(`  ${warning}`));
}
if (failed) process.exitCode = 1;
