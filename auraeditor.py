# auraeditor.py

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup
from kivy.uix.codeinput import CodeInput
from kivy.core.window import Window
from pygments.lexers import PythonLexer

from auraparser import Parser
from auralexer import Lexer
from aurapreter import Interpreter

class AurabeshEditor(App):
    def build(self):
        self.title = "Aurabesh Editor"
        layout = BoxLayout(orientation='vertical')
        
        # Ribbon
        ribbon = BoxLayout(size_hint_y=None, height=50)
        open_button = Button(text='Open')
        open_button.bind(on_release=self.open_file)
        save_button = Button(text='Save')
        save_button.bind(on_release=self.save_file)
        run_button = Button(text='Run')
        run_button.bind(on_release=self.run_program)
        ribbon.add_widget(open_button)
        ribbon.add_widget(save_button)
        ribbon.add_widget(run_button)
        
        # Editor
        self.editor = CodeInput(lexer=PythonLexer())
        
        # Terminal
        self.terminal = Label(size_hint_y=None, height=100)
        
        layout.add_widget(ribbon)
        layout.add_widget(self.editor)
        layout.add_widget(self.terminal)
        
        return layout

    def open_file(self, instance):
        content = FileChooserIconView(on_submit=self.load_file)
        popup = Popup(title="Open File", content=content, size_hint=(0.9, 0.9))
        content.bind(on_submit=lambda instance, selection, touch: popup.dismiss())
        popup.open()

    def load_file(self, chooser, selection):
        if selection:
            with open(selection[0], 'r') as f:
                self.editor.text = f.read()

    def save_file(self, instance):
        content = FileChooserIconView(on_submit=self.save_to_file)
        popup = Popup(title="Save File", content=content, size_hint=(0.9, 0.9))
        content.bind(on_submit=lambda instance, selection, touch: popup.dismiss())
        popup.open()

    def save_to_file(self, chooser, selection):
        if selection:
            with open(selection[0], 'w') as f:
                f.write(self.editor.text)

    def run_program(self, instance):
        code = self.editor.text
        tokens = Lexer(code).tokenize()
        program = Parser(tokens).parse()
        interpreter = Interpreter()
        interpreter.interpret(program)
        self.terminal.text = "Program finished running."

if __name__ == '__main__':
    AurabeshEditor().run()
