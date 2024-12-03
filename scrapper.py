import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
from urllib.parse import urlparse

def coletar_links():
    """Coleta até 4 links de pesquisa fornecidos pelo usuário"""
    links = []
    print("Digite até 4 links de pesquisa (Google, Bing ou DuckDuckGo). Deixe em branco para encerrar.")
    for i in range(4):
        link = input(f"Link {i + 1}: ").strip()
        if not link:
            break
        links.append(link)
    return links

def extrair_links_google(soup, limite=50):
    """Extrai links da página de pesquisa do Google, ignorando domínios google.com"""
    print("Extraindo links do Google...")
    resultados = []
    for a in soup.find_all('a', href=True):
        href = a['href']
        if "/url?q=" in href:
            link = href.split("/url?q=")[1].split("&")[0]
            if link.startswith("http"):
                # Exclui links do domínio google.com
                domain = urlparse(link).netloc
                if "google.com" not in domain and "google." not in domain:
                    resultados.append(link)
        if len(resultados) >= limite:
            break
    return resultados

def extrair_links_bing(soup, limite=50):
    """Extrai links da página de pesquisa do Bing, ignorando domínios bing.com"""
    print("Extraindo links do Bing...")
    resultados = []
    for a in soup.find_all('a', href=True):
        href = a['href']
        if href.startswith("http"):
            domain = urlparse(href).netloc
            if "bing.com" not in domain and "bing." not in domain:
                resultados.append(href)
        if len(resultados) >= limite:
            break
    return resultados

def extrair_links_duckduckgo(soup, limite=50):
    """Extrai links da página de pesquisa do DuckDuckGo, ignorando domínios duckduckgo.com"""
    print("Extraindo links do DuckDuckGo...")
    resultados = []
    for a in soup.find_all('a', {'class': 'result__a'}, href=True):
        href = a['href']
        if href.startswith("http"):
            domain = urlparse(href).netloc
            if "duckduckgo.com" not in domain and "duckduckgo." not in domain:
                resultados.append(href)
        if len(resultados) >= limite:
            break
    return resultados

def extrair_conteudo(url):
    """Extrai título, data e conteúdo da página"""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        resposta = requests.get(url, headers=headers, timeout=10)
        resposta.raise_for_status()
        soup = BeautifulSoup(resposta.text, 'html.parser')

        # Título da página
        titulo = soup.title.string.strip() if soup.title else "Sem título"

        # Conteúdo principal (parágrafos)
        paragrafos = soup.find_all('p')
        conteudo = " ".join([p.get_text(strip=True) for p in paragrafos if p.get_text(strip=True)])

        # Procurar a data na página
        data_publicacao = None

        # Procura tags <time> com atributo datetime
        time_tag = soup.find('time', datetime=True)
        if time_tag:
            data_publicacao = time_tag['datetime']
            data_publicacao = datetime.fromisoformat(data_publicacao).date()

        # Busca padrões comuns de datas no texto
        if not data_publicacao:
            data_formatos = [
                "%d/%m/%Y", "%Y-%m-%d", "%d %b %Y", "%B %d, %Y"
            ]
            for formato in data_formatos:
                for p in paragrafos:
                    texto = p.get_text(strip=True)
                    try:
                        data_publicacao = datetime.strptime(texto, formato).date()
                        break
                    except ValueError:
                        continue
                if data_publicacao:
                    break

        return titulo, conteudo, data_publicacao

    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar {url}: {e}")
        return None, None, None
    except Exception as e:
        print(f"Erro inesperado ao processar {url}: {e}")
        return None, None, None

def salvar_excel(dados, arquivo="resultados_raspagem.xlsx"):
    """Salva os resultados em um arquivo Excel"""
    if not dados:
        print("Nenhum dado válido para salvar.")
        return
    df = pd.DataFrame(dados)
    with pd.ExcelWriter(arquivo, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name="Resultados")
    print(f"Resultados salvos no arquivo: {arquivo}")

def processar_raspagem():
    """Fluxo principal para processar a raspagem"""
    links = coletar_links()
    if not links:
        print("Nenhum link fornecido. Encerrando.")
        return

    dados = []
    for link in links:
        try:
            resposta = requests.get(link, timeout=10)
            resposta.raise_for_status()
            soup = BeautifulSoup(resposta.text, 'html.parser')

            # Identificar o motor de busca e extrair links
            if "google.com" in link:
                urls = extrair_links_google(soup)
            elif "bing.com" in link:
                urls = extrair_links_bing(soup)
            elif "duckduckgo.com" in link:
                urls = extrair_links_duckduckgo(soup)
            else:
                print(f"Link não reconhecido: {link}. Pulando para o próximo.")
                continue

            # Raspagem de conteúdo dos links extraídos
            for url in urls:
                titulo, conteudo, data_publicacao = extrair_conteudo(url)
                # Apenas adiciona páginas válidas
                if titulo and conteudo:
                    dados.append({
                        "Título": titulo,
                        "Link": url,
                        "Data de Publicação": data_publicacao,
                        "Conteúdo": conteudo
                    })

        except requests.exceptions.RequestException as e:
            print(f"Erro ao acessar o link de pesquisa {link}: {e}")
        except Exception as e:
            print(f"Erro inesperado ao processar o link {link}: {e}")

    # Salvar os resultados em Excel
    salvar_excel(dados)

# Executar o programa
if __name__ == "__main__":
    processar_raspagem()
