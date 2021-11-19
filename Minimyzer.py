#!/bin/python3
"""
An ugly piece of code(mostly for personal use) to minimize curently active window.
"""
import sys

import gi
from gi.repository import Wnck
from gi.repository import Gtk
try:
    gi.require_version('Wnck', '3.0')
except ValueError:
    print("Error:Couldn't import Pygi bindings for Wnck", file=sys.stderr)
    sys.exit(-1)


from pynput import keyboard


screen = Wnck.Screen.get_default()
screen.force_update()


pressed_vks = set() # currently pressed keys
MINIMIZE_COMBINATION = {keyboard.Key.ctrl, keyboard.KeyCode(vk=109)}


def _minimize() -> None:
    try:
        screen.get_active_window().minimize()
    except (TypeError,AttributeError):
        pass


def get_vk(key) -> int:
    """
    Get the virtual key code from a key.
    """
    return key.vk if hasattr(key, 'vk') else key.value.vk


def is_combination_pressed(combination) -> bool:
    """ Check if a combination is satisfied using the keys pressed in pressed_vks """
    return all([get_vk(key) in pressed_vks for key in combination])


def on_press(key) -> None:
    vk = get_vk(key) 
    pressed_vks.add(vk)
    # it would seems gtk doesnt update windows titles if windows events are pending so gotta use this hack
    while Gtk.events_pending():
        Gtk.main_iteration()
    if is_combination_pressed(MINIMIZE_COMBINATION): 
        _minimize()  
            


def on_release(key) -> None:
    try:
        vk = get_vk(key)
        pressed_vks.remove(vk)  
    except KeyError:
        pass

if __name__ == '__main__':
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()  

