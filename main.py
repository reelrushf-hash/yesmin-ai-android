import json
import threading
import urllib.request
import urllib.error
from urllib.parse import quote

from kivy.app import App
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window

Window.softinput_mode = "below_target"

MODEL = "gemini-2.5-flash"
API_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    + MODEL
    + ":generateContent"
)

class YesminAIApp(App):
    def build(self):
        self.title = "YESMIN AI"
        self.history = []

        root = BoxLayout(orientation="vertical", padding=dp(10), spacing=dp(8))

        header = Label(
            text="[b]YESMIN AI[/b]\\nYour AI assistant",
            markup=True, size_hint_y=None, height=dp(58),
            font_size="21sp"
        )
        root.add_widget(header)

        self.key_input = TextInput(
            hint_text="Paste Gemini API key here (kept only in this app session)",
            password=True, multiline=False, size_hint_y=None, height=dp(48)
        )
        root.add_widget(self.key_input)

        self.status = Label(
            text="Enter your API key, type a message, then tap Send.",
            size_hint_y=None, height=dp(36), font_size="12sp"
        )
        root.add_widget(self.status)

        self.scroll = ScrollView(do_scroll_x=False)
        self.chat = BoxLayout(
            orientation="vertical", size_hint_y=None,
            spacing=dp(8), padding=(dp(4), dp(4))
        )
        self.chat.bind(minimum_height=self.chat.setter("height"))
        self.scroll.add_widget(self.chat)
        root.add_widget(self.scroll)

        bottom = BoxLayout(size_hint_y=None, height=dp(54), spacing=dp(6))
        self.message_input = TextInput(
            hint_text="Write your message...", multiline=False
        )
        self.message_input.bind(on_text_validate=lambda *_: self.send_message())
        send_button = Button(text="Send", size_hint_x=None, width=dp(82))
        send_button.bind(on_release=lambda *_: self.send_message())
        bottom.add_widget(self.message_input)
        bottom.add_widget(send_button)
        root.add_widget(bottom)

        self.add_message("YESMIN AI", "Hello! Enter your Gemini API key above and ask me something.")
        return root

    def add_message(self, speaker, text):
        safe_text = str(text).strip()
        label = Label(
            text=f"[b]{speaker}:[/b] {safe_text}",
            markup=True, size_hint_y=None, halign="left", valign="top",
            text_size=(Window.width - dp(40), None)
        )
        label.bind(texture_size=lambda widget, size: setattr(widget, "height", size[1] + dp(14)))
        self.chat.add_widget(label)
        Clock.schedule_once(lambda *_: setattr(self.scroll, "scroll_y", 0), 0.1)

    def set_status(self, text):
        self.status.text = text

    def send_message(self):
        message = self.message_input.text.strip()
        key = self.key_input.text.strip()

        if not key:
            self.set_status("Please enter your Gemini API key first.")
            return
        if not message:
            return

        self.message_input.text = ""
        self.add_message("You", message)
        self.set_status("YESMIN AI is thinking...")
        threading.Thread(
            target=self.ask_gemini, args=(key, message), daemon=True
        ).start()

    def ask_gemini(self, key, message):
        try:
            contents = list(self.history)
            contents.append({"role": "user", "parts": [{"text": message}]})
            payload = {"contents": contents}
            request = urllib.request.Request(
                API_URL + "?key=" + quote(key, safe=""),
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urllib.request.urlopen(request, timeout=60) as response:
                result = json.loads(response.read().decode("utf-8"))

            answer = result["candidates"][0]["content"]["parts"][0]["text"]
            self.history.append({"role": "user", "parts": [{"text": message}]})
            self.history.append({"role": "model", "parts": [{"text": answer}]})
            Clock.schedule_once(lambda *_: self.add_message("YESMIN AI", answer))
            Clock.schedule_once(lambda *_: self.set_status("Ready"))
        except urllib.error.HTTPError as exc:
            try:
                detail = exc.read().decode("utf-8", errors="replace")
            except Exception:
                detail = str(exc)
            status_text = f"API error {exc.code}: check key, quota, or model."
            Clock.schedule_once(lambda *_: self.set_status(status_text))
            Clock.schedule_once(lambda *_: self.add_message("Error", detail[:900]))
        except Exception as exc:
            error_text = str(exc)
            Clock.schedule_once(lambda *_: self.set_status("Connection failed. Check internet and API key."))
            Clock.schedule_once(lambda *_: self.add_message("Error", error_text[:900]))

if __name__ == "__main__":
    YesminAIApp().run()
