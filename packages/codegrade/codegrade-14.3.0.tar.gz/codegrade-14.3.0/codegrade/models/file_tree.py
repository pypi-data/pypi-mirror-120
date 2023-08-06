"""The module that defines the ``FileTree`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
import typing as t
from dataclasses import dataclass, field

import cg_request_args as rqa
from cg_maybe import Maybe, Nothing
from cg_maybe.utils import maybe_from_nullable

from .. import parsers
from ..utils import to_dict
from .base_file import BaseFile


@dataclass
class FileTree(BaseFile):
    """The FileTree represented as JSON."""

    #: The entries in this directory. This is a list that will contain all
    #: children of the directory. This key might not be present, in which case
    #: the file is not a directory.
    entries: Maybe["t.Sequence[FileTree]"] = Nothing

    raw_data: t.Optional[t.Dict[str, t.Any]] = field(init=False, repr=False)

    data_parser: t.ClassVar = rqa.Lazy(
        lambda: BaseFile.data_parser.parser.combine(
            rqa.FixedMapping(
                rqa.OptionalArgument(
                    "entries",
                    rqa.List(parsers.ParserFor.make(FileTree)),
                    doc=(
                        "The entries in this directory. This is a list that"
                        " will contain all children of the directory. This key"
                        " might not be present, in which case the file is not"
                        " a directory."
                    ),
                ),
            )
        ).use_readable_describe(True)
    )

    def __post_init__(self) -> None:
        getattr(super(), "__post_init__", lambda: None)()
        self.entries = maybe_from_nullable(self.entries)

    def to_dict(self) -> t.Dict[str, t.Any]:
        res: t.Dict[str, t.Any] = {
            "id": to_dict(self.id),
            "name": to_dict(self.name),
        }
        if self.entries.is_just:
            res["entries"] = to_dict(self.entries.value)
        return res

    @classmethod
    def from_dict(
        cls: t.Type["FileTree"], d: t.Dict[str, t.Any]
    ) -> "FileTree":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            id=parsed.id,
            name=parsed.name,
            entries=parsed.entries,
        )
        res.raw_data = d
        return res
