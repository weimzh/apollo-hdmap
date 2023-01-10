/******************************************************************************
 * Copyright 2018 The Apollo Authors. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *****************************************************************************/

#ifndef PYTHON_WRAPPER_PY_MAP_H_
#define PYTHON_WRAPPER_PY_MAP_H_

#include <unistd.h>

#include <iostream>
#include <limits>
#include <memory>
#include <mutex>
#include <set>
#include <string>
#include <thread>

#include "hdmap.h"

namespace apollo {
namespace hdmap {

class PyHdMap {
 public:
  explicit PyHdMap() {
    HDMap *hdmap = new HDMap();
    hdmap_.reset(hdmap);
  }

  int LoadMapFromFile(const std::string& map_filename) {
    return hdmap_->LoadMapFromFile(map_filename);
  }

  int GetLocalMap(double point_x, double point_y, double range_x,
                  double range_y, Map* local_map) {
    apollo::common::PointENU point;
    point.set_x(point_x);
    point.set_y(point_y);

    std::pair<double, double> range;
    range.first = range_x;
    range.second = range_y;

    int ret = hdmap_->GetLocalMap(point, range, local_map);
    return ret;
  }

  int GetNearestLane(double point_x, double point_y,
                     apollo::hdmap::LaneInfoConstPtr* nearest_lane,
                     double* nearest_s, double* nearest_l) {
    apollo::common::PointENU point;
    point.set_x(point_x);
    point.set_y(point_y);

    int ret = hdmap_->GetNearestLane(point, nearest_lane, nearest_s, nearest_l);
    return ret;
  }

 private:
  std::unique_ptr<HDMap> hdmap_;
};

}  // namespace hdmap
}  // namespace apollo

#endif  // PYTHON_WRAPPER_PY_HDMAP_H_
