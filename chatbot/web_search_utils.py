import requests
from bs4 import BeautifulSoup
import concurrent.futures

def fetch_with_timeout(url, timeout=8):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Skipping {url} due to error: {e}")
        return None

def extract_main_content(html):
    try:
        soup = BeautifulSoup(html, "html.parser")
        for tag in soup(["script", "style", "head", "nav", "footer", "iframe", "img"]):
            tag.decompose()
        return " ".join(soup.stripped_strings)
    except Exception as e:
        print(f"Error extracting main content: {e}")
        return None

def get_html_contents(urls):
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        html_contents = list(executor.map(fetch_with_timeout, urls))
    
    content_results = []
    for url, html in zip(urls, html_contents):
        if html:
            main_content = extract_main_content(html)
            if main_content:
                content_results.append({"url": url, "html": main_content})
    return [i['html'] for i in content_results]


def brave_search(query):    
    parameters = {
        "q": query,
        "country": "us",
        "search_lang": "en",
        "ui_lang": "en-US",
        "count": 20,
        "offset": 0
    }

    # Define headers
    headers = {
        "Accept": "application/json",
        "Accept-Encoding": "gzip",
        "X-Subscription-Token": os.getenv('BRAVE_API_KEY')
    }
    brave_search_api = "https://api.search.brave.com/res/v1/web/search"
    response = requests.get(brave_search_api, params=parameters, headers=headers)
    response = response.json()        
    web_result_context = ''
    urls = []
    for idx, wr in enumerate(response['web']['results']):

        cur_wr_str = f'''Search Result: {idx+1}\n'''
        for wr_key,wr_value in wr.items():                                 
            if wr_key in ['title', 'description']:
                cur_wr_str += f'''{wr_key}: {wr_value}\n'''
            elif wr_key == 'url':# and len(urls)<5:
                urls.append('https://webcache.googleusercontent.com/search?q=cache:'+wr_value)
        if len(urls)==5:
            break
            
        web_result_context += cur_wr_str+'\n\n'

    
    return web_result_context, urls