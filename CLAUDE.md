# Repository rules

This is the main repository for the Udemy course *HL7 FHIR Integration for Clinical AI* (Mohcine Madkour).

- **Do not commit PowerPoint files.** `.pptx` files are git-ignored. When a deck changes, update its `deck-source/` and `script.md`; `python tools/build_pptx.py` builds PowerPoint locally only.
- Recording scripts (`script.md`) and speaker notes are short bullets, one point per line.
- Learner resources live in each track's `resources/` folder as Markdown; list every new resource in that folder's README, the track README and the main README.
- Examples are fictional; never use real patient data.
