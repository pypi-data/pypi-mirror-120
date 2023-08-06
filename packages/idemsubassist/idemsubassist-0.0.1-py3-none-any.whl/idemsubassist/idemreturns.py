import pprint
import json

class StateReturn(dict):
    def __init__(self,
            name = None, result = None, old_obj = None, new_obj = None, comment = None):
        p = pprint.PrettyPrinter()
        super(StateReturn, self).__init__([
            ('name', name),
            ('result', result),
            ('comment', comment),
            ('changes', p.pformat(dict([
                    ('old', old_obj),
                    ('new', new_obj)
            ])))
        ])
