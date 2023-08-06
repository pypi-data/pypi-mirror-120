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


import warnings

from trilobyte.utils import sub_all, format, is_all, postfix_thread_with_branch
from trilobyte.keypoints import Keypnt

# @dev
# Support call indexing - call pattern multiple times with different texts;
# this prevents copying classes and speeds up performances
# Also allow to delete unused calls, e.g. when a search branch is deleted

# @dev
# If inputs have so far matched keypoint but keypoint is not yet completed,
#     `matched` = False, `completed` = False
# If previous inputs have matched keypoint, keypoint is complete, and next input does not match,
#     `matched` = True, `completed` = True
# If inputs have so far matched keypoint and keypoint is completed and cannot go on,
#     `matched` = True, `completed` = True
# If inputs have so far matched keypoint and keypoint is completed but can still go on,
#     `matched` = True, `completed` = False
# If previous inputs have matched keypoint, keypoint is yet to complete, and current input does not match,
#     `matched` = False, `completed` = True

# @dev
# @algorithm
# If !`matched` and !`completed` continue on current search branch with current keypoint
# If  `matched` and !`completed` continue on current search branch with current keypoint,
#                                while also forking a new search branch with next keypoint
# If !`matched` and `completed`  delete current search branch
# If  `matched` and `completed`  continue on current search branch with next keypoint

# @dev
# @algorithm
# Open new search branch with root keypoint at every new character in sequence

# @dev
# @algorithm
# When all branches have been computed, resolve conflicting (overlapping) branches,
# giving priority to branches discovered first (unless user specifies otherwise).
# Then, if user does not want recursive search, remove branches nested inside bigger branches.

# @update
# Kill branch early if already overlapped


#######################################
########## Secondary Classes ##########
#######################################

class Text(Keypnt):
    def __init__(self, value, ignore_case=False, **kwargs):
        super().__init__(**kwargs)
        if ignore_case:
            value = value.lower()
        self.value = value
        self.ignore_case = ignore_case

    def __str__(self):
        return self.inject_variable_string(
            format(self.value, replace_space=False)
        )

    def __len__(self):
        return len(self.value)

    def __struct__(self):
        return {'Text': {
            'value': self.value,
            'ignore_case': self.ignore_case
        }, 'type': 'Text'}

    def match(self, thread_id, *args, **kwargs):
        self.current_thread = thread_id
        c = self.resolve_args(['char'], [None], *args, **kwargs)['char']

        if self.ignore_case:
            _c = c.lower()
        else:
            _c = c

        if self.get_current('completed'):
            return self.generic_return()

        if _c == self.value[self.get_current('index')]:

            if self.get_current('index') == len(self.value) - 1:
                self.set_current('matched', True)
                self.set_current('completed', True)
                return self.generic_return_with_variable_handle(c)

            self.increment_current('index', 1)
            return self.generic_return_with_variable_handle(c)

        self.set_current('matched', False)
        self.set_current('index', 0)
        self.set_current('completed', True)
        self.set_current_variable('')

        return self.generic_return_with_variable_handle(c)

    def begins_with(self, c, **kwargs):
        if c is None:
            return False
        if self.value == '':
            return c == ''
        if self.ignore_case:
            c = c.lower()
        return self.value[0] == c


class RangeChar(Keypnt):
    def __init__(self, char_start, char_end, **kwargs):
        super().__init__(**kwargs)
        self.start = ord(char_start)
        self.end = ord(char_end)

    def __str__(self):
        return self.inject_variable_string(
            format('{' + chr(self.start) + '-' + chr(self.end) + '}')
        )

    def __len__(self):
        return 1

    def __struct__(self):
        return {'RangeChar': {
            'char_start': chr(self.start),
            'char_end': chr(self.end)
        }, 'type': 'RangeChar'}

    def match(self, thread_id, *args, **kwargs):
        self.current_thread = thread_id
        c = self.resolve_args(['char'], [None], *args, **kwargs)['char']
        self.set_current('matched', self.start <= ord(c) <= self.end)
        self.set_current('completed', True)

        return self.generic_return_with_variable_handle(c)

    def begins_with(self, c, **kwargs):
        if c is None:
            return False
        return self.start <= ord(c) <= self.end


class AltChar(Keypnt):
    def __init__(self, options, **kwargs):
        super().__init__(**kwargs)
        self.options = options

        for i in options:
            assert len(i) == 1, 'All alternatives in options list must be CHAR (STR of length 1)'

    def __str__(self):
        return self.inject_variable_string(format(
            '{' + ','.join([char.replace(',', '\,') for char in self.options]) + '}'
        ))

    def __len__(self):
        return 1

    def __struct__(self):
        return {'AltChar': {
            'options': self.options.copy()
        }, 'type': 'AltChar'}

    def match(self, thread_id, *args, **kwargs):
        self.current_thread = thread_id
        c = self.resolve_args(['char'], [None], *args, **kwargs)['char']

        self.set_current('matched', c in self.options)
        self.set_current('completed', True)

        return self.generic_return_with_variable_handle(c)

    def begins_with(self, c, **kwargs):
        if c is None:
            return False
        return c in self.options


class AltCharPat(Keypnt):
    def __init__(self, char_patterns, **kwargs):
        super().__init__(**kwargs)
        self.patterns = char_patterns

        for i in char_patterns:
            assert len(i) == 1, 'All alternatives in options list must be a CHAR pattern (STR of length 1)'

    def __str__(self):
        return self.inject_variable_string(format('{' + \
                                                  ','.join([sub_all(str(pat), ',', '\,')
                                                               if pat.__struct__()['type'] == 'Text'
                                                               else str(pat)
                                                               for pat in self.patterns
                                                            ]) + \
                                                  '}'))

    def __len__(self):
        return 1

    def __struct__(self):
        return {'AltCharPat': {
            'char_patterns': [pat.copy() for pat in self.patterns]
        }, 'type': 'AltCharPat'}

    def add_thread(self, id, prop='default'):
        super().add_thread(id, prop)
        for pat in self.patterns:
            pat.add_thread(id)

    def remove_thread(self, id):
        super().remove_thread(id)
        for pat in self.patterns:
            pat.remove_thread(id)

    def __verify_thread__(self, id):
        ret = super().__verify_thread__(id)
        for pat in self.patterns:
            ret = ret and pat.__verify_thread__(id)
        return ret

    def push_current_variable_override(self, thread_id):
        super().push_current_variable_override(thread_id)
        for pat in self.patterns:
            pat.push_current_variable_override(thread_id)

    def match(self, thread_id, *args, **kwargs):
        self.current_thread = thread_id
        c = self.resolve_args(['char'], [None], *args, **kwargs)['char']
        self.set_current('matched', False)
        self.set_current('completed', True)
        for pat in self.patterns:
            if pat.match(thread_id, c)[0]:
                self.set_current('matched', True)
        return self.generic_return_with_variable_handle(c)

    def begins_with(self, c, **kwargs):
        if c is None:
            return False

        ret = False
        for pat in self.patterns:
            if pat.begins_with(c, **kwargs):
                ret = True
        return ret


class AltPat(Keypnt):
    def __init__(self, patterns, **kwargs):
        self.num_patterns = len(patterns)
        self.patterns = patterns
        super().__init__(prop = {
                'index': 0,
                'matched': ([False] * self.num_patterns),
                'completed': ([False] * self.num_patterns)
        }, **kwargs)

    def __str__(self):
        return self.inject_variable_string(format('{' + \
                                                  ','.join([sub_all(str(pat), ',', '\,')
                                                               if pat.__struct__()['type'] == 'Text'
                                                               else str(pat)
                                                               for pat in self.patterns
                                                            ]) + \
                                                  '}'))

    def __lengths__(self):
        return [len(i) for i in self.patterns]

    def __maxlen__(self):
        return max(self.__lengths__())

    def __minlen__(self):
        return min(self.__lengths__())

    def __len__(self):
        if self.__minlen__() != self.__maxlen__():
            warnings.warn('\n\n  !!!  The length of this AltPat is ambiguous as its components are of differing '
                          'lengths; please specify AltPat.__maxlen__() or AltPat.__minlen__()\n', category=Warning)
        return self.__maxlen__()

    def __struct__(self):
        return {'AltPat': {
            'patterns': [pat.copy() for pat in self.patterns]
        }, 'type': 'AltPat'}

    def __reset_thread__(self, id):
        super().__reset_thread__(id)
        for pat in self.patterns:
            pat.__reset_thread__(id)

    def add_thread(self, id, prop='default'):
        super().add_thread(id, prop)
        for pat in self.patterns:
            pat.add_thread(id)

    def remove_thread(self, id):
        super().remove_thread(id)
        for pat in self.patterns:
            pat.remove_thread(id)

    def __verify_thread__(self, id):
        ret = super().__verify_thread__(id)
        for pat in self.patterns:
            ret = ret and pat.__verify_thread__(id)
        return ret

    def push_current_variable_override(self, thread_id):
        super().push_current_variable_override(thread_id)
        for pat in self.patterns:
            pat.push_current_variable_override(thread_id)

    def match(self, thread_id, *args, **kwargs):
        self.current_thread = thread_id

        if is_all(self.get_current('completed'), True):
            return True in self.get_current('matched'), True

        matched_one = False
        all_completed = True
        for pat_idx in range(self.num_patterns):
            if self.get_current('completed')[pat_idx] is not True:
                rets = self.patterns[pat_idx].match(thread_id, *args, **kwargs)

                self.get_current('matched')[pat_idx] = rets[0]
                self.get_current('completed')[pat_idx] = rets[1]

                if rets[0]:
                    matched_one = True
                if not rets[1]:
                    all_completed = False

        c = self.resolve_args(['char'], [None], *args, **kwargs)['char']
        return self.handle_current_variable_then_return(c, matched_one, all_completed)

    def begins_with(self, c, **kwargs):
        if c is None:
            return False

        ret = False
        for pat in self.patterns:
            if pat.begins_with(c, **kwargs):
                ret = True
        return ret


class RepeatPat(Keypnt):
    def __init__(self, pattern, **kwargs):
        super().__init__(**kwargs)
        self.pattern = pattern

    def __str__(self):
        return self.inject_variable_string(format('@r[{}]'.format(str(self.pattern))))

    def __len__(self):
        warnings.warn('\n\n  !!!  The length of a RepeatPat is undefined. Length of pattern repeated is returned '
                      'instead.', category=Warning)
        return len(self.pattern)

    def __struct__(self):
        return {'RepeatPat': {
            'pattern': self.pattern.copy()
        }, 'type': 'RepeatPat'}

    def __reset_thread__(self, id):
        super().__reset_thread__(id)
        self.pattern.__reset_thread__(id)

    def add_thread(self, id, prop='default'):
        super().add_thread(id, prop)
        self.pattern.add_thread(id)

    def remove_thread(self, id):
        super().remove_thread(id)
        self.pattern.remove_thread(id)

    def __verify_thread__(self, id):
        ret = super().__verify_thread__(id) and self.pattern.__verify_thread__(id)
        return ret

    def push_current_variable_override(self, thread_id):
        super().push_current_variable_override(thread_id)
        self.pattern.push_current_variable_override(thread_id)

    def match(self, thread_id, original_thread_id=None, *args, **kwargs):
        self.current_thread = thread_id
        if original_thread_id is None:
            original_thread_id = thread_id
        _resolved = self.resolve_args(['char', 'next'], [None, None], *args, **kwargs)
        c, n = _resolved['char'], _resolved['next']

        if self.get_current('completed'):
            return self.generic_return()

        rets = self.pattern.match(thread_id, *args, **kwargs)
        _matched, _completed = rets[0], rets[1]
        self.set_current('matched', _matched)



        if _matched and _completed and self.pattern.begins_with(n, original_thread_id=original_thread_id,
                                                                thread_id=thread_id):
            self.set_current('completed', False)
            self.pattern.__reset_thread__(thread_id)
        else:
            self.set_current('completed', _completed)

        return self.generic_return_with_variable_handle(c)

    def begins_with(self, c, **kwargs):
        if c is None:
            return False

        return self.pattern.begins_with(c, **kwargs)


class NegPat(Keypnt):
    def __init__(self, pattern, length=None, **kwargs):
        super().__init__(**kwargs)
        self.pattern = pattern
        self.length = length

    def __str__(self):
        if self.length is None:
            return self.inject_variable_string(format('~[{}]'.format(str(self.pattern))))
        return self.inject_variable_string(format('~({})[{}]'.format(self.length, str(self.pattern))))

    def __len__(self):
        return len(self.pattern)

    def __struct__(self):
        return {'NegPat': {
            'pattern': self.pattern.copy(),
            'length': self.length
        }, 'type': 'NegPat'}

    def __reset_thread__(self, id):
        super().__reset_thread__(id)
        self.pattern.__reset_thread__(id)

    def add_thread(self, id, prop='default'):
        super().add_thread(id, prop)
        self.pattern.add_thread(id)

    def remove_thread(self, id):
        super().remove_thread(id)
        self.pattern.remove_thread(id)

    def __verify_thread__(self, id):
        ret = super().__verify_thread__(id) and self.pattern.__verify_thread__(id)
        return ret

    def push_current_variable_override(self, thread_id):
        super().push_current_variable_override(thread_id)
        self.pattern.push_current_variable_override(thread_id)

    def match(self, thread_id, *args, **kwargs):
        self.current_thread = thread_id
        c = self.resolve_args(['char'], [None], *args, **kwargs)['char']

        if self.get_current('completed'):
            return self.generic_return()

        rets = self.pattern.match(thread_id, *args, **kwargs)
        _matched, _completed = rets[0], rets[1]
        self.set_current('matched', not _matched)
        self.set_current('completed', _completed)

        self.increment_current('index', 1)
        if self.length is not None and self.get_current('index') >= self.length:
            self.set_current('completed', True)

        return self.generic_return_with_variable_handle(c)

    def begins_with(self, c, **kwargs):
        if c is None:
            return False
        return not self.pattern.begins_with(c, **kwargs)


class SequencePat(Keypnt):
    def __init__(self, patterns, **kwargs):
        self.patterns = patterns
        self.num_patterns = len(self.patterns)

        self.num_branches = 1
        self.default_branch = 0
        super().__init__(prop={
            'branches': {
                self.default_branch: {
                    'index': 0,
                    'matched': False,
                    'completed': False
                }
            },
            'matched': False,
            'completed': False
        }, **kwargs)

    def __str__(self):
        return self.inject_variable_string('[{}]'.format(''.join(str(pat) for pat in self.patterns)))

    def __lengths__(self):
        return [len(i) for i in self.patterns]

    def __len__(self):
        return sum(self.__lengths__())

    def __struct__(self):
        return {'SequencePat': {
            'patterns': [pat.copy() for pat in self.patterns],
        }, 'type': 'SequencePat'}

    def __reset_thread__(self, id):
        _keys = list(self.threads[id]['branches'])
        super().__reset_thread__(id)
        for pat in self.patterns:
            for branch_key in _keys:
                pat.remove_thread(postfix_thread_with_branch(id, branch_key))
            pat.add_thread(postfix_thread_with_branch(id, self.default_branch))

    def add_thread(self, id, branch=None, prop='default'):
        super().add_thread(id, prop)
        if branch is None:
            branch = self.default_branch
        for pat in self.patterns:
            pat.add_thread(postfix_thread_with_branch(id, branch))

    def remove_thread(self, id):
        _keys = list(self.threads[id]['branches'])
        super().remove_thread(id)
        for pat in self.patterns:
            for branch_key in _keys:
                pat.remove_thread(postfix_thread_with_branch(id, branch_key))

    def __verify_thread__(self, id):
        ret = super().__verify_thread__(id)
        for pat in self.patterns:
            for branch_key in self.threads[id]['branches']:
                ret = ret and pat.__verify_thread__(postfix_thread_with_branch(id, branch_key))
        return ret

    def push_current_variable_override(self, thread_id):
        super().push_current_variable_override(thread_id)
        for pat in self.patterns:
            pat.push_current_variable_override(thread_id)

    def match(self, thread_id, original_thread_id=None, *args, **kwargs):
        self.current_thread = thread_id
        if original_thread_id is None:
            original_thread_id = thread_id
        _resolved = self.resolve_args(['char', 'next'], [None, None], *args, **kwargs)
        c, n = _resolved['char'], _resolved['next']

        if self.get_current('completed'):
            return self.generic_return()

        matched_one = False
        all_completed = True
        legacy_branch = self.default_branch

        for branch_key in list(self.get_current('branches').keys()):  # Use `.keys()` for fixed iteration size
            branch = self.get_current('branches')[branch_key]
            if not branch['completed']:
                pat_idx = branch['index']
                rets = self.patterns[pat_idx].match(postfix_thread_with_branch(thread_id, branch_key),
                                                    original_thread_id=thread_id, *args, **kwargs)
                _matched, _completed = rets[0], rets[1]

                if _matched and _completed:
                    branch['index'] += 1

                    if branch['index'] == self.num_patterns:
                        branch['matched'] = True
                        branch['completed'] = True
                        for pat in self.patterns:
                            pat.push_current_variable_override(thread_id)

                    elif not self.patterns[branch['index']].begins_with(
                        n,
                        thread_id=postfix_thread_with_branch(thread_id, branch_key),
                        original_thread_id=original_thread_id
                    ):
                        branch['matched'] = False
                        branch['completed'] = True

                elif _matched and not _completed:
                    branch['matched'] = (branch['index'] + 1 == self.num_patterns)

                    if branch['matched']:
                        for pat in self.patterns:
                            pat.push_current_variable_override(thread_id)

                    else:
                        self.get_current('branches')[self.num_branches] = {
                            'index': branch['index'] + 1,
                            'matched': False,
                            'completed': False
                        }

                        for pat in self.patterns:
                            pat.add_thread(postfix_thread_with_branch(thread_id, self.num_branches))
                            pat.push_current_variable_override(postfix_thread_with_branch(thread_id, self.num_branches))

                        self.num_branches += 1

                elif not _matched and _completed:
                    branch['completed'] = True

                elif not _matched and not _completed:
                    pass

                if branch['matched']:
                    matched_one = True
                    legacy_branch = branch_key
                if not branch['completed']:
                    all_completed = False

        self.set_current('matched', matched_one)
        self.set_current('completed', all_completed)

        for pat in self.patterns:
            pat.current_thread = postfix_thread_with_branch(thread_id, legacy_branch)

        return self.generic_return_with_variable_handle(c)

    def begins_with(self, c, thread_id, **kwargs):
        if c is None:
            return False
        return self.patterns[0].begins_with(c, thread_id=postfix_thread_with_branch(thread_id, self.default_branch),
                                            **kwargs)


class VariablePat(Keypnt):
    def __init__(self, var_pat_name, var_pat_dict=None, var_dict=None, func=None, **kwargs):
        super().__init__(var_dict=var_dict, prop={
            'index': 0,
            'matched': False,
            'completed': False,
            'value': ''
        }, **kwargs)

        if func is None:
            self.func = lambda x : x
        else:
            self.func = func

        if var_pat_dict is None and var_dict is not None:
            self.var_pat_dict = var_dict
        else:
            self.var_pat_dict = var_pat_dict
        self.var_pat_name = var_pat_name

    def __str__(self):
        return self.inject_variable_string(
            format('$'+self.var_pat_name, replace_space=False)
        )

    def __len__(self):
        warnings.warn('\n\n  !!!  The length of a VariablePat is undefined until runtime.\n', category=Warning)
        return float('nan')

    def __struct__(self):
        return {'VariablePat': {
            'var_pat_name': self.var_pat_name,
            'var_pat_dict': self.var_pat_dict,
            'func': self.func
        }, 'type': 'VariablePat'}

    def match(self, thread_id, original_thread_id=None, *args, **kwargs):
        self.current_thread = thread_id
        if original_thread_id is None:
            original_thread_id = thread_id
        c = self.resolve_args(['char'], [None], *args, **kwargs)['char']
        _c = self.func(c)

        if self.get_current('completed'):
            return self.generic_return()

        if self.get_current('value') == '':
            if thread_id in self.var_pat_dict and self.var_pat_name in self.var_pat_dict[thread_id]:
                self.set_current('value', self.func(self.var_pat_dict[thread_id][self.var_pat_name]))
            else:
                self.set_current('value', self.func(''))
                if self.get_current('value') == '':
                    self.set_current('matched', False)
                    self.set_current('completed', False)
                    return self.generic_return()

        if _c == self.get_current('value')[self.get_current('index')]:
            if self.get_current('index') == len(self.get_current('value')) - 1:
                self.set_current('matched', True)
                self.set_current('completed', True)
                return self.generic_return_with_variable_handle(c)

            self.increment_current('index', 1)
            return self.generic_return_with_variable_handle(c)

        self.set_current('matched', False)
        self.set_current('index', 0)
        self.set_current('completed', True)
        self.set_current_variable('')

        return self.generic_return_with_variable_handle(c)

    def begins_with(self, c, thread_id, original_thread_id, **kwargs):
        if c is None:
            return False
        c = self.func(c)

        if self.threads[thread_id]['value'] == '':
            if original_thread_id in self.var_pat_dict and self.var_pat_name in self.var_pat_dict[original_thread_id]:
                self.threads[thread_id]['value'] = self.func(self.var_pat_dict[original_thread_id][self.var_pat_name])
                return c == self.threads[thread_id]['value'][0]
            else:
                self.threads[thread_id]['value'] = self.func('')
        return self.threads[thread_id]['value'][0] == c


######################################
########## Tertiary Classes ##########
######################################


class Space(Text):
    def __init__(self, value=' ', **kwargs):
        super().__init__(value, **kwargs)

    def __str__(self):
        return self.inject_variable_string("%s")


class Tab(Text):
    def __init__(self, value='\t', **kwargs):
        super().__init__(value, **kwargs)

    def __str__(self):
        return self.inject_variable_string("%t")


class Newline(Text):
    def __init__(self, value='\n', **kwargs):
        super().__init__(value, **kwargs)

    def __str__(self):
        return self.inject_variable_string("%n")


class Return(Text):
    def __init__(self, value='\r', **kwargs):
        super().__init__(value, **kwargs)

    def __str__(self):
        return self.inject_variable_string("%r")


class Uppercase(RangeChar):
    def __init__(self, char_start='A', char_end='Z', **kwargs):
        super().__init__(char_start, char_end, **kwargs)

    def __str__(self):
        return self.inject_variable_string("%U")


class Lowercase(RangeChar):
    def __init__(self, char_start='a', char_end='z', **kwargs):
        super().__init__(char_start, char_end, **kwargs)

    def __str__(self):
        return self.inject_variable_string("%l")


class Numerical(RangeChar):
    def __init__(self, char_start='0', char_end='9', **kwargs):
        super().__init__(char_start, char_end, **kwargs)

    def __str__(self):
        return self.inject_variable_string("%d")


class Whitespace(AltChar):
    def __init__(self, options=[' ', '\t', '\n', '\r'].copy(), **kwargs):
        super().__init__(options, **kwargs)

    def __str__(self):
        return self.inject_variable_string("%w")


class Mono(AltChar):
    def __init__(self, options=[' ', '\t'].copy(), **kwargs):
        super().__init__(options, **kwargs)

    def __str__(self):
        return self.inject_variable_string("%m")


class Flush(AltChar):
    def __init__(self, options=['\n', '\r'].copy(), **kwargs):
        super().__init__(options, **kwargs)

    def __str__(self):
        return self.inject_variable_string("%f")


class Alphabetical(AltCharPat):
    def __init__(self, char_patterns=None, **kwargs):
        char_patterns = [Uppercase(), Lowercase()]
        super().__init__(char_patterns, **kwargs)

    def __str__(self):
        return self.inject_variable_string("%a")


class AlphaNum(AltCharPat):
    def __init__(self, char_patterns=None, **kwargs):
        char_patterns = [Uppercase(), Lowercase(), Numerical()]
        super().__init__(char_patterns, **kwargs)

    def __str__(self):
        return "%b"


class Exclusive(RepeatPat):
    def __init__(self, pattern=None, **kwargs):
        pattern = Mono()
        super().__init__(pattern, **kwargs)

    def __str__(self):
        return self.inject_variable_string("%e")


class Separation(RepeatPat):
    def __init__(self, pattern=None, **kwargs):
        pattern = Flush()
        super().__init__(pattern, **kwargs)

    def __str__(self):
        return self.inject_variable_string("%x")


class Omni(RepeatPat):
    def __init__(self, pattern=None, **kwargs):
        pattern = Whitespace()
        super().__init__(pattern, **kwargs)

    def __str__(self):
        return self.inject_variable_string("%o")


class Variable(AltPat):
    def __init__(self, patterns=None, **kwargs):
        patterns = [Alphabetical(), SequencePat([Alphabetical(), RepeatPat(AlphaNum())])]
        super().__init__(patterns, **kwargs)

    def __str__(self):
        return self.inject_variable_string("%v")


class OptionalRepeatedAfter(AltPat):
    def __init__(self, main_pat, rep_pat, repeat_var_name=None, repeat_var_dict=None, var_dict=None, **kwargs):
        self.main_pat = main_pat
        self.rep_pat = rep_pat
        if repeat_var_name is not None and repeat_var_dict is None:
            repeat_var_dict = var_dict
        patterns = [main_pat.copy(preserve_vars=True),
                    SequencePat([main_pat.copy(preserve_vars=True),
                                 RepeatPat(rep_pat.copy(preserve_vars=True),
                                           var_name=repeat_var_name, var_dict=repeat_var_dict)])
                   ]
        super().__init__(patterns, var_dict=var_dict, **kwargs)

    def __struct__(self):
        return {'OptionalRepeatedAfter': {
            'main_pat': self.main_pat.copy(),
            'rep_pat': self.rep_pat.copy()
        }, 'type': 'OptionalRepeatedAfter'}

    def __str__(self):
        return self.inject_variable_string("@a[{}][{}]".format(str(self.main_pat), str(self.rep_pat)))


class OptionalRepeatedBefore(AltPat):
    def __init__(self, main_pat, rep_pat, repeat_var_name=None, repeat_var_dict=None, var_dict=None, **kwargs):
        self.main_pat = main_pat
        self.rep_pat = rep_pat
        if repeat_var_name is not None and repeat_var_dict is None:
            repeat_var_dict = var_dict
        patterns = [main_pat.copy(preserve_vars=True),
                    SequencePat([RepeatPat(rep_pat.copy(preserve_vars=True),
                                           var_name=repeat_var_name, var_dict=repeat_var_dict),
                                 main_pat.copy(preserve_vars=True)])
                   ]
        super().__init__(patterns, var_dict=var_dict, **kwargs)

    def __struct__(self):
        return {'OptionalRepeatedBefore': {
            'main_pat': self.main_pat.copy(),
            'rep_pat': self.rep_pat.copy()
        }, 'type': 'OptionalRepeatedBefore'}

    def __str__(self):
        return self.inject_variable_string("@b[{}][{}]".format(str(self.main_pat), str(self.rep_pat)))


class DelimPat(SequencePat):
    def __init__(self, delim_pat, pat, **kwargs):
        self.delim_pat = delim_pat
        self.pat = pat
        patterns = [RepeatPat(SequencePat([self.pat.copy(preserve_vars=True),
                                           self.delim_pat.copy(preserve_vars=True)])),
                    self.pat.copy(preserve_vars=True)]
        super().__init__(patterns, **kwargs)

    def __struct__(self):
        return {'DelimPat': {
            'delim_pat': self.delim_pat.copy(),
            'pat': self.pat.copy()
        }, 'type': 'DelimPat'}

    def __str__(self):
        return self.inject_variable_string('@d[{}][{}]'.format(str(self.delim_pat), str(self.pat)))


class Param(DelimPat):
    def __init__(self, delim_pat=None, pat=None, **kwargs):
        delim_pat = AltPat([
            Text(","), SequencePat([Text(","), RepeatPat(Whitespace())])
        ])
        pat = Variable()
        super().__init__(delim_pat, pat, **kwargs)

    def __str__(self):
        return self.inject_variable_string("%p")
