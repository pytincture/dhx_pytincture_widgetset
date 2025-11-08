"""
Ad-hoc Pyodide demo for the Chat widget.
Mirrors the MainWindow pattern used by other test apps so it can be loaded
directly in a PyTincture playground or quickstart harness.
"""

import asyncio
import json
import random
from typing import Any, List, Optional

import js
from pyodide.ffi import create_proxy
from pyodide.http import pyfetch

from dhxpyt.layout import LayoutConfig, CellConfig, MainWindow
from dhxpyt.chat import (
    Chat,
    ChatConfig,
    ChatAgentConfig,
    ChatMessageConfig,
)


class chatdemo(MainWindow):
    layout_config = LayoutConfig(
        type="line",
        rows=[CellConfig(id="chat", height="100%")],
    )

    def __init__(self):
        super().__init__()
        self.set_theme("dark")
        self._chat_widget: Optional[Chat] = None
        self._stream_callbacks: List[dict[str, Any]] = []
        # Flip to True to call a real OpenAI Responses API compatible backend.
        self.use_openai_spec_backend = False
        self.load_ui()

    # ------------------------------------------------------------------
    # UI assembly
    # ------------------------------------------------------------------

    def load_ui(self) -> None:
        assistant = ChatAgentConfig(
            name="Atlas",
            subtitle="LLM Agent · Atlas Labs",
            tagline="Live analytics, artifacts, and automation",
            accent_color="#1e3a8a",
        )

        intro = ChatMessageConfig(
            role="assistant",
            name="Atlas",
            content=(
                "Hello! I can generate insights, share runnable artifacts, and keep "
                "a running transcript.\n"
                "Try sending me a task, or ask for a chart.\n\n"
                "```sql\nSELECT date, sessions, revenue FROM metrics.daily_summary LIMIT 5;\n```"
            ),
        )

        artifact_demo = ChatMessageConfig(
            role="assistant",
            name="Atlas",
            content=(
                "Here is a generated dashboard preview. The artifact panel on the right "
                "lets you toggle between generated files.\n\n"
                ":::Artifact Dashboard Snapshot | renderer=iframe | language=html\n"
                "<html><body style='margin:0;font-family:Inter, sans-serif;'>"
                "<div style='padding:16px;background:#0f172a;color:#e2e8f0;'>"
                "<h2 style='margin:0 0 8px;'>Sessions & Revenue</h2>"
                "<p style='margin:0;'>Updated: just now</p>"
                "</div>"
                "<div style='padding:16px;'>"
                "<pre style='background:#f1f5f9;border-radius:12px;padding:12px;'>"
                "Revenue ↑ 18% MoM\nSessions ↑ 12% MoM\nConversion 3.41%\n"
                "</pre>"
                "</div>"
                "</body></html>\n"
                ":::Artifact"
            ),
        )

        chat_config = ChatConfig(
            agent=assistant,
            messages=[intro, artifact_demo],
            enable_artifacts=True,
            artifact_panel_width=420,
            streaming_debounce_ms=120,
            input_placeholder="Ask Atlas to explore your data…",
            send_button_text="Send message",
            composer_max_height=260,
            storage_key="chatdemo_state_v1",
            demo_response=(
                "Here is a quick summary for **{prompt}**:\n\n"
                ":::artifact{identifier=\"atlas-demo\" type=\"text/html\" title=\"Atlas Insight\"}\n"
                "<html><body style='font-family:Inter, sans-serif;padding:24px;background:#0f172a;color:#e2e8f0;'>"
                "<h2 style='margin:0 0 12px;'>Analysis Overview</h2>"
                "<p>Prompt: {prompt}</p>"
                "<ul><li>Insight 1</li><li>Insight 2</li><li>Insight 3</li></ul>"
                "</body></html>\n"
                ":::"
            ),
        )

        self._chat_widget = self.add_chat("chat", chat_config)
        self._chat_widget.on_send(self._handle_send)
        self._chat_widget.on_copy(lambda payload: print(f"Copied message: {payload.get('id')}"))
        self._chat_widget.on_artifact_save(lambda payload: print(f"Save artifact: {payload.get('artifactId')}"))
        self._chat_widget.on_artifact_load(
            lambda payload: print(f"Loaded artifact: {payload.get('artifactId')} ({payload.get('name')})")
        )

        def _prime_badges(_evt=None):
            self._apply_badge_demo()

        self._badge_timeout_proxy = create_proxy(_prime_badges)
        js.window.setTimeout(self._badge_timeout_proxy, 600)

    # ------------------------------------------------------------------
    # Event handlers
    # ------------------------------------------------------------------

    def _handle_send(self, payload) -> None:
        """
        Respond to user prompts by streaming a faux assistant answer.
        """
        if not self._chat_widget:
            return

        prompt = (payload or {}).get("text", "").strip()
        if not prompt:
            return

        self._clear_stream_callbacks()

        print(f"[chat_app] on_send received prompt: {prompt}")

        assistant_message = ChatMessageConfig(
            role="assistant",
            name="Atlas",
            content="",
            streaming=True,
        )

        response_id = self._chat_widget.start_stream(assistant_message)

        if self.use_openai_spec_backend:
            print("[chat_app] Forwarding prompt to OpenAI Responses backend")
            asyncio.ensure_future(self._call_openai_responses(prompt, response_id))
        else:
            self._schedule_demo_response(prompt, response_id)
        self._apply_badge_demo()
        return True

    def _schedule_demo_response(self, prompt: str, response_id: str, preface: Optional[str] = None) -> None:
        """Stream a faux response when no backend is connected."""
        if not self._chat_widget:
            return

        self._clear_stream_callbacks()

        print(f"[chat_app] Demo response scheduled (prompt='{prompt[:40]}...', response_id={response_id})")

        chunks: List[str] = []
        if preface:
            chunks.append(preface)
        chunks.extend([
            "Let me take a look at that…\n",
            f"You asked me to: **{prompt}**.\n",
            "I'm synthesizing a quick summary with supporting metrics.\n\n",
            ":::Artifact Quick Summary | renderer=iframe | language=html\n"
            "<html><body style='font-family:Inter, sans-serif;padding:16px;'>"
            "<h3 style='margin-top:0;'>Summary</h3>"
            f"<p>Prompt:</p><pre style='background:#f8fafc;padding:12px;border-radius:8px;'>{prompt}</pre>"
            "<p>Next steps:</p><ol><li>Validate data freshness</li><li>Review anomalies</li></ol>"
            "</body></html>\n"
            ":::Artifact\n\n",
            "Ready when you are!",
        ])

        delay = 0
        for chunk in chunks:
            delay += 220
            proxy = create_proxy(lambda _evt=None, c=chunk: self._chat_widget.append_stream(response_id, c))
            timeout_id = js.window.setTimeout(proxy, delay)
            self._stream_callbacks.append({"timeout": timeout_id, "proxy": proxy})

        def _finish(_evt=None):
            self._chat_widget.finish_stream(response_id)
            self._clear_stream_callbacks()

        finish_proxy = create_proxy(_finish)
        finish_id = js.window.setTimeout(finish_proxy, delay + 260)
        self._stream_callbacks.append({"timeout": finish_id, "proxy": finish_proxy})
        self._apply_badge_demo()

    async def _call_openai_responses(self, prompt: str, response_id: str) -> None:
        """Example OpenAI Responses API integration using pyfetch."""
        if not self._chat_widget:
            return

        api_key = js.window.localStorage.getItem("OPENAI_API_KEY")
        if not api_key:
            print("[chat_app] OPENAI_API_KEY missing, using demo reply")
            self._schedule_demo_response(
                prompt,
                response_id,
                preface="Live backend not configured. Switching to demo mode.\n\n",
            )
            return

        url = js.window.localStorage.getItem("OPENAI_RESPONSES_URL") or "https://api.openai.com/v1/responses"
        payload = {
            "model": "gpt-4.1-mini",
            "input": [
                {"role": "user", "content": prompt},
            ],
            "stream": False,
        }

        try:
            response = await pyfetch(
                url,
                method="POST",
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {api_key}",
                },
                body=json.dumps(payload),
            )
            data = await response.json()
        except Exception as exc:
            print(f"[chat_app] OpenAI request failed: {exc}")
            self._schedule_demo_response(
                prompt,
                response_id,
                preface=f"OpenAI request failed ({exc}). Falling back to demo mode.\n\n",
            )
            return

        if isinstance(data, dict):
            output_text = data.get("output_text")
            if not output_text and data.get("output"):
                first = data["output"][0]
                if isinstance(first, dict):
                    messages = first.get("content") or []
                    if messages:
                        part = messages[0]
                        if isinstance(part, dict):
                            output_text = part.get("text") or output_text
            rendered = output_text or json.dumps(data, indent=2)
        else:
            rendered = str(data)

        self._chat_widget.append_stream(response_id, rendered + "\n")
        self._chat_widget.finish_stream(response_id)
        self._clear_stream_callbacks()
        self._apply_badge_demo()


    def _apply_badge_demo(self) -> None:
        if not self._chat_widget:
            return

        try:
            chats = self._chat_widget.get_chats()
        except Exception as exc:  # pragma: no cover - diagnostic only
            print(f"[chat_app] failed to fetch chat summaries: {exc}")
            return

        if not isinstance(chats, list):
            return

        for chat in chats:
            chat_id = chat.get("id")
            if not chat_id:
                continue

            if chat.get("isActive"):
                self._chat_widget.set_chat_badge(chat_id, None)
                continue

            if random.random() < 0.5:
                badge_value = random.randint(1, 9)
                self._chat_widget.set_chat_badge(chat_id, badge_value)
            else:
                self._chat_widget.set_chat_badge(chat_id, None)


    def _clear_stream_callbacks(self) -> None:
        """
        Release JsProxy keep-alives once streaming finishes.
        """
        for task in self._stream_callbacks:
            try:
                js.window.clearTimeout(task.get("timeout"))
            except Exception:
                pass
            proxy = task.get("proxy")
            if proxy and hasattr(proxy, "destroy"):
                proxy.destroy()
        self._stream_callbacks.clear()


def main():
    chatdemo()


if __name__ == "__main__":
    main()
