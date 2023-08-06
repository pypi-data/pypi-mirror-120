"""The module that defines the ``SiteSettingInput`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
import typing as t
from dataclasses import dataclass, field

import cg_request_args as rqa

from .. import parsers
from ..parsers import ParserFor, make_union
from ..utils import to_dict


@dataclass
class AutoTestMaxTimeCommandSetting:
    """ """

    name: "t.Literal['AUTO_TEST_MAX_TIME_COMMAND']"
    value: "t.Optional[t.Union[int, int, str]]"

    raw_data: t.Optional[t.Dict[str, t.Any]] = field(init=False, repr=False)

    data_parser: t.ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "name",
                rqa.StringEnum("AUTO_TEST_MAX_TIME_COMMAND"),
                doc="",
            ),
            rqa.RequiredArgument(
                "value",
                rqa.Nullable(
                    parsers.make_union(
                        rqa.SimpleValue.int,
                        rqa.SimpleValue.int,
                        rqa.SimpleValue.str,
                    )
                ),
                doc="",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> t.Dict[str, t.Any]:
        res: t.Dict[str, t.Any] = {
            "name": to_dict(self.name),
            "value": to_dict(self.value),
        }
        return res

    @classmethod
    def from_dict(
        cls: t.Type["AutoTestMaxTimeCommandSetting"], d: t.Dict[str, t.Any]
    ) -> "AutoTestMaxTimeCommandSetting":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            name=parsed.name,
            value=parsed.value,
        )
        res.raw_data = d
        return res


@dataclass
class AutoTestHeartbeatIntervalSetting:
    """ """

    name: "t.Literal['AUTO_TEST_HEARTBEAT_INTERVAL']"
    value: "t.Optional[t.Union[int, int, str]]"

    raw_data: t.Optional[t.Dict[str, t.Any]] = field(init=False, repr=False)

    data_parser: t.ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "name",
                rqa.StringEnum("AUTO_TEST_HEARTBEAT_INTERVAL"),
                doc="",
            ),
            rqa.RequiredArgument(
                "value",
                rqa.Nullable(
                    parsers.make_union(
                        rqa.SimpleValue.int,
                        rqa.SimpleValue.int,
                        rqa.SimpleValue.str,
                    )
                ),
                doc="",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> t.Dict[str, t.Any]:
        res: t.Dict[str, t.Any] = {
            "name": to_dict(self.name),
            "value": to_dict(self.value),
        }
        return res

    @classmethod
    def from_dict(
        cls: t.Type["AutoTestHeartbeatIntervalSetting"], d: t.Dict[str, t.Any]
    ) -> "AutoTestHeartbeatIntervalSetting":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            name=parsed.name,
            value=parsed.value,
        )
        res.raw_data = d
        return res


@dataclass
class AutoTestHeartbeatMaxMissedSetting:
    """ """

    name: "t.Literal['AUTO_TEST_HEARTBEAT_MAX_MISSED']"
    value: "t.Optional[int]"

    raw_data: t.Optional[t.Dict[str, t.Any]] = field(init=False, repr=False)

    data_parser: t.ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "name",
                rqa.StringEnum("AUTO_TEST_HEARTBEAT_MAX_MISSED"),
                doc="",
            ),
            rqa.RequiredArgument(
                "value",
                rqa.Nullable(rqa.SimpleValue.int),
                doc="",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> t.Dict[str, t.Any]:
        res: t.Dict[str, t.Any] = {
            "name": to_dict(self.name),
            "value": to_dict(self.value),
        }
        return res

    @classmethod
    def from_dict(
        cls: t.Type["AutoTestHeartbeatMaxMissedSetting"], d: t.Dict[str, t.Any]
    ) -> "AutoTestHeartbeatMaxMissedSetting":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            name=parsed.name,
            value=parsed.value,
        )
        res.raw_data = d
        return res


@dataclass
class AutoTestMaxJobsPerRunnerSetting:
    """ """

    name: "t.Literal['AUTO_TEST_MAX_JOBS_PER_RUNNER']"
    value: "t.Optional[int]"

    raw_data: t.Optional[t.Dict[str, t.Any]] = field(init=False, repr=False)

    data_parser: t.ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "name",
                rqa.StringEnum("AUTO_TEST_MAX_JOBS_PER_RUNNER"),
                doc="",
            ),
            rqa.RequiredArgument(
                "value",
                rqa.Nullable(rqa.SimpleValue.int),
                doc="",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> t.Dict[str, t.Any]:
        res: t.Dict[str, t.Any] = {
            "name": to_dict(self.name),
            "value": to_dict(self.value),
        }
        return res

    @classmethod
    def from_dict(
        cls: t.Type["AutoTestMaxJobsPerRunnerSetting"], d: t.Dict[str, t.Any]
    ) -> "AutoTestMaxJobsPerRunnerSetting":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            name=parsed.name,
            value=parsed.value,
        )
        res.raw_data = d
        return res


@dataclass
class AutoTestMaxConcurrentBatchRunsSetting:
    """ """

    name: "t.Literal['AUTO_TEST_MAX_CONCURRENT_BATCH_RUNS']"
    value: "t.Optional[int]"

    raw_data: t.Optional[t.Dict[str, t.Any]] = field(init=False, repr=False)

    data_parser: t.ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "name",
                rqa.StringEnum("AUTO_TEST_MAX_CONCURRENT_BATCH_RUNS"),
                doc="",
            ),
            rqa.RequiredArgument(
                "value",
                rqa.Nullable(rqa.SimpleValue.int),
                doc="",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> t.Dict[str, t.Any]:
        res: t.Dict[str, t.Any] = {
            "name": to_dict(self.name),
            "value": to_dict(self.value),
        }
        return res

    @classmethod
    def from_dict(
        cls: t.Type["AutoTestMaxConcurrentBatchRunsSetting"],
        d: t.Dict[str, t.Any],
    ) -> "AutoTestMaxConcurrentBatchRunsSetting":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            name=parsed.name,
            value=parsed.value,
        )
        res.raw_data = d
        return res


@dataclass
class AutoTestIoTestMessageSetting:
    """ """

    name: "t.Literal['AUTO_TEST_IO_TEST_MESSAGE']"
    value: "t.Optional[str]"

    raw_data: t.Optional[t.Dict[str, t.Any]] = field(init=False, repr=False)

    data_parser: t.ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "name",
                rqa.StringEnum("AUTO_TEST_IO_TEST_MESSAGE"),
                doc="",
            ),
            rqa.RequiredArgument(
                "value",
                rqa.Nullable(rqa.SimpleValue.str),
                doc="",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> t.Dict[str, t.Any]:
        res: t.Dict[str, t.Any] = {
            "name": to_dict(self.name),
            "value": to_dict(self.value),
        }
        return res

    @classmethod
    def from_dict(
        cls: t.Type["AutoTestIoTestMessageSetting"], d: t.Dict[str, t.Any]
    ) -> "AutoTestIoTestMessageSetting":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            name=parsed.name,
            value=parsed.value,
        )
        res.raw_data = d
        return res


@dataclass
class AutoTestIoTestSubMessageSetting:
    """ """

    name: "t.Literal['AUTO_TEST_IO_TEST_SUB_MESSAGE']"
    value: "t.Optional[str]"

    raw_data: t.Optional[t.Dict[str, t.Any]] = field(init=False, repr=False)

    data_parser: t.ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "name",
                rqa.StringEnum("AUTO_TEST_IO_TEST_SUB_MESSAGE"),
                doc="",
            ),
            rqa.RequiredArgument(
                "value",
                rqa.Nullable(rqa.SimpleValue.str),
                doc="",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> t.Dict[str, t.Any]:
        res: t.Dict[str, t.Any] = {
            "name": to_dict(self.name),
            "value": to_dict(self.value),
        }
        return res

    @classmethod
    def from_dict(
        cls: t.Type["AutoTestIoTestSubMessageSetting"], d: t.Dict[str, t.Any]
    ) -> "AutoTestIoTestSubMessageSetting":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            name=parsed.name,
            value=parsed.value,
        )
        res.raw_data = d
        return res


@dataclass
class AutoTestRunProgramMessageSetting:
    """ """

    name: "t.Literal['AUTO_TEST_RUN_PROGRAM_MESSAGE']"
    value: "t.Optional[str]"

    raw_data: t.Optional[t.Dict[str, t.Any]] = field(init=False, repr=False)

    data_parser: t.ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "name",
                rqa.StringEnum("AUTO_TEST_RUN_PROGRAM_MESSAGE"),
                doc="",
            ),
            rqa.RequiredArgument(
                "value",
                rqa.Nullable(rqa.SimpleValue.str),
                doc="",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> t.Dict[str, t.Any]:
        res: t.Dict[str, t.Any] = {
            "name": to_dict(self.name),
            "value": to_dict(self.value),
        }
        return res

    @classmethod
    def from_dict(
        cls: t.Type["AutoTestRunProgramMessageSetting"], d: t.Dict[str, t.Any]
    ) -> "AutoTestRunProgramMessageSetting":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            name=parsed.name,
            value=parsed.value,
        )
        res.raw_data = d
        return res


@dataclass
class AutoTestCapturePointsMessageSetting:
    """ """

    name: "t.Literal['AUTO_TEST_CAPTURE_POINTS_MESSAGE']"
    value: "t.Optional[str]"

    raw_data: t.Optional[t.Dict[str, t.Any]] = field(init=False, repr=False)

    data_parser: t.ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "name",
                rqa.StringEnum("AUTO_TEST_CAPTURE_POINTS_MESSAGE"),
                doc="",
            ),
            rqa.RequiredArgument(
                "value",
                rqa.Nullable(rqa.SimpleValue.str),
                doc="",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> t.Dict[str, t.Any]:
        res: t.Dict[str, t.Any] = {
            "name": to_dict(self.name),
            "value": to_dict(self.value),
        }
        return res

    @classmethod
    def from_dict(
        cls: t.Type["AutoTestCapturePointsMessageSetting"],
        d: t.Dict[str, t.Any],
    ) -> "AutoTestCapturePointsMessageSetting":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            name=parsed.name,
            value=parsed.value,
        )
        res.raw_data = d
        return res


@dataclass
class AutoTestCheckpointMessageSetting:
    """ """

    name: "t.Literal['AUTO_TEST_CHECKPOINT_MESSAGE']"
    value: "t.Optional[str]"

    raw_data: t.Optional[t.Dict[str, t.Any]] = field(init=False, repr=False)

    data_parser: t.ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "name",
                rqa.StringEnum("AUTO_TEST_CHECKPOINT_MESSAGE"),
                doc="",
            ),
            rqa.RequiredArgument(
                "value",
                rqa.Nullable(rqa.SimpleValue.str),
                doc="",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> t.Dict[str, t.Any]:
        res: t.Dict[str, t.Any] = {
            "name": to_dict(self.name),
            "value": to_dict(self.value),
        }
        return res

    @classmethod
    def from_dict(
        cls: t.Type["AutoTestCheckpointMessageSetting"], d: t.Dict[str, t.Any]
    ) -> "AutoTestCheckpointMessageSetting":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            name=parsed.name,
            value=parsed.value,
        )
        res.raw_data = d
        return res


@dataclass
class AutoTestUnitTestMessageSetting:
    """ """

    name: "t.Literal['AUTO_TEST_UNIT_TEST_MESSAGE']"
    value: "t.Optional[str]"

    raw_data: t.Optional[t.Dict[str, t.Any]] = field(init=False, repr=False)

    data_parser: t.ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "name",
                rqa.StringEnum("AUTO_TEST_UNIT_TEST_MESSAGE"),
                doc="",
            ),
            rqa.RequiredArgument(
                "value",
                rqa.Nullable(rqa.SimpleValue.str),
                doc="",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> t.Dict[str, t.Any]:
        res: t.Dict[str, t.Any] = {
            "name": to_dict(self.name),
            "value": to_dict(self.value),
        }
        return res

    @classmethod
    def from_dict(
        cls: t.Type["AutoTestUnitTestMessageSetting"], d: t.Dict[str, t.Any]
    ) -> "AutoTestUnitTestMessageSetting":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            name=parsed.name,
            value=parsed.value,
        )
        res.raw_data = d
        return res


@dataclass
class AutoTestCodeQualityMessageSetting:
    """ """

    name: "t.Literal['AUTO_TEST_CODE_QUALITY_MESSAGE']"
    value: "t.Optional[str]"

    raw_data: t.Optional[t.Dict[str, t.Any]] = field(init=False, repr=False)

    data_parser: t.ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "name",
                rqa.StringEnum("AUTO_TEST_CODE_QUALITY_MESSAGE"),
                doc="",
            ),
            rqa.RequiredArgument(
                "value",
                rqa.Nullable(rqa.SimpleValue.str),
                doc="",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> t.Dict[str, t.Any]:
        res: t.Dict[str, t.Any] = {
            "name": to_dict(self.name),
            "value": to_dict(self.value),
        }
        return res

    @classmethod
    def from_dict(
        cls: t.Type["AutoTestCodeQualityMessageSetting"], d: t.Dict[str, t.Any]
    ) -> "AutoTestCodeQualityMessageSetting":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            name=parsed.name,
            value=parsed.value,
        )
        res.raw_data = d
        return res


@dataclass
class AutoTestMaxResultNotStartedSetting:
    """ """

    name: "t.Literal['AUTO_TEST_MAX_RESULT_NOT_STARTED']"
    value: "t.Optional[t.Union[int, int, str]]"

    raw_data: t.Optional[t.Dict[str, t.Any]] = field(init=False, repr=False)

    data_parser: t.ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "name",
                rqa.StringEnum("AUTO_TEST_MAX_RESULT_NOT_STARTED"),
                doc="",
            ),
            rqa.RequiredArgument(
                "value",
                rqa.Nullable(
                    parsers.make_union(
                        rqa.SimpleValue.int,
                        rqa.SimpleValue.int,
                        rqa.SimpleValue.str,
                    )
                ),
                doc="",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> t.Dict[str, t.Any]:
        res: t.Dict[str, t.Any] = {
            "name": to_dict(self.name),
            "value": to_dict(self.value),
        }
        return res

    @classmethod
    def from_dict(
        cls: t.Type["AutoTestMaxResultNotStartedSetting"],
        d: t.Dict[str, t.Any],
    ) -> "AutoTestMaxResultNotStartedSetting":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            name=parsed.name,
            value=parsed.value,
        )
        res.raw_data = d
        return res


@dataclass
class AutoTestMaxUnitTestMetadataLengthSetting:
    """ """

    name: "t.Literal['AUTO_TEST_MAX_UNIT_TEST_METADATA_LENGTH']"
    value: "t.Optional[t.Union[int, str]]"

    raw_data: t.Optional[t.Dict[str, t.Any]] = field(init=False, repr=False)

    data_parser: t.ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "name",
                rqa.StringEnum("AUTO_TEST_MAX_UNIT_TEST_METADATA_LENGTH"),
                doc="",
            ),
            rqa.RequiredArgument(
                "value",
                rqa.Nullable(
                    parsers.make_union(
                        rqa.SimpleValue.int, rqa.SimpleValue.str
                    )
                ),
                doc="",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> t.Dict[str, t.Any]:
        res: t.Dict[str, t.Any] = {
            "name": to_dict(self.name),
            "value": to_dict(self.value),
        }
        return res

    @classmethod
    def from_dict(
        cls: t.Type["AutoTestMaxUnitTestMetadataLengthSetting"],
        d: t.Dict[str, t.Any],
    ) -> "AutoTestMaxUnitTestMetadataLengthSetting":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            name=parsed.name,
            value=parsed.value,
        )
        res.raw_data = d
        return res


@dataclass
class ExamLoginMaxLengthSetting:
    """ """

    name: "t.Literal['EXAM_LOGIN_MAX_LENGTH']"
    value: "t.Optional[t.Union[int, int, str]]"

    raw_data: t.Optional[t.Dict[str, t.Any]] = field(init=False, repr=False)

    data_parser: t.ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "name",
                rqa.StringEnum("EXAM_LOGIN_MAX_LENGTH"),
                doc="",
            ),
            rqa.RequiredArgument(
                "value",
                rqa.Nullable(
                    parsers.make_union(
                        rqa.SimpleValue.int,
                        rqa.SimpleValue.int,
                        rqa.SimpleValue.str,
                    )
                ),
                doc="",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> t.Dict[str, t.Any]:
        res: t.Dict[str, t.Any] = {
            "name": to_dict(self.name),
            "value": to_dict(self.value),
        }
        return res

    @classmethod
    def from_dict(
        cls: t.Type["ExamLoginMaxLengthSetting"], d: t.Dict[str, t.Any]
    ) -> "ExamLoginMaxLengthSetting":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            name=parsed.name,
            value=parsed.value,
        )
        res.raw_data = d
        return res


@dataclass
class LoginTokenBeforeTimeSetting:
    """ """

    name: "t.Literal['LOGIN_TOKEN_BEFORE_TIME']"
    value: "t.Optional[t.Sequence[t.Union[int, int, str]]]"

    raw_data: t.Optional[t.Dict[str, t.Any]] = field(init=False, repr=False)

    data_parser: t.ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "name",
                rqa.StringEnum("LOGIN_TOKEN_BEFORE_TIME"),
                doc="",
            ),
            rqa.RequiredArgument(
                "value",
                rqa.Nullable(
                    rqa.List(
                        parsers.make_union(
                            rqa.SimpleValue.int,
                            rqa.SimpleValue.int,
                            rqa.SimpleValue.str,
                        )
                    )
                ),
                doc="",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> t.Dict[str, t.Any]:
        res: t.Dict[str, t.Any] = {
            "name": to_dict(self.name),
            "value": to_dict(self.value),
        }
        return res

    @classmethod
    def from_dict(
        cls: t.Type["LoginTokenBeforeTimeSetting"], d: t.Dict[str, t.Any]
    ) -> "LoginTokenBeforeTimeSetting":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            name=parsed.name,
            value=parsed.value,
        )
        res.raw_data = d
        return res


@dataclass
class MinPasswordScoreSetting:
    """ """

    name: "t.Literal['MIN_PASSWORD_SCORE']"
    value: "t.Optional[int]"

    raw_data: t.Optional[t.Dict[str, t.Any]] = field(init=False, repr=False)

    data_parser: t.ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "name",
                rqa.StringEnum("MIN_PASSWORD_SCORE"),
                doc="",
            ),
            rqa.RequiredArgument(
                "value",
                rqa.Nullable(rqa.SimpleValue.int),
                doc="",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> t.Dict[str, t.Any]:
        res: t.Dict[str, t.Any] = {
            "name": to_dict(self.name),
            "value": to_dict(self.value),
        }
        return res

    @classmethod
    def from_dict(
        cls: t.Type["MinPasswordScoreSetting"], d: t.Dict[str, t.Any]
    ) -> "MinPasswordScoreSetting":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            name=parsed.name,
            value=parsed.value,
        )
        res.raw_data = d
        return res


@dataclass
class ResetTokenTimeSetting:
    """ """

    name: "t.Literal['RESET_TOKEN_TIME']"
    value: "t.Optional[t.Union[int, int, str]]"

    raw_data: t.Optional[t.Dict[str, t.Any]] = field(init=False, repr=False)

    data_parser: t.ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "name",
                rqa.StringEnum("RESET_TOKEN_TIME"),
                doc="",
            ),
            rqa.RequiredArgument(
                "value",
                rqa.Nullable(
                    parsers.make_union(
                        rqa.SimpleValue.int,
                        rqa.SimpleValue.int,
                        rqa.SimpleValue.str,
                    )
                ),
                doc="",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> t.Dict[str, t.Any]:
        res: t.Dict[str, t.Any] = {
            "name": to_dict(self.name),
            "value": to_dict(self.value),
        }
        return res

    @classmethod
    def from_dict(
        cls: t.Type["ResetTokenTimeSetting"], d: t.Dict[str, t.Any]
    ) -> "ResetTokenTimeSetting":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            name=parsed.name,
            value=parsed.value,
        )
        res.raw_data = d
        return res


@dataclass
class SettingTokenTimeSetting:
    """ """

    name: "t.Literal['SETTING_TOKEN_TIME']"
    value: "t.Optional[t.Union[int, int, str]]"

    raw_data: t.Optional[t.Dict[str, t.Any]] = field(init=False, repr=False)

    data_parser: t.ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "name",
                rqa.StringEnum("SETTING_TOKEN_TIME"),
                doc="",
            ),
            rqa.RequiredArgument(
                "value",
                rqa.Nullable(
                    parsers.make_union(
                        rqa.SimpleValue.int,
                        rqa.SimpleValue.int,
                        rqa.SimpleValue.str,
                    )
                ),
                doc="",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> t.Dict[str, t.Any]:
        res: t.Dict[str, t.Any] = {
            "name": to_dict(self.name),
            "value": to_dict(self.value),
        }
        return res

    @classmethod
    def from_dict(
        cls: t.Type["SettingTokenTimeSetting"], d: t.Dict[str, t.Any]
    ) -> "SettingTokenTimeSetting":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            name=parsed.name,
            value=parsed.value,
        )
        res.raw_data = d
        return res


@dataclass
class SiteEmailSetting:
    """ """

    name: "t.Literal['SITE_EMAIL']"
    value: "t.Optional[str]"

    raw_data: t.Optional[t.Dict[str, t.Any]] = field(init=False, repr=False)

    data_parser: t.ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "name",
                rqa.StringEnum("SITE_EMAIL"),
                doc="",
            ),
            rqa.RequiredArgument(
                "value",
                rqa.Nullable(rqa.SimpleValue.str),
                doc="",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> t.Dict[str, t.Any]:
        res: t.Dict[str, t.Any] = {
            "name": to_dict(self.name),
            "value": to_dict(self.value),
        }
        return res

    @classmethod
    def from_dict(
        cls: t.Type["SiteEmailSetting"], d: t.Dict[str, t.Any]
    ) -> "SiteEmailSetting":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            name=parsed.name,
            value=parsed.value,
        )
        res.raw_data = d
        return res


@dataclass
class MaxNumberOfFilesSetting:
    """ """

    name: "t.Literal['MAX_NUMBER_OF_FILES']"
    value: "t.Optional[int]"

    raw_data: t.Optional[t.Dict[str, t.Any]] = field(init=False, repr=False)

    data_parser: t.ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "name",
                rqa.StringEnum("MAX_NUMBER_OF_FILES"),
                doc="",
            ),
            rqa.RequiredArgument(
                "value",
                rqa.Nullable(rqa.SimpleValue.int),
                doc="",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> t.Dict[str, t.Any]:
        res: t.Dict[str, t.Any] = {
            "name": to_dict(self.name),
            "value": to_dict(self.value),
        }
        return res

    @classmethod
    def from_dict(
        cls: t.Type["MaxNumberOfFilesSetting"], d: t.Dict[str, t.Any]
    ) -> "MaxNumberOfFilesSetting":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            name=parsed.name,
            value=parsed.value,
        )
        res.raw_data = d
        return res


@dataclass
class MaxLargeUploadSizeSetting:
    """ """

    name: "t.Literal['MAX_LARGE_UPLOAD_SIZE']"
    value: "t.Optional[t.Union[int, str]]"

    raw_data: t.Optional[t.Dict[str, t.Any]] = field(init=False, repr=False)

    data_parser: t.ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "name",
                rqa.StringEnum("MAX_LARGE_UPLOAD_SIZE"),
                doc="",
            ),
            rqa.RequiredArgument(
                "value",
                rqa.Nullable(
                    parsers.make_union(
                        rqa.SimpleValue.int, rqa.SimpleValue.str
                    )
                ),
                doc="",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> t.Dict[str, t.Any]:
        res: t.Dict[str, t.Any] = {
            "name": to_dict(self.name),
            "value": to_dict(self.value),
        }
        return res

    @classmethod
    def from_dict(
        cls: t.Type["MaxLargeUploadSizeSetting"], d: t.Dict[str, t.Any]
    ) -> "MaxLargeUploadSizeSetting":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            name=parsed.name,
            value=parsed.value,
        )
        res.raw_data = d
        return res


@dataclass
class MaxNormalUploadSizeSetting:
    """ """

    name: "t.Literal['MAX_NORMAL_UPLOAD_SIZE']"
    value: "t.Optional[t.Union[int, str]]"

    raw_data: t.Optional[t.Dict[str, t.Any]] = field(init=False, repr=False)

    data_parser: t.ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "name",
                rqa.StringEnum("MAX_NORMAL_UPLOAD_SIZE"),
                doc="",
            ),
            rqa.RequiredArgument(
                "value",
                rqa.Nullable(
                    parsers.make_union(
                        rqa.SimpleValue.int, rqa.SimpleValue.str
                    )
                ),
                doc="",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> t.Dict[str, t.Any]:
        res: t.Dict[str, t.Any] = {
            "name": to_dict(self.name),
            "value": to_dict(self.value),
        }
        return res

    @classmethod
    def from_dict(
        cls: t.Type["MaxNormalUploadSizeSetting"], d: t.Dict[str, t.Any]
    ) -> "MaxNormalUploadSizeSetting":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            name=parsed.name,
            value=parsed.value,
        )
        res.raw_data = d
        return res


@dataclass
class MaxFileSizeSetting:
    """ """

    name: "t.Literal['MAX_FILE_SIZE']"
    value: "t.Optional[t.Union[int, str]]"

    raw_data: t.Optional[t.Dict[str, t.Any]] = field(init=False, repr=False)

    data_parser: t.ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "name",
                rqa.StringEnum("MAX_FILE_SIZE"),
                doc="",
            ),
            rqa.RequiredArgument(
                "value",
                rqa.Nullable(
                    parsers.make_union(
                        rqa.SimpleValue.int, rqa.SimpleValue.str
                    )
                ),
                doc="",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> t.Dict[str, t.Any]:
        res: t.Dict[str, t.Any] = {
            "name": to_dict(self.name),
            "value": to_dict(self.value),
        }
        return res

    @classmethod
    def from_dict(
        cls: t.Type["MaxFileSizeSetting"], d: t.Dict[str, t.Any]
    ) -> "MaxFileSizeSetting":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            name=parsed.name,
            value=parsed.value,
        )
        res.raw_data = d
        return res


@dataclass
class JwtAccessTokenExpiresSetting:
    """ """

    name: "t.Literal['JWT_ACCESS_TOKEN_EXPIRES']"
    value: "t.Optional[t.Union[int, int, str]]"

    raw_data: t.Optional[t.Dict[str, t.Any]] = field(init=False, repr=False)

    data_parser: t.ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "name",
                rqa.StringEnum("JWT_ACCESS_TOKEN_EXPIRES"),
                doc="",
            ),
            rqa.RequiredArgument(
                "value",
                rqa.Nullable(
                    parsers.make_union(
                        rqa.SimpleValue.int,
                        rqa.SimpleValue.int,
                        rqa.SimpleValue.str,
                    )
                ),
                doc="",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> t.Dict[str, t.Any]:
        res: t.Dict[str, t.Any] = {
            "name": to_dict(self.name),
            "value": to_dict(self.value),
        }
        return res

    @classmethod
    def from_dict(
        cls: t.Type["JwtAccessTokenExpiresSetting"], d: t.Dict[str, t.Any]
    ) -> "JwtAccessTokenExpiresSetting":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            name=parsed.name,
            value=parsed.value,
        )
        res.raw_data = d
        return res


@dataclass
class MaxLinesSetting:
    """ """

    name: "t.Literal['MAX_LINES']"
    value: "t.Optional[int]"

    raw_data: t.Optional[t.Dict[str, t.Any]] = field(init=False, repr=False)

    data_parser: t.ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "name",
                rqa.StringEnum("MAX_LINES"),
                doc="",
            ),
            rqa.RequiredArgument(
                "value",
                rqa.Nullable(rqa.SimpleValue.int),
                doc="",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> t.Dict[str, t.Any]:
        res: t.Dict[str, t.Any] = {
            "name": to_dict(self.name),
            "value": to_dict(self.value),
        }
        return res

    @classmethod
    def from_dict(
        cls: t.Type["MaxLinesSetting"], d: t.Dict[str, t.Any]
    ) -> "MaxLinesSetting":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            name=parsed.name,
            value=parsed.value,
        )
        res.raw_data = d
        return res


@dataclass
class NotificationPollTimeSetting:
    """ """

    name: "t.Literal['NOTIFICATION_POLL_TIME']"
    value: "t.Optional[t.Union[int, int, str]]"

    raw_data: t.Optional[t.Dict[str, t.Any]] = field(init=False, repr=False)

    data_parser: t.ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "name",
                rqa.StringEnum("NOTIFICATION_POLL_TIME"),
                doc="",
            ),
            rqa.RequiredArgument(
                "value",
                rqa.Nullable(
                    parsers.make_union(
                        rqa.SimpleValue.int,
                        rqa.SimpleValue.int,
                        rqa.SimpleValue.str,
                    )
                ),
                doc="",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> t.Dict[str, t.Any]:
        res: t.Dict[str, t.Any] = {
            "name": to_dict(self.name),
            "value": to_dict(self.value),
        }
        return res

    @classmethod
    def from_dict(
        cls: t.Type["NotificationPollTimeSetting"], d: t.Dict[str, t.Any]
    ) -> "NotificationPollTimeSetting":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            name=parsed.name,
            value=parsed.value,
        )
        res.raw_data = d
        return res


@dataclass
class ReleaseMessageMaxTimeSetting:
    """ """

    name: "t.Literal['RELEASE_MESSAGE_MAX_TIME']"
    value: "t.Optional[t.Union[int, int, str]]"

    raw_data: t.Optional[t.Dict[str, t.Any]] = field(init=False, repr=False)

    data_parser: t.ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "name",
                rqa.StringEnum("RELEASE_MESSAGE_MAX_TIME"),
                doc="",
            ),
            rqa.RequiredArgument(
                "value",
                rqa.Nullable(
                    parsers.make_union(
                        rqa.SimpleValue.int,
                        rqa.SimpleValue.int,
                        rqa.SimpleValue.str,
                    )
                ),
                doc="",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> t.Dict[str, t.Any]:
        res: t.Dict[str, t.Any] = {
            "name": to_dict(self.name),
            "value": to_dict(self.value),
        }
        return res

    @classmethod
    def from_dict(
        cls: t.Type["ReleaseMessageMaxTimeSetting"], d: t.Dict[str, t.Any]
    ) -> "ReleaseMessageMaxTimeSetting":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            name=parsed.name,
            value=parsed.value,
        )
        res.raw_data = d
        return res


@dataclass
class MaxPlagiarismMatchesSetting:
    """ """

    name: "t.Literal['MAX_PLAGIARISM_MATCHES']"
    value: "t.Optional[int]"

    raw_data: t.Optional[t.Dict[str, t.Any]] = field(init=False, repr=False)

    data_parser: t.ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "name",
                rqa.StringEnum("MAX_PLAGIARISM_MATCHES"),
                doc="",
            ),
            rqa.RequiredArgument(
                "value",
                rqa.Nullable(rqa.SimpleValue.int),
                doc="",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> t.Dict[str, t.Any]:
        res: t.Dict[str, t.Any] = {
            "name": to_dict(self.name),
            "value": to_dict(self.value),
        }
        return res

    @classmethod
    def from_dict(
        cls: t.Type["MaxPlagiarismMatchesSetting"], d: t.Dict[str, t.Any]
    ) -> "MaxPlagiarismMatchesSetting":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            name=parsed.name,
            value=parsed.value,
        )
        res.raw_data = d
        return res


@dataclass
class AutoTestMaxGlobalSetupTimeSetting:
    """ """

    name: "t.Literal['AUTO_TEST_MAX_GLOBAL_SETUP_TIME']"
    value: "t.Optional[t.Union[int, int, str]]"

    raw_data: t.Optional[t.Dict[str, t.Any]] = field(init=False, repr=False)

    data_parser: t.ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "name",
                rqa.StringEnum("AUTO_TEST_MAX_GLOBAL_SETUP_TIME"),
                doc="",
            ),
            rqa.RequiredArgument(
                "value",
                rqa.Nullable(
                    parsers.make_union(
                        rqa.SimpleValue.int,
                        rqa.SimpleValue.int,
                        rqa.SimpleValue.str,
                    )
                ),
                doc="",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> t.Dict[str, t.Any]:
        res: t.Dict[str, t.Any] = {
            "name": to_dict(self.name),
            "value": to_dict(self.value),
        }
        return res

    @classmethod
    def from_dict(
        cls: t.Type["AutoTestMaxGlobalSetupTimeSetting"], d: t.Dict[str, t.Any]
    ) -> "AutoTestMaxGlobalSetupTimeSetting":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            name=parsed.name,
            value=parsed.value,
        )
        res.raw_data = d
        return res


@dataclass
class AutoTestMaxPerStudentSetupTimeSetting:
    """ """

    name: "t.Literal['AUTO_TEST_MAX_PER_STUDENT_SETUP_TIME']"
    value: "t.Optional[t.Union[int, int, str]]"

    raw_data: t.Optional[t.Dict[str, t.Any]] = field(init=False, repr=False)

    data_parser: t.ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "name",
                rqa.StringEnum("AUTO_TEST_MAX_PER_STUDENT_SETUP_TIME"),
                doc="",
            ),
            rqa.RequiredArgument(
                "value",
                rqa.Nullable(
                    parsers.make_union(
                        rqa.SimpleValue.int,
                        rqa.SimpleValue.int,
                        rqa.SimpleValue.str,
                    )
                ),
                doc="",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> t.Dict[str, t.Any]:
        res: t.Dict[str, t.Any] = {
            "name": to_dict(self.name),
            "value": to_dict(self.value),
        }
        return res

    @classmethod
    def from_dict(
        cls: t.Type["AutoTestMaxPerStudentSetupTimeSetting"],
        d: t.Dict[str, t.Any],
    ) -> "AutoTestMaxPerStudentSetupTimeSetting":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            name=parsed.name,
            value=parsed.value,
        )
        res.raw_data = d
        return res


@dataclass
class ServerTimeDiffToleranceSetting:
    """ """

    name: "t.Literal['SERVER_TIME_DIFF_TOLERANCE']"
    value: "t.Optional[t.Union[int, int, str]]"

    raw_data: t.Optional[t.Dict[str, t.Any]] = field(init=False, repr=False)

    data_parser: t.ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "name",
                rqa.StringEnum("SERVER_TIME_DIFF_TOLERANCE"),
                doc="",
            ),
            rqa.RequiredArgument(
                "value",
                rqa.Nullable(
                    parsers.make_union(
                        rqa.SimpleValue.int,
                        rqa.SimpleValue.int,
                        rqa.SimpleValue.str,
                    )
                ),
                doc="",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> t.Dict[str, t.Any]:
        res: t.Dict[str, t.Any] = {
            "name": to_dict(self.name),
            "value": to_dict(self.value),
        }
        return res

    @classmethod
    def from_dict(
        cls: t.Type["ServerTimeDiffToleranceSetting"], d: t.Dict[str, t.Any]
    ) -> "ServerTimeDiffToleranceSetting":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            name=parsed.name,
            value=parsed.value,
        )
        res.raw_data = d
        return res


@dataclass
class BlackboardZipUploadEnabledSetting:
    """ """

    name: "t.Literal['BLACKBOARD_ZIP_UPLOAD_ENABLED']"
    value: "t.Optional[bool]"

    raw_data: t.Optional[t.Dict[str, t.Any]] = field(init=False, repr=False)

    data_parser: t.ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "name",
                rqa.StringEnum("BLACKBOARD_ZIP_UPLOAD_ENABLED"),
                doc="",
            ),
            rqa.RequiredArgument(
                "value",
                rqa.Nullable(rqa.SimpleValue.bool),
                doc="",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> t.Dict[str, t.Any]:
        res: t.Dict[str, t.Any] = {
            "name": to_dict(self.name),
            "value": to_dict(self.value),
        }
        return res

    @classmethod
    def from_dict(
        cls: t.Type["BlackboardZipUploadEnabledSetting"], d: t.Dict[str, t.Any]
    ) -> "BlackboardZipUploadEnabledSetting":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            name=parsed.name,
            value=parsed.value,
        )
        res.raw_data = d
        return res


@dataclass
class RubricsEnabledSetting:
    """ """

    name: "t.Literal['RUBRICS_ENABLED']"
    value: "t.Optional[bool]"

    raw_data: t.Optional[t.Dict[str, t.Any]] = field(init=False, repr=False)

    data_parser: t.ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "name",
                rqa.StringEnum("RUBRICS_ENABLED"),
                doc="",
            ),
            rqa.RequiredArgument(
                "value",
                rqa.Nullable(rqa.SimpleValue.bool),
                doc="",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> t.Dict[str, t.Any]:
        res: t.Dict[str, t.Any] = {
            "name": to_dict(self.name),
            "value": to_dict(self.value),
        }
        return res

    @classmethod
    def from_dict(
        cls: t.Type["RubricsEnabledSetting"], d: t.Dict[str, t.Any]
    ) -> "RubricsEnabledSetting":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            name=parsed.name,
            value=parsed.value,
        )
        res.raw_data = d
        return res


@dataclass
class AutomaticLtiRoleEnabledSetting:
    """ """

    name: "t.Literal['AUTOMATIC_LTI_ROLE_ENABLED']"
    value: "t.Optional[bool]"

    raw_data: t.Optional[t.Dict[str, t.Any]] = field(init=False, repr=False)

    data_parser: t.ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "name",
                rqa.StringEnum("AUTOMATIC_LTI_ROLE_ENABLED"),
                doc="",
            ),
            rqa.RequiredArgument(
                "value",
                rqa.Nullable(rqa.SimpleValue.bool),
                doc="",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> t.Dict[str, t.Any]:
        res: t.Dict[str, t.Any] = {
            "name": to_dict(self.name),
            "value": to_dict(self.value),
        }
        return res

    @classmethod
    def from_dict(
        cls: t.Type["AutomaticLtiRoleEnabledSetting"], d: t.Dict[str, t.Any]
    ) -> "AutomaticLtiRoleEnabledSetting":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            name=parsed.name,
            value=parsed.value,
        )
        res.raw_data = d
        return res


@dataclass
class LtiEnabledSetting:
    """ """

    name: "t.Literal['LTI_ENABLED']"
    value: "t.Optional[bool]"

    raw_data: t.Optional[t.Dict[str, t.Any]] = field(init=False, repr=False)

    data_parser: t.ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "name",
                rqa.StringEnum("LTI_ENABLED"),
                doc="",
            ),
            rqa.RequiredArgument(
                "value",
                rqa.Nullable(rqa.SimpleValue.bool),
                doc="",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> t.Dict[str, t.Any]:
        res: t.Dict[str, t.Any] = {
            "name": to_dict(self.name),
            "value": to_dict(self.value),
        }
        return res

    @classmethod
    def from_dict(
        cls: t.Type["LtiEnabledSetting"], d: t.Dict[str, t.Any]
    ) -> "LtiEnabledSetting":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            name=parsed.name,
            value=parsed.value,
        )
        res.raw_data = d
        return res


@dataclass
class LintersEnabledSetting:
    """ """

    name: "t.Literal['LINTERS_ENABLED']"
    value: "t.Optional[bool]"

    raw_data: t.Optional[t.Dict[str, t.Any]] = field(init=False, repr=False)

    data_parser: t.ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "name",
                rqa.StringEnum("LINTERS_ENABLED"),
                doc="",
            ),
            rqa.RequiredArgument(
                "value",
                rqa.Nullable(rqa.SimpleValue.bool),
                doc="",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> t.Dict[str, t.Any]:
        res: t.Dict[str, t.Any] = {
            "name": to_dict(self.name),
            "value": to_dict(self.value),
        }
        return res

    @classmethod
    def from_dict(
        cls: t.Type["LintersEnabledSetting"], d: t.Dict[str, t.Any]
    ) -> "LintersEnabledSetting":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            name=parsed.name,
            value=parsed.value,
        )
        res.raw_data = d
        return res


@dataclass
class IncrementalRubricSubmissionEnabledSetting:
    """ """

    name: "t.Literal['INCREMENTAL_RUBRIC_SUBMISSION_ENABLED']"
    value: "t.Optional[bool]"

    raw_data: t.Optional[t.Dict[str, t.Any]] = field(init=False, repr=False)

    data_parser: t.ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "name",
                rqa.StringEnum("INCREMENTAL_RUBRIC_SUBMISSION_ENABLED"),
                doc="",
            ),
            rqa.RequiredArgument(
                "value",
                rqa.Nullable(rqa.SimpleValue.bool),
                doc="",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> t.Dict[str, t.Any]:
        res: t.Dict[str, t.Any] = {
            "name": to_dict(self.name),
            "value": to_dict(self.value),
        }
        return res

    @classmethod
    def from_dict(
        cls: t.Type["IncrementalRubricSubmissionEnabledSetting"],
        d: t.Dict[str, t.Any],
    ) -> "IncrementalRubricSubmissionEnabledSetting":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            name=parsed.name,
            value=parsed.value,
        )
        res.raw_data = d
        return res


@dataclass
class RegisterEnabledSetting:
    """ """

    name: "t.Literal['REGISTER_ENABLED']"
    value: "t.Optional[bool]"

    raw_data: t.Optional[t.Dict[str, t.Any]] = field(init=False, repr=False)

    data_parser: t.ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "name",
                rqa.StringEnum("REGISTER_ENABLED"),
                doc="",
            ),
            rqa.RequiredArgument(
                "value",
                rqa.Nullable(rqa.SimpleValue.bool),
                doc="",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> t.Dict[str, t.Any]:
        res: t.Dict[str, t.Any] = {
            "name": to_dict(self.name),
            "value": to_dict(self.value),
        }
        return res

    @classmethod
    def from_dict(
        cls: t.Type["RegisterEnabledSetting"], d: t.Dict[str, t.Any]
    ) -> "RegisterEnabledSetting":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            name=parsed.name,
            value=parsed.value,
        )
        res.raw_data = d
        return res


@dataclass
class GroupsEnabledSetting:
    """ """

    name: "t.Literal['GROUPS_ENABLED']"
    value: "t.Optional[bool]"

    raw_data: t.Optional[t.Dict[str, t.Any]] = field(init=False, repr=False)

    data_parser: t.ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "name",
                rqa.StringEnum("GROUPS_ENABLED"),
                doc="",
            ),
            rqa.RequiredArgument(
                "value",
                rqa.Nullable(rqa.SimpleValue.bool),
                doc="",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> t.Dict[str, t.Any]:
        res: t.Dict[str, t.Any] = {
            "name": to_dict(self.name),
            "value": to_dict(self.value),
        }
        return res

    @classmethod
    def from_dict(
        cls: t.Type["GroupsEnabledSetting"], d: t.Dict[str, t.Any]
    ) -> "GroupsEnabledSetting":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            name=parsed.name,
            value=parsed.value,
        )
        res.raw_data = d
        return res


@dataclass
class AutoTestEnabledSetting:
    """ """

    name: "t.Literal['AUTO_TEST_ENABLED']"
    value: "t.Optional[bool]"

    raw_data: t.Optional[t.Dict[str, t.Any]] = field(init=False, repr=False)

    data_parser: t.ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "name",
                rqa.StringEnum("AUTO_TEST_ENABLED"),
                doc="",
            ),
            rqa.RequiredArgument(
                "value",
                rqa.Nullable(rqa.SimpleValue.bool),
                doc="",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> t.Dict[str, t.Any]:
        res: t.Dict[str, t.Any] = {
            "name": to_dict(self.name),
            "value": to_dict(self.value),
        }
        return res

    @classmethod
    def from_dict(
        cls: t.Type["AutoTestEnabledSetting"], d: t.Dict[str, t.Any]
    ) -> "AutoTestEnabledSetting":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            name=parsed.name,
            value=parsed.value,
        )
        res.raw_data = d
        return res


@dataclass
class CourseRegisterEnabledSetting:
    """ """

    name: "t.Literal['COURSE_REGISTER_ENABLED']"
    value: "t.Optional[bool]"

    raw_data: t.Optional[t.Dict[str, t.Any]] = field(init=False, repr=False)

    data_parser: t.ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "name",
                rqa.StringEnum("COURSE_REGISTER_ENABLED"),
                doc="",
            ),
            rqa.RequiredArgument(
                "value",
                rqa.Nullable(rqa.SimpleValue.bool),
                doc="",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> t.Dict[str, t.Any]:
        res: t.Dict[str, t.Any] = {
            "name": to_dict(self.name),
            "value": to_dict(self.value),
        }
        return res

    @classmethod
    def from_dict(
        cls: t.Type["CourseRegisterEnabledSetting"], d: t.Dict[str, t.Any]
    ) -> "CourseRegisterEnabledSetting":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            name=parsed.name,
            value=parsed.value,
        )
        res.raw_data = d
        return res


@dataclass
class RenderHtmlEnabledSetting:
    """ """

    name: "t.Literal['RENDER_HTML_ENABLED']"
    value: "t.Optional[bool]"

    raw_data: t.Optional[t.Dict[str, t.Any]] = field(init=False, repr=False)

    data_parser: t.ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "name",
                rqa.StringEnum("RENDER_HTML_ENABLED"),
                doc="",
            ),
            rqa.RequiredArgument(
                "value",
                rqa.Nullable(rqa.SimpleValue.bool),
                doc="",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> t.Dict[str, t.Any]:
        res: t.Dict[str, t.Any] = {
            "name": to_dict(self.name),
            "value": to_dict(self.value),
        }
        return res

    @classmethod
    def from_dict(
        cls: t.Type["RenderHtmlEnabledSetting"], d: t.Dict[str, t.Any]
    ) -> "RenderHtmlEnabledSetting":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            name=parsed.name,
            value=parsed.value,
        )
        res.raw_data = d
        return res


@dataclass
class EmailStudentsEnabledSetting:
    """ """

    name: "t.Literal['EMAIL_STUDENTS_ENABLED']"
    value: "t.Optional[bool]"

    raw_data: t.Optional[t.Dict[str, t.Any]] = field(init=False, repr=False)

    data_parser: t.ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "name",
                rqa.StringEnum("EMAIL_STUDENTS_ENABLED"),
                doc="",
            ),
            rqa.RequiredArgument(
                "value",
                rqa.Nullable(rqa.SimpleValue.bool),
                doc="",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> t.Dict[str, t.Any]:
        res: t.Dict[str, t.Any] = {
            "name": to_dict(self.name),
            "value": to_dict(self.value),
        }
        return res

    @classmethod
    def from_dict(
        cls: t.Type["EmailStudentsEnabledSetting"], d: t.Dict[str, t.Any]
    ) -> "EmailStudentsEnabledSetting":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            name=parsed.name,
            value=parsed.value,
        )
        res.raw_data = d
        return res


@dataclass
class PeerFeedbackEnabledSetting:
    """ """

    name: "t.Literal['PEER_FEEDBACK_ENABLED']"
    value: "t.Optional[bool]"

    raw_data: t.Optional[t.Dict[str, t.Any]] = field(init=False, repr=False)

    data_parser: t.ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "name",
                rqa.StringEnum("PEER_FEEDBACK_ENABLED"),
                doc="",
            ),
            rqa.RequiredArgument(
                "value",
                rqa.Nullable(rqa.SimpleValue.bool),
                doc="",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> t.Dict[str, t.Any]:
        res: t.Dict[str, t.Any] = {
            "name": to_dict(self.name),
            "value": to_dict(self.value),
        }
        return res

    @classmethod
    def from_dict(
        cls: t.Type["PeerFeedbackEnabledSetting"], d: t.Dict[str, t.Any]
    ) -> "PeerFeedbackEnabledSetting":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            name=parsed.name,
            value=parsed.value,
        )
        res.raw_data = d
        return res


@dataclass
class AtImageCachingEnabledSetting:
    """ """

    name: "t.Literal['AT_IMAGE_CACHING_ENABLED']"
    value: "t.Optional[bool]"

    raw_data: t.Optional[t.Dict[str, t.Any]] = field(init=False, repr=False)

    data_parser: t.ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "name",
                rqa.StringEnum("AT_IMAGE_CACHING_ENABLED"),
                doc="",
            ),
            rqa.RequiredArgument(
                "value",
                rqa.Nullable(rqa.SimpleValue.bool),
                doc="",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> t.Dict[str, t.Any]:
        res: t.Dict[str, t.Any] = {
            "name": to_dict(self.name),
            "value": to_dict(self.value),
        }
        return res

    @classmethod
    def from_dict(
        cls: t.Type["AtImageCachingEnabledSetting"], d: t.Dict[str, t.Any]
    ) -> "AtImageCachingEnabledSetting":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            name=parsed.name,
            value=parsed.value,
        )
        res.raw_data = d
        return res


@dataclass
class StudentPaymentEnabledSetting:
    """ """

    name: "t.Literal['STUDENT_PAYMENT_ENABLED']"
    value: "t.Optional[bool]"

    raw_data: t.Optional[t.Dict[str, t.Any]] = field(init=False, repr=False)

    data_parser: t.ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "name",
                rqa.StringEnum("STUDENT_PAYMENT_ENABLED"),
                doc="",
            ),
            rqa.RequiredArgument(
                "value",
                rqa.Nullable(rqa.SimpleValue.bool),
                doc="",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> t.Dict[str, t.Any]:
        res: t.Dict[str, t.Any] = {
            "name": to_dict(self.name),
            "value": to_dict(self.value),
        }
        return res

    @classmethod
    def from_dict(
        cls: t.Type["StudentPaymentEnabledSetting"], d: t.Dict[str, t.Any]
    ) -> "StudentPaymentEnabledSetting":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            name=parsed.name,
            value=parsed.value,
        )
        res.raw_data = d
        return res


SiteSettingInput = t.Union[
    AutoTestMaxTimeCommandSetting,
    AutoTestHeartbeatIntervalSetting,
    AutoTestHeartbeatMaxMissedSetting,
    AutoTestMaxJobsPerRunnerSetting,
    AutoTestMaxConcurrentBatchRunsSetting,
    AutoTestIoTestMessageSetting,
    AutoTestIoTestSubMessageSetting,
    AutoTestRunProgramMessageSetting,
    AutoTestCapturePointsMessageSetting,
    AutoTestCheckpointMessageSetting,
    AutoTestUnitTestMessageSetting,
    AutoTestCodeQualityMessageSetting,
    AutoTestMaxResultNotStartedSetting,
    AutoTestMaxUnitTestMetadataLengthSetting,
    ExamLoginMaxLengthSetting,
    LoginTokenBeforeTimeSetting,
    MinPasswordScoreSetting,
    ResetTokenTimeSetting,
    SettingTokenTimeSetting,
    SiteEmailSetting,
    MaxNumberOfFilesSetting,
    MaxLargeUploadSizeSetting,
    MaxNormalUploadSizeSetting,
    MaxFileSizeSetting,
    JwtAccessTokenExpiresSetting,
    MaxLinesSetting,
    NotificationPollTimeSetting,
    ReleaseMessageMaxTimeSetting,
    MaxPlagiarismMatchesSetting,
    AutoTestMaxGlobalSetupTimeSetting,
    AutoTestMaxPerStudentSetupTimeSetting,
    ServerTimeDiffToleranceSetting,
    BlackboardZipUploadEnabledSetting,
    RubricsEnabledSetting,
    AutomaticLtiRoleEnabledSetting,
    LtiEnabledSetting,
    LintersEnabledSetting,
    IncrementalRubricSubmissionEnabledSetting,
    RegisterEnabledSetting,
    GroupsEnabledSetting,
    AutoTestEnabledSetting,
    CourseRegisterEnabledSetting,
    RenderHtmlEnabledSetting,
    EmailStudentsEnabledSetting,
    PeerFeedbackEnabledSetting,
    AtImageCachingEnabledSetting,
    StudentPaymentEnabledSetting,
]
SiteSettingInputParser = rqa.Lazy(
    lambda: make_union(
        ParserFor.make(AutoTestMaxTimeCommandSetting),
        ParserFor.make(AutoTestHeartbeatIntervalSetting),
        ParserFor.make(AutoTestHeartbeatMaxMissedSetting),
        ParserFor.make(AutoTestMaxJobsPerRunnerSetting),
        ParserFor.make(AutoTestMaxConcurrentBatchRunsSetting),
        ParserFor.make(AutoTestIoTestMessageSetting),
        ParserFor.make(AutoTestIoTestSubMessageSetting),
        ParserFor.make(AutoTestRunProgramMessageSetting),
        ParserFor.make(AutoTestCapturePointsMessageSetting),
        ParserFor.make(AutoTestCheckpointMessageSetting),
        ParserFor.make(AutoTestUnitTestMessageSetting),
        ParserFor.make(AutoTestCodeQualityMessageSetting),
        ParserFor.make(AutoTestMaxResultNotStartedSetting),
        ParserFor.make(AutoTestMaxUnitTestMetadataLengthSetting),
        ParserFor.make(ExamLoginMaxLengthSetting),
        ParserFor.make(LoginTokenBeforeTimeSetting),
        ParserFor.make(MinPasswordScoreSetting),
        ParserFor.make(ResetTokenTimeSetting),
        ParserFor.make(SettingTokenTimeSetting),
        ParserFor.make(SiteEmailSetting),
        ParserFor.make(MaxNumberOfFilesSetting),
        ParserFor.make(MaxLargeUploadSizeSetting),
        ParserFor.make(MaxNormalUploadSizeSetting),
        ParserFor.make(MaxFileSizeSetting),
        ParserFor.make(JwtAccessTokenExpiresSetting),
        ParserFor.make(MaxLinesSetting),
        ParserFor.make(NotificationPollTimeSetting),
        ParserFor.make(ReleaseMessageMaxTimeSetting),
        ParserFor.make(MaxPlagiarismMatchesSetting),
        ParserFor.make(AutoTestMaxGlobalSetupTimeSetting),
        ParserFor.make(AutoTestMaxPerStudentSetupTimeSetting),
        ParserFor.make(ServerTimeDiffToleranceSetting),
        ParserFor.make(BlackboardZipUploadEnabledSetting),
        ParserFor.make(RubricsEnabledSetting),
        ParserFor.make(AutomaticLtiRoleEnabledSetting),
        ParserFor.make(LtiEnabledSetting),
        ParserFor.make(LintersEnabledSetting),
        ParserFor.make(IncrementalRubricSubmissionEnabledSetting),
        ParserFor.make(RegisterEnabledSetting),
        ParserFor.make(GroupsEnabledSetting),
        ParserFor.make(AutoTestEnabledSetting),
        ParserFor.make(CourseRegisterEnabledSetting),
        ParserFor.make(RenderHtmlEnabledSetting),
        ParserFor.make(EmailStudentsEnabledSetting),
        ParserFor.make(PeerFeedbackEnabledSetting),
        ParserFor.make(AtImageCachingEnabledSetting),
        ParserFor.make(StudentPaymentEnabledSetting),
    ),
)
