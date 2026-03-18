# welsh-whisperx

Gweinydd lleferydd-i-destun Cymraeg wedi'i adeiladu ar WhisperX ac wedi'i optimeiddio ar gyfer cywirdeb a chefnogaeth i'r iaith Gymraeg.

A production-ready Welsh speech-to-text server built on WhisperX, optimized for accuracy, scalability, and Welsh language support.

> **[English version below / Fersiwn Saesneg isod](#english)**

---

<a id="cymraeg"></a>

## Prif Fanteision

### 🎯 **Wedi'i Optimeiddio ar gyfer y Gymraeg**
- **Modelau wedi'u mireinio**: Modelau Whisper a Wav2Vec2 penodol i'r Gymraeg gan Techiaith
- **Normaleiddio testun Cymraeg**: Normaleiddio testun llafar yn awtomatig
  - Ehangu talfyriadau (ma'→mae, ca'l→cael)
  - Safoni amrywiadau tafodieithol (petha→pethau, gwbod→gwybod)
  - Normaleiddio rhagenwau a ffurfiau berfol
- **Canfod iaith**: Canfod Cymraeg/Saesneg yn awtomatig gyda Lingua
- **Aliniad cywir**: Stampiau amser ar lefel geiriau wedi'u hoptimeiddio ar gyfer seineg y Gymraeg

### ⚡ **Perfformiad Uchel a Graddadwyedd**
- **Cyflymu GPU**: Cefnogaeth lawn NVIDIA CUDA ar gyfer trawsgrifio cyflym
- **Gweithwyr ciw pwrpasol**: Gweithwyr blaenoriaeth uchel a rhagosodedig ar wahân, yn raddadwy'n annibynnol
- **Blaenoriaethu tasgau**: System flaenoriaethu dwy lefel (llwybro ciwiau + blaenoriaethau rhifol)
- **Swpio effeithlon**: Casgliad WhisperX ar gyfer cyflymu 12x
- **Rheoli cof**: Glanhau awtomatig ac ailgylchu gweithwyr i atal gollyngiadau cof

### 🔧 **Yn Barod ar gyfer Cynhyrchu**
- **Defnyddio mewn cynwysyddion**: Docker Compose ar gyfer amgylcheddau GPU a CPU
- **Monitro iechyd**: Gwiriadau iechyd cynhwysfawr ar gyfer yr holl wasanaethau
- **Glanhau awtomatig**: Dileu ffeiliau hen yn ôl amserlen i atal gormod o ddata ar y ddisg
- **Parhauster tasgau**: Ciw wedi'i gefnogi gan Redis yn goroesi ailgychwyn
- **Logio**: Logio fesul tasg ar gyfer dadfygio a monitro
- **Dogfennaeth API**: Dogfennau OpenAPI/Swagger wedi'u cynhyrchu'n awtomatig

### 📊 **Fformatau Allbwn Cyfoethog**
- **JSON**: Trawsgrifiad llawn gyda stampiau amser ar lefel geiriau a sgoriau
- **SRT/VTT**: Ffeiliau isdeitlau gyda rhannu llinellau deallus
- **ELAN**: Anodiadau llinell amser ar gyfer dadansoddi ieithyddol
- **Testun**: Trawsgrifiad testun plaen
- **Diarization siaradwyr**: Adnabod siaradwyr gwahanol (SIARADWR_01, ayyb.)
- **Testun wedi'i normaleiddio**: Normaleiddio testun Cymraeg wedi'i gynnwys

### 🚀 **Cyfeillgar i Ddatblygwyr**
- **API RESTful**: Diweddbwyntiau HTTP syml ar gyfer yr holl weithrediadau
- **Archwilio ciwiau**: Monitro tasgau aros a statws gweithwyr
- **Defnyddio hyblyg**: Modd CPU yn unig ar gyfer datblygu, GPU ar gyfer cynhyrchu
- **Rheoli amgylchedd**: Ffurfweddiad tryloyw gyda gwahanu cyfrinachau
- **Dogfennaeth gynhwysfawr**: Canllawiau pensaernïaeth, defnyddio, a datrys problemau

### 🔒 **Nodweddion Menter**
- **Cefnogaeth modelau preifat**: Dilysu gyda HuggingFace ar gyfer modelau preifat
- **Tracio tasgau**: IDau tasg parhaol ar draws ailgychwyn y gweinydd
- **Cadw canlyniadau**: Terfyn 7 diwrnod ar ganlyniadau gyda Redis
- **CORS wedi'i alluogi**: Mynediad API cyfeillgar i borwyr
- **Trin gwallau**: Dirywiad gosgeiddig a negeseuon gwall manwl

---

A production-ready Welsh speech-to-text server built on WhisperX, optimized for accuracy, scalability, and Welsh language support.

> **[English version below / Fersiwn Saesneg isod](#english)**

---

<a id="cymraeg"></a>

## Prif Fanteision

### 🎯 **Wedi'i Optimeiddio ar gyfer y Gymraeg**
- **Modelau wedi'u mireinio**: Modelau Whisper a Wav2Vec2 penodol i'r Gymraeg gan Techiaith
- **Normaleiddio testun Cymraeg**: Normaleiddio testun llafar yn awtomatig
  - Ehangu talfyriadau (ma'→mae, ca'l→cael)
  - Safoni amrywiadau tafodieithol (petha→pethau, gwbod→gwybod)
  - Normaleiddio rhagenwau a ffurfiau berfol
- **Canfod iaith**: Canfod Cymraeg/Saesneg yn awtomatig gyda Lingua
- **Aliniad cywir**: Stampiau amser ar lefel geiriau wedi'u hoptimeiddio ar gyfer seineg y Gymraeg

### ⚡ **Perfformiad Uchel a Graddadwyedd**
- **Cyflymu GPU**: Cefnogaeth lawn NVIDIA CUDA ar gyfer trawsgrifio cyflym
- **Gweithwyr ciw pwrpasol**: Gweithwyr blaenoriaeth uchel a rhagosodedig ar wahân, yn raddadwy'n annibynnol
- **Blaenoriaethu tasgau**: System flaenoriaethu dwy lefel (llwybro ciwiau + blaenoriaethau rhifol)
- **Swpio effeithlon**: Casgliad WhisperX ar gyfer cyflymu 12x
- **Rheoli cof**: Glanhau awtomatig ac ailgylchu gweithwyr i atal gollyngiadau cof

### 🔧 **Yn Barod ar gyfer Cynhyrchu**
- **Defnyddio mewn cynwysyddion**: Docker Compose ar gyfer amgylcheddau GPU a CPU
- **Monitro iechyd**: Gwiriadau iechyd cynhwysfawr ar gyfer yr holl wasanaethau
- **Glanhau awtomatig**: Dileu ffeiliau hen yn ôl amserlen i atal gormod o ddata ar y ddisg
- **Parhauster tasgau**: Ciw wedi'i gefnogi gan Redis yn goroesi ailgychwyn
- **Logio**: Logio fesul tasg ar gyfer dadfygio a monitro
- **Dogfennaeth API**: Dogfennau OpenAPI/Swagger wedi'u cynhyrchu'n awtomatig

### 📊 **Fformatau Allbwn Cyfoethog**
- **JSON**: Trawsgrifiad llawn gyda stampiau amser ar lefel geiriau a sgoriau
- **SRT/VTT**: Ffeiliau isdeitlau gyda rhannu llinellau deallus
- **ELAN**: Anodiadau llinell amser ar gyfer dadansoddi ieithyddol
- **Testun**: Trawsgrifiad testun plaen
- **Diarization siaradwyr**: Adnabod siaradwyr gwahanol (SIARADWR_01, ayyb.)
- **Testun wedi'i normaleiddio**: Normaleiddio testun Cymraeg wedi'i gynnwys

### 🚀 **Cyfeillgar i Ddatblygwyr**
- **API RESTful**: Diweddbwyntiau HTTP syml ar gyfer yr holl weithrediadau
- **Archwilio ciwiau**: Monitro tasgau aros a statws gweithwyr
- **Defnyddio hyblyg**: Modd CPU yn unig ar gyfer datblygu, GPU ar gyfer cynhyrchu
- **Rheoli amgylchedd**: Ffurfweddiad tryloyw gyda gwahanu cyfrinachau
- **Dogfennaeth gynhwysfawr**: Canllawiau pensaernïaeth, defnyddio, a datrys problemau

### 🔒 **Nodweddion Menter**
- **Cefnogaeth modelau preifat**: Dilysu gyda HuggingFace ar gyfer modelau preifat
- **Tracio tasgau**: IDau tasg parhaol ar draws ailgychwyn y gweinydd
- **Cadw canlyniadau**: Terfyn 7 diwrnod ar ganlyniadau gyda Redis
- **CORS wedi'i alluogi**: Mynediad API cyfeillgar i borwyr
- **Trin gwallau**: Dirywiad gosgeiddig a negeseuon gwall manwl

---

## Rhagofynion

- **Docker** a **Docker Compose** (gofynnol)
- **Linux** neu **macOS** — heb ei brofi ar Windows
- **Modd GPU**: GPU NVIDIA + nvidia-docker2
- **Cof**: Isafswm 8GB RAM (16GB+ yn argymhellir ar gyfer modd GPU)
- **Disg**: O leiaf 20GB o le rhydd ar gyfer modelau a recordiadau

---

## Cychwyn Cyflym

### Gosod Cychwynnol
```bash
# Clonio'r ystorfa
git clone https://storfa.techiaith.cymru/lleferydd/stt-cy/whisperx-server
cd whisperx-server

# Gosod ffeiliau amgylchedd
make setup

# Golygu .env.secrets ac ychwanegu eich tocyn HuggingFace
# Cewch eich tocyn o: https://huggingface.co/settings/tokens
nano .env.secrets

# Ail-gynhyrchu .env gyda'ch tocyn
make setup
```

### Defnyddio GPU (Argymhellir ar gyfer Cynhyrchu)
```bash
# Adeiladu a rhedeg gyda chefnogaeth GPU (angen nvidia-docker)
# Yn cychwyn 1 gweithiwr blaenoriaeth uchel + 1 gweithiwr rhagosodedig
make build-gpu

# Graddio gweithwyr yn annibynnol
make scale-high-gpu N=2       # 2 weithiwr blaenoriaeth uchel
make scale-default-gpu N=3    # 3 gweithiwr rhagosodedig
```

### Defnyddio CPU (Ar gyfer Datblygu/Profi)
```bash
# Adeiladu a rhedeg gyda CPU yn unig (dim GPU yn ofynnol)
# Yn cychwyn 1 gweithiwr blaenoriaeth uchel + 1 gweithiwr rhagosodedig
make build-cpu

# Graddio gweithwyr yn annibynnol
make scale-high-cpu N=2       # 2 weithiwr blaenoriaeth uchel
make scale-default-cpu N=2    # 2 weithiwr rhagosodedig
```

### Gorchmynion Cyffredin
```bash
make help          # Dangos yr holl orchmynion sydd ar gael
make ready         # Aros i'r modelau orffen llwytho
make status        # Dangos cynwysyddion sy'n rhedeg
make health        # Gwirio iechyd gwasanaeth
make logs          # Gweld logiau cynwysyddion
make down          # Stopio'r holl gynwysyddion
```

### Mynediad i'r API
Unwaith y bydd yn rhedeg, mynediad i'r API yn: http://localhost:5511

**Gwiriad Iechyd:** http://localhost:5511/health/
**Dogfennau API:** http://localhost:5511/docs (wedi'i gynhyrchu'n awtomatig gan FastAPI)

### Ap Gwe
Mae ap gwe syml ar gael yn y ffolder `app/` ar gyfer cyflwyno trawsgrifiadau a chyfieithiadau trwy'r porwr. I'w ddefnyddio:

```bash
python3 -m http.server 8080 --directory app/
```

Yna agorwch http://localhost:8080 yn eich porwr. Mae'r ap yn cysylltu â'r API ar `localhost:5511`.

---

## Enghreifftiau Defnyddio'r API

### Trawsgrifio Sain (Ffurf Fer, Cydamserol)
```bash
# Rhagosodiad: blaenoriaeth uchel (wedi'i lwybro i giw high_priority)
curl -X POST "http://localhost:5511/transcribe/" \
  -F "soundfile=@sain.wav"

# Blaenoriaeth normal yn benodol (dal yn mynd i giw high_priority)
curl -X POST "http://localhost:5511/transcribe/" \
  -F "soundfile=@sain.wav" \
  -F "priority=normal"
```

### Trawsgrifio Sain Hir (Anghydamserol)
```bash
# Cyflwyno tasg (wedi'i lwybro i giw default)
curl -X POST "http://localhost:5511/transcribe_long_form/" \
  -F "soundfile=@sain_hir.wav"

# Dychwelyd: {"id": "uuid", "version": 2, "success": true}

# Gwirio statws
curl "http://localhost:5511/get_status/?stt_id=<uuid>"

# Cael canlyniadau pan fo'n gyflawn
curl "http://localhost:5511/get_json/?stt_id=<uuid>"
curl "http://localhost:5511/get_srt/?stt_id=<uuid>"
curl "http://localhost:5511/get_vtt/?stt_id=<uuid>"
```

### Cyfieithu Sain (Cymraeg → Saesneg)
```bash
# Ffurf fer (cydamserol, uchafswm 480KB)
curl -X POST "http://localhost:5511/translate/" \
  -F "soundfile=@sain.wav"

# Ffurf hir (anghydamserol, unrhyw faint)
curl -X POST "http://localhost:5511/translate_long_form/" \
  -F "soundfile=@sain_hir.wav"
```

### Alinio Testun â Sain (Stampiau Amser fesul Gair)
```bash
# Ffurf fer (cydamserol, uchafswm 480KB)
curl -X POST "http://localhost:5511/align/" \
  -F "soundfile=@sain.wav" \
  -F "text=Mae ganddynt dau o blant, mab a merch"

# Ffurf hir (anghydamserol, unrhyw faint — yn rhedeg ar CPU)
curl -X POST "http://localhost:5511/align_long_form/" \
  -F "soundfile=@sain_hir.wav" \
  -F "text=Testun llawn i'w alinio â'r sain..."

# Gwirio statws
curl "http://localhost:5511/get_status/?stt_id=<uuid>"

# Cael canlyniadau
curl "http://localhost:5511/get_json/?stt_id=<uuid>"
```

### Mewnbwn Bysellfwrdd Amser Real (Blaenoriaeth Uchel Bob Amser)
```bash
curl -X POST "http://localhost:5511/keyboard/" \
  -F "audio_file=@mewnbwn_llais.wav"
# Wedi'i lwybro bob amser i giw high_priority gyda blaenoriaeth frys
```

---

## Pensaernïaeth

### Cydrannau

```
┌──────────────────┐
│    FastAPI App    │  Porth 5511
│ (Gweinydd API)   │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Brocer Redis    │  Porth 6379
│  (Ciw Tasgau)    │
├──────────────────┤
│ high_priority    │  /transcribe/, /keyboard/, /translate/
│ default          │  /transcribe_long_form/, /translate_long_form/
│ alignment        │  /align/, /align_long_form/
└──┬───┬───┬───────┘
   │   │   │
   ▼   ▼   ▼
┌────────┐ ┌─────────┐ ┌───────────┐
│worker  │ │worker   │ │worker     │  Yn Raddadwy'n
│-high   │ │-default │ │-alignment │  Annibynnol
│(GPU)   │ │(GPU)    │ │(CPU x2)   │
└────────┘ └─────────┘ └───────────┘
```

### Gwasanaethau

- **Application (FastAPI)**: Gweinydd API REST yn trin ceisiadau
- **worker-high (Celery)**: Pwrpasol ar gyfer tasgau blaenoriaeth uchel (`/transcribe/`, `/keyboard/`, `/translate/`)
- **worker-default (Celery)**: Pwrpasol ar gyfer tasgau rhagosodedig (`/transcribe_long_form/`, `/translate_long_form/`)
- **worker-alignment (Celery)**: Pwrpasol ar gyfer alinio ar CPU (`/align/`, `/align_long_form/`) — 2 replica rhag ofn bod tasg hir yn rhwystro
- **Redis**: Brocer negeseuon a storfa canlyniadau

### System Ciwiau a Blaenoriaethu Tasgau

Mae'r system yn defnyddio **blaenoriaethu dwy lefel**: gweithwyr ciw pwrpasol + blaenoriaethau rhifol o fewn pob ciw.

#### Llwybro Ciwiau fesul Diweddbwynt

| Diweddbwynt | Ciw | Blaenoriaeth Ddiofyn | Nodiadau |
|-------------|-----|----------------------|----------|
| `/keyboard/` | `high_priority` | 0 (brys) | Bob amser yn frys, dim paramedr blaenoriaeth |
| `/transcribe/` | `high_priority` | 0 (uchel) | Yn derbyn `high` neu `normal` |
| `/translate/` | `high_priority` | 0 (uchel) | Cyfieithu Cymraeg → Saesneg |
| `/transcribe_long_form/` | `default` | 5 (normal) | Anghydamserol, dim paramedr blaenoriaeth |
| `/translate_long_form/` | `default` | 5 (normal) | Cyfieithu anghydamserol, dim paramedr blaenoriaeth |
| `/align/` | `alignment` | 0 (brys) | Alinio testun â sain, stampiau amser fesul gair (CPU) |
| `/align_long_form/` | `alignment` | 5 (normal) | Alinio sain hir yn anghydamserol (CPU) |

#### Aseiniad Ciwiau Gweithwyr

Mae gweithwyr yn cael eu neilltuo i giwiau penodol trwy'r newidyn amgylchedd `WORKER_QUEUES`:

| Gweithiwr | Ciwiau | Dyfais | Yn Gwasanaethu |
|-----------|--------|--------|----------------|
| `worker-high` | `high_priority` | GPU | `/transcribe/`, `/keyboard/`, `/translate/` |
| `worker-default` | `default` | GPU | `/transcribe_long_form/`, `/translate_long_form/` |
| `worker-alignment` (x2) | `alignment` | CPU | `/align/`, `/align_long_form/` |

#### Blaenoriaethau Rhifol (o fewn pob ciw)

| Gwerth | Enw | Defnyddir Gan |
|--------|-----|---------------|
| 0 | brys | `/keyboard/`, `/transcribe/` gyda `priority=high`, `/translate/`, `/align/` |
| 5 | normal | `/transcribe/` gyda `priority=normal`, `/transcribe_long_form/`, `/translate_long_form/`, `/align_long_form/` |

---

## Fformat Allbwn

### Ymateb JSON
```json
{
  "id": "id_sain",
  "version": 2,
  "success": true,
  "language": "cy",
  "segments": [
    {
      "audio_id": "hash_md5",
      "start": 0.0,
      "end": 2.5,
      "text": "Mae hyn yn brawf o drawsgrifio",
      "normalized": "Mae hyn yn brawf o drawsgrifio",
      "score": 0.95,
      "words": [
        {"word": "Mae", "start": 0.0, "end": 0.3, "score": 0.98},
        {"word": "hyn", "start": 0.3, "end": 0.5, "score": 0.96}
      ],
      "chars": [...]
    }
  ]
}
```

### Nodweddion

- **Normaleiddio testun**: Mae pob segment yn cynnwys `text` gwreiddiol a `normalized` (Cymraeg safonol)
- **Stampiau amser ar lefel geiriau**: Amseru manwl gywir ar gyfer pob gair
- **Sgoriau hyder**: Sgoriau cywirdeb fesul gair a fesul segment
- **Diarization siaradwyr**: Labeli siaradwyr (SIARADWR_01, SIARADWR_02, ayyb.)
- **Canfod iaith**: Adnabod Cymraeg/Saesneg yn awtomatig

---

## Ffurfweddiad yr Amgylchedd

Mae'r prosiect hwn yn defnyddio dull hybrid ar gyfer newidynnau amgylchedd:

### Strwythur Ffeiliau
- **`config.env`** - Ffurfweddiad tryloyw (wedi'i gomitio i git)
  - Enwau modelau, gosodiadau Redis, rhagosodiadau an-sensitif
  - Golygwch y ffeil hon i newid ffurfweddiadau modelau

- **`.env.secrets`** - Gwerthoedd sensitif (wedi'i gitignore)
  - Tocynnau HuggingFace, cyfrineiriau
  - Crëwch o `.env.secrets.example`

- **`.env`** - Ffeil wedi'i chynhyrchu (wedi'i gitignore)
  - Wedi'i chreu'n awtomatig gan `make setup`
  - Yn cyfuno `config.env` + `.env.secrets`

### Prif Opsiynau Ffurfweddu

```bash
# Ffurfweddiad Model (config.env)
WHISPER_MODEL_NAME=DewiBrynJones/whisper-large-v2-ft-btb-cv-cvad-ca-wlga-cy-ct2-2511
WHISPER_MODEL_LANGUAGE=cy
WAV2VEC2_MODEL=techiaith/wav2vec2-btb-cv-ft-cv-cy

# Glanhau Ffeiliau (config.env)
CLEANUP_ENABLED=true
FILE_RETENTION_DAYS=14
CLEANUP_SCHEDULE=0 2 * * *  # 2 AM yn ddyddiol

# Cyfrinachau (.env.secrets)
HF_AUTH_TOKEN=eich_tocyn_huggingface_yma
```

### Newid Ffurfweddiad

**I newid gosodiadau model:**
```bash
# Golygu'r ffeil ffurfweddiad tryloyw
nano config.env

# Ail-gynhyrchu .env
make setup
```

**I ddiweddaru'ch tocyn HuggingFace:**
```bash
# Golygu ffeil gyfrinachau
nano .env.secrets

# Ail-gynhyrchu .env
make setup
```

---

## Dogfennaeth

### Dogfennaeth Graidd
- **[CPU_GPU_DEPLOYMENT.md](docs/CPU_GPU_DEPLOYMENT.md)** - Canllaw llawn ar gyfer defnyddio CPU vs GPU
- **[CELERY_ARCHITECTURE.md](docs/CELERY_ARCHITECTURE.md)** - Deall y system ciw tasgau
- **[DOCKER_HEALTHCHECKS.md](docs/DOCKER_HEALTHCHECKS.md)** - Monitro iechyd cynwysyddion

### Dogfennaeth Nodweddion
- **[FILE_CLEANUP.md](docs/FILE_CLEANUP.md)** - Glanhau ffeiliau trawsgrifio hen yn awtomatig
- **[TASK_PRIORITIZATION.md](docs/TASK_PRIORITIZATION.md)** - Llwybro ciwiau a system flaenoriaethu
- **[IMPROVING_ALIGNMENT.md](docs/IMPROVING_ALIGNMENT.md)** - Gwella cywirdeb stampiau amser ar lefel geiriau

### Graddio a Defnyddio
- **[GPU_SCALING.md](docs/GPU_SCALING.md)** - Terfynau cof GPU a ffurfweddiadau aml-GPU
- **[ADVANCED_SCALING.md](docs/ADVANCED_SCALING.md)** - Strategaethau graddio uwch
- **[INFERENCE_DEPLOYMENT_ALTERNATIVES.md](docs/INFERENCE_DEPLOYMENT_ALTERNATIVES.md)** - Cymhariaeth o atebion defnyddio casgliad

### Defnyddio Brodorol macOS
- **[macos/README.md](macos/README.md)** - Defnyddio Apple Silicon brodorol gyda chyflymu MLX
- **[macos/HYBRID_MLX_ARCHITECTURE.md](macos/HYBRID_MLX_ARCHITECTURE.md)** - Dogfennaeth pensaernïaeth hybrid MLX

### Dogfennaeth Dechnegol
- **[claude_refactors_2601.md](docs/claude_refactors_2601.md)** - Gwelliannau pensaernïol diweddar

---

## Graddio

### Graddio Gweithwyr yn Annibynnol

Graddiwch weithwyr blaenoriaeth uchel a rhagosodedig yn annibynnol yn seiliedig ar eich llwyth gwaith:

```bash
# Gweithwyr GPU
make scale-high-gpu N=2       # 2 weithiwr blaenoriaeth uchel (keyboard + transcribe)
make scale-default-gpu N=3    # 3 gweithiwr rhagosodedig (transcribe_long_form)

# Gweithwyr CPU
make scale-high-cpu N=2
make scale-default-cpu N=2
```

### Enghreifftiau Graddio

**Canolbwyntio ar amser real** (llawer o ddefnydd keyboard/transcribe):
```bash
make scale-high-gpu N=3       # Mwy o gapasiti blaenoriaeth uchel
make scale-default-gpu N=1    # Isafswm ffurf hir
```

**Canolbwyntio ar brosesu swp** (llawer o drawsgrifio ffurf hir):
```bash
make scale-high-gpu N=1       # Isafswm amser real
make scale-default-gpu N=3    # Mwy o gapasiti swp
```

**Cytbwys** (llwyth gwaith cymysg):
```bash
make scale-high-gpu N=2
make scale-default-gpu N=2
```

### Terfynau Cof GPU

Mae pob gweithiwr angen ~6GB VRAM. Ar gyfer un RTX 3090 (24GB):

| Ffurfweddiad | Gweithwyr Uchel | Gweithwyr Rhagosodedig | Cyfanswm VRAM |
|--------------|----------------|------------------------|----------------|
| Isafswm | 1 | 1 | ~12GB |
| Cytbwys | 2 | 2 | ~24GB (uchafswm) |
| Amser real | 3 | 1 | ~24GB (uchafswm) |

Gweler [docs/GPU_SCALING.md](docs/GPU_SCALING.md) ar gyfer ffurfweddiadau aml-GPU.

### Aseiniad Ciwiau Gweithwyr

Mae gweithwyr yn cael eu haseinio i giwiau trwy'r newidyn amgylchedd `WORKER_QUEUES` yn docker-compose:

```yaml
# docker-compose.gpu.yml
services:
  worker-high:
    environment:
      - WORKER_QUEUES=high_priority    # Tasgau blaenoriaeth uchel yn unig

  worker-default:
    environment:
      - WORKER_QUEUES=default          # Tasgau rhagosodedig yn unig

  worker-alignment:
    environment:
      - WORKER_QUEUES=alignment        # Tasgau alinio yn unig (CPU)
```

I greu gweithiwr sy'n trin y ddau giw (defnyddiol ar gyfer defnyddiadau bach):
```bash
WORKER_QUEUES=high_priority,default   # Yn gwirio high_priority yn gyntaf
```

---

## Monitro

### Gwiriadau Iechyd

```bash
# Iechyd cyffredinol y system
curl http://localhost:5511/health/

# Parodrwydd gweithwyr
curl http://localhost:5511/health/ready/

# Gwiriad bywiogrwydd
curl http://localhost:5511/health/live/
```

### Statws Ciwiau

```bash
# Gwirio hyd ciwiau a thasgau gweithredol
curl http://localhost:5511/queue/status/
```

### Logiau

```bash
# Gweld yr holl logiau
make logs

# Dilyn logiau gweithiwr blaenoriaeth uchel
docker compose -f docker-compose.gpu.yml logs -f worker-high

# Dilyn logiau gweithiwr rhagosodedig
docker compose -f docker-compose.gpu.yml logs -f worker-default

# Logiau fesul tasg (wedi'u storio yn recordings/<stt_id>.log)
curl http://localhost:5511/get_status/?stt_id=<uuid>
```

---

## Gosod

### Defnyddio Makefile (GPU yn ddiofyn)
```bash
git clone https://storfa.techiaith.cymru/lleferydd/stt-cy/whisperx-server
cd whisperx-server
make setup
make
```

### Defnyddio Docker Compose yn Uniongyrchol
```bash
# Fersiwn GPU
docker-compose -f docker-compose.gpu.yml up -d --build

# Fersiwn CPU
docker-compose -f docker-compose.cpu.yml up -d --build
```

Yna, ewch wedyn i http://localhost:5511

---

## Datrys Problemau

### Modelau ddim yn llwytho
- Gwiriwch y tocyn HuggingFace yn `.env.secrets`
- Cadarnhewch gysylltedd rhwydwaith i HuggingFace
- Adolygwch logiau gweithwyr: `make logs`

### Gwallau allan o gof
- Gostwng cydamseredd gweithwyr i 1
- Galluogi ailgylchu `max-tasks-per-child` gweithwyr (eisoes wedi'i ffurfweddu)
- Graddio i lawr nifer y gweithwyr
- Defnyddio model Whisper llai

### Trawsgrifio araf
- Defnyddio modd GPU yn lle CPU
- Gwirio a yw modelau wedi'u cadw (mae'r rhediad cyntaf yn llwytho modelau i lawr)
- Graddio gweithwyr i fyny: `make scale-high-gpu N=2` neu `make scale-default-gpu N=3`
- Defnyddio `/transcribe/` neu `/keyboard/` ar gyfer tasgau brys (ciw blaenoriaeth uchel)

### Tasgau'n sownd yn y ciw
- Gwirio statws gweithwyr: `make status`
- Archwilio'r ciw: `curl http://localhost:5511/queue/status/`
- Ailgychwyn gweithwyr: `docker compose -f docker-compose.gpu.yml restart worker-high worker-default worker-alignment`

---

## Datblygu

### Strwythur y Prosiect
```
whisperx-server/
├── api/                    # Cymhwysiad FastAPI
│   ├── main.py            # Diweddbwyntiau API
│   ├── health.py          # Rhesymeg gwirio iechyd
│   ├── queue_inspector.py # Monitro ciwiau
│   └── cleanup_scheduler.py # Glanhau ffeiliau
├── worker/                 # Gweithiwr Celery
│   ├── tasks.py           # Tasg trawsgrifio
│   ├── speech_to_text_tasks.py # Llwytho model
│   ├── normalization/     # Normaleiddio testun Cymraeg
│   └── start_workers.sh   # Sgript cychwyn gweithwyr
├── shared/                 # Cyfleusterau a rennir
│   └── stt_logger.py      # Cyfleusterau logio
├── docs/                   # Dogfennaeth
├── config.env             # Ffurfweddiad tryloyw
└── .env.secrets.example   # Templed cyfrinachau
```

---

## Trwydded

Trwydded MIT. Gweler [LICENSE](LICENSE) am fanylion.

---
---

<a id="english"></a>

> **[Fersiwn Cymraeg uchod / Welsh version above](#cymraeg)**

## Key Benefits

### 🎯 **Welsh Language Optimized**
- **Fine-tuned models**: Uses Welsh-specific Whisper and Wav2Vec2 models from Techiaith
- **Welsh normalization**: Automatic text normalization for Welsh verbatim speech
  - Expands contractions (ma'→mae, ca'l→cael)
  - Standardizes dialectal variations (petha→pethau, gwbod→gwybod)
  - Normalizes pronouns and verb forms
- **Language detection**: Automatic Welsh/English detection with Lingua
- **Accurate alignment**: Word-level timestamps optimized for Welsh phonetics

### ⚡ **High Performance & Scalability**
- **GPU acceleration**: Full NVIDIA CUDA support for fast transcription
- **Dedicated queue workers**: Separate high-priority and default workers, independently scalable
- **Task prioritization**: Two-level priority system (queue routing + numeric priorities)
- **Efficient batching**: WhisperX batched inference for 12x speedup
- **Memory management**: Automatic cleanup and worker recycling to prevent memory leaks

### 🔧 **Production Ready**
- **Containerized deployment**: Docker Compose for GPU and CPU environments
- **Health monitoring**: Comprehensive health checks for all services
- **Automatic cleanup**: Scheduled deletion of old files to prevent disk bloat
- **Task persistence**: Redis-backed queue survives restarts
- **Logging**: Per-task logging for debugging and monitoring
- **API documentation**: Auto-generated OpenAPI/Swagger docs

### 📊 **Rich Output Formats**
- **JSON**: Full transcription with word-level timestamps and scores
- **SRT/VTT**: Subtitle files with intelligent line splitting
- **ELAN**: Timeline annotations for linguistic analysis
- **Text**: Plain text transcription
- **Speaker diarization**: Identifies different speakers (SIARADWR_01, etc.)
- **Normalized text**: Welsh-specific text normalization included

### 🚀 **Developer Friendly**
- **RESTful API**: Simple HTTP endpoints for all operations
- **Queue inspection**: Monitor pending tasks and worker status
- **Flexible deployment**: CPU-only mode for development, GPU for production
- **Environment management**: Transparent config with secret separation
- **Comprehensive docs**: Architecture, deployment, and troubleshooting guides

### 🔒 **Enterprise Features**
- **Private model support**: Authenticate with HuggingFace for private models
- **Task tracking**: Persistent task IDs across server restarts
- **Result caching**: 7-day result expiration with Redis backend
- **CORS enabled**: Browser-friendly API access
- **Error handling**: Graceful degradation and detailed error messages

---

## Prerequisites

- **Docker** and **Docker Compose** (required)
- **Linux** or **macOS** — untested on Windows
- **GPU Mode**: NVIDIA GPU + nvidia-docker2
- **Memory**: Minimum 8GB RAM (16GB+ recommended for GPU mode)
- **Disk**: At least 20GB free space for models and recordings

---

## Quick Start

### Initial Setup
```bash
# Clone repository
git clone https://storfa.techiaith.cymru/lleferydd/stt-cy/whisperx-server
cd whisperx-server

# Set up environment files
make setup

# Edit .env.secrets and add your HuggingFace token
# Get your token from: https://huggingface.co/settings/tokens
nano .env.secrets

# Regenerate .env with your token
make setup
```

### GPU Deployment (Recommended for Production)
```bash
# Build and run with GPU support (requires nvidia-docker)
# Starts 1 high-priority worker + 1 default worker
make build-gpu

# Scale workers independently
make scale-high-gpu N=2       # 2 high-priority workers
make scale-default-gpu N=3    # 3 default workers
```

### CPU Deployment (For Development/Testing)
```bash
# Build and run with CPU-only support (no GPU required)
# Starts 1 high-priority worker + 1 default worker
make build-cpu

# Scale workers independently
make scale-high-cpu N=2       # 2 high-priority workers
make scale-default-cpu N=2    # 2 default workers
```

### Common Commands
```bash
make help          # Show all available commands
make ready         # Wait for models to finish loading
make status        # Show running containers
make health        # Check service health
make logs          # View container logs
make down          # Stop all containers
```

### Access the API
Once running, access the API at: http://localhost:5511

**Health Check:** http://localhost:5511/health/
**API Docs:** http://localhost:5511/docs (FastAPI auto-generated)

### Web App
A simple web app is available in the `app/` folder for submitting transcriptions and translations via the browser. To use it:

```bash
python3 -m http.server 8080 --directory app/
```

Then open http://localhost:8080 in your browser. The app connects to the API on `localhost:5511`.

---

## API Usage Examples

### Transcribe Audio (Short Form, Synchronous)
```bash
# Default: high priority (routed to high_priority queue)
curl -X POST "http://localhost:5511/transcribe/" \
  -F "soundfile=@audio.wav"

# Explicit normal priority (still routed to high_priority queue)
curl -X POST "http://localhost:5511/transcribe/" \
  -F "soundfile=@audio.wav" \
  -F "priority=normal"
```

### Transcribe Long Audio (Asynchronous)
```bash
# Submit task (routed to default queue)
curl -X POST "http://localhost:5511/transcribe_long_form/" \
  -F "soundfile=@long_audio.wav"

# Returns: {"id": "uuid", "version": 2, "success": true}

# Check status
curl "http://localhost:5511/get_status/?stt_id=<uuid>"

# Get results when complete
curl "http://localhost:5511/get_json/?stt_id=<uuid>"
curl "http://localhost:5511/get_srt/?stt_id=<uuid>"
curl "http://localhost:5511/get_vtt/?stt_id=<uuid>"
```

### Translate Audio (Welsh → English)
```bash
# Short form (synchronous, max 480KB)
curl -X POST "http://localhost:5511/translate/" \
  -F "soundfile=@audio.wav"

# Long form (asynchronous, any size)
curl -X POST "http://localhost:5511/translate_long_form/" \
  -F "soundfile=@long_audio.wav"
```

### Align Text to Audio (Word-level Timestamps)
```bash
# Short form (synchronous, max 480KB)
curl -X POST "http://localhost:5511/align/" \
  -F "soundfile=@audio.wav" \
  -F "text=Mae ganddynt dau o blant, mab a merch"

# Long form (asynchronous, any size — runs on CPU)
curl -X POST "http://localhost:5511/align_long_form/" \
  -F "soundfile=@long_audio.wav" \
  -F "text=Full text to align against the audio..."

# Check status
curl "http://localhost:5511/get_status/?stt_id=<uuid>"

# Get results
curl "http://localhost:5511/get_json/?stt_id=<uuid>"
```

### Real-time Keyboard Input (Always High Priority)
```bash
curl -X POST "http://localhost:5511/keyboard/" \
  -F "audio_file=@voice_input.wav"
# Always routed to high_priority queue with urgent priority
```

---

## Architecture

### Components

```
┌──────────────────┐
│    FastAPI App    │  Port 5511
│   (API Server)   │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│   Redis Broker   │  Port 6379
│   (Task Queue)   │
├──────────────────┤
│ high_priority    │  /transcribe/, /keyboard/, /translate/
│ default          │  /transcribe_long_form/, /translate_long_form/
│ alignment        │  /align/, /align_long_form/
└──┬───┬───┬───────┘
   │   │   │
   ▼   ▼   ▼
┌────────┐ ┌─────────┐ ┌───────────┐
│worker  │ │worker   │ │worker     │  Independently
│-high   │ │-default │ │-alignment │  Scalable
│(GPU)   │ │(GPU)    │ │(CPU x2)   │
└────────┘ └─────────┘ └───────────┘
```

### Services

- **Application (FastAPI)**: REST API server handling requests
- **worker-high (Celery)**: Dedicated to high-priority tasks (`/transcribe/`, `/keyboard/`, `/translate/`)
- **worker-default (Celery)**: Dedicated to default tasks (`/transcribe_long_form/`, `/translate_long_form/`)
- **worker-alignment (Celery)**: Dedicated CPU alignment worker (`/align/`, `/align_long_form/`) — 2 replicas so a long task doesn't block short requests
- **Redis**: Message broker and result backend

### Task Queue & Priority System

The system uses **two-level prioritization**: dedicated queue workers + numeric priorities within each queue.

#### Queue Routing by Endpoint

| Endpoint | Queue | Default Priority | Notes |
|----------|-------|------------------|-------|
| `/keyboard/` | `high_priority` | 0 (urgent) | Always urgent, no priority parameter |
| `/transcribe/` | `high_priority` | 0 (high) | Accepts `high` or `normal` |
| `/translate/` | `high_priority` | 0 (high) | Welsh → English translation |
| `/transcribe_long_form/` | `default` | 5 (normal) | Asynchronous, no priority parameter |
| `/translate_long_form/` | `default` | 5 (normal) | Async translation, no priority parameter |
| `/align/` | `alignment` | 0 (urgent) | Align text to audio, word-level timestamps (CPU) |
| `/align_long_form/` | `alignment` | 5 (normal) | Async long audio alignment (CPU) |

#### Worker Queue Assignment

Workers are dedicated to specific queues via the `WORKER_QUEUES` environment variable:

| Worker | Queues | Device | Serves |
|--------|--------|--------|--------|
| `worker-high` | `high_priority` | GPU | `/transcribe/`, `/keyboard/`, `/translate/` |
| `worker-default` | `default` | GPU | `/transcribe_long_form/`, `/translate_long_form/` |
| `worker-alignment` (x2) | `alignment` | CPU | `/align/`, `/align_long_form/` |

#### Numeric Priorities (within each queue)

| Value | Name | Used By |
|-------|------|---------|
| 0 | urgent | `/keyboard/`, `/transcribe/` with `priority=high`, `/translate/`, `/align/` |
| 5 | normal | `/transcribe/` with `priority=normal`, `/transcribe_long_form/`, `/translate_long_form/`, `/align_long_form/` |

---

## Output Format

### JSON Response
```json
{
  "id": "audio_id",
  "version": 2,
  "success": true,
  "language": "cy",
  "segments": [
    {
      "audio_id": "md5_hash",
      "start": 0.0,
      "end": 2.5,
      "text": "Mae hyn yn brawf o drawsgrifio",
      "normalized": "Mae hyn yn brawf o drawsgrifio",
      "score": 0.95,
      "words": [
        {"word": "Mae", "start": 0.0, "end": 0.3, "score": 0.98},
        {"word": "hyn", "start": 0.3, "end": 0.5, "score": 0.96}
      ],
      "chars": [...]
    }
  ]
}
```

### Features

- **Text normalization**: Each segment includes both original `text` and `normalized` (standardized Welsh)
- **Word-level timestamps**: Precise timing for each word
- **Confidence scores**: Per-word and per-segment accuracy scores
- **Speaker diarization**: Speaker labels (SIARADWR_01, SIARADWR_02, etc.)
- **Language detection**: Automatic Welsh/English identification

---

## Environment Configuration

This project uses a hybrid approach for environment variables:

### File Structure
- **`config.env`** - Transparent configuration (committed to git)
  - Model names, Redis settings, non-sensitive defaults
  - Edit this file to change model configurations

- **`.env.secrets`** - Sensitive values (gitignored)
  - HuggingFace tokens, passwords
  - Create from `.env.secrets.example`

- **`.env`** - Generated file (gitignored)
  - Automatically created by `make setup`
  - Merges `config.env` + `.env.secrets`

### Key Configuration Options

```bash
# Model Configuration (config.env)
WHISPER_MODEL_NAME=DewiBrynJones/whisper-large-v2-ft-btb-cv-cvad-ca-wlga-cy-ct2-2511
WHISPER_MODEL_LANGUAGE=cy
WAV2VEC2_MODEL=techiaith/wav2vec2-btb-cv-ft-cv-cy

# File Cleanup (config.env)
CLEANUP_ENABLED=true
FILE_RETENTION_DAYS=14
CLEANUP_SCHEDULE=0 2 * * *  # 2 AM daily

# Secrets (.env.secrets)
HF_AUTH_TOKEN=your_huggingface_token_here
```

### Modifying Configuration

**To change model settings:**
```bash
# Edit the transparent config file
nano config.env

# Regenerate .env
make setup
```

**To update your HuggingFace token:**
```bash
# Edit secrets file
nano .env.secrets

# Regenerate .env
make setup
```

---

## Documentation

### Core Documentation
- **[CPU_GPU_DEPLOYMENT.md](docs/CPU_GPU_DEPLOYMENT.md)** - Complete guide for CPU vs GPU deployment
- **[CELERY_ARCHITECTURE.md](docs/CELERY_ARCHITECTURE.md)** - Understanding the task queue system
- **[DOCKER_HEALTHCHECKS.md](docs/DOCKER_HEALTHCHECKS.md)** - Container health monitoring

### Feature Documentation
- **[FILE_CLEANUP.md](docs/FILE_CLEANUP.md)** - Automatic cleanup of old transcription files
- **[TASK_PRIORITIZATION.md](docs/TASK_PRIORITIZATION.md)** - Queue routing and priority system
- **[IMPROVING_ALIGNMENT.md](docs/IMPROVING_ALIGNMENT.md)** - Enhancing word-level timestamp accuracy

### Scaling & Deployment
- **[GPU_SCALING.md](docs/GPU_SCALING.md)** - GPU memory limits and multi-GPU configurations
- **[ADVANCED_SCALING.md](docs/ADVANCED_SCALING.md)** - Advanced scaling strategies
- **[INFERENCE_DEPLOYMENT_ALTERNATIVES.md](docs/INFERENCE_DEPLOYMENT_ALTERNATIVES.md)** - Comparison of inference deployment solutions

### macOS Native Deployment
- **[macos/README.md](macos/README.md)** - Native Apple Silicon deployment with MLX acceleration
- **[macos/HYBRID_MLX_ARCHITECTURE.md](macos/HYBRID_MLX_ARCHITECTURE.md)** - MLX hybrid architecture documentation

### Technical Documentation
- **[claude_refactors_2601.md](docs/claude_refactors_2601.md)** - Recent architectural improvements

---

## Scaling

### Independent Worker Scaling

Scale high-priority and default workers independently based on your workload:

```bash
# GPU workers
make scale-high-gpu N=2       # 2 high-priority workers (keyboard + transcribe)
make scale-default-gpu N=3    # 3 default workers (transcribe_long_form)

# CPU workers
make scale-high-cpu N=2
make scale-default-cpu N=2
```

### Scaling Examples

**Real-time focused** (lots of keyboard/transcribe usage):
```bash
make scale-high-gpu N=3       # More high-priority capacity
make scale-default-gpu N=1    # Minimal long-form
```

**Batch processing focused** (lots of long-form transcription):
```bash
make scale-high-gpu N=1       # Minimal real-time
make scale-default-gpu N=3    # More batch capacity
```

**Balanced** (mixed workload):
```bash
make scale-high-gpu N=2
make scale-default-gpu N=2
```

### GPU Memory Limits

Each worker needs ~6GB VRAM. For a single RTX 3090 (24GB):

| Configuration | High Workers | Default Workers | Total VRAM |
|---------------|-------------|-----------------|------------|
| Minimal | 1 | 1 | ~12GB |
| Balanced | 2 | 2 | ~24GB (max) |
| Real-time focused | 3 | 1 | ~24GB (max) |

See [docs/GPU_SCALING.md](docs/GPU_SCALING.md) for multi-GPU configurations.

### Worker Queue Assignment

Workers are assigned to queues via the `WORKER_QUEUES` environment variable in docker-compose:

```yaml
# docker-compose.gpu.yml
services:
  worker-high:
    environment:
      - WORKER_QUEUES=high_priority    # Only high-priority tasks

  worker-default:
    environment:
      - WORKER_QUEUES=default          # Only default tasks

  worker-alignment:
    environment:
      - WORKER_QUEUES=alignment        # Alignment tasks only (CPU)
```

To create a worker that handles both queues (useful for small deployments):
```bash
WORKER_QUEUES=high_priority,default   # Checks high_priority first
```

---

## Monitoring

### Health Checks

```bash
# Overall system health
curl http://localhost:5511/health/

# Worker readiness
curl http://localhost:5511/health/ready/

# Liveness check
curl http://localhost:5511/health/live/
```

### Queue Status

```bash
# Check queue lengths and active tasks
curl http://localhost:5511/queue/status/
```

### Logs

```bash
# View all logs
make logs

# Follow high-priority worker logs
docker compose -f docker-compose.gpu.yml logs -f worker-high

# Follow default worker logs
docker compose -f docker-compose.gpu.yml logs -f worker-default

# Per-task logs (stored in recordings/<stt_id>.log)
curl http://localhost:5511/get_status/?stt_id=<uuid>
```

---

## Installation

### Using Makefile (GPU by default)
```bash
git clone https://storfa.techiaith.cymru/lleferydd/stt-cy/whisperx-server
cd whisperx-server
make setup
make
```

### Using Docker Compose Directly
```bash
# GPU version
docker-compose -f docker-compose.gpu.yml up -d --build

# CPU version
docker-compose -f docker-compose.cpu.yml up -d --build
```

Then navigate to http://localhost:5511

---

## Troubleshooting

### Models not loading
- Check HuggingFace token in `.env.secrets`
- Verify network connectivity to HuggingFace
- Review worker logs: `make logs`

### Out of memory errors
- Reduce worker concurrency to 1
- Enable `max-tasks-per-child` worker recycling (already configured)
- Scale down number of workers
- Use smaller Whisper model

### Slow transcription
- Use GPU mode instead of CPU
- Check if models are cached (first run downloads models)
- Scale up workers: `make scale-high-gpu N=2` or `make scale-default-gpu N=3`
- Use `/transcribe/` or `/keyboard/` for urgent tasks (high-priority queue)

### Tasks stuck in queue
- Check worker status: `make status`
- Inspect queue: `curl http://localhost:5511/queue/status/`
- Restart workers: `docker compose -f docker-compose.gpu.yml restart worker-high worker-default worker-alignment`

---

## Development

### Project Structure
```
whisperx-server/
├── api/                    # FastAPI application
│   ├── main.py            # API endpoints
│   ├── health.py          # Health check logic
│   ├── queue_inspector.py # Queue monitoring
│   └── cleanup_scheduler.py # File cleanup
├── worker/                 # Celery worker
│   ├── tasks.py           # Transcription task
│   ├── speech_to_text_tasks.py # Model loading
│   ├── normalization/     # Welsh text normalization
│   └── start_workers.sh   # Worker startup script
├── shared/                 # Shared utilities
│   └── stt_logger.py      # Logging utilities
├── docs/                   # Documentation
├── config.env             # Transparent configuration
└── .env.secrets.example   # Secret template
```

---

## License

MIT License. See [LICENSE](LICENSE) for details.

---
