from chat import chat_qwen as chat
from datasets import load_dataset
dataset=load_dataset(r"ceval/ceval-exam",name="computer_network")

def test_model(N = 5):
    cnt = 0
    for i in range(N):
        questions = dataset['test'][i]['question']
        n = len(questions)
        question = "计算各个选项的正确的概率,返回只包含一个字母,即正确概率最高的选项\n"
        for j in range(n):
            question += questions[j]
        answer = dataset['test'][i]['answer']
        response = chat(question)
        if answer[0] == response[2]:
            cnt += 1
        print(len(response),response[2])
        print(f"answer:{answer}\nresponse:{response}\n")
    return cnt / N
if __name__ == "__main__":
    zero_shot = test_model(50)
    print(f"zero shot accuracy:{zero_shot}")