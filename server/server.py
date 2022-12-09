from http.server import BaseHTTPRequestHandler, HTTPServer
import json, tantivy, os, pickle
from urllib.parse import urlparse, parse_qs

# Index schema
schema_builder = tantivy.SchemaBuilder()
schema_builder.add_text_field("url", stored=True)
schema_builder.add_text_field("title", stored=True)
schema_builder.add_text_field("body", stored=True)
schema = schema_builder.build()

# List of indexed urls
# Used to avoid wasting space on duplicate entries
urls = list()

# load/createindex directory and url list
if not os.path.exists("index"):
    os.makedirs("index")
if os.path.exists("index/urls"):
    with open("index/urls", "rb") as fp:
        urls = pickle.load(fp)

index = tantivy.Index(schema, path=os.getcwd() + '/index')

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # serve query form at localhost:8000/
        if (self.path == '/'):
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()
            with open('search.html', 'rb') as file:
                self.wfile.write(file.read())

        # queries
        elif (self.path.startswith('/query?q=')):
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()

            print("\n----- Received Query ----->\n")
            term = parse_qs(urlparse(self.path).query)['q'][0]
            message = searchIndex(term)
            self.wfile.write(bytes(message, "utf8"))
            print("\n<----- End Query -----\n")

        else:
            self.send_response(404)
            self.send_header('Content-type','text/html')
            self.end_headers()
            message = "Nope"
            self.wfile.write(bytes(message, "utf8"))

    # receive and index page data from user
    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()

        print("\n----- Received Page ----->\n")
        length = int(self.headers['Content-Length'])
        data = json.loads(self.rfile.read(length))
        indexPage(data)
        print("\n<----- End Page -----\n")

        message = "Ok"
        self.wfile.write(bytes(message, "utf8"))


def indexPage(data: dict):
    """ Inserts a page into the index

    data - dictionary containing page information
    Expects 'url', 'title', and 'body' fields
    """

    # should update entries on duplicate urls, but
    if (data['url'] in urls):
        print("Duplicate, skipping")
        return

    print("Indexing", data['url'])
    print(data['title'])

    index.reload()
    writer = index.writer()
    # writer.delete_documents(field_name = "url", field_value = data['url'])
    # writer.commit()
    writer.add_document(tantivy.Document(
        url = data['url'],
        title = data['title'],
        body = data['body']
    ))
    writer.commit()

    # update url list and save it to disk
    urls.append(data['url'])
    with open("index/urls", "wb") as fp:
        pickle.dump(urls, fp)

def searchIndex(term: str):
    """ Queries the index

    term - string to search for in the index
    return: string containing the search results in html format
    """
    index.reload()
    
    searcher = index.searcher()
    query = index.parse_query(term, ["title", "body"])
    results = searcher.search(query)
    results_html = ""

    print(term)
    print(results)
    print()

    # construct html with results
    # despite results.count giving values greater than 10, results seems
    # to max out at 10 actual entries. look into this
    for i in range(min(10,results.count)):
        print(i, ":", results.hits[i])
        score, addr = results.hits[i]
        result = searcher.doc(addr)
        title = result["title"][0]
        url = result["url"][0]

        print("Title:", title)
        print("Url:", url)
        print("Score:", score)
        print()

        results_html += '<div class="result">'
        results_html += str(i) + ": " + title
        results_html += '<br>'
        results_html += '<a href="' + url + '">' + url + '</a><br>'
        results_html += 'Score: ' + str(score)
        results_html += '</div>'

    return results_html

with HTTPServer(('', 8000), handler) as server:
    server.serve_forever()
