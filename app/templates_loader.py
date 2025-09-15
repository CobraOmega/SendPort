from jinja2 import Environment, FileSystemLoader, select_autoescape
import os 

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "..", "templates")
env = Environment(loader=FileSystemLoader(TEMPLATE_DIR), autoescape=select_autoescape(["html", "xml"]))

def render_template(template_name: str, context: dict) -> str:
    tmpl = env.get_template(template_name)
    return tmpl.render(**context)