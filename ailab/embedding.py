from modelscope.models import Model
from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks

def sentence_embedding(source_sentence:list,sentences_to_compare:list = []) -> dict:
    model_id = "iic/nlp_gte_sentence-embedding_english-small"
    pipe = pipeline(Tasks.sentence_embedding,
                model = model_id,
                sequence_length = 512,
                model_revision = "master")

    inputs = {
        "source_sentence":source_sentence,
        "sentences_to_compare":sentences_to_compare
    }

    result = pipe(input = inputs)
    return result