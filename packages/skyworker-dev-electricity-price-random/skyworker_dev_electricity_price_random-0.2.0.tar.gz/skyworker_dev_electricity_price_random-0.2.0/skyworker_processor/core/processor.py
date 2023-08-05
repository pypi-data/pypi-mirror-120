"""
This file is part of the Omedia Skyworker Processor.

(c) 2021 Omedia <welcome@omedia.dev>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Written by Temuri Takalandze <t.takalandze@omedia.dev>, August 2021
"""

# pylint: disable=W0613

import random
import time
from datetime import datetime
from typing import Dict

import pandas as pd


InputDict = Dict[str, Dict[str, str]]


def _compose_entry(measurement: str, timestamp: pd.Timestamp):
    """
    Compose new Time Series entry.
    """

    return {
        "timestamp": int(timestamp.timestamp()),
        "measurement": measurement,
        "value": round(random.uniform(1, 3), 1),
    }


def process(
    measurement: str,
    data_source: Dict[str, any],
    time_series: InputDict,
    tags: InputDict,
    date_from: datetime,
    date_to: datetime,
) -> pd.DataFrame:
    # Simulate calculation delay.
    time.sleep(3)

    data_frame = pd.DataFrame(
        map(lambda x: _compose_entry(measurement, x), pd.date_range(start=date_from, end=date_to))
    )
    data_frame.index = data_frame["timestamp"]
    data_frame["time"] = data_frame["timestamp"].map(datetime.fromtimestamp)
    del data_frame["timestamp"]

    return data_frame
