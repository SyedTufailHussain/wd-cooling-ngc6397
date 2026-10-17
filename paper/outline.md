# Research note outline (RNAAS, about 1,000 words, check current limits)

**Working title:** Sensitivity of the NGC 6397 white dwarf cooling sequence to the ¹²C(α,γ)¹⁶O rate and an extra cooling channel

1. **Motivation (about 120 words):** white dwarf cooling ages are used as cluster clocks; the C/O profile depends on the ¹²C(α,γ) rate; an extra cooling channel would shift the faint end.
2. **Method (about 300 words):** MESA version and settings, mass grid, rate multipliers, extra-cooling parameterisation, how tracks become a luminosity function, the likelihood.
3. **Data (about 100 words):** the published NGC 6397 white dwarf luminosity function, with citation, bins and any completeness corrections.
4. **Results (about 300 words):** 2 or 3 figures: tracks vs rate, model vs observed LF, constraint on the extra-cooling parameter.
5. **Caveats and conclusion (about 150 words):** single mass, IMF and IFMR treatment, systematics, what a full paper would add.

## Before submitting
- [ ] Scoop check done and the novelty statement written (Fleury et al. 47 Tuc axion work; arXiv:2410.14014)
- [ ] All numbers regenerate from `scripts/` with one command
- [ ] Code released with a Zenodo DOI and cited in the note
- [ ] Supervisor has read it and agreed on authorship
- [ ] Current RNAAS author guidelines and ORCID requirement checked

## Needed upgrades to `wdcool` before any claim
- Integrate over progenitor mass (IMF and initial-final mass relation) instead of one mass
- Photometric errors and completeness
- Convert luminosity to the observed magnitude system with a cited bolometric correction
