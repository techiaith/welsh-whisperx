#!/usr/bin/env python3
"""
Welsh Language Data - Shared normalization patterns

This module contains all the linguistic data used by Welsh normalizers.
All normalization rules and lookup tables are centralized here to ensure
consistency across different normalizer implementations.
"""

# ============================================================================
# PRONOUN NORMALIZATIONS
# ============================================================================
PRONOUN_CORRECTIONS = {
    "nw": "nhw",
    "n'w": "nhw",
    "nw'n": "nhw'n",
    "nw'm": "nhw'm",
    "nw'r": "nhw'r",
    "nhwn": "nhw'n",
    "'u": "eu",
    "'ych": "eich",
    "'yng": "ein",
    "'ym": "ein",
    "wnna": "hwnna",        
    "wnna'n": "hwnna'n",
}

# ============================================================================
# VERB CONTRACTIONS
# ============================================================================
VERB_CONTRACTIONS = {
    "ca'l": "cael",
    "ca'": "cael",
    "ga'l": "gael",
    "ga'": "gaf",
    "cha'l": "chael",
    "bo'": "bod",
    "fo'": "fod",
    "ne'": "neu",
    "gor'o'": "gorfod",
    "gor'o": "gorfod",
    "gorfo": "gorfod",
    "goffod": "gorfod",
    "'neud": "gwneud",
    "neud": "gwneud",
    "gneu": "gwneud",
    "nath": "gwnaeth",
    "natha": "gwnaeth",
    "nathon": "wnaethon",
    "nathoch": "wnaethoch",
    "nethon": "wnaethon",
    "netho": "wnaethon",
    "neith": "gwnaiff",
    "neshi": "nes i",
    "nesh": "nes",
    "newch": "gwnewch",
    "newn": "wnawn",
    "by'": "bydd",
    "fy'": "fydd",
    "gewn": "gawn",
    "gesh": "ges",
}

# ============================================================================
# MAE CONTRACTIONS
# ============================================================================
MAE_CONTRACTIONS = {
    "ma'": "mae",
    "ma'r": "mae'r",
    "ma'n": "mae'n",
}

# ============================================================================
# OTHER CONTRACTIONS
# ============================================================================
OTHER_CONTRACTIONS = {
    "'di": "ydy",
    "'na": "yna",
    "'ne": "yna",
    "'ma": "yma",
    "fama": "fan yma",
    "fyma": "fan yma",
    "fana": "fan yna",
    "fyna": "fan 'na",
    "fan'cw": "fan acw",
    "'lly": "felly",
    "'elly": "felly",
    "lly": "felly",
    "'llu": "felly",
    "'fo": "efo",
    "'da": "gyda",
    "'wan": "rŵan",
    "rwan": "rŵan",
    "ŵan": "rŵan",
    "'w'rach": "hwyrach",
    "'chos": "achos",
    "'c'os": "achos",
    "chos": "achos",
    "'im": "dim",
    "im": "dim",
    "dwi'm": "dwi ddim",
    "dwim": "dwi ddim",
    "'nol": "yn ôl",
    "'fyd": "hefyd",
    "'to": "eto",
    "'nabod": "adnabod",
    "ty'd": "tyrd",
    "'stafell": "ystafell",
    "'sgubor": "ysgubor",
    "'mlan": "ymlaen",
    "'mlaen": "ymlaen",
    "'drycha": "edrycha",
    "'drychwch": "edrychwch",
    "'wharae": "chwarae",
    "'run": "yr un",
    "run": "yr un",
    "'biti": "piti",
    "'wna": "hwnna",
    "'ddo": "iddo",
    "'tai": "petai",
    "'swn": "buaswn",
    "'sa": "buasai",
    "'chydig": "ychydig",
    "'lla": "efallai",
    "'yn": "fy",
    "'i'n": "hi'n",
    "o'no": "ohono",
    "'ta'": "yntau",
    "'am": "yna ddim",
    "'ndoes": "onid oes",
    "'ddan": "oedden",
    "'thrawon": "athrawon",
    "'sych": "bysych",
    "fel 'a": "fel yna",
}

# ============================================================================
# VOWEL REDUCTIONS - PLURALS
# ============================================================================
PLURAL_REDUCTIONS = {
    # North forms (-a)
    "petha": "pethau",
    "betha": "bethau",
    "weithia": "weithiau",
    "weithia'": "weithiau",
    "withia": "weithiau",
    "withia'": "weithiau",
    "gora": "gorau",
    "gora'": "gorau",
    "cynta": "cyntaf",
    "cynta'": "cyntaf",
    "gynta'": "gyntaf",
    "cynhara": "cynharaf",
    "nesa": "nesaf",
    "nesa'": "nesaf",
    "ola": "olaf",
    "ola'": "olaf",
    "pwysa": "pwysau",
    "bwysa'": "bwysau",
    "lleisia": "lleisiau",
    "lleisia'": "lleisiau",
    "lleisa": "lleisiau",
    "cymeriade": "cymeriadau",
    "profiada": "profiadau",
    "profiade": "profiadau",
    "brofiade": "brofiadau",
    "brofiada": "brofiadau",
    "sgilia": "sgiliau",
    "sgilia'": "sgiliau",
    "hawlia'": "hawliau",
    "hawlie": "hawliau",
    "ffinia'": "ffiniau",
    "llunia'": "lluniau",
    "norma'": "normau",
    "cama'": "camau",
    "cyfrynga'": "cyfryngau",
    "cyfrynge": "cyfryngau",
    "emosiyna": "emosiynau",
    "hemosiyna": "hemosiynau",
    "dyddia'": "dyddiau",
    "dyddia": "dyddiau",
    "sesiyna": "sesiynau",
    "problema": "problemau",
    "gema": "gemau",
    "gema'": "gemau",
    "gweithgaredda": "gweithgareddau",
    "anawstera": "anawsterau",
    "grwpia'": "grwpiau",
    "heria'": "heriau",
    "radda": "raddau",
    "radde": "raddau",
    "gwasanaetha'": "gwasanaethau",
    "gwasanaethe": "gwasanaethau",
    "wasanaetha'": "wasanaethau",
    "bywyda": "bywydau",
    "asiantaetha": "asiantaethau",
    "asiantaethe": "asiantaethau",
    "sgyrsia'": "sgyrsiau",
    "syniada": "syniadau",
    "syniade": "syniadau",
    "cymwystere": "cymwysterau",
    "teuluodd": "teuluoedd",
    "deuluodd": "deuluoedd",
    "newidiada": "newidiadau",
    "ffrindia": "ffrindiau",
    "elfenna'": "elfennau",
    "elfenna": "elfennau",
    "elfenne": "elfennau",
    "dyheada": "dyheadau",
    "pyncia'": "pynciau",
    "penderfyniada": "penderfyniadau",
    "mudiada": "mudiadau",
    "gyfnoda": "gyfnodau",
    "sylwada'": "sylwadau",
    "patryma": "patrymau",
    "ddatblygiada": "ddatblygiadau",
    "cyrsia": "cyrsiau",
    "terme": "termau",
    "terma": "termau",
    "clwbia": "clybiau",
    "systema": "systemau",
    "diwyllianna": "diwylliannau",
    "geiria'": "geiriau",
    "apia": "apiau",
    "agwedda'": "agweddau",
    "sefydliada": "sefydliadau",
    "cymuneda": "cymunedau",
    "gwefanna": "gwefannau",
    "anwyldera": "anhwylderau",
    "tegana": "teganau",
    "brojecta": "brojectau",
    "anabledda": "anableddau",
    "anabledde": "anableddau",
    "cyfrifoldeba": "cyfrifoldebau",
    "perthnasa'": "perthnasau",
    "trafodaethe": "trafodaethau",
    "adolygiada": "adolygiadau",
    "awdurdoda'": "awdurdodau",
    "astudiaethe": "astudiaethau",
    "polisia": "polisïau",
    "darpariaetha": "darpariaethau",
    "effeithia'": "effeithiau",
    "effeithie": "effeithiau",
    "canlyniade": "canlyniadau",
    "cyffuria": "cyffuriau",
    "risge": "risgiau",
    "delwedda'": "delweddau",
    "delwedde": "delweddau",
    "amgylchiada": "amgylchiadau",
    "ffactora'": "ffactorau",
    "orie": "oriau",
    "oria": "oriau",
    "cwestiyna'": "cwestiynau",
    "adroddiada": "adroddiadau",
    "trefniada": "trefniadau",
    "bwyntia'": "bwyntiau",
    "saithdega": "saithdegau",
    "chwedega": "chwedegau",
    "harddega": "harddegau",
    "blynyddodd": "blynyddoedd",
    "disgwyliada": "disgwyliadau",
    "potie": "potiau",

    # South forms (-e)
    "pethe": "pethau",
    "bethe": "bethau",
    "weithie": "weithiau",
    "gore": "gorau",
    "coese": "coesau",
    "enwe": "enwau",
    "pwyse": "pwysau",
    "geirie": "geiriau",
    "ffrindie": "ffrindiau",
}

# ============================================================================
# VOWEL REDUCTIONS - VERBS
# ============================================================================
VERB_REDUCTIONS = {
    "dechre": "dechrau",
    "dechra": "dechrau",
    "dechra'": "dechrau",
    "ddechre": "ddechrau",
    "gweitho": "gweithio",
    "gwithio": "gweithio",
    "disgwl": "disgwyl",
    "gobitho": "gobeithio",
    "grando": "gwrando",
    "gwryndo": "gwrando",
    "gadal": "gadael",
    "gada'l": "gadael",
    "gade'l": "gadael",
    "adal": "adael",
    "cyrradd": "cyrraedd",
    "gyrradd": "gyrraedd",
    "diodde": "dioddef",
    "cwmpo": "cwympo",
    "lico": "licio",
    "timlo": "teimlo",
    "chwara": "chwarae",
    "chware": "chwarae",
    "clwad": "clywed",
    "clywad": "clywed",
    "glywad": "glywed",
    "glwad": "glywed",
    "deu": "dweud",
    "deud": "dweud",
    "deu'": "dweud",
    "ddeu": "ddweud",
    "weud": "ddweud",
    "deutha": "dweud wrth",
    "daetho": "dweud wrth",
    "ymatab": "ymateb",
    "myn'": "mynd",
    "arfar": "arfer",
    "ymarfar": "ymarfer",
    "bita": "bwyta",
    "dadla": "dadlau",
    "ffindio": "ffeindio",
    "ffeithio": "effeithio",
    "cerddad": "cerdded",
    "iste": "eistedd",
    "cyfadda": "cyfaddef",
    "gorffan": "gorffen",
    "darllan": "darllen",
    "edrach": "edrych",
    "gwynebu": "gwynebu",
    "styried": "ystyried",
    "ystyriad": "ystyried",
    "atab": "ateb",
    "wela'": "gwelaf",
    "gwel'": "gweld",
    "ath": "aeth",
    "dath": "daeth",
    "ddath": "ddaeth",
    "ddoth": "ddaeth",
}

# ============================================================================
# VOWEL REDUCTIONS - INTERNAL
# ============================================================================
INTERNAL_REDUCTIONS = {
    "gwbod": "gwybod",
    "gwbo": "gwybod",
    "wbod": "wybod",
    "w'bod": "wybod",
    "me'wl": "meddwl",
    "mewl": "meddwl",
    "me'l": "meddwl",
    "m'wl": "meddwl",
    "m'wn": "mewn",
    "mew'": "mewn",
    "meddw'": "meddwl",
    "meddwlgarwch": "meddylgarwch",
    "sicir": "sicr",
    "amsar": "amser",
    "mowr": "mawr",
    "amal": "aml",
    "wthnos": "wythnos",
    "wsos": "wythnos",
    "cymyd": "cymryd",
    "cymud": "cymryd",
    "ymlan": "ymlaen",
    "hunen": "hunain",
    "angan": "angen",
    "hangan": "hangen",
    "angenion": "anghenion",
    "hannar": "hanner",
    "hwna": "hwnna",
    "ynny": "hynny",
    "hynna'": "hynnaf",
    "'ynny": "hynny",
    "'ny": "hynny",
    "yne": "hynny",
    "chydig": "ychydig",
    "chdig": "ychydig",
    "rei": "rhai",
    "rhei": "rhai",
    "eryll": "eraill",
    "hunianiaeth": "hunaniaeth",
    "hunanieth": "hunaniaeth",
    "ymwybyddieth": "ymwybyddiaeth",
    "trw": "trwy",
    "trw'r": "trwy'r",
    "drw": "drwy",
    "drost": "dros",
    "wth": "wrth",
    "eitha": "eithaf",
    "eitha'": "eithaf",
    "itha": "eithaf",
    "mwya": "mwyaf",
    "mwya'": "mwyaf",
    "fwya'": "fwyaf",
    "fwya": "fwyaf",
    "isa": "isaf",
    "llawar": "llawer",
    "elle": "efalle",
    "ella": "efallai",
    "gwanol": "gwahanol",
    "gwahaniath": "gwahaniaeth",
    "gwahanieth": "gwahaniaeth",
    "wahanieth": "wahaniaeth",
    "dalld": "deall",
    "diall": "deall",
    "deallt": "deall",
    "hydnod": "hyd yn oed",
    "hanas": "hanes",
    "cyfla": "cyfle",
    "enghraiff": "enghraifft",
    "enhraifft": "enghraifft",
    "pentre": "pentref",
    "cartra": "cartref",
    "cartre": "cartref",
    "traffath": "trafferth",
    "negas": "neges",
    "blesar": "bleser",
    "plesar": "pleser",
    "gynhenydd": "gynhenid",
    "ersdalwm": "ers dalwm",
    "problam": "problem",
    "broblam": "broblem",
    "cwbwl": "cwbl",
    "gwbwl": "gwbl",
    "dat": "dad",
    "amrywieth": "amrywiaeth",
    "ystol": "ystod",
    "pŵar": "pŵer",
    "cyffwr": "cyffwrdd",
    "camtrin": "cam-trin",
    "cwricilwm": "cwricwlwm",
    "darpariath": "darpariaeth",
    "cymddeithasol": "cymdeithasol",
    "trosglwyddiadwy": "trosglwyddadwy",
    "sicrau": "sicrhau",
    "cydnabot": "cydnabod",
    "ugian": "ugain",
    "ugen": "ugain",
    "bymthag": "bymtheg",
    "ddeugen": "ddeugain",
    "gweud": "dweud",
    "sy": "sydd",
    "Portsmuth": "Portsmouth",
    "mown": "mewn",
}

# ============================================================================
# SPELLING STANDARDIZATIONS
# ============================================================================
SPELLING_CORRECTIONS = {
    "rwbeth": "rhywbeth",
    "rwbath": "rhywbeth",
    "wbath": "rhywbeth",
    "rhwbath": "rhywbeth",
    "rywbath": "rhywbeth",
    "rhwbeth": "rhywbeth",
    "rwle": "rywle",
    "gellu": "gallu",
    "efyd": "hefyd",
    "cymra'g": "cymraeg",
    "gymra'g": "gymraeg",
    "lloeger": "lloegr",
    "ytrach": "hytrach",
    "sicirhau": "sicrhau",
    "jys": "jyst",
    "sud": "sut",
    "be'": "beth",
    "rhyfadd": "rhyfedd",
    "cymru": "Cymru",
    "gymru": "Gymru",
    "cymraeg": "Cymraeg",
    "gymraeg": "Gymraeg",
    "ewrop": "Ewrop",
    "sgandenafia": "Sgandinafia",
    "bobol": "bobl",
    "pobol": "pobl",
    "isie": "eisiau",
    "isia": "eisiau",
    "isio": "eisiau",
    "isio'i": "eisiau ei",
    "isio'u": "eisiau eu",
    "eisia": "eisiau",
    "roid": "roi",
    "rhoid": "rhoi",
    "powb": "pawb",
    "rywyn": "rywun",
    "rwun": "rywun",
    "unryw": "unrhyw",
    "ffor": "ffordd",
    "fatha": "fath â",
    "fatha'": "fath â",
    "ginnon": "gennym",
    "ganddon": "gennym",
    "ginon": "gynnon",
    "gennyn": "gennym",
    "genddyn": "ganddyn",
    "gannyn": "ganddyn",
    "gathon": "cawson",
    "gafal": "gafael",
    "dwytha": "diwetha",
    "dwetha": "diwetha",
    "'nde": "ynde",
    "nacdi": "nac ydi",
    "on'": "ond",
    "ont": "ond",
    "on'd": "onid",
    "ne'n": "neu'n",
    "neu'": "neud",
    "ynnyn": "ynddyn",
    "wt": "wyt",
    "ydan": "ydym",
    "ydach": "ydych",
    "odd": "oedd",
    "o'dd": "oedd",
    "o'd'd": "oedd",
    "do'dd": "doedd",
    "do'": "doedd",
    "oddan": "oedden",
    "oddwn": "oeddwn",
    "odden": "oedden",
    "oddyn": "oedden",
    "oeddan": "oedden",
    "o'dden": "oedden",
    "oddach": "oeddech",
    "oddat": "oeddet",
    "odda": "roedd",
    "swn": "buaswn",
    "basai": "buasai",
    "sa": "buasai",
    "sa'n": "bysa'n",
    "dyla": "dylai",
    "dylia": "dylai",
    "ch'mod": "chi'n gwybod",
    "chi'mod": "chi'n gwybod",
    "ch'mo'": "chi'n gwybod",
    "ch'mo": "chi'n gwybod",
    "ch'mbo'": "chi'n gwybod",
    "d'chmod": "chi'n gwybod",
    "d'ch'mod": "chi'n gwybod",
    "d'ch'od": "chi'n gwybod",
    "dach'mod": "chi'n gwybod",
    "dach'bo'": "chi'n gwybod",
    "ch'bo'": "chi'n gwybod",
    "ch'od": "chi'n gwybod",
    "ch'bod": "chi'n gwybod",
    "dych'bo'": "chi'n gwybod",
    "dych'mod": "chi'n gwybod",
    "t'o'": "ti'n gwybod",
    "t'mo'": "ti'n gwybod",
    "t'bo'": "ti'n gwybod",
    "t'w'o'": "ti'n gwybod",
    "t'": "ti'n gwybod",
    "sti": "wyddost ti",
    "su'": "sydd",
    "sy'": "sydd",
    "d'chi'n": "rydych chi'n",
    "dach": "dych",
    "sbio": "sbïo",
    "ano": "arno",
    "ry": "rhy",
    "dou": "dau",
    "ddou": "ddau",
    "flan": "flân",
    "dy'": "dydd",
    "camra": "camera",
    "barbiciw": "barbeciw",
    "capal": "capel",
    "nyrfys": "nerfus",
    "coedan": "coeden",
    "ogyn": "hogyn",
    "gry": "gryf",
    "wedig": "enwedig",
    "fforyma": "fforymau",
    "cynor": "cyngor",
    "pethan": "petha'n",
    "osa": "oes yna",
    "jiom": "dydi o ddim",
    "rhai'": "rhaid",
    "rai'": "raid",
    "wi": "dw i",
    "dwi": "dw i",
    "mlynadd": "mlynedd",
    "flynadd": "flynedd",
    "ifan'": "ifanc",
    "adag": "adeg",
    "gra": "gryf",
    "ama": "amau",
    "m'e": "mae",
    "hy'": "hyd",
    "y'": "yn",
    "resyme":"resymau",
    "dalld": "deall",
}

# ============================================================================
# HESITATION STANDARDIZATION
# ============================================================================
HESITATION_STANDARDIZATION = {
    "yym": "ym",
    "yy": "ym",
    "yrm": "ym",
    "ymm": "ym",
}

# ============================================================================
# CONTEXT RULES FOR MA'
# ============================================================================

# Lookup table for normalizing followers after "ma'"
# ma' ALWAYS becomes mae
# This maps the follower word to what the follower should become
# e.g., "ma' nw" -> "mae nhw" (nw becomes nhw)
#       "ma' nhw" -> "mae nhw" (nhw stays nhw)
#       "ma' wnna" -> "mae hwnna" (wnna becomes hwnna)
#       "ma' 'na" -> "mae 'na" ('na stays 'na)
MA_FOLLOWERS = {
    # Existential/possessive patterns (follower stays same)
    "'na": "'na",           # ma' 'na -> mae 'na (there is)
    "na": "na",             # ma' na -> mae na
    "'di": "'di",           # ma' 'di -> mae 'di
    "'da": "'da",           # ma' 'da fi -> mae 'da fi (I have)

    # Pronouns (follower normalized to standard form)
    "nw": "nhw",            # ma' nw -> mae nhw
    "n'w": "nhw",           # ma' n'w -> mae nhw
    "nw'n": "nhw'n",        # ma' nw'n -> mae nhw'n
    "nw'm": "nhw'm",        # ma' nw'm -> mae nhw'm
    "fe": "fe",             # ma' fe -> mae fe
    "fe'n": "fe'n",         # ma' fe'n -> mae fe'n
    "hi": "hi",             # ma' hi -> mae hi
    "hi'n": "hi'n",         # ma' hi'n -> mae hi'n
    "nhw": "nhw",           # ma' nhw -> mae nhw
    "nhw'n": "nhw'n",       # ma' nhw'n -> mae nhw'n

    # Possession markers (follower stays same)
    "gen": "gen",           # ma' gen i -> mae gen i
    "genna": "genna",       # ma' genna i -> mae genna i
    "genno": "genno",       # ma' genno fo -> mae genno fo
    "genni": "genni",       # ma' genni -> mae genni
    "gyda": "gyda",         # ma' gyda fi -> mae gyda fi
    "gynnon": "gynnon",     # ma' gynnon ni -> mae gynnon ni
    "gynno": "gynno",       # ma' gynno fo -> mae gynno fo
    "gynni": "gynni",       # ma' gynni hi -> mae gynni hi
    "gynna": "gynna",       # ma' gynna i -> mae gynna i

    # Demonstrative patterns (follower stays same or gets normalized)
    "hwnna": "hwnna",       # ma' hwnna -> mae hwnna
    "hwnna'n": "hwnna'n",   # ma' hwnna'n -> mae hwnna'n
    "honna": "honna",       # ma' honna -> mae honna
    "honna'n": "honna'n",   # ma' honna'n -> mae honna'n
    "hynny": "hynny",       # ma' hynny -> mae hynny
    "hynny'n": "hynny'n",   # ma' hynny'n -> mae hynny'n
    "hynna": "hynna",       # ma' hynna -> mae hynna
    "hynna'n": "hynna'n",   # ma' hynna'n -> mae hynna'n
    "hwn": "hwn",           # ma' hwn -> mae hwn
    "hon": "hon",           # ma' hon -> mae hon

    # Modal patterns (follower normalized to standard form)
    "raid": "rhaid",        # ma' raid -> mae rhaid (must)
    "rhaid": "rhaid",       # ma' rhaid -> mae rhaid
    "angen": "angen",       # ma' angen -> mae angen (need)
    "isio": "eisiau",       # ma' isio -> mae eisiau (want)
    "isie": "eisiau",       # ma' isie -> mae eisiau
    "eisiau": "eisiau",     # ma' eisiau -> mae eisiau
    "'sha": "eisiau",       # ma' 'sha -> mae eisiau

    # Repetition (hesitation) (follower normalized to standard form)
    "ma'": "mae",           # ma' ma' -> mae mae
    "ma'r": "mae'r",        # ma' ma'r -> mae mae'r
    "ma'n": "mae'n",        # ma' ma'n -> mae mae'n
}

# ============================================================================
# CONTEXT RULES FOR 'DI
# ============================================================================

# Pronouns that precede 'di (safe to expand 'di → wedi after these)
DI_WEDI_SAFE_PRECEDERS = {
    "dwi", "fi", "ti", "ni", "chi", "nhw", "nw", "n'w",
    "sy", "sydd", "oedd", "o'dd", "ma'", "mae",
}

# ============================================================================
# MULTI-WORD REPLACEMENTS
# ============================================================================

# Multi-word phrase replacements
# Format: "phrase in lowercase" : "normalized phrase"
# These are checked BEFORE single-word replacements
MULTI_WORD_REPLACEMENTS = {
    "o's gynnoch": "oes gynnoch",
    "o's gynno": "oes gynno",
    "o's gynni": "oes gynni",
    "o's gynna": "oes gynna",
    "o's gen": "oes gen",
    "o's gyda": "oes gyda",
    "dan dred": "dan draed",
    "dan dra'": "dan draed",
    "neshi dweud": "nes i ddweud",
    "neshi deud": "nes i ddeud",
    "neshi wneud": "nes i wneud",
    "neshi neud": "nes i neud",
}
