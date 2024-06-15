import requests
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import string
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

class Crawler:
    def __init__(self, keyword):
        self.keyword = keyword
        self.results = []

    def crawl(self, url):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                text = soup.get_text()
                cleaned_text = self.limpar_texto(text)
                if self.keyword in cleaned_text:
                    self.results.append({'url': url, 'texto_limpo': cleaned_text})
        except Exception as e:
            print(f"Erro ao acessar {url}: {e}")

    def limpar_texto(self, texto):
        texto = texto.lower()
        texto = texto.translate(str.maketrans('', '', string.punctuation))
        palavras = word_tokenize(texto)
        palavras = [palavra for palavra in palavras if palavra not in stopwords.words('english')]
        ps = PorterStemmer()
        palavras = [ps.stem(palavra) for palavra in palavras]
        return ' '.join(palavras)

    def get_results(self):
        return self.results

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/processar', methods=['POST'])
def processar():
    data = request.get_json()
    print("Dados recebidos do cliente:", data)
    urls = data.get('urls', [])
    keyword = data.get('keyword', '')

    crawler = Crawler(keyword)
    for url in urls:
        print(f"Processando URL: {url}")
        crawler.crawl(url)

    print("Resultados da busca:", crawler.get_results())
    return jsonify(crawler.get_results())

if __name__ == '__main__':
    nltk.download('punkt')
    nltk.download('stopwords')
    app.run(debug=True)
