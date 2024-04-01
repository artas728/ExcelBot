from asyncio import sleep
import panel as pn
from ai_handler import process_user_message
from api_handler import api_call

pn.extension()

def fake_handler(input):
    return input.split(" ")


async def callback(contents: str, user: str, instance: pn.chat.ChatInterface):
    # operation, message = await process_user_message(contents, instance.history)
    operation, message = fake_handler(contents)
    try:
        message = api_call(operation, message)
    except Exception as e:
        message = f"Operation failed. Error: {str(e)}"
    for char in message:
        await sleep(0.02)
        message += char
        yield message


chat_interface = pn.chat.ChatInterface(callback=callback)
chat_interface.send(
    "Enter a message in the TextInput below and receive an echo!",
    user="System",
    respond=False,
)
chat_interface.servable()