from chat import chat_qwen
import gradio as gr

def chat_ui():
    demo = gr.Interface(fn = chat_qwen,
                        inputs = gr.Textbox(lines = 3,label = "Question"),
                        outputs = gr.Textbox(lines = 10, label = "Response"),
                        title = "Chat with Qwen")
    demo.launch()

if __name__ == "__main__":
    chat_ui()