import verses
import markdown_viewer
from random import choice
from subprocess import Popen, PIPE
from rich.segment import Segment
from textual.app import App, ComposeResult, events
from textual.containers import Container, Horizontal, VerticalScroll, ScrollableContainer
from textual.widget import Widget
from textual.scroll_view import ScrollView
from textual.geometry import Size
from textual.strip import Strip
from textual.widgets import (Header, Button, Label, TabbedContent, TabPane, Select, Static,
                             Tree, ListItem, ListView, MarkdownViewer)


class TabsContent(Static):
    def __init__(self, *children: Widget):
        super().__init__(*children)
        self.Bible_all_book_verses_label = None
        self.Bible_verses_label = None
        self.random_Bible_verse_label = None
        self.tabs = ("Вірші", "Теми", "Розбір")
        self.themes = verses.themes
        self.ids = verses.ids

    def compose(self) -> ComposeResult:
        with TabbedContent(*self.tabs):
            with TabPane("Вірші", id="verses"):
                yield MarkdownViewer(markdown_viewer.MARKDOWN, show_table_of_contents=True, id="markdown")

            with TabPane("Теми", id="themes"):
                yield Static("Теми\n")
                with Container():
                    with VerticalScroll(id="left_themes"):
                        n = 0
                        for k in self.themes.keys():
                            yield Button(k, id=f"{self.ids[n]} t", classes="button_themes")
                            n += 1
                self.Bible_verses_label = Static("Біблійні вірші по темам")
                yield ListView(ListItem(self.Bible_verses_label, id="verses_list"), id="themes_verses")

            with TabPane("Розбір", id="analysis"):
                yield Label("Теми для розбору\n")
                with Container(id="container-analysis"):
                    with VerticalScroll(id="left_random"):
                        n = 0
                        for k in self.themes.keys():
                            yield Button(k, id=f"{self.ids[n]} a", classes="button_themes")
                            n += 1
                self.random_Bible_verse_label = Static("Не випадкові вірші", id="random_verses")
                yield self.random_Bible_verse_label

    def theme_verses(self, theme: str):
        theme_verses_string = ""
        for k, v in verses.bible_verses[theme].items():
            result_verse = f"[b]{k}[/b]\n{v}"
            theme_verses_string += f"{result_verse}\n\n"
        theme_verses_string = theme_verses_string[:-2]
        self.Bible_verses_label.update(theme_verses_string)

    def random_verse(self, theme: str):
        verse_theme = verses.bible_verses[theme]
        verse_nv_list = choice(list(verse_theme.items()))
        copy_verse = f"{verse_nv_list[0]}\n{verse_nv_list[1]}"
        result_verse = f"[b]{verse_nv_list[0]}[/b]\n{verse_nv_list[1]}"
        # with Popen(["xclip", "-selection", "clipboard"], stdin=PIPE) as pipe:
        #     pipe.communicate(input=copy_verse.encode("utf-8"))
        self.random_Bible_verse_label.update(result_verse)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "grace t":
            self.theme_verses("благодать")
        elif event.button.id == "blessing t":
            self.theme_verses("благословення")
        elif event.button.id == "faith t":
            self.theme_verses("віра")
        elif event.button.id == "eternal life t":
            self.theme_verses("вічне життя")
        elif event.button.id == "help t":
            self.theme_verses("допомога")
        elif event.button.id == "Jesus is God t":
            self.theme_verses("Ісус - Бог")
        elif event.button.id == "patience t":
            self.theme_verses("терпіння")

        elif event.button.id == "grace a":
            self.random_verse("благодать")
        elif event.button.id == "blessing a":
            self.random_verse("благословення")
        elif event.button.id == "faith a":
            self.random_verse("віра")
        elif event.button.id == "eternal life a":
            self.random_verse("вічне життя")
        elif event.button.id == "help a":
            self.random_verse("допомога")
        elif event.button.id == "Jesus is God a":
            self.random_verse("Ісус - Бог")
        elif event.button.id == "patience a":
            self.random_verse("терпіння")


class BibleVersesApp(App):
    CSS_PATH = "style_Bible_verses.tcss"

    def compose(self) -> ComposeResult:
        close_button = Button("⇦", id="close")
        yield close_button
        yield TabsContent()
        yield Header(show_clock=True)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "close":
            self.exit(event.button.id)


if __name__ == "__main__":
    app = BibleVersesApp()
    app.run()
