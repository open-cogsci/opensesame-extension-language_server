#-*- coding:utf-8 -*-

"""
This file is part of OpenSesame.

OpenSesame is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

OpenSesame is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with OpenSesame.  If not, see <http://www.gnu.org/licenses/>.
"""

from libopensesame.py3compat import *
import sys
from pyqode.qt.QtCore import Signal
from libqtopensesame.misc.config import cfg
from pyqode_extras.widgets import FallbackCodeEdit
from pyqode.core import modes, panels
from pyqode.language_server.backend import server, workers
from pyqode.language_server import modes as lsp_modes


class LanguageServerMixin(object):
    
    server_status_changed = Signal(str, str, int, int)
    mimetypes = None  # Specified in subclasses
    language_server_command = None
    language_identifier = None
    language = None
    
    def _disable_mode(self, mode):
        
        if mode not in self.modes.keys():
            return
        self.modes.remove(mode)
        
    def _disable_panel(self, panel):
        
        for position in self.panels.keys():
            if panel in self.panels._panels[position]:
                break
        else:
            return
        self.panels.remove(panel)
    
    def _enable_mode(self, mode):
        
        if mode.name in self.modes.keys():
            return
        self.modes.append(mode)
    
    def _enable_panel(self, panel, position):
        
        for p in self.panels.keys():
            if panel.name in self.panels._panels[p]:
                return
        self.panels.append(panel, position)
    
    def _enable_lsp_modes(self):
        
        if cfg.lsp_code_completion:
            self._enable_mode(modes.CodeCompletionMode())
        if cfg.lsp_calltips:
            self._enable_mode(lsp_modes.CalltipsMode())
        if cfg.lsp_diagnostics:
            diagnostics_mode = lsp_modes.DiagnosticsMode()
            diagnostics_mode.set_ignore_rules(
                [
                    ir.strip()
                    for ir in cfg.lsp_diagnostics_ignore.split(u';')
                    if ir.strip()
                ]
            )
            diagnostics_mode.server_status_changed.connect(
                self._on_server_status_changed
            )
            self._enable_mode(diagnostics_mode)
            self._enable_panel(
                panels.CheckerPanel(),
                panels.GlobalCheckerPanel.Position.LEFT
            )
            self._enable_panel(
                panels.GlobalCheckerPanel(),
                panels.GlobalCheckerPanel.Position.RIGHT
            )
        if cfg.lsp_symbols:
            self._enable_mode(lsp_modes.SymbolsMode())

    def _start_backend(self):
        
        self.backend.start(
            server.__file__,
            sys.executable,
            [
                '--command', self.language_server_command,
                '--langid', self.language_identifier,
            ] + self.extension_manager.provide('ide_project_folders'),
            reuse=True,
            share_id=self.language_server_command
        )
        
    def _on_server_status_changed(self, status, pid):
        
        self.server_status_changed.emit(
            self.language_identifier,
            self.language_server_command,
            status,
            pid
        )
        
    def change_project_folders(self, folders):
        
        self.backend.send_request(
            workers.change_project_folders,
            {'folders': folders}
        )
        
    def setPlainText(self, *args, **kwargs):
        
        super().setPlainText(*args, **kwargs)
        self.backend.send_request(
            workers.open_document,
            {
                'code': self.toPlainText().replace(u'\u2029', u'\n'),
                'path': self.file.path,
            }
        )

    def __repr__(self):
        
        return '{}(path={})'.format(self.__class__.__name__, self.file.path)

    def clone(self):

        return self.__class__(parent=self.parent())


class LanguageServerCodeEdit(LanguageServerMixin, FallbackCodeEdit):

    def __init__(self, parent):

        super().__init__(parent)
        self._enable_lsp_modes()
