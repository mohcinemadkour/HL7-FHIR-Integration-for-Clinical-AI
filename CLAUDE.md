# Repository rules

This is the main repository for the Udemy course *HL7 FHIR Integration for Clinical AI* (Mohcine Madkour).

- **Always keep the latest decks as PowerPoint in the repo.** Whenever a deck changes, update its `deck-source/` and `script.md`, then run `python tools/build_pptx.py` and commit the regenerated `.pptx` files in the same commit.
- Recording scripts (`script.md`) and speaker notes are short bullets, one point per line.
- Learner resources live in each track's `resources/` folder as Markdown; list every new resource in that folder's README, the track README and the main README.
- Examples are fictional; never use real patient data.
