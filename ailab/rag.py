from search_wiki import search_wikipedia
from embedding import sentence_embedding
from vector_store import vectorstore
from chat import chat_qwen
import numpy as np

class RAG:
    def __init__(self,query:str):
        self.query = query
        self.context = self.retrieve_context(query)

    def retrieve_context(self,query:str) -> str:
        search_results = search_wikipedia(query)
        if not search_results:
            return "No relevant information found."
        db_vectors = np.array(sentence_embedding(search_results,[])["text_embedding"])
        query_vector = np.array(sentence_embedding([query],[])["text_embedding"])

        vs = vectorstore(db_vectors)
        distances = vs.query(query_vector, k=5)
        context = [search_results[idx] for dist, idx in distances]
        return "\n".join(context)
    
    def prompt(self) -> str:
        prompt = f"根据以下内容和你的知识储备回答问题:\n{self.context}\n问题是:{self.query}\n你的答案是"
        print(prompt)
        return prompt
    
    def answer(self) -> str:
        prompt = self.prompt()
        response = chat_qwen(prompt)
        return response
    
if __name__ == "__main__":
    query = input("请输入你的问题:")
    rag = RAG(query)
    answer = rag.answer()
    print(f"回答是:{answer}")


    
    