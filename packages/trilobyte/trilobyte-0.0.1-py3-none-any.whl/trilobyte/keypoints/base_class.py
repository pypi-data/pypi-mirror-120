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


from trilobyte.utils import duplicate_dict
import warnings


class Keypnt:
    def __init__(self, prop='default', name=None, track_var=False, var_name=None, var_dict=None, **kwargs):
        self.track_var = track_var
        self.var_name = var_name
        self.var_dict = var_dict

        if prop == 'default':
            self.prop_template = {
                'index': 0,
                'matched': False,
                'completed': False
            }
        else:
            self.prop_template = duplicate_dict(prop)
        self.prop_template = self.inject_var(self.prop_template)
        self.threads = {}
        self.current_thread = None

        self.name = name
        self.kwargs = kwargs

    def __reset__(self):
        self.__init__(duplicate_dict(self.prop_template))

    def __hard_reset__(self):
        self.__init__('default')

    def __reset_thread__(self, id):
        self.threads[id] = duplicate_dict(self.prop_template)

    def __reset_current_thread__(self):
        self.__reset_thread__(self.current_thread)

    def is_var(self):
        return self.var_name is not None

    def inject_var(self, prop):
        if self.is_var():
            prop['var'] = ''
            prop['var_completed'] = False
        return prop

    def varify(self, var_name, var_dict):
        self.var_name = var_name
        self.var_dict = var_dict
        self.prop_template = self.inject_var(self.prop_template)

    def add_prop(self, key, default_val):
        if key in self.prop_template:
            warnings.warn('\n\n  !!!  Key {} already exists in properties for {}\n'.format(key, repr(self)),
                          category=Warning)
        self.prop_template[key] = default_val

    def add_thread(self, id, prop='default'):
        if id in self.threads:
            warnings.warn('\n\n  !!!  Thread ID {} has already been used for {}\n'.format(id, repr(self)),
                          category=Warning)
        if prop == 'default':
            prop = duplicate_dict(self.prop_template)
        else:
            prop = self.inject_var(prop)
        self.threads[id] = prop

    def remove_thread(self, id):
        if not self.__verify_thread__(id):
            warnings.warn('\n\n  !!!  Bad thread ID {} for {}\n'.format(id, repr(self)), category=Warning)
        else:
            del self.threads[id]

    def __verify_thread__(self, id):
        return id in self.threads

    def get_current(self, key):
        return self.threads[self.current_thread][key]

    def set_current(self, key, val):
        self.threads[self.current_thread][key] = val
        return val

    def increment_current(self, key, inc):
        oldval = self.threads[self.current_thread][key]
        newval = oldval + inc
        self.threads[self.current_thread][key] = newval
        return newval

    def push_current_variable(self):
        if self.is_var():
            if self.current_thread in self.var_dict:
                self.var_dict[self.current_thread][self.var_name] = self.get_current('var')
            else:
                self.var_dict[self.current_thread] = {self.var_name: self.get_current('var')}

    def push_current_variable_override(self, thread_id):
        if self.is_var():
            if self.current_thread is None:
                val = ''
            else:
                val = self.get_current('var')
                if (val == '' and self.current_thread in self.var_dict and
                        self.var_name in self.var_dict[self.current_thread]):
                    val = self.var_dict[self.current_thread][self.var_name]

            if thread_id in self.var_dict:
                self.var_dict[thread_id][self.var_name] = val
            else:
                self.var_dict[thread_id] = {self.var_name: val}

    def set_current_variable(self, val):
        if self.is_var():
            self.set_current('var', val)

    def get_current_variable(self):
        if self.is_var():
            return self.get_current('var')

    def increment_current_variable(self, inc):
        if self.is_var():
            self.increment_current('var', inc)

    def handle_current_variable(self, c, matched, completed):
        if self.is_var():
            if matched:
                self.increment_current_variable(c)
                self.push_current_variable()
            elif not completed:
                self.increment_current_variable(c)

    def handle_current_variable_then_return(self, c, matched, completed):
        if self.is_var():
            self.handle_current_variable(c, matched, completed)
        return matched, completed

    def generic_return_with_variable_handle(self, c):
        if self.is_var():
            self.handle_current_variable(c, *self.generic_return())
        return self.generic_return()

    def inject_variable_string(self, s):
        if self.is_var():
            return '${}[{}]'.format(self.var_name, s)
        return s

    def resolve_args(self, flags, defaults, *args, **kwargs):
        ret = {}

        for i in range(len(args)):
            ret[flags[i]] = args[i]

        for k in kwargs:
            if k in flags:
                ret[k] = kwargs[k]

        for i in range(len(flags)):
            if flags[i] not in ret:
                ret[flags[i]] = defaults[i]

        return ret

    def generic_return(self):
        return self.get_current('matched'), self.get_current('completed')

    def __str__(self):
        pass  # To implement

    def __len__(self):
        pass  # To implement

    def __struct__(self):  # To override
        return {'{Keypnt name}': {
            'args': '{args}}'
        }, 'type': '{Keypnt name}', 'pattern_decorator': bool, 'singular': bool, 'deco_key': '{pattern_arg}'}
        # `singular` and `deco_key` required only when `pattern_decorator == True`

    def __repr__(self):
        s = str(self)
        s = s.replace('"', '\\"')
        return '<trilo.tr: type: {}, value: "{}"; at {}>'.format(self.__struct__()['type'], s, hex(id(self)))

    def match(self, thread_id, *args, **kwargs):
        pass  # To implement

    def begins_with(self, c, **kwargs):
        if c is None:
            return False
        pass  # To implement

    def copy(self, preserve_vars=False):
        struct = self.__struct__()
        pattern_type = struct['type']
        kwargs = struct[pattern_type]
        if preserve_vars:
            kwargs['var_name'] = self.var_name
            kwargs['var_dict'] = self.var_dict
        return type(self)(**kwargs)
