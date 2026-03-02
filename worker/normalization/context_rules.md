# Welsh Speech Normalization: Context Rules

## Overview

This document describes the context-dependent normalization rules discovered from analyzing 21,259 verbatim Welsh speech transcriptions.

---

## Rule 1: `ma'` Normalization

**The problem**: `ma'` (colloquial form of `mae` = "is") appears 4,421 times. About 50% should stay as `ma'` and 50% could be normalized to `mae`.

### Keep as `ma'` when followed by:

| Following Word | Count | Pattern | Meaning |
|---------------|-------|---------|---------|
| `'na` | 538 | `ma' 'na` | "there is" (existential) |
| `nw'n` | 331 | `ma' nw'n` | "they are" |
| `fe'n` | 139 | `ma' fe'n` | "he is" |
| `nw` | 137 | `ma' nw` | "they" |
| `n'w` | 135 | `ma' n'w` | "they" |
| `fe` | 126 | `ma' fe` | "he" |
| `raid` | 97 | `ma' raid` | "must" |
| `hwnna'n` | 78 | `ma' hwnna'n` | "that is" |
| `'di` | 50 | `ma' 'di` | (perfect aspect) |
| `hi`, `hi'n` | 40 | `ma' hi'n` | "she is" |
| `nhw`, `nhw'n` | 38 | `ma' nhw'n` | "they are" |
| `'da` | 27 | `ma' 'da fi` | "I have" |
| `gen`, `gyda`, `gynnon` | 53 | possession | "have/has" |

**Rule**: If `ma'` is followed by any of these, **keep as `ma'`**.

### Normalize `ma'` → `mae` when followed by:

| Following Word | Count | Example |
|---------------|-------|---------|
| `pobol`/`bobol` | 75 | `mae pobol yn...` |
| `pawb` | 30 | `mae pawb yn...` |
| `lot` | 38 | `mae lot o...` |
| General nouns | varies | `mae'r car yn...` |

**Rule**: If `ma'` is followed by a general noun/subject, **normalize to `mae`**.

### Flag as uncertain:

Any `ma' + X` where X is not in either list should be **flagged for manual review**.

---

## Rule 2: `'di` Expansion

**The problem**: `'di` (colloquial form of `wedi` = "have/has") appears 1,563 times.

### Safe to expand when preceded by:

| Preceding Word | Count | Example | Result |
|---------------|-------|---------|--------|
| `dwi` | 187 | `dwi 'di gweld` | `dwi wedi gweld` |
| `ni` | 117 | `ni 'di bod` | `ni wedi bod` |
| `fi` | 111 | `fi 'di neud` | `fi wedi neud` |
| `ti` | 74 | `ti 'di gweld` | `ti wedi gweld` |
| `sy` | 68 | `sy 'di dod` | `sy wedi dod` |
| `nw`/`n'w` | 81 | `nw 'di gweld` | `nhw wedi gweld` |
| `chi` | 29 | `chi 'di clywed` | `chi wedi clywed` |
| `ma'`/`mae` | 85 | `ma' 'di digwydd` | keep as-is |

**Rule**: If `'di` is preceded by a pronoun, **expand to `wedi`**.

### Keep as `'di` when:

| Preceding Word | Example | Meaning |
|---------------|---------|---------|
| `be'` | `be' 'di hwnna` | "what is that" |
| Other non-pronouns | varies | uncertain |

**Rule**: If `'di` is not preceded by a known pronoun, **flag for review**.

---

## Rule 3: Hesitation Handling

### Position Analysis

| Position | `yym` count | `yy` count |
|----------|-------------|------------|
| Start | 683 | 446 |
| Middle | 1,613 | 1,798 |
| End | 422 | 140 |

### Double Hesitations

| Pattern | Count |
|---------|-------|
| `yy yy` | 91 |
| `yym yy` | 49 |
| `yy yym` | 33 |
| `yym yym` | 12 |

### Suggested Rules:

1. **Collapse doubles**: `yy yy` → `yy`, `yym yy` → `yym`
2. **Remove boundary hesitations**: Remove `yym`/`yy` at start or end of utterance
3. **Keep middle hesitations**: They mark speech rhythm

---

## Rule 4: False Starts

False starts (words ending in `-`) often precede words starting with the same sound:

| Pattern | Count | What Follows |
|---------|-------|--------------|
| `o- o...` | 34 | Repeated start |
| `y- yn` | 31 | → `yn` |
| `a- a...` | 25 | Repeated start |
| `m- ma` | 23 | → `ma` or `mae` |

**Rule**: Safe to remove false starts. The complete word usually follows.

---

## Rule 5: `bo'` Normalization

`bo'` (colloquial `bod` = "that/being") is **generally safe to normalize** to `bod`.

### Typical contexts:

| Pattern | Count | Example |
|---------|-------|---------|
| `bo' + pronoun` | 400+ | `bo' ni'n gwybod` |
| `bo' 'na` | 93 | `bo' 'na problem` |

**Rule**: `bo'` → `bod` is almost always safe.

---

## Rule 6: `nw`/`n'w` → `nhw`

This is **always safe** regardless of context.

| Preceding | Count |
|-----------|-------|
| `ma'` | 272 |
| `bo'` | 51 |
| `iddyn` | 41 |
| `ohonyn` | 23 |
| Other | varies |

**Rule**: `nw` → `nhw` and `n'w` → `nhw` are context-independent.

---

## Implementation Summary

### Always Safe (Context-Independent)

```python
# These corrections can always be applied
ALWAYS_SAFE = {
    "nw": "nhw",
    "n'w": "nhw", 
    "nw'n": "nhw'n",
    "ca'l": "cael",
    "ga'l": "gael",
    "bo'": "bod",
    "gwbod": "gwybod",
    "rwbeth": "rhywbeth",
    # ... etc
}
```

### Context-Dependent (Need Rules)

```python
# ma' -> mae: only when NOT followed by protected words
MA_PROTECTED = {"'na", "nw'n", "fe'n", "hi'n", "raid", ...}

# 'di -> wedi: only when preceded by pronoun  
DI_SAFE_PRECEDERS = {"dwi", "fi", "ti", "ni", "chi", ...}
```

### Flag for Review (Uncertain)

- `ma'` followed by unknown word
- `'di` not preceded by pronoun
- Any pattern not matching known rules

---

## Files

| File | Description |
|------|-------------|
| `welsh_normalizer_context.py` | Context-aware normalizer with flagging |
| `welsh_normalizer.py` | Simple configurable normalizer |
| `PATTERN_ANALYSIS.md` | Full pattern frequency analysis |