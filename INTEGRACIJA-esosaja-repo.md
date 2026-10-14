# Kā ielikt uzdevumu esošajā `m1-setup-check` repozitorijā

Princips: uzdevums dzīvo **savā apakšmapē** `praktiskie-darbi/m2-iesniegumi/` ar savu `CLAUDE.md`,
`app.py` un `tests/`. Nekas no M1 (`app/`, `tests/`, `pytest.ini`, CI) netiek aiztikts; studentiem
nav jāpārbūvē Codespace.

## 1. Faili (pasniedzējs, 5 min)

```
praktiskie-darbi/
└── m2-iesniegumi/
    ├── README.md  BACKLOG.md  CLAUDE.md
    ├── app.py  schema.sql  requirements.txt  setup-m2.sh
    ├── templates/  static/  tests/  docs/
```

Kopē šīs mapes saturu uz `praktiskie-darbi/m2-iesniegumi/` (bez `.devcontainer/` un `.gitignore` –
tie šeit ir tikai variantam «jauns repo»). Saknes `.gitignore` pievieno:

```
praktiskie-darbi/m2-iesniegumi/data.db
praktiskie-darbi/m2-iesniegumi/a11y-report.md
```

Commit → push → studenti Codespace terminālī `git pull`.

## 2. Vide (students, ~3 min, vienreiz)

```bash
bash praktiskie-darbi/m2-iesniegumi/setup-m2.sh
```

Uzstāda Flask, Playwright + Chromium un axe. Konteineris NAV jāpārbūvē. Ja gribi, lai nākamreiz
viss ir jau iekšā, pievieno esošajā `.devcontainer/devcontainer.json` pie `postCreateCommand`:
`&& pip install -r praktiskie-darbi/m2-iesniegumi/requirements.txt && python -m playwright install --with-deps chromium`
– bet tas stāsies spēkā tikai pēc «Rebuild Container».

## 3. Claude Code un CLAUDE.md

- Saknes `CLAUDE.md` (M1 noteikumi) Claude ielādē vienmēr. Apakšmapes `CLAUDE.md` – kad strādā tajā mapē.
- Lai nebūtu konflikta, studenti **palaiž `claude` no apakšmapes**: `cd praktiskie-darbi/m2-iesniegumi && claude`.
  Tad abi faili ir kontekstā, un apakšmapes faila pirmā rinda pasaka, ka tas ir prioritārs šajā mapē.
- Pārbaudi saknes `CLAUDE.md`: ja tur ir rindas tipa «visi testi ar pytest», «nemainīt struktūru»,
  «koda stils X» – vai nu tās nav pretrunā, vai pieraksti saknē: «Mapē praktiskie-darbi/m2-iesniegumi spēkā tās mapes CLAUDE.md».
- `.claude/settings.json`: ja tur ir `permissions.allow` saraksts, pievieno
  `"Bash(python app.py*)"`, `"Bash(python tests/a11y_check.py*)"`, `"Bash(sqlite3*)"` – citādi Claude katru reizi prasīs atļauju.

## 4. Ko pārbaudīt, lai M1 daļa nesalūst

| Vieta | Risks | Ko darīt |
|-------|-------|----------|
| `pytest.ini` / `tests/` | pytest savāc arī mūsu failus | mūsu fails ir `a11y_check.py` (bez `test_`), netiek savākts; ja `testpaths` ir norādīts – nekas nemainās |
| `.github/workflows` | CI lintē visus `*.py` vai dzen pytest pār visu repo | pievieno `praktiskie-darbi/m2-iesniegumi` pie ignorējamiem ceļiem vai pieņem, ka tas ir mācību kods |
| `Makefile` | ērtības | pievieno mērķus: `m2-setup`, `m2-run`, `m2-a11y` (zemāk) |
| Ports | M1 app arī uz 5000? | mūsu `app.py` lasa `PORT` – `PORT=5001 python app.py` |

```make
m2-setup:
	bash praktiskie-darbi/m2-iesniegumi/setup-m2.sh
m2-run:
	cd praktiskie-darbi/m2-iesniegumi && python app.py
m2-a11y:
	cd praktiskie-darbi/m2-iesniegumi && python tests/a11y_check.py
```

## 5. Alternatīva: jauns repo

Ja gribi tīru vidi – šī mape tāda, kāda ir (ar `.devcontainer/`), kā GitHub *template repository*;
studenti «Use this template» → «Create codespace». Mīnuss: jauna Codespace būvēšana ~5 min katram
un `ANTHROPIC_API_KEY` / Claude pieteikšanās jāsakārto no jauna.
