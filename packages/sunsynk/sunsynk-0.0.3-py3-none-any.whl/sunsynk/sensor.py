"""Sensor classes represent modbus registers for an inverter."""
from __future__ import annotations

import logging
from math import modf
from typing import Any, Callable, List, Optional, Sequence, Tuple, Union

import attr

_LOGGER = logging.getLogger(__name__)


def tup(val: Any) -> Tuple[int]:
    """Return a tuple."""
    if isinstance(val, tuple):
        return val  # type: ignore
    if isinstance(val, int):
        return (val,)
    return tuple(val)  # type: ignore


@attr.define(slots=True)
class Sensor:
    """Sunsynk sensor."""

    register: Tuple[int] = attr.field(converter=tup)
    name: str = attr.field()
    unit: str = attr.field(default="")
    factor: float = attr.field(default=1)
    value: Union[float, int, str, None] = None
    func: Optional[Callable[[float], float]] = attr.field(default=None)

    def append_to(self, arr: List[Sensor]) -> Sensor:
        """Append to a list of sensors."""
        arr.append(self)
        return self

    @property
    def id(self) -> str:  # pylint: disable=invalid-name
        """Get the sensor ID."""
        return slug(self.name)


class HSensor(Sensor):
    """Hybrid sensor."""


def group_sensors(
    sensors: Sequence[Sensor], allow_gap: int = 3
) -> Sequence[Sequence[int]]:
    """Group sensor registers into blocks for reading."""
    if not sensors:
        return []
    regs = set()
    for sen in sensors:
        regs |= set(sen.register)
    adr = sorted(regs)
    cgroup = [adr[0]]
    groups = [cgroup]
    for idx in range(1, len(adr)):
        gap = adr[idx] - adr[idx - 1]
        if gap > allow_gap or len(cgroup) >= 60:
            cgroup = []
            groups.append(cgroup)
        cgroup.append(adr[idx])
    return groups


def update_sensors(
    sensors: Sequence[Sensor], register: int, values: Sequence[int]
) -> None:
    """Update sensors."""
    hreg = register + len(values)
    for sen in sensors:
        if sen.register[0] <= register or sen.register[0] >= hreg:
            continue

        if len(sen.register) > 2:  # serial?
            res = ""
            for regv in sen.register:
                b16 = values[regv - register]
                res += chr(b16 >> 8)
                res += chr(b16 & 0xFF)
            sen.value = res
            continue

        hval = 0
        try:
            hval = values[sen.register[1] - register]  # type: ignore
        except IndexError:
            pass
        lval = values[sen.register[0] - register]

        sen.value = round((lval + (hval << 16)) * sen.factor, 2)
        if sen.func:
            sen.value = sen.func(sen.value)
        if isinstance(sen.value, float):
            if modf(sen.value)[0] == 0:
                sen.value = int(sen.value)
        _LOGGER.debug(
            "%s low=%d high=%d value=%d%s",
            sen.name,
            lval,
            hval,
            sen.value,
            sen.unit,
        )


def slug(name: str) -> str:
    """Create a slug."""
    return name.lower().replace(" ", "_")


def offset100(val: float) -> float:
    """Offset by 100 for temperature."""
    return val - 100


def sd_status(val: float) -> str:
    """Offset by 100 for temperature."""
    if val == 1000:
        return "fault"
    if val == 2000:
        return "ok"
    return f"unknown {val}"
