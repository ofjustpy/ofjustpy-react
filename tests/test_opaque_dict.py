from addict_tracking_changes import Dict

from typing import NamedTuple

from typing import NamedTuple, Any, Type

from typing import NamedTuple, Any, Type
from collections import namedtuple

def make_opaque_dict(adict: dict):
    fields = adict.keys()
    print (fields)
    tpl_cls = namedtuple("tt", fields)
    return  tpl_cls(*adict.values())
    




adict = {'a': 1,
         'b': 2,
         'c': {'c1': 1, 'c2':2}
         }
X = make_opaque_dict(adict)
print(X.a)  # prints 1
print(X.b)  # prints 2
print(X.c)  # prints 3


aa = Dict(track_changes=1)
# dc = make_opaque_dict_class({'h':1})
aa.X = X

for _ in aa.get_changed_history():
    print(_)
    
z = Dict(aa.X._asdict())
print(z.c.c2)
