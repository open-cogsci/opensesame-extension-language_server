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
from ._language_server_code_edit import \
    LanguageServerCodeEdit


class RCodeEdit(LanguageServerCodeEdit):
    """https://github.com/REditorSupport/languageserver"""
    
    mimetypes = ['text/x-r', 'text/x-R']
    language_server_command = 'R --slave -e "languageserver::run()"'
    language = 'R'

    def __init__(self, *args, **kwargs):
        
        super().__init__(*args, **kwargs)
        self._word_separators.remove('.')