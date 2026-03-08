## Package Manager Dependency Resolution

### Topic
Comparing how package managers solve dependency resolution: pip (backtracking), UV (PubGrub)

### Core Thesis
Dependency resolution is fundamentally an NP-hard problem (SAT). Different package managers handle this differently:

1. **Backtracking (pip)** - Try versions, hit conflict, backtrack, repeat. Simple but slow.

2. **PubGrub (UV)** - Conflict-driven learning. When it hits a conflict, it derives *why* and prunes entire classes of solutions. Originated from Dart's package manager.

### Key Research Findings

**pip parallelisation history:**
- GitHub issue #825 requesting parallel downloads opened March 2013 - still open 12+ years later
- Limited `--use-feature=fast-deps` added in 2020, not default
- Challenges: Python's GIL, cross-platform compatibility, progress bar UI, threading complexity

**UV architecture (from source):**
- Uses async/await with semaphore-controlled concurrency (`crates/uv-resolver/src/resolver/provider.rs`)
- Parallel metadata fetches and downloads by default
- PubGrub implementation in `crates/uv-resolver/`

**pip architecture (from source):**
- `RequirementPreparer` class processes requirements sequentially
- `_prepare_linked_requirement` handles one requirement at a time
- Batch downloading exists but limited scope

### Planned Deliverables

**Toy implementations** - Backtracking and PubGrub resolvers in Python solving the same synthetic dependency graph

**Synthetic dataset** - `package_index.json` with 7 packages containing two hidden conflicts (json-lib and crypto version bounds). Solvable by backtracking/PubGrub
