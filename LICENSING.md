# Licensing and provenance

## Licence scope

This repository is distributed under the Apache License, Version 2.0. See
[LICENSE](LICENSE) for the terms and [NOTICE](NOTICE) for attribution and
provenance information.

The licence applies only to rights that Dynamic Devices Ltd and the project
contributors are entitled to grant. It does not assert ownership of Qiskit,
established quantum algorithms, scientific results, third-party material, or
the names and trade marks of their respective owners.

## Project history

Alex Lennon assembled this repository on 15 October 2025 as an early
LLM-assisted exploration of Qiskit and quantum computing. The Git history
records who committed the files, but it does not establish that every generated
line originated with the committer or provide complete training-data
provenance for the LLM output.

The README declared Apache 2.0 from the first commit. A standalone `LICENSE`
file was added on 18 September 2026 so that the terms were complete and easy to
find. SPDX identifiers and this more detailed provenance record were added
later; their absence from an earlier file snapshot does not change the
repository-level declaration that accompanied that snapshot.

## Qiskit and established algorithms

The project uses the Qiskit SDK and demonstrates established techniques such
as Bell-state preparation, Deutsch-Jozsa, Bernstein-Vazirani, Grover search,
the quantum Fourier transform, VQE, teleportation and error-correction
circuits. Dynamic Devices does not claim ownership of those algorithms or
ideas. Qiskit and its own examples retain their applicable licences and
notices.

One specific source relationship was identified during a September 2026
provenance review. The H2 Hamiltonian operators and coefficients in
`examples/vqe_example.py` were adapted from the Apache-2.0-licensed
[Qiskit algorithms tutorial](https://github.com/Qiskit/qiskit-tutorials/blob/aefaab4294fab55cff2afaaba846726c5d8174c1/tutorials/algorithms/01_algorithms_introduction.ipynb),
first committed to that repository in 2020. This project's version rounds the
coefficients, adds a `YY` term and places the data in a different example
implementation. The source and changes are recorded in that file and in
[NOTICE](NOTICE).

The same review compared the nine file blobs supplied in the PQID licensing
enquiry with current or archived official Qiskit SDK, tutorial, textbook and
community-tutorial sources. It did not identify another verbatim copied block
beyond routine imports, standard API calls and canonical circuit operations.
That is a record of the review performed, not a guarantee that no unidentified
third-party influence exists in LLM-assisted output.

## Files covered by the provenance review

- `advanced_quantum_algorithms.py`
- `src/quantum_algorithms.py`
- `src/quantum_circuits.py`
- `examples/quantum_games.py`
- `quantum_showcase.py`
- `examples/vqe_example.py`
- `examples/algorithms.py`
- `quantum_trading_backtester.py`
- `test_quantum_hardware.py`

## Reuse and attribution

When redistributing or adapting material from this repository, follow
[Apache-2.0 section 4](https://www.apache.org/licenses/LICENSE-2.0#redistribution):
include a copy of the licence, mark modified files, and retain applicable
copyright, patent, trade mark and attribution notices, including `NOTICE`.

Referencing the repository URL, source path and Git commit or blob ID is
recommended so that readers can identify the exact material used. This is a
provenance recommendation rather than an additional licence condition.
