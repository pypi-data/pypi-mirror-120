"""
“Commons Clause” License Condition v1.0

The Software is provided to you by the Licensor under the License, as defined below, subject to the following condition.

Without limiting other conditions in the License, the grant of rights under the License will not include, and the License does not grant to you, the right to Sell the Software.

For purposes of the foregoing, “Sell” means practicing any or all of the rights granted to you under the License to provide to third parties, for a fee or other consideration (including without limitation fees for hosting or consulting/ support services related to the Software), a product or service whose value derives, entirely or substantially, from the functionality of the Software. Any license notice or attribution required by the License must also include this Commons Clause License Condition notice.

Software: Trilobyte

License: GNU General Public License Version 3

Licensor: SONG YIDING

Trilobyte is a powerful text-pattern parsing engine.
Copyright (C) 2021  SONG YIDING

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""


class KeyPntConverter(object):
    def __init__(self, KeyPntPat):
        self.keypnt_pat = KeyPntPat

    def convert(self, *args, **kwargs):
        struct = self.keypnt_pat.__struct__()
        if struct['type'] == 'Text':
            return struct['value']

        return ''


class VariableConverter(object):
    def __init__(self, var_name, func=None, **kwargs):
        self.var_name = var_name
        if func is not None:
            self.func = func
        else:
            self.func = lambda x : x
        self.keyword_args = kwargs

    def convert(self, var_dict, *args, **kwargs):
        if self.var_name in var_dict:
            return self.func(var_dict[self.var_name], **self.keyword_args)
        return ''


class TextConverter(object):
    def __init__(self, value):
        self.value = value

    def convert(self, *args, **kwargs):
        return self.value
