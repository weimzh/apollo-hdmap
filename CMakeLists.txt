cmake_minimum_required(VERSION 3.10)
project(apollo_hdmap)

set(CMAKE_CXX_STANDARD 17)

find_package(PkgConfig REQUIRED)
find_package(Protobuf REQUIRED)
find_package(nlohmann_json REQUIRED)

pkg_check_modules(GLOG REQUIRED libglog)
pkg_check_modules(EIGEN3 REQUIRED eigen3)

protobuf_generate_cpp(PROTO_SRCS PROTO_HDRS
    proto/map_crosswalk.proto
    proto/map_junction.proto
    proto/map_geometry.proto
    proto/map_overlap.proto
    proto/geometry.proto
    proto/map_pnc_junction.proto
    proto/map_lane.proto
    proto/map_road.proto
    proto/map_speed_control.proto
    proto/map_rsu.proto
    proto/map_id.proto
    proto/map.proto
    proto/map_parking_space.proto
    proto/map_clear_area.proto
    proto/map_stop_sign.proto
    proto/map_signal.proto
    proto/map_speed_bump.proto
    proto/map_yield_sign.proto
    proto/error_code.proto
    proto/header.proto
    proto/navigation.proto
    proto/error_code.proto
    proto/pnc_point.proto
)

add_library(apollo_hdmap SHARED
    src/hdmap_util.cc
    src/adapter/xml_parser/junctions_xml_parser.cc
    src/adapter/xml_parser/util_xml_parser.cc
    src/adapter/xml_parser/objects_xml_parser.cc
    src/adapter/xml_parser/signals_xml_parser.cc
    src/adapter/xml_parser/roads_xml_parser.cc
    src/adapter/xml_parser/header_xml_parser.cc
    src/adapter/xml_parser/coordinate_convert_tool.cc
    src/adapter/xml_parser/lanes_xml_parser.cc
    src/adapter/opendrive_adapter.cc
    src/adapter/proto_organizer.cc
    src/hdmap.cc
    src/hdmap_common.cc
    src/hdmap_impl.cc
    src/math/aabox2d.cc
    src/math/math_utils.cc
    src/math/vec2d.cc
    src/math/box2d.cc
    src/math/polygon2d.cc
    src/math/line_segment2d.cc
    src/math/linear_interpolation.cc
    src/file.cc
    ${PROTO_SRCS}
)

target_include_directories(apollo_hdmap PRIVATE .
    ${Protobuf_INCLUDE_DIRS}
    ${nlohmann_json_INCLUDE_DIRS}
    ${CMAKE_CURRENT_BINARY_DIR}
    ${GLOG_INCLUDE_DIRS}
    ${EIGEN3_INCLUDE_DIRS}
    ./src
)

set_target_properties(
    apollo_hdmap
    PROPERTIES
    LINKER_LANGUAGE CXX
)

target_link_libraries(apollo_hdmap ${PROTOBUF_LIBRARY} ${GLOG_LIBRARIES})
