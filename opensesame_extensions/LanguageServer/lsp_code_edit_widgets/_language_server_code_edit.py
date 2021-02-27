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
    
    """A base class for code edits that support language serves. The reason for
    using a mixin rather than subclassing a CodeEdit directly (as below) is to
    allow this functionality to different kinds of CodeEdit widgets.
    """
    
    mimetypes = None  # Specified in subclasses
    language_server_command = None  # Specified in subclass
    language = None  # Specified in subclass
    supports_workspace_folders = True
    supports_calltips = True
    supports_completions = True
    supports_diagnostics = True
    supports_symbols = True
    server_status_changed = Signal(str, str, int, int, dict)
    
    @property
    def language_server_pid(self):
        
        try:
            return self._language_server_pid
        except AttributeError:
            return None
    
    @property
    def language_server_status(self):
        
        try:
            return self._language_server_status
        except AttributeError:
            return workers.SERVER_NOT_STARTED
    
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
        
    def _move_mode_to_end(self, mode_name):
        """Moves a mode to the end by disabling and then enabling it. The main
        reason for doing this is to have this mode process key events last.
        """
        if mode_name not in self.modes.keys():
            return
        mode = self.modes.get(mode_name)
        mode.enabled = False
        mode.enabled = True
    
    def _enable_panel(self, panel, position):
        
        for p in self.panels.keys():
            if panel.name in self.panels._panels[p]:
                return
        self.panels.append(panel, position)
    
    def _enable_lsp_modes(self):
        
        if cfg.lsp_code_completion and self.supports_completions:
            self._enable_mode(modes.CodeCompletionMode())
            self._enable_mode(modes.AutoCompleteMode())
            # These modes consume key presses that are used by the completion
            # modes, and should therefore be moved to the end.
            self._move_mode_to_end('AutoIndentMode')
            self._move_mode_to_end('SmartBackSpaceMode')
        if cfg.lsp_calltips and self.supports_calltips:
            self._enable_mode(lsp_modes.CalltipsMode())
        # The diagnostics mode also does some bookkeeping that is generally
        # required for LSP support. Therefore it's always installed, but only
        # shows the actual diagnostics if the show_diagnostics keyword is True.
        diagnostics_mode = lsp_modes.DiagnosticsMode(
            show_diagnostics=cfg.lsp_diagnostics and self.supports_diagnostics
        )
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
        if cfg.lsp_diagnostics and self.supports_diagnostics:
            self._enable_panel(
                panels.CheckerPanel(),
                panels.GlobalCheckerPanel.Position.LEFT
            )
            self._enable_panel(
                panels.GlobalCheckerPanel(),
                panels.GlobalCheckerPanel.Position.RIGHT
            )
        if cfg.lsp_symbols and self.supports_symbols:
            self._enable_mode(
                lsp_modes.SymbolsMode(
                    cfg.lsp_symbols_kind.split(';')
                    if isinstance(cfg.lsp_symbols_kind, basestring)
                    else []
                )
            )

    def _start_backend(self):
        
        args = [
            '--command', self.language_server_command,
            '--langid', self.language,
        ]
        if self.supports_workspace_folders:
            args += ['--project-folders'] + \
                self.extension_manager.provide('ide_project_folders')
        self.backend.start(
            server.__file__,
            sys.executable,
            args,
            reuse=True,
            share_id=self.language_server_command
        )
        
    def _on_server_status_changed(self, status, pid, capabilities):
        
        self.server_status_changed.emit(
            self.language,
            self.language_server_command,
            status,
            pid,
            capabilities
        )
        self._language_server_pid = pid
        self._language_server_status = status
        self._language_server_capabilities = capabilities
        
    def change_project_folders(self, folders):
        
        self.backend.send_request(
            workers.change_project_folders,
            {'folders': folders}
        )
        
    def setPlainText(self, *args, **kwargs):
        
        super().setPlainText(*args, **kwargs)
        self.backend.send_request(
            workers.run_diagnostics,
            {'code': self._text(), 'path': self.file.path}
        )

    def __repr__(self):
        
        return '{}(path={})'.format(self.__class__.__name__, self.file.path)

    def clone(self):

        return self.__class__(parent=self.parent())
        
    def close(self, clear=True):

        self.backend.send_request(
            workers.close_document,
            {'code': self._text(), 'path': self.file.path}
        )
        super().close(clear=True)
        
    def _text(self):
        
        return self.toPlainText().replace(u'\u2029', u'\n')


class LanguageServerCodeEdit(LanguageServerMixin, FallbackCodeEdit):

    def __init__(self, parent):

        super().__init__(parent)
        self._enable_lsp_modes()
