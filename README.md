# Boris — Dai, dai, dai!

Questo README lo scriviamo in italiano, perché **l'inglese c'ha rotto il cazzo**.
Se ti senti come Stanis e ti sembra troppo italiano, c'è la [versione inglese](README.en.md): thank you for being so not Italian.

16 clip vocali da **Boris**, pronte per [PeonPing](https://github.com/PeonPing/peon-ping):
René, Duccio, Stanis e tutta la troupe reagiscono alle smarmellate del tuo coding agent.
Contiene linguaggio esplicito. E ci mancherebbe pure.

## Installazione — Dai, dai, dai!

Hai già configurato PeonPing per il tuo editor? Allora apri tutto:

1. Scarica **[boris-1.0.0.zip](https://raw.githubusercontent.com/mgallo/openpeon-boris/main/downloads/boris-1.0.0.zip)**.
2. Estrai l'archivio: troverai una cartella chiamata `boris`.
3. Apri un terminale nella cartella che contiene `boris` ed esegui:

   ```sh
   peon packs install-local ./boris
   peon packs use boris
   ```

E ora possiamo girare. Lo ZIP contiene solo il manifest, gli audio e i crediti.
Non devi clonare il repository né eseguire gli script Python del progetto.
PeonPing gestisce le proprie dipendenze di esecuzione.
Il checksum dell'archivio è in [SHA256SUMS](downloads/SHA256SUMS).

Per sostituire un'installazione di Boris già presente, esegui
`peon packs install-local ./boris --force`, poi `peon packs use boris`.

Vuoi sentire se funziona? Dai, facciamo una prova:

```sh
peon preview task.complete
```

Boris non è ancora nel registro OpenPeon: finché non viene accettato, usa lo
ZIP qui sopra. Dopo la registrazione potrai installarlo anche con
`peon packs use --install boris`.

## Non hai PeonPing? — Non c'hai capito un cazzo?

Installa PeonPing una volta, poi configura l'integrazione per il tuo editor seguendo le
[istruzioni ufficiali](https://github.com/PeonPing/peon-ping#install).
Con Homebrew su macOS o Linux:

```sh
brew install PeonPing/tap/peon-ping
peon-ping-setup
```

Segui le istruzioni dell'adattatore per il tuo editor, poi installa Boris come indicato sopra.
Il soundpack fornisce i suoni; PeonPing e l'adattatore dell'editor li fanno partire.
Gli eventi disponibili dipendono dall'adattatore.

## Comandi

Per mettere in pausa, riprendere, regolare il volume e controllare lo stato:

```sh
peon pause
peon resume
peon volume 0.5
peon status
```

## Cosa sentirai — Ce se capisce e ’nce se capisce

| Categoria | Clip |
| --- | --- |
| `session.start` | Dai, dai, dai! / Apri tutto |
| `task.acknowledge` | Apri tutto / Dai, dai, dai! |
| `task.complete` | Mito, genio / Bucio de culo / Sticazzi |
| `task.error` | A cazzo di cane / Cagna maledetta / È stato stocazzo / Sei molto italiano |
| `input.required` | Ce se capisce e ’nce se capisce / Ma tu chi cazzo sei? |
| `resource.limit` | La qualità c’ha rotto er cazzo / Attaccati al cazzo |
| `user.spam` | Muto / Non mi devi rompere i coglioni |
| `session.end` | Sticazzi |
| `task.progress` | Se me vedi distratto… |

`task.acknowledge` è disabilitato per impostazione predefinita in PeonPing.
`session.end` e `task.progress` sono categorie CESP opzionali: gli hook integrati
attuali di PeonPing non le attivano. Restano disponibili per le anteprime e i lettori compatibili.

## Sviluppo — La qualità c’ha rotto er cazzo

Nel repository trovi anche una soundboard per il browser e strumenti Python opzionali
per la validazione, la riproduzione locale e la creazione degli archivi di rilascio.
Questi strumenti non fanno parte del soundpack scaricabile.

La documentazione tecnica qui sotto è ancora in inglese. Stanis approverebbe:

- [Guida allo sviluppo e ai rilasci](docs/development.md)
- [Configurazione facoltativa dell'ambiente di lavoro](docs/local-setup.md)
- [Crediti e provenienza degli audio](CREDITS.md)

Il pack segue [CESP 1.0](https://openpeon.com/spec). Le clip non sono modificate
e durano circa 0,7–6,8 secondi. Tutti i diritti sugli audio restano ai rispettivi titolari.
