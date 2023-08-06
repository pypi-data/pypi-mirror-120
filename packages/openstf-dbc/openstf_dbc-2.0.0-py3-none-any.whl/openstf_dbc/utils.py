# SPDX-FileCopyrightText: 2021 2017-2021 Alliander N.V. <korte.termijn.prognoses@alliander.com>
#
# SPDX-License-Identifier: MPL-2.0
import datetime

import pandas as pd

DEFAULT_FREQ = "15min"
DEFAULT_TZ = datetime.timezone.utc


def genereate_datetime_index(start, end, freq=None):
    # Use timezone info from start if given
    tz = getattr(start, "tzinfo", DEFAULT_TZ)

    if not freq:
        freq = DEFAULT_FREQ

    return pd.date_range(
        start=start,
        end=end,
        freq=freq,
        tz=tz,
    )
