set(E00GRID_DRIVER_SOURCES
    entrypoint.cpp
    e00grid/e00griddataset.cpp
)

add_library(gdal_E00GRID SHARED ${E00GRID_DRIVER_SOURCES})

set_target_properties(gdal_E00GRID PROPERTIES PREFIX "")
set_target_properties(gdal_E00GRID PROPERTIES OUTPUT_NAME "gdal_E00GRID")

target_include_directories(gdal_E00GRID PRIVATE ${CMAKE_SOURCE_DIR}/src ${GDAL_INCLUDE_DIR})
target_link_libraries(gdal_E00GRID PUBLIC ${GDAL_LIBRARY})

install(TARGETS gdal_E00GRID DESTINATION lib/gdalplugins)
