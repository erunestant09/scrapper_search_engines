# Raspagem de Resultados de Pesquisa

Este repositório contém um script em Python que realiza raspagem de páginas da web a partir de resultados de pesquisa fornecidos pelos motores de busca **Google**, **Bing** e **DuckDuckGo**. O script processa links de pesquisa fornecidos pelo usuário, acessa os resultados mais relevantes e coleta informações como título, link, data de publicação e conteúdo principal das páginas. Apenas páginas válidas (sem erros de acesso) são registradas no arquivo Excel gerado.

---

## **Funcionalidades**

1. **Coleta de Links de Pesquisa**:
   - O usuário pode fornecer até 4 links de pesquisa de **Google**, **Bing** ou **DuckDuckGo**.

2. **Extração de Links dos Resultados**:
   - O script identifica automaticamente o motor de busca e extrai os links relevantes, ignorando:
     - Links do próprio motor de busca (como `google.com`, `bing.com` e `duckduckgo.com`).
     - Subdomínios dos motores de busca (como `news.google.com`).

3. **Raspagem de Páginas**:
   - Para cada link extraído, o script tenta acessar a página e coletar:
     - **Título**
     - **Conteúdo principal**
     - **Data de publicação** (se disponível)
     - **Link original**

4. **Registro de Páginas Válidas**:
   - Somente páginas válidas (sem erros de acesso ou raspagem) são registradas no arquivo final.

5. **Geração de Planilha Excel**:
   - Todas as informações coletadas são salvas em um arquivo Excel chamado `resultados_raspagem.xlsx`.

---

## **Requisitos**

Antes de executar o script, instale as dependências necessárias:

```bash
pip install requests beautifulsoup4 pandas openpyxl
