# I Lupi dell'Assia

**Un modulo per Rural Gothic** di Smart Bonsai Games

> *"Ogni cacciatore è anche la preda. E il diavolo tiene sempre i conti."*

Ispirato a *Angel Heart: Ascensore per l'Inferno*

## Panoramica

Inverno 1778. Sei mercenari dell'Assia-Kassel ricevono l'ordine di indagare su un massacro di civili in una valle isolata del Connecticut. Le descrizioni dei criminali sono vaghe ma inquietanti: certi dettagli sembrano quasi familiari.

Uno scenario di orrore psicologico dove i giocatori sono sia gli investigatori che i colpevoli: il Diavolo li ha riportati sulla scena del crimine perché giudichino se stessi.

## Struttura

Il modulo è composto da tre documenti:

| Documento | Contenuto |
| --- | --- |
| **Modulo Base** | Scenario completo: mistero, luoghi, personaggi, meccaniche, dilemmi, finali |
| **Pregenerati** | 6 schede personaggio con segreti terribili e tabella corrispondenze |
| **Supplemento Cronista** | Materiali espansi: lettere complete, guida Hannah, varianti, albero decisionale |

## Build locale

### Requisiti

- Python 3.10+
- pandoc
- weasyprint

### Installazione

```bash
pip install weasyprint
```

### Generare i PDF

```bash
# Tutti e tre i moduli
bash scripts/build-pdf.sh all

# Singolo modulo
bash scripts/build-pdf.sh modulo-base
bash scripts/build-pdf.sh pregenerati
bash scripts/build-pdf.sh supplemento
```

I PDF vengono generati in `output/`.

## Build automatica (GitHub Actions)

La repository include un workflow GitHub Actions che genera automaticamente i PDF:

- **Su tag `v*`**: crea una Release GitHub con tutti i PDF allegati
- **Su `workflow_dispatch`**: genera i PDF come artifact scaricabile

## Struttura repository

```
i-lupi-dell-assia/
├── .github/workflows/build-pdf.yml
├── content/
│   ├── modulo-base/          # 16 file markdown
│   ├── pregenerati/          # 5 file markdown
│   └── supplemento/          # 10 file markdown
├── scripts/
│   ├── assemble.py           # Script di assemblaggio e build
│   ├── build-pdf.sh          # Wrapper shell
│   └── pdf-style.css         # Stile PDF (Rural Gothic theme)
├── assets/fonts/             # Font custom (opzionale)
├── output/                   # PDF generati
├── requirements.txt
└── README.md
```

## Versione

**v1.1** — Post Chaos Testing (300.000 sessioni simulate, 8 fix critici, 10 chiarificazioni)

## Licenza

Tutti i contenuti sono proprietà dell'autore. Rural Gothic è un sistema di Smart Bonsai Games.
