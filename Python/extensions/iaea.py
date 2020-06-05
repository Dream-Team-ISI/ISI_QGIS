from markdown.extensions import Extension
from markdown.inlinepatterns import SimpleTagPattern, InlineProcessor
import xml.etree.ElementTree as etree

DEL_RE = r'(--)(.*?)--'

class ISI_Report(Extension):
   def extendMarkdown(self, md):
       del_tag = SimpleTagPattern(DEL_RE, 'del')
       # Insert code here to change markdown's behavior.
       md.inlinePatterns.add('del', del_tag, '>not_strong')

class DelInlineProcessor(InlineProcessor):
    def handleMatch(self, m, data):
        el = etree.Element('i')
        el.set('style', 'delstyle')
        el.text = "<b>Analyst Comment: </b>" + m.group(1)
        return el, m.start(0), m.end(0)

class DelExtension(Extension):
    def extendMarkdown(self, md):
        DEL_PATTERN = r'--(.*?)--'  # like --del--
        md.inlinePatterns.register(DelInlineProcessor(DEL_PATTERN, md), 'del', 175)
