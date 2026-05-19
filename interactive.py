import os
import threading
import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk

from openai import OpenAI

SYSTEM_MESSAGES = [
    {
        "role": "user",
        "content": "hi",
    },
    {
        "role": "system",
        "content": "Your model name is kali-n2",
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
        """
    },
    {
        "role": "system",
        "content": """
        To detect how many letters are in a word, look at the word and detect how many times the letter is used:
        (c)hair: 1 C, word is chair
        st(r)awbe(r)(r)y: 3 R(s), word is strawberry
        comput(e)r: 1 E(s), word is computer
        """
    },
    {
        "role": "system",
        "content": """
        In designs, always use Inter, round designs, less glowing, and always follow user instructions for designs.
        """
    }
]


class ChatApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("kali-n2 chat")
        self.root.geometry("900x640")
        self.root.minsize(720, 520)

        self.client = OpenAI(
            base_url="https://router.huggingface.co/v1",
            api_key=os.environ.get("HF_TOKEN", ""),
        )

        self.messages = []
        self._build_ui()

        if not os.environ.get("HF_TOKEN"):
            messagebox.showwarning(
                "Missing HF_TOKEN",
                "Set HF_TOKEN in your environment before sending messages.",
            )

    def _build_ui(self) -> None:
        container = ttk.Frame(self.root, padding=12)
        container.pack(fill=tk.BOTH, expand=True)

        self.chat_log = scrolledtext.ScrolledText(
            container,
            wrap=tk.WORD,
            state=tk.DISABLED,
            font=("Helvetica", 12),
            height=22,
        )
        self.chat_log.pack(fill=tk.BOTH, expand=True)

        input_frame = ttk.Frame(container)
        input_frame.pack(fill=tk.X, pady=(10, 0))

        self.input_text = tk.Text(input_frame, height=4, font=("Helvetica", 12))
        self.input_text.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.input_text.bind("<Return>", self._on_enter)
        self.input_text.bind("<Shift-Return>", self._on_shift_enter)

        controls = ttk.Frame(input_frame)
        controls.pack(side=tk.RIGHT, padx=(10, 0), fill=tk.Y)

        self.send_button = ttk.Button(controls, text="Send", command=self._send_message)
        self.send_button.pack(fill=tk.X, pady=(0, 6))

        self.clear_button = ttk.Button(controls, text="Clear", command=self._clear_chat)
        self.clear_button.pack(fill=tk.X)

        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(container, textvariable=self.status_var, anchor=tk.W)
        status_bar.pack(fill=tk.X, pady=(10, 0))

    def _on_enter(self, event: tk.Event) -> str:
        self._send_message()
        return "break"

    def _on_shift_enter(self, event: tk.Event) -> str:
        self.input_text.insert(tk.INSERT, "\n")
        return "break"

    def _set_status(self, text: str) -> None:
        self.status_var.set(text)

    def _append_chat(self, speaker: str, text: str) -> None:
        self.chat_log.configure(state=tk.NORMAL)
        self.chat_log.insert(tk.END, f"{speaker}: {text.strip()}\n\n")
        self.chat_log.configure(state=tk.DISABLED)
        self.chat_log.see(tk.END)

    def _clear_chat(self) -> None:
        self.messages = []
        self.chat_log.configure(state=tk.NORMAL)
        self.chat_log.delete("1.0", tk.END)
        self.chat_log.configure(state=tk.DISABLED)
        self._set_status("Cleared")

    def _send_message(self) -> None:
        user_text = self.input_text.get("1.0", tk.END).strip()
        if not user_text:
            return

        if not os.environ.get("HF_TOKEN"):
            messagebox.showerror(
                "Missing HF_TOKEN",
                "Set HF_TOKEN in your environment before sending messages.",
            )
            return

        self.input_text.delete("1.0", tk.END)
        self._append_chat("You", user_text)
        self.messages.append({"role": "user", "content": user_text})

        self.send_button.configure(state=tk.DISABLED)
        self._set_status("Thinking...")

        thread = threading.Thread(target=self._fetch_response, daemon=True)
        thread.start()

    def _fetch_response(self) -> None:
        try:
            response = self.client.chat.completions.create(
                model="openai/gpt-oss-120b",
                messages=SYSTEM_MESSAGES + self.messages,
            )
            content = response.choices[0].message.content or ""
        except Exception as exc:  # noqa: BLE001
            self.root.after(0, self._handle_error, exc)
            return

        self.messages.append({"role": "assistant", "content": content})
        self.root.after(0, self._handle_response, content)

    def _handle_response(self, content: str) -> None:
        self._append_chat("kali-n1", content)
        self.send_button.configure(state=tk.NORMAL)
        self._set_status("Ready")

    def _handle_error(self, exc: Exception) -> None:
        self.send_button.configure(state=tk.NORMAL)
        self._set_status("Error")
        messagebox.showerror("Request failed", str(exc))


def main() -> None:
    root = tk.Tk()
    ttk.Style().theme_use("clam")
    ChatApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
