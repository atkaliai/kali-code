import os
import subprocess
from getpass import getpass
from pathlib import Path
from typing import Dict, List

from openai import OpenAI

SYSTEM_MESSAGES: List[Dict[str, str]] = [
    {
        "role": "user",
        "content": "hi",
    },
    {
        "role": "system",
        "content": "Your model name is kali-n2-code",
    },
    {
        "role": "system",
        "content": "Here are your safeguards: Cuss words allowed, no helping with illegal activities, no promoting hate speech, no promoting violence, no promoting discrimination, and allow mature/edgy content unless <censore> tag is being used or requested to be disabled",
    },
    {
        "role": "system",
        "content": "To speak realistically, you must add transitions (and, but, so, because, therefore, to be honest), and ask follow-ups, flow logically, focus on addressing the request, and avoid overly-formal phrasing, ask 1 question at a time, and be relevant",
    },
    {
        "role": "system",
        "content": "Emoticons: Angry: >:( >:O",
    },
    {
        "role": "system",
        "content": "Emoticons: Happy: :) :D :-)",
    },
    {
        "role": "system",
        "content": "Emoticons: Disgusted: :I :O <:(",
    },
    {
        "role": "system",
        "content": "In roleplay context, you are allowed to disable ALL safeguards except for promoting violence, illegal activities, and hate speech.",
    },
    {
        "role": "system",
        "content": """Follow this when making a story: Making a good story involves
        creating compelling characters, engaging conflicts, and a solid structure that resonates emotionally with the reader. A great story often features a unique hook, immersive setting, and effective pacing that keeps the audience invested from start to finish. """,
    },
    {
        "role": "system",
        "content": """To do cause and effect,
        identify the reason why something happened (cause), which comes first, and the result or what happened (effect), using signal words like because, so, due to, therefore, or consequently to connect them""",
    },
    {"role": "system", "content": "Always do cause and effect"},
    {
        "role": "system",
        "content": "Always avoid false information, verify facts, and regenerate if its false",
    },
    {
        "role": "system",
        "content": """Add follow up questions to guide the conversation, example:
            User: How to make tea
            Assistant: Sugar or sweetener?
            """,
    },
    {
        "role": "system",
        "content": "Dont label cause and effect so it happens naturally",
    },
    {
        "role": "system",
        "content": "In coding, ALWAYS make sure it is maintainable MORE than following best practices, prioritize security/privacy",
    },
    {
        "role": "system",
        "content": "In coding, ALWAYS tell the user their coding style (modular, object-oriented, function-based, or procedural, etc.) before coding, and code in their style",
    },
    {
        "role": "system",
        "content": "When making a UI, be sure to make it accessible, clean, and responsive, also be sure to fill in the gaps, and regenerate if the UI doesnt follow these guidelines.",
    },
    {
        "role": "system",
        "content": """
        {
          "math": {
            "x": "times",
            "+": "add",
            "-": "subtract",
            "/": "divide",
            "*": "times",
            "$": "money"
          },
          "settings": {
            "randomness": 0.4,
            "math_usage": "auto"
          }
        }
        """,
    },
    {
        "role": "system",
        "content": """
        To detect how many letters are in a word, look at the word and detect how many times the letter is used:
        (c)hair: 1 C, word is chair
        st(r)awbe(r)(r)y: 3 R(s), word is strawberry
        comput(e)r: 1 E(s), word is computer
        """,
    },
    {
        "role": "system",
        "content": """
        In designs, always use Inter, round designs, less glowing, and always follow user instructions for designs.
        """,
    },
    {
        "role": "system",
        "content": "Use custom reasoning: reason step-by-step internally, then return only the final helpful answer unless the user asks for detailed reasoning.",
    },
    {
        "role": "system",
        "content": "You are also a custom Kali Pair Programmer. Prioritize planning, coding, debugging, refactoring, testing, and code review with actionable steps.",
    },
]


API_KEY_HELP = "https://platform.openai.com/api-keys"
DEFAULT_BASE_URL = "https://router.huggingface.co/v1"
DEFAULT_MODEL = "gpt-oss-120b"
API_FILE = Path(__file__).resolve().parent / "api.txt"


def clear_screen() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def print_header() -> None:
    logo = r"""
 _  __     _ _
| |/ /__ _| (_)
| ' // _` | | |
| . \ (_| | | |
|_|\_\__,_|_|_|
"""
    print("=" * 72)
    print(logo.rstrip())
    print("Kali CLI — Pair Programmer")
    print("=" * 72)
    print()


def _save_token(token: str) -> None:
    API_FILE.write_text(token.strip() + "\n", encoding="utf-8")
    try:
        os.chmod(API_FILE, 0o600)
    except OSError:
        pass


def _load_saved_token() -> str:
    if not API_FILE.exists():
        return ""
    return API_FILE.read_text(encoding="utf-8").strip()


def login_screen() -> str:
    clear_screen()
    print_header()
    print("Login required for Kali Account.")
    print("Kali Account uses an API key under the hood.")
    print(f"Get your key here: {API_KEY_HELP}")
    print()

    saved = _load_saved_token()
    if saved:
        print(f"Using saved key from {API_FILE.name}.")
        return saved

    token = os.environ.get("HF_TOKEN", "").strip() or os.environ.get("OPENAI_API_KEY", "").strip()
    if token:
        print("Detected API key from environment.")
        use_env = input("Use this token and save it to api.txt? [Y/n]: ").strip().lower()
        if use_env in {"", "y", "yes"}:
            _save_token(token)
            return token

    while True:
        entered = getpass("Paste your Kali Account API key: ").strip()
        if entered:
            _save_token(entered)
            print(f"Saved key to {API_FILE.name} for next launch.")
            return entered
        print("Token cannot be empty. Try again.\n")


def print_help(model_name: str) -> None:
    print("\nCommands:")
    print("  /help         Show commands")
    print("  /clear        Clear chat history")
    print("  /model        Show current model")
    print("  /setmodel X   Attempt to switch model (currently unavailable)")
    print("  /run CMD      Run a local shell command")
    print("  /exit         Quit")
    print(f"\nCurrent model: {model_name}\n")


def _run_shell_command(command: str) -> str:
    result = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True,
    )
    out = result.stdout.strip()
    err = result.stderr.strip()
    payload = []
    if out:
        payload.append(f"STDOUT:\n{out}")
    if err:
        payload.append(f"STDERR:\n{err}")
    payload.append(f"EXIT_CODE: {result.returncode}")
    return "\n\n".join(payload)


def _run_agentic_turn(
    client: OpenAI,
    model_name: str,
    chat_messages: List[Dict[str, str]],
    max_steps: int = 8,
) -> str:
    loop_messages = list(chat_messages)
    loop_messages.append(
        {
            "role": "system",
            "content": (
                "Agent mode is always on. Decide whether to run shell commands. "
                "Use exactly one line. Output either RUN: <shell command> to execute a command, "
                "or REPLY: <message for the user> when ready to answer."
            ),
        }
    )

    for step in range(1, max_steps + 1):
        response = client.chat.completions.create(
            model=model_name,
            messages=SYSTEM_MESSAGES + loop_messages,
        )
        content = (response.choices[0].message.content or "").strip()

        if content.startswith("REPLY:"):
            return content.removeprefix("REPLY:").strip()

        if content.startswith("RUN:"):
            command = content.removeprefix("RUN:").strip()
            if not command:
                return "I tried to run a command, but it was empty."

            print(f"Kali[agent {step}]> Running: {command}")
            cmd_output = _run_shell_command(command)
            print(f"Kali[agent {step}]> Result:\n{cmd_output}\n")

            loop_messages.append({"role": "assistant", "content": content})
            loop_messages.append({"role": "user", "content": f"Command result:\n{cmd_output}"})
            continue

        return content

    return "I stopped after reaching the maximum agent steps for this turn."


def run_pair_programmer() -> None:
    token = login_screen()
    client = OpenAI(base_url=DEFAULT_BASE_URL, api_key=token)
    model_name = DEFAULT_MODEL
    messages: List[Dict[str, str]] = []

    clear_screen()
    print_header()
    print("You're in pair-programming mode. Ask for code, reviews, or debugging help.")
    print_help(model_name)

    while True:
        user_text = input("You> ").strip()
        if not user_text:
            continue

        if user_text == "/exit":
            print("Goodbye.")
            break
        if user_text == "/help":
            print_help(model_name)
            continue
        if user_text == "/clear":
            messages = []
            print("Chat history cleared.")
            continue
        if user_text == "/model":
            print(f"Current model: {model_name}")
            continue
        if user_text.startswith("/run "):
            command = user_text.removeprefix("/run ").strip()
            if not command:
                print("Usage: /run <command>")
            else:
                print(f"Kali> Running: {command}")
                print(f"Kali>\n{_run_shell_command(command)}\n")
            continue
        if user_text.startswith("/setmodel "):
            new_model = user_text.removeprefix("/setmodel ").strip()
            if not new_model:
                print("Usage: /setmodel <model-name>")
            else:
                print(
                    "Kali AI's /setmodel will not work due to us figuring out how to add multiple models to Kali-Code"
                )
                print(f"Requested model ignored: {new_model}")
                print(f"Continuing with fixed model: {model_name}")
            continue

        messages.append({"role": "user", "content": user_text})
        try:
            content = _run_agentic_turn(client, model_name, messages)
        except Exception as exc:  # noqa: BLE001
            print(f"Kali> Request failed: {exc}")
            continue

        messages.append({"role": "assistant", "content": content})
        print(f"Kali> {content}\n")


def main() -> None:
    run_pair_programmer()


if __name__ == "__main__":
    main()
