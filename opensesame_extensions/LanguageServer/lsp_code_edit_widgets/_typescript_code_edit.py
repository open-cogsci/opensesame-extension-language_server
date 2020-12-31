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
from lsp_code_edit_widgets._language_server_code_edit import \
    LanguageServerCodeEdit


class TypeScriptCodeEdit(LanguageServerCodeEdit):
    """https://github.com/theia-ide/typescript-language-server"""
    
    mimetypes = [
        'application/javascript',
        'application/x-javascript',
        'application/typescript',
        'application/x-typescript',
        'text/javascript',
        'text/x-javascript',
        'text/typescript',
        'text/x-typescript'
    ]
    language_server_command = 'typescript-language-server --stdio'
    language = 'typescript'
