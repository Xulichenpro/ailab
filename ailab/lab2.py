from modelscope.models import Model
from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks

model_id = "iic/nlp_gte_sentence-embedding_english-small"
pipe = pipeline(Tasks.sentence_embedding,
              model = model_id,
              sequence_length = 512,
              model_revision = "master")

inputs = {
    "source_sentence":["Hello, my dog is cute"],
    "sentences_to_compare":["Hello, my dog is lovely","Hello, my cat is cute","Hello, my pet is adorable"]
}

result = pipe(input = inputs)
print(result)