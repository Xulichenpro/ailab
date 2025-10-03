import wikipedia

def search_wikipedia(query, num_results=5):
    try:
        wikipedia.set_lang("en")
        # Search for the query on Wikipedia
        search_results = wikipedia.search(query, results=num_results)
        
        # Fetch the summary for each result
        summaries = []
        for title in search_results:
            try:
                summary = wikipedia.summary(title, sentences=5)
                summaries.append(summary)
            except wikipedia.DisambiguationError as e:
                summaries.append(f"Disambiguation error: {e.options}")
            except wikipedia.PageError:
                pass
        
        return summaries
    except Exception as e:
        return [str(e)]
    
if __name__ == "__main__":
    query = input("Enter your search query: ")
    results = search_wikipedia(query)
    for i, summary in enumerate(results):
        print(f"Result {i+1}:\n{summary}\n")