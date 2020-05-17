# -*- coding: utf-8 -*-

from voluptuous import Length, All, Coerce, Required, Range


int_range = All(Coerce(int), Range(min=1, max=150))
only_num_id = All(Coerce(str), Length(min=10, max=20))

page_schema = {
    Required("page"): int_range,
    Required("page_size"): int_range
}

