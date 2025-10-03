import numpy as np
from langchain_text_splitters import SpacyTextSplitter
from embedding import sentence_embedding

class vectorstore:
    def __init__(self,vector:np.array):
        self.vector = vector
    
    def query(self,query_vector:np.array,k:int) -> list:
        n = len(self.vector)
        distances = []
        for i in range(n):
            dist = np.linalg.norm(self.vector[i] - query_vector)
            distances.append((dist, i))

        distances.sort()
        return distances[:k]

if __name__ == "__main__":
    with open("speech.txt", encoding="utf-8") as f:
        speech = f.read()

    text_splitter = SpacyTextSplitter(chunk_size=50,chunk_overlap=0)
    texts = text_splitter.split_text(speech)

    for i in range(len(texts)):
        print(f"=== Chunk {i} ===")
        print(texts[i])

    query = "It is altogether fitting and proper that we should do this."
    result = sentence_embedding(texts,[])
    db_vectors= np.array(result["text_embedding"]).astype("float32")
    query_result = sentence_embedding([query],[])
    query_vector = np.array(query_result["text_embedding"]).astype("float32")


    vs = vectorstore(db_vectors)
    k = 2
    res = vs.query(query_vector,k)
    print("\n-------------------- 搜索结果 --------------------")
    print("最相似的向量在原始数据中的索引 (indices) 及对应距离:")
    print(res)
    for dist, idx in res:
        print(f"Index: {idx}, Distance: {dist}, Text: {texts[idx]}")