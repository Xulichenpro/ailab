from langchain_text_splitters import SpacyTextSplitter
from modelscope.models import Model
from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
import numpy as np
import faiss


# This is a long document we can split up.
with open("speech.txt", encoding="utf-8") as f:
    speech = f.read()

text_splitter = SpacyTextSplitter(chunk_size=50,chunk_overlap=0)

texts = text_splitter.split_text(speech)

for i in range(len(texts)):
    print(f"=== Chunk {i} ===")
    print(texts[i])

model_id = "iic/nlp_gte_sentence-embedding_english-small"
pipe = pipeline(Tasks.sentence_embedding,
              model = model_id,
              sequence_length = 512,
              model_revision = "master")

inputs = {
    "source_sentence":texts
}

que = "It is altogether fitting and proper that we should do this."
input_query = {
    "source_sentence":[que]
}
result = pipe(input = inputs)
query_result = pipe(input = input_query)
query_vector = np.array(query_result["text_embedding"]).astype("float32")

# print(result["text_embedding"])
vectors = result["text_embedding"]

d = 384
db_vectors = np.array(vectors).astype("float32")
index = faiss.IndexFlatL2(d)

index.add(db_vectors)

print("索引中的向量数量 (添加后):", index.ntotal)

k = 1
distances, indices = index.search(query_vector, k)

print("\n-------------------- 搜索结果 --------------------")
print("最相似的向量在原始数据中的索引 (indices):")
print(indices)
print("对应的距离 (distances):")
print(distances)

# 5. 可选：获取对应的原始向量
# 第一个查询向量最相似的 5 个向量的索引是 indices[0]
for i in indices[0]:
    print(f"索引 {i} 对应的向量: \n{db_vectors[i]}, 对应文本: \n{texts[i]}\n")