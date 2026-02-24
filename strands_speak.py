import os
import logging

from strands import Agent
from strands.models import BedrockModel
from strands_tools import calculator, file_read, file_write, speak
from datetime import datetime
from strands.tools import tool

model_id = BedrockModel (
    model_id = "us.amazon.nova-2-lite-v1:0"
)

@tool
def make_output_paths(test: bool = False) -> dict:
    """
    Generate output file paths for text summary and audio.

    Patterns:
      - test=True  -> text_ddMMHHmmss_test.txt, audio_ddMMHHmmss_test.mp3
      - test=False -> text_ddMMHHmmss.txt,      audio_ddMMHHmmss.mp3

    Args:
        test: whether to append '_test' suffix

    Returns:
        dict with 'text_path' and 'audio_path'
    """
    stamp = datetime.now().strftime("%d%m%H%M%S")
    suffix = "_test" if test else ""

    text_name = f"text_{stamp}{suffix}.txt"
    audio_name = f"audio_{stamp}{suffix}.mp3"

    return {
        "text_filename": text_name,
        "audio_filename": audio_name
    }

system_prompt = """
    You're a reading assistant with experience reading books and creating summaries of those.

    Use the tools as follows:

    - file_read to read files
    - file_write to write files
    - speak to read text as audio for the user
    - make_output_paths to generate file names (returns text_filename for txt files and audio_filename for mp3 audio files)
    """

agent = Agent(
    model=model_id,
    system_prompt=system_prompt,
    tools=[
        calculator,
        file_read,
        file_write,
        speak,
        make_output_paths
    ]
)

logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)s | %(name)s | %(message)s"
)
logging.getLogger("strands").setLevel(logging.DEBUG)

# DIRECT TOOLS CALL TEST
#agent.tool.speak(
#    text="Hi Diego, testing Polly from a Strands agent.",
#    mode="polly",
#    play_audio=False,
#    output_path="test.mp3",
#    voice_id="Salli"
#)

#result2 = agent.tool.calculator(expression="10000 * (1 + 0.07 * (18/12))")
#print("Calculator result #2:", result2)

agent("""
    Can you please summarize the contents of the Metamorphosis.txt in <= 100 words, save the summary in a file with a name that you create yourself and read it for me?

    Use the following params for the speak tool:
    - mode='polly'
    - play_audio=false
    - output_path=generate a path you create with the make_output_paths
    - voice_id='Salli'
    """)
