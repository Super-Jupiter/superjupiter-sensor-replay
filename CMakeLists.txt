cmake_minimum_required(VERSION 3.16)
project(SuperJupiterSensorReplay VERSION 0.1.0 LANGUAGES CXX)

set(_superjupiter_sensor_replay_top_level OFF)
if(CMAKE_CURRENT_SOURCE_DIR STREQUAL CMAKE_SOURCE_DIR)
  set(_superjupiter_sensor_replay_top_level ON)
endif()
option(SUPERJUPITER_SENSOR_REPLAY_BUILD_TESTS "Build SensorReplay tests" ${_superjupiter_sensor_replay_top_level})
option(SUPERJUPITER_SENSOR_REPLAY_BUILD_EXAMPLES "Build SensorReplay host example" ${_superjupiter_sensor_replay_top_level})
option(SUPERJUPITER_SENSOR_REPLAY_INSTALL "Generate SensorReplay install rules" ${_superjupiter_sensor_replay_top_level})

add_library(SuperJupiterSensorReplay INTERFACE)
add_library(SuperJupiter::SensorReplay ALIAS SuperJupiterSensorReplay)
set_target_properties(SuperJupiterSensorReplay PROPERTIES EXPORT_NAME SensorReplay)
target_include_directories(SuperJupiterSensorReplay INTERFACE
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/src>
  $<INSTALL_INTERFACE:include>)
target_compile_features(SuperJupiterSensorReplay INTERFACE cxx_std_11)

if(SUPERJUPITER_SENSOR_REPLAY_BUILD_TESTS)
  enable_testing()
  add_executable(superjupiter-sensor-replay-tests tests/test.cpp)
  target_link_libraries(superjupiter-sensor-replay-tests PRIVATE SuperJupiter::SensorReplay)
  add_test(NAME superjupiter-sensor-replay-tests COMMAND superjupiter-sensor-replay-tests)
  add_executable(superjupiter-sensor-replay-namespace-test tests/namespace_isolation.cpp)
  target_link_libraries(superjupiter-sensor-replay-namespace-test PRIVATE SuperJupiter::SensorReplay)
  add_test(NAME superjupiter-sensor-replay-namespace-test COMMAND superjupiter-sensor-replay-namespace-test)
endif()
if(SUPERJUPITER_SENSOR_REPLAY_BUILD_EXAMPLES)
  add_executable(superjupiter-sensor-replay-replay tools/replay.cpp)
  target_link_libraries(superjupiter-sensor-replay-replay PRIVATE SuperJupiter::SensorReplay)
endif()
if(SUPERJUPITER_SENSOR_REPLAY_INSTALL)
  include(CMakePackageConfigHelpers)
  set(_superjupiter_sensor_replay_package_dir lib/cmake/SuperJupiterSensorReplay)
  install(TARGETS SuperJupiterSensorReplay EXPORT SuperJupiterSensorReplayTargets)
  install(FILES src/SuperJupiterSensorReplay.h DESTINATION include)
  install(EXPORT SuperJupiterSensorReplayTargets NAMESPACE SuperJupiter::
    DESTINATION ${_superjupiter_sensor_replay_package_dir})
  configure_package_config_file(cmake/SuperJupiterSensorReplayConfig.cmake.in
    ${CMAKE_CURRENT_BINARY_DIR}/SuperJupiterSensorReplayConfig.cmake
    INSTALL_DESTINATION ${_superjupiter_sensor_replay_package_dir})
  write_basic_package_version_file(${CMAKE_CURRENT_BINARY_DIR}/SuperJupiterSensorReplayConfigVersion.cmake
    VERSION ${PROJECT_VERSION} COMPATIBILITY SameMinorVersion ARCH_INDEPENDENT)
  install(FILES ${CMAKE_CURRENT_BINARY_DIR}/SuperJupiterSensorReplayConfig.cmake
    ${CMAKE_CURRENT_BINARY_DIR}/SuperJupiterSensorReplayConfigVersion.cmake
    DESTINATION ${_superjupiter_sensor_replay_package_dir})
  install(FILES LICENSE DESTINATION share/licenses/SuperJupiterSensorReplay)
endif()
