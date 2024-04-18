from mkdocs.plugins import BasePlugin
from mkdocs.config import config_options


class CustomFooterPlugin(BasePlugin):
    config_scheme = (
        ('link_url', config_options.Type(str, default='')),
        ('link_text', config_options.Type(str, default='')),
        ('link_style', config_options.Type(str, default='color: deeppink;'))
    )

    def on_page_content(self, html, page, config, **kwargs):
        link_html = f'<a href="{self.config["link_url"]}" style="{self.config["link_style"]}">{self.config["link_text"]}</a>'
        return html + f'<footer>{link_html}</footer>'