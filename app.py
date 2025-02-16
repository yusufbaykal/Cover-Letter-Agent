from smolagents import CodeAgent, HfApiModel
import yaml
from tools.final_answer import FinalAnswerTool
from tools.web_search import DuckDuckGoSearchTool
from tools.extract_text_from_pdf import ExtractTextFromPdfTool
from Gradio_UI import GradioUI
import os

extract_text_from_pdf = ExtractTextFromPdfTool()
final_answer = FinalAnswerTool()

model = HfApiModel(
    max_tokens=4096,
    temperature=0.7,
    model_id='Qwen/Qwen2.5-Coder-32B-Instruct',
    custom_role_conversions=None,
    token=""
)

with open("prompts.yaml", 'r') as stream:
    prompt_templates = yaml.safe_load(stream)

agent = CodeAgent(
    model=model,
    tools=[
        final_answer,
        extract_text_from_pdf,
        DuckDuckGoSearchTool(),
    ],
    max_steps=4,
    verbosity_level=1,
    prompt_templates=prompt_templates,
    additional_authorized_imports=['PyPDF2', 'requests', 'yaml', 'bs4']
)

ui = GradioUI(agent, file_upload_folder="uploads")
if not os.path.exists("uploads"):
    os.makedirs("uploads")
ui.launch()