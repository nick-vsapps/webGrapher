import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import networkx as nx
import matplotlib.pyplot as plt
import logging

logging.basicConfig(level=logging.WARN, format='%(asctime)s - %(levelname)s - %(message)s')

def get_links(url):
    try:
        logging.info(f"Fetching links from {url}")
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a')
        return [link.get('href') for link in links if link.get('href') is not None]
    except Exception as e:
        logging.error(f"Error fetching links from {url}: {e}")
        return []

def create_graph(url, depth, graph=None, base_url=None):
    if graph is None:
        graph = nx.Graph()

    if depth == 0:
        return graph

    links = get_links(url)
    for link in links:
        if link.startswith('http'):
            if base_url is not None and link.startswith(base_url):
                relative_path = urlparse(link).path
                graph.add_edge(url, relative_path)
                logging.info(f"Adding edge: {url} -> {relative_path}")
            else:
                graph.add_edge(url, link)
                logging.info(f"Adding edge: {url} -> {link}")
            create_graph(link, depth - 1, graph, base_url)
            
    return graph

def draw_graph(graph):
    pos = nx.spring_layout(graph)
    nodes = nx.draw_networkx_nodes(graph, pos, node_size=800, node_color='skyblue', alpha=0.7)
    nx.draw_networkx_edges(graph, pos, width=1.0, alpha=0.5)
    nx.draw_networkx_labels(graph, pos, font_size=8)
    plt.show()

if __name__ == "__main__":
    logging.info("Starting the spider graph generation script")
    starting_url = input("Enter the starting URL: ")
    depth_limit = int(input("Enter the depth limit: "))

    graph = create_graph(starting_url, depth_limit)
    draw_graph(graph)
    logging.info("Script execution completed")
