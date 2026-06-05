---
name: add-cute-black-cat
description: >
  One-command workflow that takes one image path and uses Grok Imagine image_edit
  to add a cute anime-style black cat into the photo. Use when the user runs
  /add-cute-black-cat, grok skill add-cute-black-cat, or asks to add a cute black
  cat, kawaii cat, or chibi black cat to a photo or image.
metadata:
  short-description: "Add a cute anime black cat to any photo"
---

# Add Cute Black Cat

Simple one-command workflow: take one image path and use Grok Imagine to add **one** cute anime-style black cat into the photo.

## Usage

```text
/add-cute-black-cat <image_path>
```

Examples:

```text
/add-cute-black-cat photo.jpg
/add-cute-black-cat pic/my_dog.jpg
```

Equivalent CLI:

```bash
grok skill add-cute-black-cat photo.jpg
grok skill add-cute-black-cat pic/my_dog.jpg
```

## Automatic workflow

Follow these steps every time the skill is invoked. Do **not** skip steps.

### 1. Resolve input

- The **first and only** positional argument is the image path.
- Resolve to an absolute path. If the file does not exist, stop and tell the user.
- Supported formats: `.jpg`, `.jpeg`, `.png`, `.webp`, `.gif`, `.bmp`, `.tiff`, `.tif` (any format `image_edit` accepts).

Optional helper (paths and output name only):

```bash
python3 .grok/skills/add-cute-black-cat/scripts/resolve_paths.py <image_path>
```

This prints JSON: `{"input": "...", "output": "...", "stem": "..."}`.

### 2. Load the imagine skill

Read `/work-dir/.grok/skills/imagine/SKILL.md` (or workspace-relative `.grok/skills/imagine/SKILL.md`) before calling image tools. Follow its prompting and `image_edit` rules.

### 3. Choose cat placement (before editing)

Inspect the image (read it with the Read tool). Pick **one** natural placement that fits the scene, for example:

- on someone's lap
- on a shoulder
- sitting on a table or counter
- peeking from a corner or behind furniture
- curled on a couch or bed
- beside the main subject on the ground

Record the chosen placement in one short phrase (e.g. `"on the left arm of the sofa"`). You will include this in the edit prompt and in the final log.

### 4. Edit with `image_edit` (required)

Use Grok Imagine **`image_edit`** — do **not** use `image_gen` for this skill. Do **not** write heavy Python or OpenCV pipelines; the edit is done by the image tool.

**Inputs:**

- `image`: absolute path to the input file (single reference)
- `prompt`: use this template, filling in `{placement}`:

```text
Add exactly one cute chibi kawaii anime-style black cat into this photo at {placement}.
The cat has big sparkling eyes, a small body, playful pose, glossy black fur with subtle white accents on chest and paws.
Integrate the cat naturally into the scene with matching perspective, scale, shadows, and contact with surfaces.
Preserve the original photo's lighting, color grading, style, and overall quality. Do not change unrelated parts of the image.
```

Keep the prompt to 2–5 sentences. Describe only what changes; state what must stay the same.

If the tool returns a file path, use that. If it returns inline image data, save it yourself (step 5).

### 5. Save output

- Output directory: **current working directory** (where the user ran the command), unless they specified another save location.
- Output filename: `<original_stem>_with_cat.jpg`
  - Example: `photo.jpg` → `photo_with_cat.jpg`
  - Example: `pic/my_dog.png` → `my_dog_with_cat.jpg`
- If the edit result is PNG or another format, convert or save as JPEG (quality ~90) so the final file ends in `.jpg`.
- Do **not** overwrite the input file.

Minimal save helper (only if needed after `image_edit`):

```bash
python3 .grok/skills/add-cute-black-cat/scripts/save_as_jpg.py <source_image> <output_path>
```

### 6. Print log

Print a short, user-visible summary:

```text
add-cute-black-cat: done
  input:  <absolute input path>
  output: <absolute output path>
  cat:    one chibi kawaii black cat at <placement phrase>
```

If the edit was blocked by moderation, say so clearly and do not retry with paraphrased prompts to evade filters.

## Agent checklist

- [ ] Exactly one image path argument
- [ ] Input file exists; input file not modified
- [ ] `imagine` skill guidance followed
- [ ] `image_edit` used (not `image_gen`)
- [ ] Exactly **one** cat added
- [ ] Output saved as `<stem>_with_cat.jpg` in the working directory
- [ ] Log printed with placement

## File layout

```text
.grok/skills/add-cute-black-cat/
├── SKILL.md
└── scripts/
    ├── resolve_paths.py
    └── save_as_jpg.py
```

## Dependencies

No extra packages required for the core workflow (`image_edit` only).

Optional helpers use Python 3 stdlib plus Pillow if `save_as_jpg.py` is needed:

```bash
pip install --break-system-packages Pillow
```

Container-aware (Podman Ubuntu): use `--break-system-packages` when installing Pillow system-wide.