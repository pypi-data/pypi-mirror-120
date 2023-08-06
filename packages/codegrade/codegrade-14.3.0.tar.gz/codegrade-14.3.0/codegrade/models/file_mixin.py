"""The module that defines the ``FileMixin`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
import typing as t
from dataclasses import dataclass, field

import cg_request_args as rqa

from ..utils import to_dict


@dataclass
class FileMixin:
    """The base JSON representation of a file."""

    #: The id of this file
    id: "str"
    #: The local name of this file, this does **not** include any parent
    #: directory names, nor does it include trailing slashes for directories.
    name: "str"

    raw_data: t.Optional[t.Dict[str, t.Any]] = field(init=False, repr=False)

    data_parser: t.ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "id",
                rqa.SimpleValue.str,
                doc="The id of this file",
            ),
            rqa.RequiredArgument(
                "name",
                rqa.SimpleValue.str,
                doc=(
                    "The local name of this file, this does **not** include"
                    " any parent directory names, nor does it include trailing"
                    " slashes for directories."
                ),
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> t.Dict[str, t.Any]:
        res: t.Dict[str, t.Any] = {
            "id": to_dict(self.id),
            "name": to_dict(self.name),
        }
        return res

    @classmethod
    def from_dict(
        cls: t.Type["FileMixin"], d: t.Dict[str, t.Any]
    ) -> "FileMixin":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            id=parsed.id,
            name=parsed.name,
        )
        res.raw_data = d
        return res
