import locale
import os
import re
from shutil import copytree, copy2
from subprocess import run
from tempfile import TemporaryDirectory
from typing import Dict, Any

import jinja2
import roman
from num2words import num2words

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'templates')
TEX_MAIN = 'main.tex'


def amount_spelled(amount: float):
    return "\\textbf{{{}}} (słownie: \\textit{{{} złotych {:02}/100}})".format(
        locale.currency(amount, grouping=True).replace(' ', ' '),
        num2words(int(amount), lang='pl'),
        int((amount * 100) % 100))


def render_template(template_name: str, context: Dict[str, Any]):
    latex_jinja_env = jinja2.Environment(
        block_start_string=r'\BLOCK{',
        block_end_string='}',
        variable_start_string=r'\VAR{',
        variable_end_string='}',
        comment_start_string=r'\#{',
        comment_end_string='}',
        line_statement_prefix='%%',
        line_comment_prefix='%#',
        trim_blocks=True,
        autoescape=False,
        loader=jinja2.FileSystemLoader(TEMPLATE_DIR)
    )
    latex_jinja_globals = {
        'num2words': num2words,
        'int': int,
        'locale': locale,
        'roman': roman.toRoman,
        'amount_spelled': amount_spelled
    }
    template = latex_jinja_env.get_template(os.path.join(template_name, TEX_MAIN), globals=latex_jinja_globals)
    rendered = template.render(**context)
    return re.sub(r'(\s[oiwza]) ', r'\1 ', rendered)


def render_pdf(template_name: str, context: Dict[str, Any], out_pdf: str):
    with TemporaryDirectory() as tmp:
        copytree(os.path.join(TEMPLATE_DIR, template_name), tmp, dirs_exist_ok=True)
        with open(os.path.join(tmp, TEX_MAIN), 'w') as main_tex:
            rendered = render_template(template_name, context)
            main_tex.write(rendered)
        run(['lualatex', 'main.tex'], cwd=tmp)
        copy2(os.path.join(tmp, 'main.pdf'), out_pdf)
