#!/bin/bash
# Copy shared folder to api and worker directories for Docker build
# This is needed because Docker cannot access parent directories

echo "Copying shared folder to api and worker directories..."
cp -rv shared api
cp -rv shared worker
echo "Done!"
