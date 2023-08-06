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

from trilobyte.keypoints import *
from trilobyte.utils import cruise_over, cruise_until, duplicate_dict

# \                               / Makes the trilo treat the following expression as normal text
# ~ ( num ) [ pat ]               / Take the negative of pat, optionally supplying max checking length as a
#                                   number `num`
# * [ text ]                        Ignore case

# { char1 - char2 }               / Command that detects any character between char1 and char2 on UNICODE
#                                   (inclusive)
# { pat1 , pat2 , pat3 , ... }    / Command that detects any trilo between the list of alternatives (use `\,`
#                                   to avoid compiler treating `,` as a delimiter)

# @r ( $var / num ) [ pat ]       / Command that detects repeated patterns of pat (r for repeat),
#                                   optionally specify a variable name `var` for the number of repetitions matched,
#                                   or supplying a number `num` which fixes the number of repetitions
# @d [ delim_pat ] [ pat ]        / Command that detects a list of pat delimited by delim_pat (d for delimited)
# @a [ main_pat ] [ rep_pat ]     / Command that detects main_pat, followed by an optional repeated occurrence of
#                                   rep_pat after (a for after)
# @b [ rep_pat ] [ main_pat ]     / Command that detects main_pat, preceded by an optional repeated occurrence of
#                                   rep_pat before (b for before)

# %s                              / The space character
# %t                              / The tab character
# %n                              / The newline character
# %r                              / The return character

# %w                              / Any whitespace character, including newline
# %m                              / Only spaces or tabs (m = s + t, also think of it mono - all on 1 line!)
# %f                              / Only newline or return (f = n + r, also think of it as flush)
# %U                              / Any uppercase character
# %l                              / Any lowercase character
# %a                              / Any alphabetical character
# %d                              / Any numerical digit
# %b                              / Any alphanumeric character (b for basic)

# %v                              / Shorthand for any sequence of alphanumeric characters that doesn't
#                                   start with a number (v for variable, as these are generally named in
#                                   this convention)
# %o                              / Shorthand for repetition of %w (o = r + w, also think of it as omni -
#                                   everything!)
# %e                              / Shorthand for repetition of %m (e = r + m, also think of it as exclusive)
# %x                              / Shorthand for repetition of %f (x = r + f, also think of X as separation -
#                                   that's what a sequence of %f is anyway)
# %p                              / Shorthand for any comma-delimited sequence of %v (v for parameters, as
#                                   these are generally formatted in this convention)

# $var [ pat ]                    / Represents the expression that follows pat as a variable (use '' for pat
#                                   in order to detect any possible expression)

# `find_all` function               Returns start and end indices of matches and a dictionary of variables
#   `resolver` arg; takes:
#     `first`
#     `longest`
#     `most_expressions`
#     `sort_first`
#     `sort_longest`
#     `sort_most_expressions`
#   `keep_subpatterns` flag         Whether or not to return matches within a matched expression

# `find_once` function              Identical to calling `find_all` with `keep_subpatterns` = False, and
#                                   resolver` = i in {'first', 'longest', 'most_expressions'}

# `replace_all` function
# `replace_once` function

# `mask` function                   Mask patterns; these areas of text will not be operated on until `recover()`

# `recover`` function               Remove all masks


TRIGGERS = ['\\', '~', '*', '@', '%', '$', '(', '[', '{']
NON_TEXTS = ['~', '*', '@', '%', '$', '(', '[', '{']

EXPRESS_MAPPINGS = {
    's': Space, 't': Tab, 'n': Newline, 'r': Return,
    'w': Whitespace, 'm': Mono, 'f': Flush, 'U': Uppercase, 'l': Lowercase,
    'a': Alphabetical, 'd': Numerical, 'b': AlphaNum,
    'v': Variable, 'o': Omni, 'e': Exclusive, 'x': Separation, 'p': Param
}


def collapse_patterns(patterns):
    if len(patterns) == 1:
        ret = patterns[0]
    else:
        ret = SequencePat(patterns)
    return ret

def flush_check(buf, patterns):
    if buf != '':
        patterns.append(Text(buf))


class Trilo:
    def __init__(self, patterns, var_name=None, var_dict=None, force_var_dict=True):
        if var_dict is None:
            self.var_dict = {}
        else:
            self.var_dict = var_dict

        if type(patterns).__name__ == 'str':
            self.patterns = self.str2keypoints(patterns, self.var_dict)
        elif type(patterns).__name__ == 'list':
            self.patterns = patterns
        else:
            warnings.warn("Cannot parse argument `patterns`")

        for pat in self.patterns:
            if pat.is_var:
                pat.var_dict = self.var_dict

        self.overall_op = collapse_patterns(self.patterns)
        self.var_name = var_name
        if var_name is not None:
            self.overall_op.varify(var_name=self.var_name, var_dict=self.var_dict)

    def handleReplacement(self, replacement_obj):
        if type(replacement_obj).__name__ == 'str':
            converters = self.str2converters(replacement_obj)
        elif type(replacement_obj).__name__ == 'list':
            converters = replacement_obj
        else:
            warnings.warn("Cannot parse argument `replacement_obj`")
            return False
        return converters

    def str2converters(self, s):
        pass

    def str2keypoints(self, s, var_dict):
        """
        Still under construction
        :param s:
        :param var_dict:
        :return:
        """
        proc = s.strip()
        suppress = False

        patterns = []
        buf = ''

        for i in range(0, len(s)):
            c = proc[i]
            if c == '\\':
                if proc[i+1] in TRIGGERS:
                    buf += proc[i+1]
                    i += 2
                else:
                    raise SyntaxError("Unknown expression {} at position {}. Use {} for one backslash.".format(
                        proc[i:i+2], i, '\\\\'
                    ))

            elif c == '~':
                flush_check(buf, patterns)

                start_idx = cruise_over(proc, i+1)
                if not start_idx:
                    raise SyntaxError("Unknown expression at position {}".format(start_idx))

                start = proc[start_idx]
                if start == '(':
                    end_idx = cruise_until(proc, start+1)

                elif start == '[':
                    pass

                else:
                    raise SyntaxError("Unknown expression {} at position {}. Expecting ( or [.".format(n, n_idx))

            else:
                buf += c

            i += 1

        flush_check(buf, patterns)

        return patterns

    def find_first(self, text):
        l = len(text)
        THREAD_ID = 0
        i = 0
        matched = False
        self.overall_op.add_thread(THREAD_ID)

        while i < l:
            self.overall_op.__reset_thread__(THREAD_ID)
            if THREAD_ID in self.var_dict:
                del self.var_dict[THREAD_ID]

            if self.overall_op.begins_with(text[i], thread_id=THREAD_ID):
                for e in range(i, l):
                    _m, _c = self.overall_op.match(
                        THREAD_ID, char=text[e], next=text[e+1] if e < len(text) - 1 else None
                    )
                    if _m:
                        matched = True
                        start = i
                        end = e + 1
                    if _c:
                        break

                if matched:
                    break

            i += 1

        self.overall_op.remove_thread(THREAD_ID)

        if matched:
            if THREAD_ID in self.var_dict:
                vdict = duplicate_dict(self.var_dict[THREAD_ID])
                del self.var_dict[THREAD_ID]
            else:
                vdict = {}
            return matched, start, end, vdict
        return matched

    def replace_all(self, text, replacement_obj, allow_nested=False):
        converters = self.handleReplacement(replacement_obj)

        if allow_nested:
            res = self.find_first(text)

            while res:
                _, start, end, vdict = res
                rep = ''
                for conv in converters:
                    rep += conv.convert(var_dict=vdict)
                text = text[:start] + rep + text[end:]
                res = self.find_first(text)

            return text

        else:
            ret = ''
            remaining = text
            res = self.find_first(remaining)

            while res:
                _, start, end, vdict = res
                rep = ''
                for conv in converters:
                    rep += conv.convert(var_dict=vdict)
                ret += remaining[:start] + rep
                remaining = remaining[end:]
                if len(remaining) <= 0:
                    break
                res = self.find_first(remaining)

            return ret + remaining

    # def split(self):
