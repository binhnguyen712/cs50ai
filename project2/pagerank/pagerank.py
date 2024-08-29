import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    transition_model = {}
    linked_page = set()
    linked_page.update(corpus[page])
    if linked_page:
        for p in corpus:
            if p in linked_page:
                transition_model[p] = damping_factor/len(linked_page) + (1-damping_factor)/len(corpus)
            else:
                transition_model[p] = (1 - damping_factor)/len(corpus)
    else:
        for p in corpus:
            transition_model[p] = 1/len(corpus)
    return transition_model


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pagerank = { key: 0 for key in corpus}
    random_page = random.choice(list(corpus))

    for _ in range(1, n):
        sample_model = transition_model(corpus, random_page, damping_factor)
        for key in pagerank:
            pagerank[key] += sample_model[key]
        weights = [sample_model[i] for i in sample_model]
        random_page = random.choices(list(sample_model.keys()), weights=weights, k=1)[0]
    for page in pagerank:
        pagerank[page] /= n

    return pagerank

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pagerank = {key: 1/len(corpus) for key in corpus}
    converged = False
    while not converged:
        new_pagerank = {}
        converged = True
        for page in corpus:
            new_rank = (1-damping_factor)/len(corpus)
            for l in corpus:
                if len(corpus[l]) == 0:
                    new_rank += damping_factor * (pagerank[l] / len(corpus))
                elif page in corpus[l] and len(corpus[l]) > 0:
                    new_rank += damping_factor*(pagerank[l]/len(corpus[l]))
            new_pagerank[page] = new_rank
            if abs(new_pagerank[page] - pagerank[page]) > 0.001:
                converged = False
        pagerank = new_pagerank
    return pagerank


if __name__ == "__main__":
    main()
