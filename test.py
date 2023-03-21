import feedparser

# Arxiv API URL
base_url = 'http://export.arxiv.org/api/query?'

# Search parameters
search_query = 'cat:nlin AND all:emergence'
sort_by = 'submittedDate'
sort_order = 'descending'
max_results = 5

# Construct query URL
query = f'search_query={search_query}&sortBy={sort_by}&sortOrder={sort_order}&max_results={max_results}'

# Send query to Arxiv API
response = feedparser.parse(base_url + query)

# Extract paper information
papers = []
for entry in response.entries:
    title = entry.title
    summary = entry.summary
    authors = ', '.join(author.name for author in entry.authors)
    link = entry.link
    
    papers.append({'title': title, 'summary': summary, 'authors': authors, 'link': link})

# Print results
for paper in papers:
    print(f"Title: {paper['title']}")
    print(f"Authors: {paper['authors']}")
    print(f"Summary: {paper['summary']}")
    print(f"Link: {paper['link']}")
    print('\n')
