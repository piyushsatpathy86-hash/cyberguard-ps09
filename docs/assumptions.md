# Assumptions & Limitations

Log model caveats, dataset provenance notes, and scope limitations here as
they come up during build — don't leave this until submission week.

## Model Caveats
- _(e.g. deepfake detector is pretrained/not fine-tuned on our domain — expect lower accuracy on edge cases)_

## Dataset Provenance
- See `app/data/raw/README.md` for the full per-file tagging.

## Decision-Support Framing
CyberGuard outputs are decision-support signals, not certified diagnoses.
Every risk score and explanation should be read as "indicators suggest..."
rather than a definitive verdict — reflect this in UI copy and demo narration.

## Known Limitations
- _(fill in as discovered — e.g. CPU-only inference, English-primary phishing model, small anomaly training set, etc.)_
