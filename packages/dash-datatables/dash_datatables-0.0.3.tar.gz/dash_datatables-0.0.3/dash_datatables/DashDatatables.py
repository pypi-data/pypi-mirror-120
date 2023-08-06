# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class DashDatatables(Component):
    """A DashDatatables component.
Wrapper for Datatables

Keyword arguments:

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- ajax (string; optional):
    Load data for the table's content from an Ajax source
    https://datatables.net/reference/option/ajax.

- className (string; default 'table table-sm table-striped table-bordered'):
    The tables class name.

- column_defs (list; optional):
    Allows you to assign specific options to columns  in the table,
    see:  https://datatables.net/reference/option/columnDefs.

- columns (list; optional):
    Column names and attributes.

- data (list; optional):
    Table data.

- editable (boolean; default False):
    Set `True` to enable row editing.

- footer_values (list of strings; optional):
    Table footer column values.

- order (list; optional):
    Sort order.

- pagelength (number; default 25):
    Number of rows on a page.

- table_event (boolean | number | string | dict | list; optional):
    Report table events.

- width (string; optional):
    Percentage of container to use for table."""
    @_explicitize_args
    def __init__(self, ajax=Component.UNDEFINED, id=Component.UNDEFINED, editable=Component.UNDEFINED, data=Component.UNDEFINED, columns=Component.UNDEFINED, column_defs=Component.UNDEFINED, table_event=Component.UNDEFINED, footer_values=Component.UNDEFINED, order=Component.UNDEFINED, pagelength=Component.UNDEFINED, width=Component.UNDEFINED, className=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'ajax', 'className', 'column_defs', 'columns', 'data', 'editable', 'footer_values', 'order', 'pagelength', 'table_event', 'width']
        self._type = 'DashDatatables'
        self._namespace = 'dash_datatables'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'ajax', 'className', 'column_defs', 'columns', 'data', 'editable', 'footer_values', 'order', 'pagelength', 'table_event', 'width']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}
        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(DashDatatables, self).__init__(**args)
