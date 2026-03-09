# lock-on

Toy implementations of Backtracking and PubGrub dependency resolution algorithms in Python, comparing how pip and UV solve the same problem.


## Requirements

- [uv](https://docs.astral.sh/uv/getting-started/installation/) 

## Usage

```bash
# Run the backtracker
uv run main.py backtrack

# Run PubGrub
uv run main.py pubgrub

# Enable verbose logging to see the resolution trace
uv run main.py backtrack -v
uv run main.py pubgrub -v
```

Top-level requirements are defined in `deps/requirements.txt`. The resolved output is written to `deps/lock.json`.
