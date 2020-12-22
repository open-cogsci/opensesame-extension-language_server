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
from libqtopensesame.misc.config import cfg
from pyqode_extras.widgets import FallbackCodeEdit
from pyqode.core import api, modes, panels
from pyqode.language_server.backend import server, workers
from pyqode.language_server import modes as lsp_modes


class LanguageServerMixin(object):
    
    mimetypes = None  # Specified in subclasses
    language_server_command = None
    language_identifier = None
    language = None
    
    def _enable_lsp_modes(self):
        
        if cfg.lsp_code_completion:
            self.modes.append(modes.CodeCompletionMode())
        if cfg.lsp_calltips:
            self.modes.append(lsp_modes.CalltipsMode())
        if cfg.lsp_diagnostics:
            self.modes.append(lsp_modes.DiagnosticsMode())
            self.panels.append(panels.CheckerPanel())
            self.panels.append(
                panels.GlobalCheckerPanel(),
                panels.GlobalCheckerPanel.Position.RIGHT
            )

    def _start_backend(self):
        
        self.backend.start(
            server.__file__,
            sys.executable,
            [
                '--command', self.language_server_command,
                '--langid', self.language_identifier
            ],
            reuse=True,
            share_id=self.language_server_command
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
