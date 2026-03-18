# Normaleiddiwr Lleferydd Cymraeg / Welsh Speech Normalizer

## Cymraeg

### Trosolwg

Mae'r modiwl hwn yn normaleiddio trawsgrifiadau lleferydd Cymraeg air-am-air
(verbatim) i ffurfiau mwy darllenadwy. Pan fydd modelau adnabod lleferydd
(fel Whisper) yn trawsgrifio Cymraeg llafar, maen nhw'n aml yn cynhyrchu
ffurfiau tafodiaith, byrfoddau, a sillafu ansafonol. Mae'r normaleiddiwr yn
trosi'r ffurfiau hyn i'r Gymraeg ysgrifenedig safonol, tra'n cadw ystyr y
testun gwreiddiol.

### Enghreifftiau

| Verbatim (gwreiddiol) | Normalaidd (canlyniad) | Esboniad |
|------------------------|------------------------|----------|
| `bo' nw'n gwbod` | `bod nhw'n gwybod` | Ehangu byrfoddau berfol a rhagenwol, adfer llafariaid mewnol |
| `ma' nw 'di ca'l` | `mae nhw wedi cael` | Normaleiddio `ma'`→`mae`, `'di`→`wedi` (cyd-destunol), `ca'l`→`cael` |
| `petha <anadlu> dechre` | `pethau dechrau` | Safoni lluosogion tafodieithol, dileu tagiau di-leferydd |
| `rwbeth *actually* gwbod` | `rhywbeth actually gwybod` | Cywiro sillafu, dileu sêr o eiriau Saesneg |
| `yym dwi'm isio` | `ym dwi ddim eisiau` | Safoni petruster, ehangu negyddion, safoni sillafu |

### Categorïau Normaleiddio

Mae'r normaleiddiwr yn trin y categorïau canlynol, a phob un yn gallu cael
ei droi ymlaen neu i ffwrdd yn annibynnol:

- **Tagiau di-leferydd**: Dileu marcwyr fel `<anadlu>`, `<chwerthin>`, `<aneglur>`
- **Sêr (cod-newid)**: Dileu `*...*` o gwmpas geiriau Saesneg
- **Rhagenwau**: `nw`→`nhw`, `'u`→`eu`, `'ych`→`eich`
- **Byrfoddau berfol**: `ca'l`→`cael`, `bo'`→`bod`, `neud`→`gwneud`, `nath`→`gwnaeth`
- **Byrfoddau `mae`**: `ma'`→`mae` gyda normaleiddio dilynwyr cyd-destunol
- **`'di` cyd-destunol**: `'di`→`wedi` dim ond pan fo rhagenw yn dod o'i flaen (e.e. `dwi 'di`→`dwi wedi`)
- **Byrfoddau eraill**: `'na`→`yna`, `'ma`→`yma`, `'lly`→`felly`, `'chos`→`achos`, ac ati
- **Lluosogion tafodieithol**: `-a` (Gogledd) a `-e` (De) → `-au` safonol (e.e. `petha`/`pethe`→`pethau`)
- **Berfau tafodieithol**: `dechre`→`dechrau`, `gweitho`→`gweithio`, `clwad`→`clywed`
- **Llafariaid mewnol**: `gwbod`→`gwybod`, `me'wl`→`meddwl`, `amsar`→`amser`
- **Sillafu**: `rwbeth`→`rhywbeth`, `isio`→`eisiau`, `pobol`→`pobl`
- **Petruster**: Safoni `yym`/`yy`/`yrm`→`ym`, neu eu dileu'n gyfan gwbl
- **Dechreuadau ffals**: Dileu geiriau sy'n cael eu torri cyn eu gorffen (e.e. `m-`, `o-`)
- **Ymadroddion aml-air**: `o's gynnoch`→`oes gynnoch`, `dan dred`→`dan draed`

### Fflagio Achosion Ansicr

Mae'r normaleiddiwr yn fflagio achosion lle mae'r normaleiddio cywir yn amwys.
Er enghraifft, mae `'di` heb ragenw o'i flaen yn cael ei fflagio i'w adolygu
â llaw, yn hytrach na'i drawsnewid yn anghywir.

### Defnydd

```python
from normalization.welsh_normalizer import WelshNormalizer

# Creu gyda gosodiadau rhagosodedig (y rhan fwyaf o normaleiddiadau ymlaen)
normalizer = WelshNormalizer()

# Normaleiddio testun
result = normalizer.normalize("bo' nw'n gwbod <anadlu> petha")
# → "bod nhw'n gwybod pethau"

# Normaleiddio gyda fflagiau ansicr
result, flags = normalizer.normalize_with_flags("be' 'di hwnna")
# flags yn rhestru unrhyw achosion amwys

# Normaleiddio ffeil SRT (isdeitlau)
normalizer.normalize_srt_file("input.srt", "output.srt")
```

#### Llinell orchymyn

```bash
# Normaleiddio testun
python -m normalization.welsh_normalizer --text "bo' nw'n gwbod"

# Normaleiddio ffeil SRT
python -m normalization.welsh_normalizer --srt input.srt --output output.srt

# Cadw'r testun gwreiddiol uwchben y testun normalaidd yn yr allbwn
python -m normalization.welsh_normalizer --srt input.srt --output output.srt --include-original

# Dangos y cyfluniad presennol
python -m normalization.welsh_normalizer --text "test" --show-config
```

### Strwythur Ffeiliau

| Ffeil | Disgrifiad |
|-------|------------|
| `welsh_normalizer.py` | Y prif ddosbarth `WelshNormalizer` — rheolwr normaleiddio cyfluniadwy |
| `welsh_data.py` | Yr holl dablau chwilio ieithyddol: rhagenwau, byrfoddau, lluosogion, sillafu, ayyb |
| `tokenization.py` | Tocyneiddio sy'n cadw atalnodi a bylchau |

---

## English

### Overview

This module normalizes Welsh verbatim speech transcriptions into more readable
written equivalents. When speech recognition models (such as Whisper) transcribe
spoken Welsh, they often produce dialectal forms, contractions, and
non-standard spellings. The normalizer converts these into standard written
Welsh while preserving the original meaning.

### Examples

| Verbatim (input) | Normalized (output) | Explanation |
|-------------------|---------------------|-------------|
| `bo' nw'n gwbod` | `bod nhw'n gwybod` | Expand verb and pronoun contractions, restore internal vowels |
| `ma' nw 'di ca'l` | `mae nhw wedi cael` | Normalize `ma'`→`mae`, `'di`→`wedi` (contextual), `ca'l`→`cael` |
| `petha <anadlu> dechre` | `pethau dechrau` | Standardize dialectal plurals, remove non-speech tags |
| `rwbeth *actually* gwbod` | `rhywbeth actually gwybod` | Fix spelling, remove asterisks from English words |
| `yym dwi'm isio` | `ym dwi ddim eisiau` | Standardize hesitation, expand negation, fix spelling |

### Normalization Categories

The normalizer handles the following categories, each of which can be
independently enabled or disabled:

- **Non-speech tags**: Remove markers like `<anadlu>` (breathing), `<chwerthin>` (laughter), `<aneglur>` (unclear)
- **Asterisks (code-switching)**: Remove `*...*` around English words
- **Pronouns**: `nw`→`nhw` (they), `'u`→`eu` (their), `'ych`→`eich` (your)
- **Verb contractions**: `ca'l`→`cael` (get), `bo'`→`bod` (be/that), `neud`→`gwneud` (do), `nath`→`gwnaeth` (did)
- **`mae` contractions**: `ma'`→`mae` (is) with contextual follower normalization
- **Contextual `'di`**: `'di`→`wedi` (have/has) only when preceded by a pronoun (e.g. `dwi 'di`→`dwi wedi`)
- **Other contractions**: `'na`→`yna` (there), `'ma`→`yma` (here), `'lly`→`felly` (so), `'chos`→`achos` (because), etc.
- **Dialectal plurals**: `-a` (North) and `-e` (South) → standard `-au` (e.g. `petha`/`pethe`→`pethau`, things)
- **Dialectal verbs**: `dechre`→`dechrau` (start), `gweitho`→`gweithio` (work), `clwad`→`clywed` (hear)
- **Internal vowels**: `gwbod`→`gwybod` (know), `me'wl`→`meddwl` (think), `amsar`→`amser` (time)
- **Spelling**: `rwbeth`→`rhywbeth` (something), `isio`→`eisiau` (want), `pobol`→`pobl` (people)
- **Hesitations**: Standardize `yym`/`yy`/`yrm`→`ym`, or remove entirely
- **False starts**: Remove truncated words (e.g. `m-`, `o-`)
- **Multi-word phrases**: `o's gynnoch`→`oes gynnoch` (do you have), `dan dred`→`dan draed` (underfoot)

### Flagging Uncertain Cases

The normalizer flags cases where the correct normalization is ambiguous.
For example, `'di` without a preceding pronoun is flagged for manual review
rather than being incorrectly transformed. This is based on analysis of
21,259 verbatim Welsh speech transcriptions.

### Usage

```python
from normalization.welsh_normalizer import WelshNormalizer

# Create with default settings (most normalizations enabled)
normalizer = WelshNormalizer()

# Normalize text
result = normalizer.normalize("bo' nw'n gwbod <anadlu> petha")
# → "bod nhw'n gwybod pethau"

# Normalize with uncertainty flags
result, flags = normalizer.normalize_with_flags("be' 'di hwnna")
# flags lists any ambiguous cases

# Normalize an SRT subtitle file
normalizer.normalize_srt_file("input.srt", "output.srt")
```

#### Command line

```bash
# Normalize text
python -m normalization.welsh_normalizer --text "bo' nw'n gwbod"

# Normalize an SRT file
python -m normalization.welsh_normalizer --srt input.srt --output output.srt

# Keep original text above normalized text in output
python -m normalization.welsh_normalizer --srt input.srt --output output.srt --include-original

# Show current configuration
python -m normalization.welsh_normalizer --text "test" --show-config
```

### Configuration

All normalization categories can be toggled individually:

```python
normalizer = WelshNormalizer(
    remove_tags=True,              # Remove <anadlu> etc.
    remove_asterisks=True,         # Remove *English* markers
    expand_pronouns=True,          # nw → nhw
    expand_verb_contractions=True,  # ca'l → cael
    expand_mae_contractions=True,   # ma' → mae
    normalize_ma_with_followers=True,  # ma' nw → mae nhw
    expand_di_contextual=True,      # dwi 'di → dwi wedi
    standardize_plurals=True,       # petha → pethau
    standardize_verbs=True,         # dechre → dechrau
    standardize_internal=True,      # gwbod → gwybod
    standardize_spelling=True,      # rwbeth → rhywbeth
    remove_hesitations=False,       # Keep hesitations (default)
    standardize_hesitations=True,   # yym → ym
    remove_false_starts=True,       # Remove m-, o- etc.
    flag_uncertain=True,            # Flag ambiguous cases
    custom_corrections={"myword": "replacement"},  # Add your own
)
```

### File Structure

| File | Description |
|------|-------------|
| `welsh_normalizer.py` | Main `WelshNormalizer` class — configurable normalization engine |
| `welsh_data.py` | All linguistic lookup tables: pronouns, contractions, plurals, spelling, etc. |
| `tokenization.py` | Punctuation- and whitespace-preserving tokenizer |
