import inspect
import types
from typing import Any, Dict, List, Optional, Tuple, Union

from rich.console import Console
from rich.highlighter import ReprHighlighter
from rich.pretty import Pretty
from rich.style import Style
from rich.syntax import Syntax
from rich.text import Text

from .utils import is_selectable

highlighter = ReprHighlighter()


PUBLIC = "PUBLIC"
PRIVATE = "PRIVATE"

console = Console()


def safegetattr(obj, attr):
    try:
        return getattr(obj, attr)
    except Exception:
        return None


class CachedObject:
    def __init__(
        self,
        obj: Any,
        parent_path: Text = None,
        attr_name: str = None,
        index: Any = None,
    ):
        self.obj = obj
        self.is_callable = callable(obj)
        self.selected_cached_obj: CachedObject
        self.plain_attrs = dir(self.obj)

        if self.obj is None:
            self.dotpath = highlighter("None")

        elif attr_name is not None:
            if not parent_path:
                self.dotpath = Text(attr_name, style=Style(color="cyan"))
            else:
                self.dotpath = (
                    parent_path
                    + Text(".", style=Style(color="white"))
                    + Text(attr_name, style=Style(color="cyan"))
                )

        elif index is not None:
            if type(index) == str:
                repr_index = console.render_str(f'"{index}"')
            else:
                repr_index = console.render_str(str(index))
            if not parent_path:
                self.dotpath = (
                    Text("[", style=Style(color="white"))
                    + repr_index
                    + Text("]", style=Style(color="white"))
                )
            else:
                self.dotpath = (
                    parent_path
                    + Text("[", style=Style(color="white"))
                    + repr_index
                    + Text("]", style=Style(color="white"))
                )
        else:
            raise ValueError("Need to specify an attribute name or an index")

        self.attr_name = attr_name if attr_name else repr(self.obj)

        if "__weakref__" in self.plain_attrs:
            # Ignore weakrefs
            self.plain_attrs.remove("__weakref__")

        self.plain_public_attributes = sorted(
            attr for attr in self.plain_attrs if not attr.startswith("_")
        )
        self.plain_private_attributes = sorted(
            attr for attr in self.plain_attrs if attr.startswith("_")
        )

        self.public_attributes: Dict[str, CachedObject] = {}
        self.private_attributes: Dict[str, CachedObject] = {}
        self.filtered_public_attributes: Dict[str, CachedObject] = {}
        self.filtered_private_attributes: Dict[str, CachedObject] = {}
        # TODO display # of hidden items?
        # self._hidden_public_attributes = {}
        # self._hidden_private_attributes = {}

        try:
            self._source = inspect.getsource(self.obj)  # type: ignore
        except Exception:
            self._source = ""

        self.length: Optional[str]

        try:
            self.length = str(len(self.obj))  # type: ignore
        except TypeError:
            self.length = None

        self.isbuiltin = inspect.isbuiltin(self.obj)
        self.isclass = inspect.isclass(self.obj)
        self.isclass = inspect.isclass(self.obj)
        self.isfunction = inspect.isfunction(self.obj)
        self.ismethod = inspect.ismethod(self.obj)
        self.ismodule = inspect.ismodule(self.obj)
        self.filters: List[types.FunctionType] = []

        # Highlighted attributes
        self.typeof: Text = highlighter(str(type(self.obj)))
        self.docstring: Text = console.render_str(inspect.getdoc(self.obj) or "None")
        self.docstring_lines = self.docstring.split()
        self.repr = highlighter(repr(self.obj))
        self.repr.overflow = "ellipsis"
        self.pretty = Pretty(self.obj)

        self.text = Text(self.attr_name, style=Style(), overflow="ellipsis")
        if self.ismodule:
            self.text.style = Style(color="blue")
        elif self.isclass:
            self.text.style = Style(color="magenta")
        if self.isfunction:
            self.text += Text("()", style=Style(color="white"))
        # elif callable(self.obj):
        #     pass
        #     # self.text.style = Style(color="yellow", dim=True)
        elif type(self.obj) in (dict, set):
            self.text += Text("{}", style=Style(color="white"))
        elif type(self.obj) == list:
            self.text += Text("[]", style=Style(color="white"))
        elif type(self.obj) == tuple:
            self.text += Text("()", style=Style(color="white"))
        elif self.obj in (None, (), {}, [], set()):
            self.text.style = Style(dim=True, italic=True)
        # else:
        #     self.text.style = Style()

    @property
    def title(self):
        # for cases when the object is a huge dictionary we shouldnt try to render the whole dict
        if len(self.repr.plain) > console.width - 4:
            return Text(self.attr_name) + Text(" ") + self.typeof
        title = self.repr.copy()
        title.truncate(console.width - 4)
        return title

    def cache(self):
        if not self.public_attributes:
            for attr in self.plain_public_attributes:
                self.public_attributes[attr] = CachedObject(
                    safegetattr(self.obj, attr),
                    parent_path=self.dotpath,
                    attr_name=attr,
                )

        if not self.private_attributes:
            for attr in self.plain_private_attributes:
                self.private_attributes[attr] = CachedObject(
                    safegetattr(self.obj, attr),
                    parent_path=self.dotpath,
                    attr_name=attr,
                )

        self.filter()

    def set_filters(self, filters: List[types.FunctionType]):
        self.filters = filters
        self.filter()

    def filter(self):
        self.filtered_public_attributes = {}
        if not self.filters:
            self.filtered_public_attributes = self.public_attributes
        else:
            for attr, cached_obj in self.public_attributes.items():
                # Only keep objects that match the filter
                for _filter in self.filters:
                    if _filter(cached_obj):
                        self.filtered_public_attributes[attr] = cached_obj
                        break

        self.filtered_private_attributes = {}
        if not self.filters:
            self.filtered_private_attributes = self.private_attributes
        else:
            for attr, cached_obj in self.private_attributes.items():
                # Only keep objects that match the filter
                for _filter in self.filters:
                    if _filter(cached_obj):
                        self.filtered_private_attributes[attr] = cached_obj
                        break

        self.filtered_dict: Dict[str, Tuple[Text, CachedObject]] = {}
        if type(self.obj) == dict:
            for key, val in self.obj.items():
                repr_key: Text
                repr_val: Text

                if type(key) == str:
                    repr_key = console.render_str(f'"{key}"')
                elif type(key) in (int, float, dict, list, set, tuple, bool, None):
                    repr_key = console.render_str(str(key))
                else:
                    repr_key = highlighter(str(key))

                repr_val = highlighter(str(type(val)))

                if not is_selectable(val):
                    repr_val.style += " dim italic"
                    repr_val.style = repr_val.style.strip()

                line = Text(" ") + repr_key + Text(": ") + repr_val
                line.overflow = "ellipsis"
                self.filtered_dict[key] = (
                    line,
                    CachedObject(val, parent_path=self.dotpath, index=key),
                )
            if self.filters:
                for attr, (line, cached_obj) in self.filtered_dict.copy().items():
                    for _filter in self.filters:
                        if _filter(cached_obj):
                            self.filtered_dict[attr] = (line, cached_obj)
                            break
                    else:
                        del self.filtered_dict[attr]

        self.filtered_list: List[Tuple[Text, CachedObject]] = []
        if type(self.obj) in (list, tuple, set):

            for index, item in enumerate(self.obj):
                line = (
                    Text(" [", style=Style(color="white"))
                    + Text(str(index), style=Style(color="blue"))
                    + Text("] ", style=Style(color="white"))
                    + highlighter(str(type(item)))
                )
                if not is_selectable(item):
                    line.style += Style(dim=True, italic=True)

                self.filtered_list.append(
                    (line, CachedObject(item, parent_path=self.dotpath, index=index))
                )
            if self.filters:
                new_filtered_list: List[Tuple[Text, CachedObject]] = []
                for line, cached_obj in self.filtered_list:
                    for _filter in self.filters:
                        if _filter(cached_obj):
                            new_filtered_list.append((line, cached_obj))
                            break
                self.filtered_list = new_filtered_list

    def get_source(
        self, term_height: int = 0, fullscreen: bool = False
    ) -> Union[Syntax, str]:
        if not fullscreen and not term_height:
            raise ValueError("Need a terminal height")

        if not self._source:
            return "[red italic]Source code unavailable"

        if fullscreen:
            return Syntax(
                self._source, "python", line_numbers=True, background_color="default"
            )
        else:
            return Syntax(
                self._source,
                "python",
                line_numbers=True,
                line_range=(0, term_height),
                background_color="default",
            )
