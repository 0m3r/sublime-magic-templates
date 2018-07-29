import sublime
import sublime_plugin

from .magento.Magento   import *
from .magento.classname import getClassName
from .magento.namespace import getNamespace
from .magento.template  import Template
from IpAddress.ipaddress.IpAddress import IpAddress as IpAddress

class InsertIfIpCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        ip = IpAddress.instance().get()

        # assume it's a Magento 2 if namespace is found
        namespace = self.view.find_by_selector('meta.namespace.php')
        if namespace:
            command = "\\Magento\\Framework\\App\\ObjectManager::getInstance()->get('\\Magento\\Framework\\HTTP\\PhpEnvironment\\RemoteAddress')->getRemoteAddress()"
        else:
            command = "Mage::helper('core/http')->getRemoteAddr()"

        template = "if ('%s' === " + command + ") {\n    $0\n}"

        for region in self.view.sel():
            if not region.empty():
                text = self.view.substr(region).replace('$', '\\$')
                self.view.run_command('insert_snippet', {'contents': template % (ip)})
                self.view.run_command('insert_snippet', {'contents': text})
            else:
                self.view.run_command('insert_snippet', {'contents': template % (ip)})

class GenerateContentCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.run_command('insert_snippet', {
            'contents': Template(self.view.file_name()).render()
        })

class GenerateClassCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        template = "namespace %s;\n\nclass %s extends $1\n{\n    $2\n}"
        self.view.run_command('insert_snippet', {
            'contents': template % (
                getNamespace(self.view.file_name()),
                getClassName(self.view.file_name())
            )
        })

class InsertClassNameCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.run_command('insert_snippet', {
            'contents': "${1:%s}" % getClassName(self.view.file_name())
        })

class InsertNamespaceCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.run_command('insert_snippet', {
            'contents': "${1:%s}" % getNamespace(self.view.file_name())
        })

class GenerateContentOnFileCreation(sublime_plugin.EventListener):
    def on_load(self, view):
        if view.file_name() is not None and view.size() == 0:
            view.run_command('insert_snippet', {
                'contents': Template(view.file_name()).render()
            })
