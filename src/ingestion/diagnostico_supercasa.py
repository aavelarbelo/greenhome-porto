r"""GreenHome Porto — primeiro teste de navegação, baseado no scraper UrbanEco.

OBJETIVO
    Abrir UMA página da SuperCasa e guardar até TRÊS cartões de anúncios.
    Texto visível e HTML renderizado ficam guardados sem interpretar os campos.
    Este é um diagnóstico da ingestão; os resultados ainda não são dados analíticos.

O QUE FOI REAPROVEITADO DO ORIGINAL
    - Selenium + Chrome + ChromeDriverManager para controlar o navegador.
    - As URLs das condições (novo, usado).
    - Os seletores div.list__properties-main e article.property-card.
    - WebDriverWait para esperar pelo conteúdo.

O QUE MUDA NESTE TESTE
    - Uma página, sem paginação, e até três cartões.
    - Espera pelos cartões, em vez de apenas pelo contentor e uma pausa fixa.
    - Cada execução cria uma pasta nova em data/raw/diagnostico_supercasa/
      (protegida pelo .gitignore; nada é substituído — decisão D3).
    - Preço, área, classe energética e freguesia não são interpretados aqui.
    - Não usa Pandas, PostgreSQL, Docker, .env nem os CSV do UrbanEco.
    - Os seletores existentes são hipóteses a confirmar no navegador atual.

COMO LER
    1. verificar_ambiente: confirma Python e dependências instaladas.
    2. create_driver: inicia o Chrome com janela visível.
    3. capturar_cartoes: abre a página, espera e lê até três cartões.
    4. guardar_evidencias: guarda HTML renderizado e imagem da página.
    5. main: organiza a execução, o relatório, os erros e o fecho do Chrome.

EXECUÇÃO (PowerShell, na raiz do projeto, com o .venv ativo)
    cd C:\dev\projects\greenhome-porto
    .\.venv\Scripts\Activate.ps1
    python src\ingestion\diagnostico_supercasa.py --verificar-ambiente
    python src\ingestion\diagnostico_supercasa.py --condicao novo
    python src\ingestion\diagnostico_supercasa.py --condicao usado

SAÍDA
    data/raw/diagnostico_supercasa/<data-hora-UTC>_<condicao>/
        execucao.log   : etapas executadas e eventuais erros
        resumo.json    : ambiente, URL final, contagens e estado
        cartoes.jsonl  : um objeto JSON por cartão capturado
        pagina.html    : HTML renderizado pelo Chrome, não a resposta HTTP original
        pagina.png     : captura da janela do Chrome

    Se o Chrome não arrancar, só haverá log e resumo. Se a página bloquear ou
    os seletores deixarem de funcionar, o teste termina com erro e guarda as
    evidências que conseguir. Não há tentativas de contornar bloqueios.
    Cada condição (novo/usado) é uma amostra parcial do mercado.
    Verificar robots.txt e termos de utilização antes de qualquer execução.

REFERÊNCIA DE ESPERAS
    https://www.selenium.dev/documentation/webdriver/waits/
"""

from __future__ import annotations

import argparse
import importlib.metadata
import json
import logging
import sys
from datetime import datetime, timezone
from pathlib import Path


# [Correção 4] Várias condições: imóveis novos são quase todos A/A+, por isso
# a D6 (classe energética real) precisa também de usados.
# URLs confirmadas no scraper original (scrape_properties_selenium.py, linhas 59-60).
TARGET_URLS = {
    "novo": "https://supercasa.pt/comprar-casas/porto/com-novo",
    "usado": "https://supercasa.pt/comprar-casas/porto/com-bom-estado",
}
CARDS_CONTAINER_SELECTOR = "div.list__properties-main"
PROPERTY_CARD_SELECTOR = "article.property-card"
MAX_CARDS = 3
WAIT_SECONDS = 30
DEPENDENCIES = ("selenium", "webdriver-manager")

# [Correção 1] Raiz do projeto: este ficheiro está em src/ingestion/,
# por isso sobe dois níveis (ingestion -> src -> raiz).
PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_ROOT = PROJECT_ROOT / "data" / "raw" / "diagnostico_supercasa"


def verificar_ambiente() -> tuple[dict, bool]:
    """Consulta versões locais; não instala pacotes nem abre o navegador."""
    versions = {"python": sys.version.split()[0], "python_executable": sys.executable}
    # [Correção 8] D7: o projeto usa Python 3.13 (a 3.14 do Windows não conta).
    ok = sys.version_info[:2] == (3, 13)
    print(f"Python: {versions['python']}")
    print(f"Executável: {sys.executable}")
    if not ok:
        print("Este projeto usa Python 3.13 (decisão D7). Ativa o .venv e tenta de novo.")
    for package in DEPENDENCIES:
        try:
            versions[package] = importlib.metadata.version(package)
            print(f"{package}: {versions[package]}")
        except importlib.metadata.PackageNotFoundError:
            versions[package] = None
            print(f"{package}: não instalado neste ambiente")
            ok = False
    if not ok:
        print("Se faltarem pacotes, instala-os com o mesmo executável Python:")
        print(f'& "{sys.executable}" -m pip install selenium webdriver-manager')
    return versions, ok


def create_driver():
    """Reaproveita a configuração essencial do Chrome do scraper original."""
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager

    options = Options()
    options.add_argument("--window-size=1280,900")
    # O gestor pode descarregar o driver compatível na primeira execução.
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)


def guardar_json(path: Path, content: dict) -> None:
    """Cria o ficheiro; falha se ele já existir, evitando substituição acidental."""
    with path.open("x", encoding="utf-8") as handle:
        json.dump(content, handle, ensure_ascii=False, indent=2)


def capturar_cartoes(driver, target_url: str, condicao: str, output: Path, summary: dict, logger) -> None:
    """Navega uma vez e preserva o conteúdo observado, sem classificar imóveis."""
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.support.ui import WebDriverWait

    logger.info("[2/5] A abrir uma página (%s): %s", condicao, target_url)
    summary["etapa"] = "abrir_pagina"
    driver.set_page_load_timeout(45)
    driver.get(target_url)

    logger.info("[3/5] A esperar até %s segundos pelos cartões.", WAIT_SECONDS)
    summary["etapa"] = "localizar_cartoes"
    selector = f"{CARDS_CONTAINER_SELECTOR} {PROPERTY_CARD_SELECTOR}"
    # Nota: avança assim que existe pelo menos 1 cartão; o total pode ser maior.
    cards = WebDriverWait(driver, WAIT_SECONDS).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector))
    )
    summary["cartoes_encontrados"] = len(cards)
    summary["url_final"] = driver.current_url
    summary["titulo_pagina"] = driver.title
    logger.info("Cartões encontrados: %s. Serão guardados até %s.", len(cards), MAX_CARDS)

    summary["etapa"] = "guardar_cartoes"
    summary["cartoes_guardados"] = 0
    with (output / "cartoes.jsonl").open("x", encoding="utf-8") as handle:
        for index, card in enumerate(cards[:MAX_CARDS], start=1):
            # .text é o texto visível devolvido pelo Selenium; outerHTML é o
            # elemento renderizado. Não são cópias byte a byte da resposta HTTP.
            record = {
                "condicao": condicao,
                "posicao_na_pagina": index,
                "recolhido_em_utc": datetime.now(timezone.utc).isoformat(),
                "pagina_origem": driver.current_url,
                "texto_visivel": card.text,
                "html_renderizado": card.get_attribute("outerHTML"),
                "links_observados": [
                    link.get_attribute("href")
                    for link in card.find_elements(By.CSS_SELECTOR, "a[href]")
                ],
            }
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")
            handle.flush()
            summary["cartoes_guardados"] += 1
            logger.info("Cartão %s guardado. Início do texto: %r", index, card.text[:160])


def guardar_evidencias(driver, output: Path, summary: dict, logger) -> None:
    """Tenta guardar também o que o navegador mostrou em caso de erro."""
    summary["erros_evidencias"] = []
    try:
        summary["url_final"] = driver.current_url
        summary["titulo_pagina"] = driver.title
        with (output / "pagina.html").open("x", encoding="utf-8") as handle:
            handle.write(driver.page_source)
    except Exception as exc:
        message = f"Não foi possível guardar o HTML: {type(exc).__name__}: {exc}"
        summary["erros_evidencias"].append(message)
        logger.warning(message)
    try:
        image_bytes = driver.get_screenshot_as_png()
        with (output / "pagina.png").open("xb") as handle:
            handle.write(image_bytes)
    except Exception as exc:
        message = f"Não foi possível guardar a imagem: {type(exc).__name__}: {exc}"
        summary["erros_evidencias"].append(message)
        logger.warning(message)


def main() -> int:
    parser = argparse.ArgumentParser(description="Diagnóstico SuperCasa: uma página, até três cartões.")
    parser.add_argument("--verificar-ambiente", action="store_true", help="Mostrar versões locais e terminar.")
    parser.add_argument(
        "--condicao",
        choices=sorted(TARGET_URLS),
        default="novo",
        help="Condição dos imóveis a observar (predefinição: novo).",
    )
    args = parser.parse_args()
    environment, ok = verificar_ambiente()
    if args.verificar_ambiente or not ok:
        return 0 if ok else 2

    target_url = TARGET_URLS[args.condicao]
    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S_%fZ") + f"_{args.condicao}"
    output = OUTPUT_ROOT / run_id
    output.mkdir(parents=True, exist_ok=False)
    logger = logging.getLogger("greenhome.diagnostico")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    handlers = [logging.StreamHandler(sys.stdout), logging.FileHandler(output / "execucao.log", mode="x", encoding="utf-8")]
    for handler in handlers:
        handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
        logger.addHandler(handler)

    summary = {
        "run_id": run_id,
        "estado": "iniciado",
        "etapa": "iniciar_chrome",
        "ambiente": environment,
        "condicao": args.condicao,
        "pagina_pedida": target_url,
        "limite_paginas": 1,
        "limite_cartoes": MAX_CARDS,
        "cartoes_guardados": 0,
        "pasta_saida": str(output),
    }
    driver = None
    exit_code = 1
    try:
        logger.info("[1/5] A iniciar o Chrome com janela visível.")
        driver = create_driver()
        summary["versao_chrome"] = driver.capabilities.get("browserVersion")
        summary["versao_chromedriver"] = driver.capabilities.get("chrome", {}).get("chromedriverVersion")
        capturar_cartoes(driver, target_url, args.condicao, output, summary, logger)
        summary["estado"] = "captura_concluida"
        summary["etapa"] = "concluido"
        exit_code = 0
    except KeyboardInterrupt:
        summary["estado"] = "interrompido"
        logger.warning("Execução interrompida pelo utilizador.")
        exit_code = 130
    except Exception as exc:
        summary["estado"] = "erro"
        summary["erro_tipo"] = type(exc).__name__
        summary["erro_mensagem"] = str(exc)
        logger.exception("O diagnóstico parou na etapa %s.", summary["etapa"])
    finally:
        logger.info("[4/5] A guardar as evidências disponíveis.")
        if driver is not None:
            guardar_evidencias(driver, output, summary, logger)
            try:
                driver.quit()
            except Exception as exc:
                logger.warning("Erro ao fechar o Chrome: %s", exc)
        summary["terminado_em_utc"] = datetime.now(timezone.utc).isoformat()
        guardar_json(output / "resumo.json", summary)
        logger.info("[5/5] Estado: %s. Resultados em: %s", summary["estado"], output)
        for handler in handlers:
            logger.removeHandler(handler)
            handler.close()
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
