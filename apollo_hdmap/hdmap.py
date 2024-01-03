#!/usr/bin/env python3

# ****************************************************************************
# Copyright 2019 The Apollo Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ****************************************************************************
# -*- coding: utf-8 -*-
"""Module for wrapper hdmap."""

import collections
import importlib
import os
import sys

wrapper_lib_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(wrapper_lib_path)
sys.path.append(os.path.dirname(__file__))

_HDMAP = importlib.import_module('_apollo_hdmap_wrapper')

import map_pb2
import map_lane_pb2
import map_junction_pb2

class HDMap(object):
    """
    Class for HDMap wrapper.
    """

    ##
    # @brief the constructor function.
    #
    # @param file_name the record file name.
    def __init__(self):
        self.hdmap = _HDMAP.new_PyHdMap()

    def __del__(self):
        _HDMAP.delete_PyHdMap(self.hdmap)

    def LoadMapFromFile(self, map_path):
        return _HDMAP.PyHdMap_LoadMapFromFile(self.hdmap, map_path)

    def GetLocalMap(self, point_x, point_y, range_x, range_y):
        s = _HDMAP.PyHdMap_GetLocalMap(self.hdmap, point_x, point_y, range_x, range_y)
        if s is None or len(s) == 0:
            return None
        mp = map_pb2.Map()
        mp.ParseFromString(s)
        return mp

    def GetNearestLane(self, point_x, point_y):
        s = _HDMAP.PyHdMap_GetNearestLane(self.hdmap, point_x, point_y)
        if s is None:
            return None
        mp = map_lane_pb2.Lane()
        mp.ParseFromString(s['lane'])
        s['lane'] = mp
        return s

    def GetLanesWithHeading(self, point_x, point_y, distance, central_heading, max_heading_difference):
        s = _HDMAP.PyHdMap_GetLanesWithHeading(self.hdmap, point_x, point_y, distance, central_heading, max_heading_difference)
        if s is None or len(s) == 0:
            return None
        ret = []
        for lane in s:
            mp = map_lane_pb2.Lane()
            mp.ParseFromString(lane)
            ret.append(mp)
        return ret
    
    def GetNearestLaneWithHeading(self, point_x, point_y, distance, central_heading, max_heading_difference):
        s = _HDMAP.PyHdMap_GetNearestLaneWithHeading(self.hdmap, point_x, point_y, distance, central_heading, max_heading_difference)
        if s is None:
            return None
        mp = map_lane_pb2.Lane()
        mp.ParseFromString(s['lane'])
        s['lane'] = mp
        return s
    
    def GetJunctions(self, point_x, point_y, distance):
        s = _HDMAP.PyHdMap_GetJunctions(self.hdmap, point_x, point_y, distance)
        if s is None or len(s) == 0:
            return None
        ret = []
        for junction in s:
            mp = map_junction_pb2.Junction()
            mp.ParseFromString(junction)
            ret.append(mp)
        return ret
