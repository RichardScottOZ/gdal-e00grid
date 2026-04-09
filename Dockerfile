# Dockerfile for building GDAL with the E00Grid driver plugin
# and Python bindings
#
# Usage:
#   docker build -t gdal-e00grid .
#   docker run --rm -it gdal-e00grid python3 -c "from osgeo import gdal; print(gdal.GetDriverByName('E00GRID'))"

FROM ghcr.io/osgeo/gdal:ubuntu-small-latest

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    cmake \
    g++ \
    make \
    libgdal-dev \
    python3-pip \
    python3-pytest \
    && rm -rf /var/lib/apt/lists/*

# Copy source code
WORKDIR /src
COPY . .

# Build the E00GRID driver plugin
RUN mkdir -p _build && cd _build && \
    cmake .. && \
    make && \
    make install

ENV GDAL_DRIVER_PATH=/usr/local/lib/gdalplugins

# Verify the plugin is installed
RUN ls -la ${GDAL_DRIVER_PATH}/

# Run a quick verification
RUN python3 -c "from osgeo import gdal; drv = gdal.GetDriverByName('E00GRID'); print('E00GRID driver:', 'available' if drv else 'NOT FOUND')"

WORKDIR /src
CMD ["python3", "-m", "pytest", "tests/", "-v"]
