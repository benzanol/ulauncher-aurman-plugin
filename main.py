from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from ulauncher.api.shared.action.CopyToClipboardAction import CopyToClipboardAction
import requests
import subprocess
import os

#Proxies = {"http": "http://127.0.0.1:7890", "https": "http://127.0.0.1:7890"}


class Extension(Extension):

    def __init__(self):
        super(Extension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())


class KeywordQueryEventListener(EventListener):
    def on_event(self, event, extension):
        query = event.get_argument() or str()
        if len(query.strip()) == 0:
            return RenderResultListAction([
                ExtensionResultItem(icon='icon.png',
                                    name='No input',
                                    on_enter=HideWindowAction())
            ])
        else:
            data = subprocess.Popen(["yay", "-Ss", str(query)], stdout = subprocess.PIPE)
            cmd = str(data.communicate())

            packages = [] # List of packages
            pkg_num = 0 # Number of packages
            i = 3 # Character index
            while i < len(cmd):
                packages.append([])
                repo = ""
                name = ""
                description = ""
                while i < len(cmd) and cmd[i] != '/':
                    repo += cmd[i]
                    i += 1
                i += 1
                while i < len(cmd) and cmd[i] != ' ':
                    name += cmd[i]
                    i += 1
                while i < len(cmd) and cmd[i] != '\\':
                    i += 1
                i += 6
                while i < len(cmd) and cmd[i] != '\\':
                    description += cmd[i]
                    i += 1
                packages[pkg_num].append(name)
                packages[pkg_num].append(description)
                packages[pkg_num].append(repo)
                pkg_num += 1
                i += 2

            del packages[len(packages) - 1]

            items = []
            for q in packages:
                if q[2] == "aur":
                    items.append(ExtensionResultItem(icon='icon.png',
                                                     name=q[0] + "  (" + q[2] + ")",
                                                     description=q[1],
                                                     on_enter=CopyToClipboardAction("yay -S " + q[0])))
                else:
                    items.append(ExtensionResultItem(icon='icon.png',
                                                     name=q[0] + "  (" + q[2] + ")",
                                                     description=q[1],
                                                     on_enter=CopyToClipboardAction("sudo pacman -S " + q[0])))

            return RenderResultListAction(items)


if __name__ == '__main__':
    Extension().run()
