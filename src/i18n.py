"""Translations for Ethical Web Scraping Studio."""

TEXTS = {
    "en": {
        "tag": "RESPONSIBLE DATA EXTRACTION", "title": "Ethical Web Scraping Studio",
        "subtitle": "Collect structured public data with clear limits, respectful delays and a transparent page-by-page log.",
        "settings": "Collection settings", "source": "Data source", "demo_source": "Product catalog demo (offline)",
        "books_source": "Books to Scrape (live)", "quotes_source": "Quotes to Scrape (live)", "pages_limit": "Maximum pages",
        "delay": "Delay between pages (seconds)", "timeout": "Request timeout (seconds)",
        "ethics": "Only allowlisted practice sites are available. robots.txt is checked before live collection.",
        "why": "Responsible scraping from request to export", "card1": "Polite collection", "card1_text": "Page limits, delays and robots.txt checks protect source websites.",
        "card2": "Structured parsing", "card2_text": "HTML cards and pagination become consistent records.",
        "card3": "Traceable execution", "card3_text": "Every visited page, status and extracted record count is logged.",
        "offline": "The demonstration runs entirely offline.", "live": "This option visits a public website created for scraping practice.", "run": "Start collection",
        "success": "Collection completed successfully", "pages": "Pages visited", "records": "Records collected", "requests": "HTTP requests",
        "elapsed": "Total time", "average": "Records per page", "data": "Extracted data", "summary": "Data summary", "log": "Collection log",
        "preview": "Extracted records", "numeric": "Numeric profile", "categories": "Most common values", "empty": "No records were found on the selected pages.",
        "download_csv": "Download CSV", "download_json": "Download JSON", "error": "Collection failed", "footer": "Built with Python, Beautiful Soup, requests and Streamlit · Responsible scraping portfolio project",
    },
    "pt": {
        "tag": "EXTRAÇÃO RESPONSÁVEL DE DADOS", "title": "Estúdio de Web Scraping Ético",
        "subtitle": "Colete dados públicos estruturados com limites claros, intervalos respeitosos e registro transparente de cada página.",
        "settings": "Configurações da coleta", "source": "Fonte de dados", "demo_source": "Catálogo de produtos fictício (offline)",
        "books_source": "Books to Scrape (online)", "quotes_source": "Quotes to Scrape (online)", "pages_limit": "Limite de páginas",
        "delay": "Intervalo entre páginas (segundos)", "timeout": "Tempo limite da requisição (segundos)",
        "ethics": "Somente sites de prática autorizados estão disponíveis. O robots.txt é verificado antes da coleta online.",
        "why": "Scraping responsável da requisição à exportação", "card1": "Coleta respeitosa", "card1_text": "Limites, intervalos e robots.txt protegem os sites de origem.",
        "card2": "Extração estruturada", "card2_text": "Elementos HTML e paginação viram registros consistentes.",
        "card3": "Execução rastreável", "card3_text": "Cada página, status e quantidade extraída fica registrada.",
        "offline": "A demonstração funciona totalmente offline.", "live": "Esta opção visita um site público criado para prática de scraping.", "run": "Iniciar coleta",
        "success": "Coleta concluída com sucesso", "pages": "Páginas visitadas", "records": "Registros coletados", "requests": "Requisições HTTP",
        "elapsed": "Tempo total", "average": "Registros por página", "data": "Dados extraídos", "summary": "Resumo dos dados", "log": "Registro da coleta",
        "preview": "Registros extraídos", "numeric": "Perfil numérico", "categories": "Valores mais frequentes", "empty": "Nenhum registro foi encontrado nas páginas selecionadas.",
        "download_csv": "Baixar CSV", "download_json": "Baixar JSON", "error": "Falha na coleta", "footer": "Desenvolvido com Python, Beautiful Soup, requests e Streamlit · Projeto de scraping responsável",
    },
    "es": {
        "tag": "EXTRACCIÓN RESPONSABLE DE DATOS", "title": "Estudio de Web Scraping Ético",
        "subtitle": "Recopile datos públicos estructurados con límites claros, pausas respetuosas y un registro transparente de cada página.",
        "settings": "Configuración de recopilación", "source": "Fuente de datos", "demo_source": "Catálogo de productos de muestra (offline)",
        "books_source": "Books to Scrape (online)", "quotes_source": "Quotes to Scrape (online)", "pages_limit": "Límite de páginas",
        "delay": "Pausa entre páginas (segundos)", "timeout": "Tiempo límite de solicitud (segundos)",
        "ethics": "Solo están disponibles sitios de práctica autorizados. Se verifica robots.txt antes de la recopilación online.",
        "why": "Scraping responsable desde la solicitud hasta la exportación", "card1": "Recopilación respetuosa", "card1_text": "Los límites, pausas y robots.txt protegen los sitios de origen.",
        "card2": "Extracción estructurada", "card2_text": "Los elementos HTML y la paginación se convierten en registros consistentes.",
        "card3": "Ejecución trazable", "card3_text": "Cada página, estado y cantidad extraída queda registrada.",
        "offline": "La demostración funciona completamente offline.", "live": "Esta opción visita un sitio público creado para practicar scraping.", "run": "Iniciar recopilación",
        "success": "Recopilación completada correctamente", "pages": "Páginas visitadas", "records": "Registros recopilados", "requests": "Solicitudes HTTP",
        "elapsed": "Tiempo total", "average": "Registros por página", "data": "Datos extraídos", "summary": "Resumen de datos", "log": "Registro de recopilación",
        "preview": "Registros extraídos", "numeric": "Perfil numérico", "categories": "Valores más frecuentes", "empty": "No se encontraron registros en las páginas seleccionadas.",
        "download_csv": "Descargar CSV", "download_json": "Descargar JSON", "error": "Error de recopilación", "footer": "Creado con Python, Beautiful Soup, requests y Streamlit · Proyecto de scraping responsable",
    },
}


def t(language: str, key: str) -> str:
    return TEXTS[language][key]
