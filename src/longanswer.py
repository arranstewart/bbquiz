from mako.template import Template
from renderer import template_filename
import question

class LongAnswer(question.Question):
    """
    Long-answer ("essay") question.

    .question longanswer
        .text Question text
    """

    def __init__(self):
        super().__init__()
        self.text = None

    def parse2(self, parser, cmd, arg):
        if cmd == 'text':
            self.text = arg
        else:
            parser._raise("Expecting 'text'")

        while True:
            line = parser.next_interesting_line()
            if line is None:
                break
            command, arg = parser.parse_command(line)
            if command == 'question' or command == 'pool':
                parser.putback = line
                break
            elif command == 'text':
                parser._raise("More than one 'text' for same question.")
            else:
                parser._raise("Unexpected command.")
        if self.text is None:
            parser._raise("Question without 'text'.")
        return self

    def render(self, qn, idgen, renderer):
        assert self.text is not None, "Long answer question with no question text"
        self.rendered = renderer.render_text(self.text)
        template = Template(filename = template_filename("longanswer"))
        fragment = template.render(
            question=self,
            title = qn,
            id = idgen()
        )
        return fragment

    def display(self, fmt):
        return f"""
<h3 class="doc">Long answer ("essay") question ({self.config['points']} points)</h3>
<div class="stem">{fmt(self.text)}</div>
<div class="note">{self.note}</div>
"""
