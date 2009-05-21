import inspect
import os.path
import sys

import Tkinter

import rope
import ropeide.core
from rope.base import project, exceptions
from ropeide.extension import SimpleAction
from ropeide.menubar import MenuAddress


def show_about_dialog(context):
    toplevel = Tkinter.Toplevel()
    toplevel.title('About Ropeide')
    text = '%s - version %s\n' % (rope.INFO, rope.VERSION)
    text += '%s - version %s\n\n%s\n' % \
         (ropeide.INFO, ropeide.VERSION, ropeide.COPYRIGHT)
    label = Tkinter.Label(toplevel, text=text, height=16, width=70,
                          justify=Tkinter.LEFT, relief=Tkinter.GROOVE)
    def ok():
        toplevel.destroy()
    def show_gpl():
        show_copying(context)
        toplevel.destroy()
    label.grid(row=0, column=0, columnspan=2)
    ok_button = Tkinter.Button(toplevel, text='OK', command=ok, width=20)
    gpl_button = Tkinter.Button(toplevel, text='Show GNU GPL',
                                command=show_gpl, width=20)
    gpl_button.grid(row=1, column=0)
    ok_button.grid(row=1, column=1)
    ok_button.focus_set()
    toplevel.bind('<Escape>', lambda event: ok())
    toplevel.bind('<Control-g>', lambda event: ok())
    toplevel.bind('<Return>', lambda event: ok())

def show_doc(context, name):
    ropeide_path = os.path.dirname(inspect.getsourcefile(ropeide))
    rope_path = os.path.dirname(inspect.getsourcefile(rope))
    # Checking whether rope is installed or not
    no_project = project.get_no_project()
    resource = None
    def parent(path):
        return os.path.join(path, os.pardir)
    paths = [rope_path, ropeide_path,
             parent(ropeide_path), parent(rope_path), '.']
    for root in paths:
        try:
            resource = no_project.get_resource(root + '/' + name)
            break
        except exceptions.RopeError:
            continue
    if resource is None:
        raise exceptions.RopeError('Document %s was not found' % name)
    editor_manager = context.get_core().get_editor_manager()
    editor_manager.get_resource_editor(resource, readonly=True)


def show_readme(context):
    show_doc(context, 'README.txt')

def show_features(context):
    show_doc(context, 'docs/rope.txt')

def show_overview(context):
    show_doc(context, 'docs/overview.txt')

def show_tutorial(context):
    show_doc(context, 'docs/tutorial.txt')

def show_contributing(context):
    show_doc(context, 'docs/contributing.txt')

def show_library(context):
    show_doc(context, 'docs/library.txt')

def show_copying(context):
    show_doc(context, 'COPYING')


core = ropeide.core.Core.get_core()
core.add_menu_cascade(MenuAddress(['Help'], 'h'), ['all', 'none'])
actions = []

actions.append(SimpleAction('readme', show_readme, 'C-h r',
                            MenuAddress(['Help', 'Ropeide Readme'], 'r')))
actions.append(SimpleAction('features', show_features, 'C-h f',
                            MenuAddress(['Help', 'Rope Features'], 'f')))
actions.append(SimpleAction('overview', show_overview, 'C-h o',
                            MenuAddress(['Help', 'Rope Overview'], 'o')))
actions.append(SimpleAction('tutorial', show_tutorial, 'C-h t',
                            MenuAddress(['Help', 'Ropeide Tutorial'], 't')))

actions.append(SimpleAction('contributing', show_contributing, 'C-h c',
                            MenuAddress(['Help', 'Contributing'], 'n', 1)))
actions.append(SimpleAction('library', show_library, 'C-h l',
                            MenuAddress(['Help', 'Using Rope As A Library'],
                                        'l', 1)))

actions.append(SimpleAction('about', show_about_dialog, 'C-h a',
                            MenuAddress(['Help', 'About Ropeide'], 'a', 2)))

for action in actions:
    core.register_action(action)
