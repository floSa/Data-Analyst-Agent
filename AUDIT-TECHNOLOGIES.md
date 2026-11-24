# Audit technologies : Data-Analyst-Agent

Date : 2026-11-04. Ce n'est pas un avis juridique ; les points ⚖️ sont à faire valider par un juriste.

**Méthode.** Licences, dates et statuts vérifiés en direct (PyPI, GitHub, Hugging Face, Docker Hub). Pas de mémoire. Ce qui n'a pas pu être vérifié est listé en section 7.

**Légende.** ✅ OK · ⚠️ OK sous conditions · ❌ bloquant.
**Maintenance.** ACTIF < 6 mois · RALENTI 6 à 18 mois · ABANDONNÉ > 18 mois, archivé ou déprécié.
Un paquet abandonné mais permissif reste utilisable en code fermé : le risque est la sécurité, pas la licence.

**Mode de livraison principal : on-prem** (images Docker chez le client, donc redistribution).

---

## 1. Verdict

- ✅ **Aucun bloquant commercial** sur le code tiers ni sur les poids du LLM, en SaaS comme en on-prem.
- ✅ **Le LLM Gemma 4 E4B est en Apache-2.0** (vérifié sur Hugging Face). Le README du projet (« licence éditeur à relire ») est périmé. ⚖️ Une page « Prohibited use » reste dans la doc Gemma ; le texte Apache servi ne la cite pas.
- ✅ **Aucun GPL/AGPL au runtime.** Seul du MPL-2.0 (certifi, orjson, tqdm, libzmq du bac à sable), OK non modifié.
- ❌ **Aucun fichier `LICENSE`** dans le projet, et le README annonce MIT à tort. Pour vendre : EULA ou licence propriétaire.
- ⚠️ **nginx 1.27 est hors support** et exposé côté client (image du 2025-04-16).
- ⚠️ **Jeux de données :** Titanic a une licence inconnue et contient des noms réels. California Housing n'a pas de licence explicite.

---

## 2. Actions

| Prio | Action | Pourquoi |
|---|---|---|
| **P0** | Ajouter un `LICENSE` propriétaire ou une EULA | Rien n'est déclaré |
| **P0** | Générer `THIRD-PARTY-NOTICES` : CC BY 4.0 (Iris), MIT/BSD/Apache, MPL-2.0, texte Apache-2.0 de Gemma 4 | Obligations de licence |
| **P0** | ⚖️ Faire valider la page « Prohibited use » de Gemma 4 | Ambiguïté non levée |
| **P0** | Retirer ou remplacer `titanic.csv` et `california_housing.csv.gz` du livrable | Licence inconnue, noms réels |
| P1 | nginx → `nginx:1.30-alpine` (`deploy/compose.yaml`) | Hors support, dizaines d'avis 2026 |
| P1 | `uv lock --upgrade-package pydantic-ai-slim` (→ 2.65.0), certifi, urllib3, httpx2, langgraph-sdk, opentelemetry-api | 9 avis sur pydantic-ai 2.22.0 |
| P1 | Bac à sable : pillow 13.0.0, tornado 6.6. Aligner pandas (3.0.3 / 3.0.5) et duckdb (1.5.4 / 1.5.5) | 39 et 9 avis ; versions décalées |
| P1 | Corriger les docs périmées : README (licence), `CADRAGE.md` (Qwen3-Coder), `MOTEUR.md` (vLLM 0.28.0) | Incohérences |
| P1 | Documenter « socket Docker = accès root à l'hôte » dans le dossier de sécurité client | Risque déjà connu (`docs/INSTALLATION.md` l.253) |
| P2 | Excel : openpyxl → calamine | Abandonné |
| P2 | esprima → Playwright (dev) | Abandonné |
| P2 | Tester DuckDB 2.0 avant de lever le plancher ; mettre `<2.0` d'ici là | Nouveau parseur |
| P2 | Envisager de sortir LangGraph | Graphe de 8 nœuds, une douzaine de transitifs |
| P2 | ⚖️ Relire la licence NVIDIA si l'image `vllm-openai` est livrée | Base `nvidia/cuda` |

---

## 3. Dépendances directes

### Runtime (✅ SaaS et ✅ on-prem, sauf mention ; garder les mentions de licence)

| Composant | Rôle | Version → dernière | Maintenance | Licence |
|---|---|---|---|---|
| argon2-cffi | Hash des mots de passe | 25.1.0 (2025-06) | RALENTI (stable) | MIT |
| duckdb | Moteur SQL | 1.5.5 → 2.0.0 (2026-10-21) | ACTIF | MIT |
| fastapi | API | 0.141.1 → 0.162.0 | ACTIF | MIT |
| joblib | Chargement des modèles | 1.5.3 → 1.6.0 | ACTIF | BSD-3-Clause |
| langgraph | Routage en graphe | 1.2.10 → 1.2.19 | ACTIF | MIT |
| **openpyxl** | Lecture Excel | 3.1.5 (2024-06-28) | **ABANDONNÉ** | MIT |
| pandas | Données | 3.0.5 → 3.1.0 | ACTIF | BSD-3-Clause |
| pg8000 | Pilote Postgres | 1.31.5 → 1.31.6 | ACTIF | BSD-3-Clause |
| pydantic, pydantic-settings | Typage, réglages | 2.13.4, 2.14.2 | ACTIF | MIT |
| pydantic-ai-slim[openai] | Agents LLM | 2.22.0 → 2.65.0 (2026-11-03) | ACTIF | MIT |
| python-multipart | Formulaires | 0.0.32 → 0.0.33 | ACTIF | Apache-2.0 |
| pyyaml | Catalogue, comptes | 6.0.3 | RALENTI (stable) | MIT |
| scikit-learn | Modèles ML | 1.9.0 → 1.9.1 | ACTIF | BSD-3-Clause |
| sqlalchemy | Accès Postgres | 2.0.51 → 2.1.8 | ACTIF | MIT |
| sqlglot | Garde-fou SQL | 30.19.0 → 30.29.0 | ACTIF | MIT |
| uvicorn | ASGI | 0.52.1 → 0.54.0 | ACTIF | BSD-3-Clause |

Notes :
- **duckdb 2.0** : les fichiers créés par la 2.0 ne sont pas lisibles par les versions antérieures. Le projet n'ouvre les `.duckdb` qu'en lecture seule ou en mémoire. La 1.5.x est supportée jusqu'en mars 2027.
- **joblib** : `joblib.load` exécute du code (pickle). Ne jamais charger un artefact fourni par un tiers ou un client.
- **pydantic-ai** : 54 releases en 90 jours. Les avis que j'ai lus portent sur des fonctions non utilisées par le dépôt.
- **pg8000** : dépôt sur Codeberg, un seul mainteneur.
- **sqlglot** : montées majeures fréquentes, à épingler.

### Dev, non livré (`--no-dev`)

| Composant | Version | Maintenance | Licence |
|---|---|---|---|
| esprima | 4.0.1 (2018-08-24) | **ABANDONNÉ** | BSD |
| jupytext, pre-commit, pytest, pytest-cov | à jour | ACTIF | MIT |
| pytest-playwright | 0.8.0 → 0.10.0 | ACTIF | Apache-2.0 |
| ruff | 0.16.1 → 0.17.3 (borné `<0.17`) | ACTIF | MIT |
| testcontainers | 4.15.0 | ACTIF | Apache-2.0 |

---

## 4. Transitifs à connaître

| Paquet | Licence | Tiré par | Conséquence |
|---|---|---|---|
| certifi 2026.7.22 | MPL-2.0 | httpx, requests | ✅ non modifié. Avis corrigé en 2026.10.18. |
| tqdm, orjson | MPL-2.0 (…) | openai, langsmith | ✅ non modifiés |
| text-unidecode 1.3 | Artistic **ou** GPL | python-slugify → pytest-playwright | **Dev-only**. Si un jour livré : choisir Artistic. |
| pytest-base-url | MPL-2.0 | pytest-playwright | Dev-only |
| httpx 0.28.1 | BSD-3-Clause | openai | Sans release depuis 23 mois. Fork `httpx2` (BSD-3, 2026-10-21) déjà dans le lock : 6 avis, corrigés en 2.12.0. |
| urllib3 2.7.0 | MIT | requests | 3 avis, corrigés en 2.8.0 |
| tiktoken 0.13.0 | MIT | pydantic-ai [openai] | Non utilisé. Télécharge son vocabulaire sur Internet à la première utilisation : à vérifier en site isolé. |
| langchain-core, langsmith, ormsgpack, xxhash, uuid-utils | MIT, BSD, Apache | langgraph | Une douzaine de paquets pour un graphe de 8 nœuds |
| virtualenv, filelock | MIT | pre-commit | Dev-only, nombreux avis |

**`pip-audit` :** runtime 23 avis (dont 9 pydantic-ai). Bac à sable : 39 pillow 12.3.0 (corrigés en 13.0.0), 9 tornado 6.5.7 (corrigés en 6.6).

---

## 5. Modèles ML et jeux de données

| Élément | Référence | Licence vérifiée | Verdict |
|---|---|---|---|
| LLM servi | `google/gemma-4-E4B-it-qat-w4a16-ct` (maj 2026-07-20) | **Apache-2.0** | ✅ SaaS et on-prem. Garder le texte Apache-2.0. ⚖️ page « Prohibited use ». |
| LLM cité dans `docs/CADRAGE.md` | Qwen3-Coder-30B-A3B | Apache-2.0 | ✅ Jamais chargé en réel, doc périmée |
| LLM des bancs d'essai | Qwen2.5-7B-AWQ, 1.5B | Apache-2.0 | ✅ Tests seulement |
| Variantes « abliterated » | Aucune référencée | n/a | À interdire dans la doc d'exploitation |
| Serveur d'inférence | vLLM 0.33.0 (2026-11-02), dépôt privé `llm-service` non audité | Apache-2.0 | ✅ |
| `models/*.joblib` | 3 pipelines scikit-learn | Dérivés des jeux ci-dessous | ⚠️ Pickle ; liés à scikit-learn 1.9.0 |
| Iris | Fisher 1936, UCI | **CC BY 4.0** | ✅ avec attribution |
| California Housing | StatLib, recensement US 1990 | Aucune licence explicite | ⚠️ Risque faible. Ne pas livrer si inutile. |
| **Titanic** | Identique au `train.csv` de Kaggle | **Non vérifié** | ❌ À remplacer par un jeu synthétique |
| `sources/metier`, `demonstration` | Générées par scripts à graine fixe | Propriété du projet | ✅ |

---

## 6. Images Docker, infra et front

| Composant | Version | Dernière | Maintenance | Licence | Verdict |
|---|---|---|---|---|---|
| python:3.12-slim | tag mobile | 2026-11-02 | ACTIF | PSF + paquets Debian (dont GPL/LGPL) | ⚠️ Livrer l'image = textes de licence et sources GPL |
| docker:29-cli (binaire copié) | v29.9.3 | 2026-11-03 | ACTIF | **Apache-2.0** | ✅ |
| uv (`ghcr.io/astral-sh/uv:0.11`) | 0.11.9 | 0.13.7 | ACTIF | MIT ou Apache-2.0 | ✅ |
| **nginx 1.27-alpine** | tag figé 2025-04-16 | 1.30.6 stable | **ABANDONNÉ** | BSD-2-Clause | Licence ✅, **sécurité ❌** |
| PostgreSQL | fourni par l'hôte | | | PostgreSQL License | ✅ |
| Socket `/var/run/docker.sock` | | | | | ⚠️ Équivalent root. Le bac à sable est durci (`--network=none`, `--cap-drop=ALL`, `--read-only`, `no-new-privileges`). Pour un client exigeant : proxy de socket restreint ou Docker rootless. |
| Bac à sable : matplotlib 3.11.0, plotly 6.9.0, altair 6.2.2 | | | ACTIF | PSF-like, MIT, BSD | ✅ |
| Bac à sable : pillow 12.3.0, tornado 6.5.7 | | 13.0.0, 6.6 | ACTIF | MIT-CMU, Apache-2.0 | ✅ mais 39 et 9 avis |
| Bac à sable : pyzmq 27.1.0 | | 27.3.0 | ACTIF | BSD-3 (libzmq MPL-2.0) | ✅ non modifié |
| Bac à sable : numpy, scipy, statsmodels, prince… | | | | BSD, MIT, Apache | ✅ (« pas de pingouin GPL-3 » imposé par `requirements.in`) |
| **Front (chat, login)** | | | | Code du projet | ✅ **Aucun asset externe** : pas de CDN, police web, lib de graphiques ni rendu markdown |
| Playwright | 1.62.0 → 1.64.1 | | ACTIF | Apache-2.0 | ✅ dev/CI |
| vllm/vllm-openai | latest | 2026-11-02 | ACTIF | Apache-2.0 + NVIDIA Deep Learning Container License | ⚖️ si livré |

---

## 7. Alternatives

### openpyxl (abandonné, MIT, aucun risque légal)

Un seul usage runtime : `pd.read_excel` (`duckdb_excel.py:90`).

| Alternative | Licence | Dernière release | Effort | Limites |
|---|---|---|---|---|
| **python-calamine** (`engine="calamine"`) | MIT | 0.9.1 (2026-11-03) | S | Lecture seule, suffit |
| fastexcel | MIT | 0.21.0 | S | Lecture seule |
| xlsxwriter | BSD-2-Clause | 3.3.1 | S | Écriture seule (seed, tests) |

### esprima (dev-only)

| Alternative | Licence | Effort | Limites |
|---|---|---|---|
| Playwright (exécuter `new Function(script)` dans la page) | Apache-2.0 | S | Test marqué `ui`, processus séparé |
| tree-sitter-javascript 0.25.0 | MIT | S | Ajoute `tree-sitter` |

### LangGraph (MIT, ACTIF ; risque = couplage éditeur LangChain Inc.)

| Alternative | Licence | Effort | Limites |
|---|---|---|---|
| Code maison (fonctions + transitions) | Propriétaire | S-M | Graphe simple (`graph.py:544`). Supprime une douzaine de transitifs. |
| `pydantic-graph` (déjà installé via pydantic-ai) | MIT | M | Lié à pydantic-ai |
| LlamaIndex Workflows, smolagents | non vérifiées | M-L | Non examinées |

PydanticAI : pas d'alternative nécessaire (couplage limité à `Agent`, `RunContext`, `UsageLimits`, `OpenAIChatModel`). Le risque est le rythme de releases.

### nginx

| Alternative | Licence | Effort | Limites |
|---|---|---|---|
| **nginx:1.30-alpine** | BSD-2-Clause | S | Config actuelle (`http2 on;`) valable |
| Caddy | non vérifiée | M | Non examiné |

DuckDB : pas de migration utile. SQLite, DataFusion, Polars, ClickHouse local non évalués.

---

## 8. À valider et non vérifié

**⚖️ Juriste :** page « Prohibited use » de Gemma 4 · NVIDIA Deep Learning Container License si l'image vLLM est livrée.

**Non vérifié :**
- Licence du jeu Titanic (page Kaggle illisible sans JavaScript).
- Licences des navigateurs Playwright.
- Clauses de redistribution de la licence NVIDIA des conteneurs.
- Activité du dépôt openpyxl (hébergé sur heptapod, API inaccessible).
- Alternatives LlamaIndex Workflows, smolagents et Caddy.
- Appels sortants à l'exécution (langsmith, tiktoken, genai-prices) : analyse par `grep` seulement.
- Dépôt `llm-service` : privé, non audité.
- Licences des bibliothèques natives dans les wheels scipy, numpy, pillow.
