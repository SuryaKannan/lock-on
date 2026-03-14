# lock-on

> Read the full write-up [here](https://suryakannan.com/projects/lock-on/)

Toy implementations of Backtracking and DPLL (with unit propagation) dependency resolution algorithms in Python, illustrating how pip-style resolvers work and how constraint propagation improves on naive backtracking.

## Requirements

- [uv](https://docs.astral.sh/uv/getting-started/installation/)

## Usage

```bash
# Run the backtracker
uv run main.py backtrack

# Run DPLL with unit propagation
uv run main.py dpll

# Enable verbose logging to see the resolution trace
uv run main.py backtrack -v
uv run main.py dpll -v
```

Top-level requirements are defined in `deps/requirements.txt`. The resolved output is written to `deps/lock.json`.

## How it works

Both resolvers operate over a synthetic package index (`deps/dep_graph.json`) containing 7 packages with two hidden conflicts:

- **`json-lib` conflict** — `api@2.0.0` requires `json-lib>=2.0.0`, but both versions of `database` require `json-lib<2.0.0`. The resolver must backtrack from `api@2.0.0` to `api@1.0.0`.
- **`crypto` conflict** — `auth@2.0.0` requires `crypto>=2.0.0`, but both versions of `cache` require `crypto<2.0.0`. The resolver must select `auth@1.0.0` to allow `crypto@1.5.0` to satisfy both constraints.

The resolved `lock.json` looks like:

```json
{
    "api": "1.0.0",
    "database": "2.0.0",
    "json-lib": "1.5.0",
    "auth": "1.0.0",
    "cache": "2.0.0",
    "crypto": "1.5.0"
}
```

You can modify `deps/dep_graph.json` and `deps/requirements.txt` to test different scenarios.
