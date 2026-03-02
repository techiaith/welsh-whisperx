# Welsh Verbatim Speech Patterns Analysis

## Overview

This analysis examines **21,259 verbatim transcriptions** of Welsh speech to identify patterns that could be candidates for "light normalization". The patterns are grouped by category to help you decide which normalizations to apply.

**Important**: This is a discovery document. You decide which patterns to normalize based on your project's goals.

---

## Category A: Non-Speech Sound Tags

**Recommendation: These should almost certainly be removed**

These are annotations added during transcription to mark non-speech sounds:

| Tag | Meaning | Count |
|-----|---------|-------|
| `<anadlu>` | breathing | 4,869 |
| `<chwerthin>` | laughter | 630 |
| `<aneglur>` | unclear speech | 368 |
| `<twtian>` | tutting | 256 |
| `<cerddoriaeth>` | music | 106 |
| `<ochneidio>` | sighing | 41 |
| `<clirio gwddf>` | clearing throat | 25 |
| `<tros-siarad>` | overlapping speech | 17 |
| `<sniffian>` | sniffing | 6 |
| `<peswch>` | coughing | 3 |

**Note**: There are also typo variants like `<anadalu>`, `<chwethin>`, `<andlu>`, etc. A regex pattern `<[^>]+>` will catch all of these.

---

## Category B: Code-Switched English Words

**Recommendation: Remove asterisks, keep the words**

English words and phrases are marked with asterisks in the transcriptions:

| Pattern | Count |
|---------|-------|
| `*like*` | 96 |
| `*actually*` | 64 |
| `*Tour de France*` | 52 |
| `*Vuelta*` | 50 |
| `*Facebook*` | 49 |
| `*migraine*` | 48 |
| `*migraines*` | 42 |
| `*Froome*` | 40 |
| `*Sky*` | 38 |
| `*Twitter*` | 30 |

There are approximately **400 unique English words/phrases** marked this way.

---

## Category C: Contractions

**Your decision needed**: Expand to full form or keep contracted?

### C1: Pronoun Contractions

| Verbatim | Full Form | Count | Notes |
|----------|-----------|-------|-------|
| `nw` | `nhw` | 1,352 | "they/them" |
| `n'w` | `nhw` | 652 | "they/them" with apostrophe |
| `nw'n` | `nhw'n` | 585 | "they" + progressive particle |

### C2: Verb Contractions

| Verbatim | Full Form | Count | Notes |
|----------|-----------|-------|-------|
| `ca'l` | `cael` | 1,011 | "to get" |
| `ga'l` | `gael` | 363 | "to get" (soft mutation) |
| `bo'` | `bod` | ~840 | "that/being" |
| `me'wl` | `meddwl` | 178 | "to think" |
| `ne'` | `neu` | 238 | "or" |

### C3: 'Mae' (is) Contractions

| Verbatim | Full Form | Count | Notes |
|----------|-----------|-------|-------|
| `ma'` | `mae` | 4,421 | Very frequent! |
| `ma'r` | `mae'r` | 787 | "is the" |
| `ma'n` | `mae'n` | 615 | "is" + particle |

**Consideration**: `ma'` alone accounts for 4,421 occurrences. This is very common in spoken Welsh. Expanding it may feel "over-normalized".

### C4: Article Contractions

| Verbatim | Count | Notes |
|----------|-------|-------|
| `o'r` | 815 | "of the" - standard written form |
| `i'r` | 778 | "to the" - standard written form |
| `a'r` | 407 | "and the" - standard written form |
| `efo'r` | 134 | "with the" (North) |
| `gyda'r` | 83 | "with the" (South) |

**Note**: `o'r`, `i'r`, `a'r` are actually standard in written Welsh, not colloquial contractions.

### C5: Other Common Contractions

| Verbatim | Full Form | Count | Notes |
|----------|-----------|-------|-------|
| `'di` | `wedi` | 1,563 | "have/has" (perfective) |
| `'na` | `yna` | 1,419 | "there" |
| `'ma` | `yma` | 370 | "here" |
| `'dan` | `rydyn/rydym` | 389 | "we are" |
| `o'n` | `roeddwn/oeddwn` | 1,333 | "I was/were" |
| `o'dd` | `roedd/oedd` | 599 | "was/were" |
| `do's` | `does` | 87 | "there isn't" |
| `o's` | `oes` | 99 | "is there?" |
| `dwi'm` | `dydw i ddim` | 164 | "I don't/am not" |

---

## Category D: Vowel Reductions

**Your decision needed**: These are spoken pronunciations. Normalize to written standard?

### D1: Plural Suffix Reductions

In speech, the plural `-au` often becomes `-a` (North) or `-e` (South):

| Spoken (N) | Spoken (S) | Standard | Count (N/S) | Meaning |
|------------|------------|----------|-------------|---------|
| `petha` | `pethe` | `pethau` | 149/204 | "things" |
| `betha` | `bethe` | `pethau` | 40/67 | "things" (mutated) |
| `weithia` | `weithie` | `weithiau` | 35/39 | "sometimes" |
| - | `coese` | `coesau` | -/24 | "legs" |
| - | `cymeriade` | `cymeriadau` | -/23 | "characters" |
| - | `pwyse` | `pwysau` | -/23 | "pressure" |
| `gora` | `gore` | `gorau` | 34/31 | "best" |
| - | `enwe` | `enwau` | -/31 | "names" |

### D2: Verb Stem Reductions

| Spoken | Standard | Count | Meaning |
|--------|----------|-------|---------|
| `dechre` | `dechrau` | 98 | "start" |
| `dechra` | `dechrau` | 45 | "start" (North) |
| `ddechre` | `ddechrau` | 37 | "start" (mutated) |
| `gweitho` | `gweithio` | 42 | "work" |
| `disgwl` | `disgwyl` | 55 | "expect" |
| `gobitho` | `gobeithio` | 20 | "hope" |
| `grando` | `gwrando` | 30 | "listen" |
| `gadal` | `gadael` | 27 | "leave" |
| `cyrradd` | `cyrraedd` | 34 | "arrive" |
| `diodde` | `dioddef` | 18 | "suffer" |
| `cwmpo` | `cwympo` | 13 | "fall" |
| `lico` | `licio` | 34 | "like" |
| `timlo` | `teimlo` | 30 | "feel" |

### D3: Internal Vowel Reductions

| Spoken | Standard | Count | Meaning |
|--------|----------|-------|---------|
| `gwbod` | `gwybod` | 291 | "know" |
| `gwbo` | `gwybod` | 83 | "know" (more reduced) |
| `sicir` | `sicr` | 71 | "certain" |
| `amsar` | `amser` | 37 | "time" |
| `mowr` | `mawr` | 38 | "big" |
| `amal` | `aml` | 54 | "often" |
| `wthnos` | `wythnos` | 64 | "week" |
| `cymyd` | `cymryd` | 31 | "take" |
| `ymlan` | `ymlaen` | 14 | "forward" |

---

## Category E: Spelling Standardizations

**Your decision needed**: Standardize variant spellings?

| Spoken | Standard | Count | Meaning |
|--------|----------|-------|---------|
| `rwbeth` | `rhywbeth` | 214 | "something" |
| `rwbath` | `rhywbeth` | 104 | "something" |
| `wbath` | `rhywbeth` | 47 | "something" |
| `gellu` | `gallu` | 102 | "can/able" |
| `efyd` | `hefyd` | 29 | "also" |
| `cymra'g` | `cymraeg` | 52 | "Welsh" |
| `lloeger` | `lloegr` | 20 | "England" |
| `ytrach` | `hytrach` | 22 | "rather" |
| `sicirhau` | `sicrhau` | 34 | "ensure" |

---

## Category F: Hesitation and Filler Markers

**Your decision needed**: Keep? Remove? Standardize?

### F1: Filled Pauses

| Pattern | Count |
|---------|-------|
| `yym` | 3,308 |
| `yy` | 2,587 |
| `yrm` | 137 |
| `ymm` | 32 |

**Options**:
1. Keep all as-is (preserves spoken character)
2. Standardize all to one form (e.g., all become `ym`)
3. Remove all (cleaner text but loses spoken feel)

### F2: False Starts

Words that are cut off mid-utterance:

| Pattern | Count |
|---------|-------|
| `m-` | 150 |
| `o-` | 107 |
| `a-` | 106 |
| `s-` | 92 |
| `y-` | 74 |
| `d-` | 72 |
| `dy-` | 59 |

**Options**:
1. Keep as-is
2. Remove entirely

---


## Category H: Regional Variants

**Your decision needed**: Standardize to one dialect or keep regional forms?

| North | South | Standard | Meaning | N count / S count |
|-------|-------|----------|---------|-------------------|
| `isio` | `isie` | `eisiau` | "want" | 214 / 119 |
| `rwan` | `nawr` | - | "now" | 8 / 228 |
| `efo` | `gyda` | - | "with" | 514 / 450 |
| `fo` | `fe` | - | "he" | 272 / 565 |
| `allan` | `mas` | - | "out" | 255 / 105 |
| `fatha` | - | `fel` | "like" | 314 / - |

---

## Summary: Suggested Normalization Tiers

### Tier 1: Almost Certainly Normalize
- Remove `<tag>` markers for non-speech sounds
- Remove asterisks from `*English*` words

### Tier 2: Commonly Normalized
- `nw` / `n'w` → `nhw`
- `ca'l` / `ga'l` → `cael` / `gael`
- `bo'` → `bod`
- `gwbod` → `gwybod`
- `rwbeth`/`rwbath`/`wbath` → `rhywbeth`

### Tier 3: Consider Your Goals
- `ma'` → `mae` (very frequent - may over-normalize)
- Vowel reductions in verbs and plurals
- Regional variants (depends on your standardization goals)

### Tier 4: Preserve Spoken Character
- Hesitation markers (`yym`, `yy`)
- False starts (`m-`, `a-`, etc.)

---

## What You Should Decide

1. **How "normalized" should "light normalization" be?**
   - Just clean up markup? (Tiers 1-2)
   - Also standardize spelling? (+ Tier 3)
   - Remove spoken features? (+ Tier 4)

2. **Regional handling?**
   - Keep North/South variants as-is?
   - Standardize to one dialect?
   - Standardize to literary Welsh?

3. **Hesitation markers?**
   - Keep for spoken authenticity?
   - Standardize to one form?
   - Remove entirely?

---

*Analysis based on 21,259 verbatim transcriptions from train.tsv, validation.tsv, and test.tsv*
