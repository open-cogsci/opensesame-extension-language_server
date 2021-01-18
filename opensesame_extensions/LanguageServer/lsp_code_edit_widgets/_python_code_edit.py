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
from libqtopensesame.misc.config import cfg
from lsp_code_edit_widgets._language_server_code_edit import \
    LanguageServerMixin
from pyqode_extras.widgets import PythonCodeEdit as OriginalPythonCodeEdit


class PylsCodeEdit(LanguageServerMixin, OriginalPythonCodeEdit):
    """https://github.com/palantir/python-language-server"""

    mimetypes = ['text/x-python']
    language_server_command = 'pyls'
    language = 'python'

    def __init__(self, parent):

        super().__init__(parent)
        self._disable_original_modes()
        self._enable_lsp_modes()
        
    def _disable_original_modes(self):
        
        if not cfg.lsp_code_completion:
            self._disable_mode('CodeCompletionMode')
        if not cfg.lsp_diagnostics:
            self._disable_panel('CheckerPanel')
            self._disable_panel('GlobalCheckerPanel')
        for mode in (
            'CalltipsMode',
            'PyFlakesChecker',
            'PEP8CheckerMode',
        ):
            self._disable_mode(mode)
            

class JediCodeEdit(PylsCodeEdit):
    """https://github.com/palantir/python-language-server"""

    language_server_command = 'jedi-language-server'
    supports_workspace_folders = False


PythonCodeEdit = PylsCodeEdit
