# 🪵 gipity (gpt) codebase prompt

strip a codebase down into a clean prompt-friendly format (for when llms are actually useful).

## what it does

- walks a directory, skips the noise (e.g. `.git`, `node_modules`, etc.)
- only shows files with useful extensions (`.py`, `.js`, `.ts`, etc.)
- optionally inlines the content of specific files
- copies the whole thing to your clipboard
- basically turns a codebase into a ChatGPT prompt

## how to use

```bash
python wood_chipper.py /some/project
```

→ dumps the structure of `/some/project`

```bash
python wood_chipper.py /some/project main.py,utils.py
```

→ dumps structure + includes full contents of `main.py` and `utils.py`

## example

```
dir: app
 file: main.py
/some/project/main.py:
# this is main.py file contents...
 file: config.py
/some/project/config.py:
# this is config.py file contents...
```

copied to clipboard, ready to paste into chatgpt.
