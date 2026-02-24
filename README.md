# AWS Strands Tools Test

A small Python demo that uses **AWS Bedrock** and **Strands agents** to summarize text (e.g. Kafka's *Metamorphosis*) and generate spoken summaries via Amazon Polly. It showcases built-in and custom tools, direct tool calls for testing, and logging for debugging.

This demo was inspired in the YouTubeVideo from AWS Developers [Strands Tools: Building Custom AI Agents with Python
](https://www.youtube.com/watch?v=EGhIZCfOvG4)

---

## Brief Description

This repository demonstrates:

- **Strands agents** on AWS Bedrock (Nova model) with a reading-assistant system prompt.
- **Built-in tools** from `strands-agents-tools`: `calculator`, `file_read`, `file_write`, and `speak` (Polly).
- **User-defined tools**: `make_output_paths` for generating timestamped output filenames.
- **Workflow**: The agent reads a source file (e.g. *Metamorphosis*), writes a short summary to a text file, and uses the `speak` tool to produce an MP3. You can switch voices (e.g. `Salli`, `Lupe`) and languages as needed.

The original demo was created in **Spanish** using the **Lupe** Polly voice; the code can be adapted for other languages and voices.

---

## Copyright Notice — Source Texts

This project includes two plain-text versions of **Franz Kafka’s *Metamorphosis*** (*Die Verwandlung*):

| File             | Language | Notes                                                                 |
|------------------|----------|-----------------------------------------------------------------------|
| `Metamorphosis.txt` | English  | Translation by David Wyllie (Project Gutenberg EBook #5200).          |
| `Metamorfosis.txt`  | Spanish  | Spanish-language version of the same work.                            |

These files are used **only for local testing and demonstration** of the Strands agent (summarization and text-to-speech). **No copyright infringement is intended.** The English text is from the public domain / Project Gutenberg; the Spanish version is included for language-demo purposes. If you are the rights holder of any included material and object to its use here, please open an issue so it can be removed or replaced.

---

## Prerequisites

- **Python 3.10+**
- **AWS account** with access to:
  - Amazon Bedrock (model: `us.amazon.nova-2-lite-v1:0`)
  - Amazon Polly (for the `speak` tool)
- **AWS CLI** installed and configured with credentials that have the above permissions.

---

## Setup

### 1. Clone the repository

```bash
git clone <repository-url>
cd aws-strands-tools-test
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it:

- **Windows (PowerShell):**  
  `.\.venv\Scripts\Activate.ps1`
- **Windows (CMD):**  
  `.\.venv\Scripts\activate.bat`
- **Linux / macOS:**  
  `source .venv/bin/activate`

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure AWS credentials for the agents

The Strands agent and Bedrock/Polly calls use your **default AWS credentials**. Ensure the AWS CLI is configured:

```bash
aws configure
```

Provide:

- **AWS Access Key ID**
- **AWS Secret Access Key**
- **Default region** (e.g. `us-east-1`), which must support Bedrock and Polly.

Alternatively, set environment variables:

```bash
set AWS_ACCESS_KEY_ID=your_access_key
set AWS_SECRET_ACCESS_KEY=your_secret_key
set AWS_DEFAULT_REGION=us-east-1
```

(Use `export` instead of `set` on Linux/macOS.)

Ensure the IAM user/role has permissions for:

- `bedrock:InvokeModel` (for the Nova model)
- Polly permissions required by the `speak` tool (e.g. `polly:SynthesizeSpeech`).

---

## Tools

### Built-in tools (`strands-agents-tools`)

- **`calculator`** — Evaluate math expressions.
- **`file_read`** — Read file contents (e.g. `Metamorphosis.txt`, `Metamorfosis.txt`).
- **`file_write`** — Write text to files (e.g. summary output).
- **`speak`** — Synthesize speech with Amazon Polly (`mode='polly'`), optional playback, and configurable `output_path` and `voice_id` (e.g. `Salli`, `Lupe`).

### User-defined tool

- **`make_output_paths(test: bool = False)`** — Returns a dict with `text_filename` and `audio_filename` using a timestamp; if `test=True`, filenames get a `_test` suffix. Used so the agent can generate consistent output paths for summaries and audio.

The agent’s system prompt instructs it to use these tools in sequence: read source → write summary → generate paths → speak summary to audio.

---

## Running the agent

With the virtual environment active and AWS configured:

```bash
python strands_speak.py
```

The script will:

1. Use the agent to read `Metamorphosis.txt`.
2. Summarize it (e.g. ≤100 words).
3. Save the summary to a timestamped text file.
4. Call the `speak` tool with the requested parameters (e.g. `voice_id='Salli'`, `play_audio=False`) and save the MP3.

To use the **Spanish** file and **Lupe** voice, change the prompt in `strands_speak.py` to reference `Metamorfosis.txt` and set `voice_id='Lupe'`.

---

## Commented code: direct tool calls

For **testing and debugging**, the repo includes commented-out examples of calling tools **directly** (without going through the agent loop):

- **`speak`** — Direct Polly call with custom text, `output_path`, and `voice_id` (e.g. `Lupe`).
- **`calculator`** — Direct evaluation of an expression.

Uncomment the relevant block in `strands_speak.py` and comment out the `agent("""...""")` call if you want to run only the direct tool test.

---

## Logging and debugging

Logging is enabled to trace agent and tool behavior:

```python
logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)s | %(name)s | %(message)s"
)
logging.getLogger("strands").setLevel(logging.DEBUG)
```

This prints debug messages from the application and the `strands` logger so you can follow tool invocations, model requests, and errors.

---

## Project layout

```
aws-strands-tools-test/
├── README.md
├── requirements.txt          # boto3, strands-agents, strands-agents-tools
├── strands_speak.py         # Agent definition, tools, and demo prompt
├── Metamorphosis.txt        # Kafka, English (David Wyllie / Project Gutenberg)
└── Metamorfosis.txt         # Kafka, Spanish (demo only; see copyright notice)
```

---

## Other details

- **Model**: `us.amazon.nova-2-lite-v1:0` (Bedrock).
- **Voice**: Default in the main prompt is `Salli` (English). For the original Spanish demo, use **Lupe** and `Metamorfosis.txt`.
- **Output**: Summary and audio filenames are timestamped (and optionally suffixed with `_test` via `make_output_paths(test=True)`).

If you hit Bedrock or Polly permission errors, confirm your AWS region supports the chosen model and that your IAM credentials have the required Bedrock and Polly permissions.
