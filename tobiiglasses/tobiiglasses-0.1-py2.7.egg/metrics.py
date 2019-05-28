#   Copyright (C) 2019  Davide De Tommaso
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>

from tobiiglasses.filters.df import BetweenTimestamps
from tobiiglasses.events import GazeEvents
import numpy as np

def IntervalDuration(ts_from, ts_to):
    return (ts_to - ts_from)

def TotalFixationNr(gaze_events, ts_filter):
    return len(gaze_events.toDataFrame(ts_filter=ts_filter).dropna(axis=1).values)

def FixationDuration_SD(gaze_events, ts_filter):
    df = gaze_events.toDataFrame(ts_filter=ts_filter)
    res = list(df[GazeEvents.EventDuration].dropna().values)
    if len(res) > 0:
        res = np.array(res,dtype='double')
        return np.std(res)
    return None

def FixationPointX_SD(gaze_events, ts_filter):
    df = gaze_events.toDataFrame(ts_filter=ts_filter)
    res = list(df[GazeEvents.Fixation_X].dropna().values)
    if len(res) > 0:
        res = np.array(res,dtype='double')
        return np.std(res)
    return None

def FixationPointY_SD(gaze_events, ts_filter):
    df = gaze_events.toDataFrame(ts_filter=ts_filter)
    res = list(df[GazeEvents.Fixation_Y].dropna().values)
    if len(res) > 0:
        res = np.array(res,dtype='double')
        return np.std(res)
    return None

def AOIs_TTFF(gaze_events, aoi_label, ts_from, ts_to):
    ft = BetweenTimestamps(ts_from, ts_to, columns=[GazeEvents.Timestamp, GazeEvents.AOI])
    df = gaze_events.toDataFrame(ts_filter=ft)
    res = df.loc[df.AOI == aoi_label, GazeEvents.Timestamp]
    if res.count() > 0:
        return res.iloc[0] - ts_from
    return None

def AOIs_FirstFixationDuration(gaze_events, aoi_label, ts_from, ts_to):
    ft = BetweenTimestamps(ts_from, ts_to, columns=[GazeEvents.Timestamp, GazeEvents.AOI, GazeEvents.EventDuration])
    df = gaze_events.toDataFrame(ts_filter=ft)
    res = df.loc[df.AOI == aoi_label, GazeEvents.EventDuration]
    if res.count() > 0:
        return res.iloc[0]
    return None

def AOIs_TotalFixationDuration(gaze_events, aoi_label, ts_from, ts_to):
    ft = BetweenTimestamps(ts_from, ts_to, columns=[GazeEvents.Timestamp, GazeEvents.AOI, GazeEvents.EventDuration])
    df = gaze_events.toDataFrame(ts_filter=ft)
    tot = df.loc[:, GazeEvents.EventDuration].sum()
    if tot > 0:
        aoi_sum = df.loc[df.AOI == aoi_label, GazeEvents.EventDuration].sum()
        return (aoi_sum*100.0)/tot
    return 0
