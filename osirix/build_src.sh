#! /bin/sh

# Build the cpp definitions
../grpc/install/bin/protoc -I protos --grpc_out=cpp --plugin=protoc-gen-grpc=../grpc/install/bin/grpc_cpp_plugin protos/osirix.proto

../grpc/install/bin/protoc -I protos --cpp_out=cpp osirix.proto roi.proto roivolume.proto dcmpix.proto vrcontroller.proto viewercontroller.proto browsercontroller.proto dicomimage.proto dicomstudy.proto dicomseries.proto utilities.proto types.proto

# Build the Python definitions
python -m grpc_tools.protoc -I protos --python_out=python --grpc_python_out=python osirix.proto
python -m grpc_tools.protoc -I protos --python_out=python roi.proto roivolume.proto dcmpix.proto vrcontroller.proto viewercontroller.proto browsercontroller.proto dicomimage.proto dicomstudy.proto dicomseries.proto utilities.proto types.proto
