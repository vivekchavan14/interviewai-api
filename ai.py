from vertexai.preview.language_models import ChatModel, ChatSession, ChatMessage

bison_model = ChatModel.from_pretrained("chat-bison@001")

def palm(message: str, context: str, history: list):
    valid_history = [ChatMessage(h["content"], h['author']) for h in history if "content" in h and "author" in h]
    chat = ChatSession(model=bison_model, context=context, message_history=valid_history, temperature=0.94)
    response = chat.send_message(message)
    return response
