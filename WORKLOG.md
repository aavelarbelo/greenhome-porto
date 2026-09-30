# WORKLOG — GreenHome Porto

Fonte única de contexto do projeto. 
---

## ⏸️ Onde parámos (2026-09-30)

A D8 foi aplicada: a estrutura de pastas segue a secção 4 do README. Commit `5748519` no GitHub.
Próximo: `WORKLOG.md` e `requirements.txt` no repositório, depois o diagnóstico do scraper.

## ▶️ Próxima sessão (por esta ordem, um passo de cada vez)

1. [x] Rotina de início: entrar na pasta, ativar o `.venv`, confirmar `(.venv)` e `python --version` 3.13.3
2. [x] Aplicar a D8: remover `data/interim`, `data/sample`, `src/greenhome`, `scripts`, `notebooks`, `reports`; criar `src/ingestion`; tirar `!data/sample/**` do `.gitignore`
3. [x] `git ls-files` para confirmar (8 ficheiros); commit `5748519` + push
4. [ ] Guardar este `WORKLOG.md` na raiz do projeto (ao lado do `README.md`)
5. [ ] `pip freeze | Out-File -Encoding utf8 requirements.txt` (não usar `>`, que no PowerShell 5 grava em UTF-16)
6. [ ] `git add WORKLOG.md requirements.txt` → commit → push
7. [ ] Localizar o `diagnostico_supercasa.py` (Downloads ou uma pasta GreenHome antiga) e movê-lo para `src/ingestion/`. Deixar de usar qualquer pasta GreenHome antiga.
8. [ ] Só depois: primeira execução do diagnóstico com o site real
9. [ ] (Mais tarde) Perfil do GitHub: a secção "Featured" chama ao projeto "UrbanEco" e o link aponta para `energy-value-index-porto`. Corrigir para "GreenHome Porto".

## Rotina de início de sessão

```powershell
cd C:\dev\projects\greenhome-porto
.\.venv\Scripts\Activate.ps1
python --version   # tem de dizer 3.13.3
```

## Regras de trabalho

- Uma única conversa de orientação (Claude). Este ficheiro é o backup do contexto.
- Um passo de cada vez. Antes de cada comando: onde, em que pasta, o que faz e o resultado esperado.
- O README é o documento de referência do projeto: a prática segue o README, não o contrário.
- As edições de ficheiros são explicadas com o rato (por exemplo, "três cliques na linha e escreve por cima"), não com atalhos de teclado.
- Verificar antes de alterar (por exemplo, listar o conteúdo antes de apagar).

---

## Decisões

| # | Decisão | Porquê | Estado | Data |
|---|---|---|---|---|
| D1 | Todo o código novo vive no GreenHome. O UrbanEco (`C:\dev\archive\urbaneco-analytics`) é só consulta. | Separar o projeto novo do antigo e preservar os originais. | ✅ | 2026-09-29 |
| D2 | Um componente do UrbanEco só é reaproveitado depois de explicado e verificado. | O scraper antigo tem erros conhecidos. Perceber antes de reutilizar. | ✅ | 2026-09-29 |
| D3 | O raw guarda os valores originais com data de recolha e nunca é substituído. | Permite repetir a limpeza a partir da origem. Corrige o problema do UrbanEco. | ✅ | 2026-09-29 |
| D4 | A área do anúncio é útil ou bruta? O README define `area_m2` como área útil: o diagnóstico tem de confirmar se o site a mostra. | Muda o significado do €/m². | ⏳ | |
| D5 | Distinguir um duplicado por erro do mesmo anúncio observado noutra recolha. | Necessário para o histórico. | ⏳ | |
| D6 | Quantos imóveis têm classe energética real (não ausente nem mal extraída)? | Crítico para responder à pergunta do projeto. | ⏳ | |
| D7 | Python 3.13.3 no `.venv`. | Estável para selenium, pandas e psycopg. A 3.14 (padrão do Windows) não é usada. O README já diz 3.13. | ✅ | 2026-09-29 |
| D8 | A estrutura de pastas segue integralmente a secção 4 do README. As pastas são criadas quando a etapa correspondente começa (`src/processing`, `src/analytics` e `.env.example` ficam para mais tarde). | O README é o documento de referência. A estrutura anterior vinha de um modelo genérico (Cookiecutter Data Science). | ✅ | 2026-09-30 |
| D9 | Organização geral do PC: `C:\dev\` com `projects`, `learning`, `archive`, `scratch`. | Um sítio fixo para cada coisa, caminhos curtos e sem espaços, fora do OneDrive. | ✅ | 2026-09-29 |

### Estrutura atual no Git (após a D8)

```
.gitignore
README.md
data/processed/.gitkeep
data/raw/.gitkeep
docs/.gitkeep
sql/.gitkeep
src/ingestion/.gitkeep
tests/.gitkeep
```

---

## Estado atual

### ✅ Concluído
- Estrutura `C:\dev\` (projects, learning, archive, scratch)
- Repositório clonado para `C:\dev\projects\greenhome-porto`
- `.gitignore`: ignora `.venv/`, `data/**` exceto os `.gitkeep`, `.env`, `__pycache__/`, `*.pyc`, `.ipynb_checkpoints/`, `logs/`, `Thumbs.db`, `.vscode/`
- Commits `3645893` (estrutura inicial) e `5748519` (D8), já no GitHub
- `.venv` com Python 3.13.3 + selenium 4.49, webdriver-manager 4.1.2, pandas 3.0.6
- UrbanEco copiado para `C:\dev\archive\urbaneco-analytics`. O original continua em `C:\2025 ISEP\8. Seminars\urbaneco-analytics`
- Confirmado com `git log --all` que o `apikey.txt` e o `.env` do UrbanEco nunca foram para o Git

### ⏳ Pendente
- `WORKLOG.md` e `requirements.txt` no repositório
- Colocar o script de diagnóstico em `src/ingestion/` e executá-lo pela primeira vez
- D4, D5 e D6 (dependem do diagnóstico)
- Corrigir a secção "Featured" do perfil do GitHub

## Problemas conhecidos do scraper do UrbanEco
- Só lê os cartões da página de resultados, por isso ano, piso e casas de banho ficam sempre `None`.
- A regex da classe energética apanha letras soltas (por exemplo, "garagem e varanda" é lido como E).
- O "raw" já vem transformado, filtrado e sem duplicados, e é substituído em cada execução.
- Não se sabe se a área é útil ou bruta.

---

## Registo de sessões

### 2026-09-29
- Diagnóstico do README e do scraper original (480 linhas). Criado o script de diagnóstico (247 linhas), apenas para diagnóstico e ainda não executado com o site real.
- Organização do ambiente: `C:\dev\`, clone, `.gitignore`, `.venv` (3.13.3) e bibliotecas.
- Commit `3645893` enviado para o GitHub.
- UrbanEco arquivado. Chaves verificadas: seguras.
- Revisão do GitHub: a estrutura de pastas criada não corresponde à do README, e daí a decisão D8. O "Featured" do perfil está desatualizado.
- **Aprendizagens:** no PowerShell o hífen faz parte do nome dos comandos (`Out-Null`, `-ItemType`). O `>>` indica um bloco por fechar. O `clone` traz do GitHub para o PC, e o `push` envia do PC para o GitHub. O venv é a "cozinha" do projeto.

### 2026-09-30
- D8 aplicada: 6 pastas removidas com `git rm` (depois de confirmar que só tinham o `.gitkeep`), `src/ingestion` criada, exceção `!data/sample/**` retirada do `.gitignore`. Commit `5748519`.
- **Aprendizagens:** o `git rm` apaga o ficheiro e deixa a remoção pronta para o commit. O Git não guarda pastas vazias, daí o `.gitkeep`. O `Get-Content` do PowerShell 5 mostra os acentos de ficheiros UTF-8 como "lixo", mas o ficheiro está bem (confirma-se no VS Code). Ficheiros vazios e iguais aparecem no commit como `rename`.
