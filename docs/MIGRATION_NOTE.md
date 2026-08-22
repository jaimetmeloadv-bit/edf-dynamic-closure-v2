# Public-repository migration note

The Dynamic Closure project was developed as a sequence of notebook entries with local scripts, machine-readable outputs, figures, theoretical notes, and later consolidation files.

The first public GitHub migration preserves the **scientific equations, tests, logical dependencies, random seeds, and principal diagnostics** of Entries 01–16, but several early-to-middle entry scripts were normalized during transfer so that they use repository-relative output paths and a more compact executable layout. They should therefore not be interpreted as byte-for-byte archival copies of every local development file.

The public repository distinguishes three layers:

1. **Analytic result** — the mathematical proof or proposition stated in the Version-2 manuscript and theoretical notes.
2. **Executable certificate** — a Python implementation that independently verifies arithmetic, matrix-algebra, topology, or reduced-dynamics identities.
3. **Historical robustness/discovery record** — parameter sweeps, null controls, alternative models, and stronger claims later weakened by falsification.

The normalized public scripts do not change the scientific status of the results. Where an analytic proof exists, the proof is authoritative. Numerical scripts are certificates, countermodel searches, and robustness tests.

The repository will continue to receive the full machine-readable outputs and historical theoretical notes as the archival migration is completed. No result should be inferred merely from a missing historical file during that migration.

The manuscript source under `manuscript/` is the theorem-led publication version and should be used for the current mathematical statement of EDF Version 2.
