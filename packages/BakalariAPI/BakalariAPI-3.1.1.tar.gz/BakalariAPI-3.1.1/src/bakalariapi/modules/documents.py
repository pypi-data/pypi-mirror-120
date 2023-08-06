"""Modul obsahující funkce týkající se dokumentů."""
from typing import cast

from bs4.element import Tag  # Kvůli mypy - https://github.com/python/mypy/issues/10826

from ..bakalari import BakalariAPI, Endpoint, _register_parser
from ..looting import GetterOutput, ResultSet

# from ..objects import Grade
# from ..sessions import RequestsSession