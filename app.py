from google import genai
import gradio as gr
import time
import os

client = genai.Client(api_key=os.environ.get("GEMMA_API_KEY"))

def get_tiny_step(task, history_text):
    prompt = f"""
    Task: "clean the house"
    Next tiny action: Put the dirty clothes from the floor into one basket.

    Task: "study for exam"
    Next tiny action: Open your textbook to page one of your topic.

    Task: "{task}"
    Steps already done: {history_text if history_text else "None yet"}
    Next tiny action:
    """
    for attempt in range(4):
        try:
            response = client.models.generate_content(
                model="gemma-4-26b-a4b-it",
                contents=prompt
            )
            return response.text
        except Exception as e:
            print(f"Attempt {attempt+1} error: {e}")
            time.sleep(5)
    return "The AI is a bit busy right now — please try again in a few seconds."

def start_task(task):
    if not task.strip():
        return gr.update(value="⚠️ Please type a task first.", visible=True), "", task, gr.update(visible=False), gr.update(value="", visible=False)
    step = get_tiny_step(task, "")
    return gr.update(value=f"✅  {step}", visible=True), step, task, gr.update(visible=True), gr.update(value="STEP 1", visible=True)

def next_step(task, history_text, step_count_text):
    step = get_tiny_step(task, history_text)
    updated_history = history_text + "\n" + step
    try:
        count = int(step_count_text.replace("STEP ", "")) + 1
    except:
        count = 2
    return gr.update(value=f"✅  {step}", visible=True), updated_history, task, gr.update(visible=True), gr.update(value=f"STEP {count}", visible=True)

def new_task():
    return "", gr.update(value="", visible=False), "", "", gr.update(visible=False), gr.update(value="", visible=False)

def show_loading():
    return gr.update(value="⏳ Thinking...", visible=True)

logo_html = """
<div style="display:flex; justify-content:center; margin-bottom:18px;">
  <svg width="90" height="90" viewBox="0 0 100 100">
    <defs>
      <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#fb923c"/>
        <stop offset="100%" stop-color="#f43f5e"/>
      </linearGradient>
      <filter id="glow">
        <feGaussianBlur stdDeviation="3" result="blur"/>
        <feMerge>
          <feMergeNode in="blur"/>
          <feMergeNode in="SourceGraphic"/>
        </feMerge>
      </filter>
    </defs>
    <circle cx="50" cy="50" r="46" fill="url(#grad1)" filter="url(#glow)"/>
    <path d="M28 60 L44 42 L56 52 L74 32" stroke="white" stroke-width="7" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
    <circle cx="74" cy="32" r="7" fill="white"/>
  </svg>
</div>
"""

custom_css = """
html, body {
    margin: 0 !important;
    padding: 0 !important;
    height: 100% !important;
    overflow-x: hidden !important;
}

/* Master alignment container to force everything dead center on all device widths */
.gradio-container {
    min-height: 100vh !important;
    width: 100% !important;
    max-width: 100% !important;
    margin: 0 !important;
    padding: 0 !important;
    display: flex !important;
    justify-content: center !important;
    align-items: center !important;
    font-family: 'Poppins', 'Segoe UI', sans-serif;

    background:
        radial-gradient(circle at 15% 20%, rgba(251, 146, 60, 0.22) 0%, transparent 45%),
        radial-gradient(circle at 85% 15%, rgba(244, 63, 94, 0.18) 0%, transparent 45%),
        radial-gradient(circle at 80% 80%, rgba(168, 85, 247, 0.15) 0%, transparent 50%),
        linear-gradient(160deg, #070913 0%, #0c0f1d 50%, #04050a 100%) !important;
}

/* The element container: zero background, zero boxes, items float naturally */
#content-wrap {
    width: min(92vw, 500px) !important;
    max-width: 500px !important;
    margin: 40px auto !important;
    display: flex !important;
    flex-direction: column !important;
    align-items: stretch !important;
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    backdrop-filter: none !important;
    overflow: visible !important;
    gap: 16px !important;
}

/* Fix structural auto-scrolling issues injected by Gradio layout engines */
#content-wrap > div {
    overflow: visible !important;
}

#title-md h1 {
    text-align: center;
    font-size: 3em;
    font-weight: 800;
    margin: 0 0 8px 0;
    background: linear-gradient(90deg, #fb923c, #f43f5e, #a855f7);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: -1.5px;
}
#subtitle-md {
    text-align: center;
    color: #cbd5e1 !important;
    margin: 0 0 24px 0;
    font-size: 1.1em;
    font-weight: 300;
    letter-spacing: 0.4px;
}
#field-label {
    text-align: center !important;
    color: #fb923c !important;
    font-weight: 600;
    font-size: 0.85em;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 4px;
}
#step-counter {
    text-align: center;
    color: #fb923c !important;
    font-weight: 700;
    font-size: 0.95em;
    margin: 16px 0 4px 0;
    letter-spacing: 3px;
}

.gradio-container label > span {
    display: none !important;
}

/* Inner box styling for Task Input fields */
.gradio-container input[type="text"], .gradio-container textarea {
    background: rgba(255, 255, 255, 0.04) !important;
    border: 1px solid rgba(251, 146, 60, 0.25) !important;
    border-radius: 14px !important;
    color: #f8fafc !important;
    font-size: 1.05em !important;
    font-weight: 300 !important;
    padding: 14px 16px !important;
    min-height: 50px !important;
    box-shadow: none !important;
    transition: all 0.25s ease;
}
.gradio-container input[type="text"]:focus, .gradio-container textarea:focus {
    border-color: #fb923c !important;
    background: rgba(255, 255, 255, 0.07) !important;
    outline: none !important;
}
textarea::placeholder, input::placeholder {
    color: #64748b !important;
    font-weight: 300 !important;
}

/* Stylized Inner box styling specifically handling the AI Step Output */
#step-output textarea {
    background: rgba(16, 185, 129, 0.06) !important;
    border: 1px solid rgba(52, 211, 153, 0.35) !important;
    border-radius: 16px !important;
    color: #d1fae5 !important;
    font-weight: 400 !important;
    text-align: center;
    padding: 18px !important;
    line-height: 1.6 !important;
}

button {
    border-radius: 30px !important;
    font-weight: 600 !important;
    font-size: 1em !important;
    padding: 14px 10px !important;
    min-height: 52px !important;
    border: none !important;
    cursor: pointer !important;
}

footer {display: none !important;}

@media (max-width: 480px) {
    #title-md h1 { font-size: 2.2em; }
    #subtitle-md { font-size: 0.95em; margin-bottom: 20px; }
    #content-wrap { padding: 10px !important; margin: 20px auto !important;}
}
"""

theme = gr.themes.Soft(
    primary_hue="orange",
    secondary_hue="slate",
    neutral_hue="slate",
    font=gr.themes.GoogleFont("Poppins")
)

with gr.Blocks(title="JustBegin", theme=theme, css=custom_css) as demo:
    with gr.Column(elem_id="content-wrap"):
        gr.HTML(logo_html)
        gr.Markdown("# JustBegin", elem_id="title-md")
        gr.Markdown("Turn any overwhelming task into one tiny, doable step.", elem_id="subtitle-md")

        gr.Markdown("What are you stuck on?", elem_id="field-label")
        task_box = gr.Textbox(
            placeholder="e.g. study for exam, clean the house...",
            lines=1,
            show_label=False
        )

        with gr.Row():
            start_btn = gr.Button("🚀  Get my first step", variant="primary")
            new_btn = gr.Button("🔄  New task")

        step_counter = gr.Markdown("", elem_id="step-counter", visible=False)

        output_box = gr.Textbox(
            interactive=False,
            elem_id="step-output",
            lines=2,
            visible=False,
            show_label=False
        )

        next_btn = gr.Button("✅  Done! Next step", visible=False)

    history_state = gr.State("")
    task_state = gr.State("")

    start_btn.click(show_loading, outputs=output_box).then(
        start_task,
        inputs=[task_box],
        outputs=[output_box, history_state, task_state, next_btn, step_counter]
    )

    next_btn.click(show_loading, outputs=output_box).then(
        next_step,
        inputs=[task_state, history_state, step_counter],
        outputs=[output_box, history_state, task_state, next_btn, step_counter]
    )

    new_btn.click(
        new_task,
        outputs=[task_box, output_box, history_state, task_state, next_btn, step_counter]
    )

demo.launch(share=True)
