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


WHITESPACES = [
    ' ',
    '\t'
    '\n',
    '\r'
]


def sub_all(s, target, replacement):
    s = s.replace(target, replacement)
    return s


def format(s, replace_space=True):
    if replace_space:
        s = s.replace(' ', '%s')
    s = s.replace('\t', '%t')
    s = s.replace('\n', '%n')
    s = s.replace('\r', '%r')
    return s


def replace_unless_preceded_by_backslash(s, orig, new):
    ret = ''
    buf = ''
    idx = 0

    for i in range(len(s)):
        if s[i] == orig[idx]:
            if idx == 0 and i > 0 and s[i-1] == '\\':
                ret += buf + s[i]
                idx = 0
                buf = ''
            else:
                idx += 1
                buf += s[i]

            if idx == len(orig):
                ret += new
                idx = 0
                buf = ''
        else:
            ret += buf + s[i]
            idx = 0
            buf = ''

    return ret


def split_unless_preceded_by_backslash(s, delim):
    ret = []
    to_add = ''
    buf = ''
    idx = 0

    for i in range(len(s)):
        if s[i] == delim[idx]:
            if idx == 0 and i > 0 and s[i-1] == '\\':
                to_add += buf + s[i]
                idx = 0
                buf = ''
            else:
                idx += 1
                buf += s[i]

            if idx == len(delim):
                ret.append(to_add)
                idx = 0
                buf = ''
                to_add = ''
        else:
            to_add += buf + s[i]
            idx = 0
            buf = ''

    ret.append(to_add)

    return ret


def is_all(arr, element):
    ret = True
    for i in arr:
        if i != element:
            ret = False
    return ret


def duplicate_dict(d):
    ret = {}
    for k in list(d.keys()):
        if type(d[k]) == list:
            ret[k] = d[k].copy()
        elif type(d[k]) == dict:
            ret[k] = duplicate_dict(d[k])
        else:
            ret[k] = d[k]
    return ret


def postfix_thread_with_branch(id, branch):
    return '{}_{}'.format(id, branch)


def cruise_over(s, idx, ignores=' \t\n\r'):
    for i in range(idx, len(s)):
        if s[i] not in ignores:
            break

    if i == (len(s) - 1) and s[i] in ignores:
        return False

    return i


def cruise_until(s, idx, triggers):
    for i in range(idx, len(s)):
        if s[i] in triggers:
            break

    if i == (len(s) - 1) and s[i] not in triggers:
        return False

    return i
