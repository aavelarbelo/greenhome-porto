# WORKLOG — GreenHome Porto

Fonte única de contexto do projeto. Se mudar de conversa ou ferramenta, colar este ficheiro para retomar.

---

## ⏸️ Onde parámos (2026-09-30, fim do dia)

O diagnóstico foi executado pela 1.ª vez e **o SuperCasa bloqueia o Selenium** com um anti-bot ("Executando verificação de segurança"). O scraper original do UrbanEco também é bloqueado: o problema é do site e não do código.
Não contornamos a proteção (D10). O Idealista está excluído (não permite recolha).
Existe um dataset de junho de 2026 (`DataSet_Scraping_FINAL.xlsx`). A **D11 está proposta, mas não decidida**: usá-lo como fonte oficial. Antes de decidir, avaliamos a qualidade do dataset.

## ▶️ Próxima sessão (um passo de cada vez)

1. [ ] Rotina de início (pasta, `.venv`, `python --version` 3.13.3)
2. [ ] Copiar `DataSet_Scraping_FINAL.xlsx` para `data/raw/` (gitignored; nunca vai para o GitHub, D10)
3. [ ] Avaliar a qualidade do dataset, antes de decidir a D11:
   - Qual é o separador mais próximo do original (`Dataset_geral`, `Dataset_geralV2`, `PivotDatasetV2`) e o que mudou entre eles?
   - Número de linhas, duplicados por `url`, valores em falta por coluna
   - `classe_Energética`: distribuição de valores, ausentes e sinais do bug da regex (excesso de "E"?) → D6
   - `area_ut` vs `area_br`: preenchimento e coerência (útil ≤ bruta?) → D4
   - Há data de recolha por linha? → D3/D5
   - Proveniência: que script gerou o dataset? (provavelmente `scrape_supercasa.py` no arquivo do UrbanEco, ainda não revisto)
4. [ ] Decidir a D11 com base na avaliação
5. [ ] (Mais tarde) Perfil do GitHub: a secção "Featured" chama ao projeto "UrbanEco" e o link aponta para `energy-value-index-porto`. Corrigir para "GreenHome Porto".

## Rotina de início de sessão

```powershell
cd C:\dev\projects\greenhome-porto
.\.venv\Scripts\Activate.ps1
python --version   # tem de dizer 3.13.3
```

## Regras de trabalho

- Uma única conversa de orientação (Claude). Este ficheiro é o backup do contexto.
- **Um único passo por mensagem.** Começa com uma frase: em que passo estamos e o que vamos fazer. Espera pela confirmação antes de avançar.
- Antes de cada comando: onde, em que pasta, o que faz e o resultado esperado.
- As edições de ficheiros são explicadas com o rato (por exemplo, "três cliques na linha e escreve por cima"), não com atalhos de teclado.
- Verificar antes de alterar (listar antes de apagar, `git diff` antes do commit).
- O README é o documento de referência: a prática segue o README, não o contrário.

---

## Decisões

| # | Decisão | Porquê | Estado | Data |
|---|---|---|---|---|
| D1 | Todo o código novo vive no GreenHome. O UrbanEco (`C:\dev\archive\urbaneco-analytics`) é só consulta. | Separar o projeto novo do antigo e preservar os originais. | ✅ | 2026-09-29 |
| D2 | Um componente do UrbanEco só é reaproveitado depois de explicado e verificado. | O scraper antigo tem erros conhecidos. | ✅ | 2026-09-29 |
| D3 | O raw guarda os valores originais com data de recolha e nunca é substituído. | Permite repetir a limpeza a partir da origem. | ✅ | 2026-09-29 |
| D4 | A área do anúncio é útil ou bruta? O README define `area_m2` como área útil. O dataset de junho tem `area_ut` e `area_br` em colunas separadas, o que pode resolver a D4. | Muda o significado do €/m². | ⏳ | |
| D5 | Distinguir um duplicado por erro do mesmo anúncio observado noutra recolha. | Necessário para o histórico. | ⏳ | |
| D6 | Quantos imóveis têm classe energética real (não ausente nem mal extraída)? | Crítico para a pergunta do projeto. | ⏳ | |
| D7 | Python 3.13.3 no `.venv`. | Estável para selenium, pandas e psycopg. A 3.14 não é usada. | ✅ | 2026-09-29 |
| D8 | A estrutura de pastas segue integralmente a secção 4 do README. As pastas são criadas quando a etapa começa. | O README é o documento de referência. | ✅ | 2026-09-30 |
| D9 | Organização geral do PC: `C:\dev\` com `projects`, `learning`, `archive`, `scratch`. | Um sítio fixo para cada coisa. | ✅ | 2026-09-29 |
| D10 | Uso ético e legal dos dados: recolha em pequena escala e com pausas; dados brutos só locais; publicação apenas de agregados; sem dados pessoais de anunciantes; sem treino de IA; **não contornar proteções anti-bot**. Email ao SuperCasa a pedir autorização: opcional, não enviado. | `robots.txt` (permite `/comprar-casas/`, `ai-train=no`) e Condições de Utilização (4.2 meios de obtenção, 4.3 n.º 8 dados pessoais, 7 base de dados, 12 uso pessoal). | ✅ | 2026-09-30 |
| D11 | **Proposta:** usar o `DataSet_Scraping_FINAL.xlsx` (jun/2026) como fonte oficial, como "retrato do mercado em junho de 2026". A mudança de fonte fica documentada no README como uma descoberta de engenharia. O scraper não é apagado: fica como evidência. | O SuperCasa bloqueia a recolha automática e o Idealista não permite recolha. | ⏳ por decidir, depois da avaliação de qualidade | |

---

## Estado atual

### ✅ Concluído
- Estrutura `C:\dev\`, clone, `.gitignore`, `.venv` (3.13.3), `requirements.txt` (UTF-8)
- Estrutura de pastas alinhada com o README (D8)
- `src/ingestion/diagnostico_supercasa.py`: original (commit `5d4c1a9`) e versão corrigida (commit `0dbfb6d`): saída em `data/raw/diagnostico_supercasa/`, `--condicao novo|usado`, exige Python 3.13
- URLs confirmadas no scraper original: novo = `.../porto/com-novo`, usado = `.../porto/com-bom-estado` (também existem `com-para-reformar` e `com-em-construcao`)
- `robots.txt` e Condições de Utilização do SuperCasa verificados → D10
- 1.ª execução do diagnóstico (`--condicao novo`): **bloqueado pelo anti-bot**. Evidências em `data/raw/diagnostico_supercasa/20260930T205926_487042Z_novo/`

### ⏳ Pendente
- Avaliar a qualidade do dataset de junho e decidir a D11
- D4, D5 e D6 (dependem da avaliação)
- Rever o `scrape_supercasa.py` do arquivo do UrbanEco (proveniência do dataset)
- Corrigir a secção "Featured" do perfil do GitHub

## Problemas conhecidos

### Scraper do UrbanEco
- Só lê os cartões da página de resultados, por isso ano, piso e casas de banho ficam sempre `None`.
- A regex da classe energética apanha letras soltas (por exemplo, "garagem e varanda" é lido como E).
- O "raw" já vem transformado, filtrado e sem duplicados, e é substituído em cada execução.

### Fontes de dados
- **SuperCasa:** anti-bot ativo (confirmado em 30/09 com o diagnóstico e com o scraper original). O Selenium é detetado e não chega à página de anúncios.
- **Idealista:** excluído (não permite recolha; já era assim no UrbanEco).

---

## Registo de sessões

### 2026-09-29
- Diagnóstico do README e do scraper original (480 linhas). Criado o script de diagnóstico (247 linhas).
- Organização do ambiente: `C:\dev\`, clone, `.gitignore`, `.venv` (3.13.3). Commit `3645893`.
- UrbanEco arquivado. Chaves verificadas: seguras.
- Decisão D8 (estrutura do README).
- **Aprendizagens:** no PowerShell o hífen faz parte do nome dos comandos. O `>>` indica um bloco por fechar. O `clone` traz do GitHub, o `push` envia para o GitHub. O venv é a "cozinha" do projeto.

### 2026-09-30
- D8 aplicada (`5748519`). `WORKLOG.md` + `requirements.txt` (`90fdbb8`).
- Script de diagnóstico: original (`5d4c1a9`) e revisão técnica com as correções 1, 2, 4 e 8 (`0dbfb6d`). A URL de "usado" que eu tinha deduzido estava errada e foi corrigida a partir do scraper original.
- `robots.txt` e termos verificados → D10.
- 1.ª execução do diagnóstico: bloqueado pelo anti-bot. O script parou e guardou as evidências, como previsto. Testes com o scraper original: também bloqueado.
- Idealista confirmado como excluído. Encontrado o dataset de junho de 2026 → proposta D11.
- **Aprendizagens:** o `git rm` apaga o ficheiro e deixa a remoção pronta para o commit. O Git não guarda pastas vazias (daí o `.gitkeep`). O `Get-Content` do PowerShell 5 mostra os acentos de UTF-8 como "lixo", mas o ficheiro está bem. Fazer commit do original antes da correção permite rever a correção com `git diff`. Confirmar dados (URLs) antes do commit evita gravar suposições. Um diagnóstico que falha com evidências é um sucesso: encontrou o problema real.
