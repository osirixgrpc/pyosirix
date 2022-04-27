import sys
import json
from .Exceptions import GrpcException, WaitException, OsirixServiceException
from .Wait import Wait
from .ViewerController import ViewerController
from .DCMPix import DCMPix
from .VRController import VRController
from .ROI import ROI
from .Dicom import DicomSeries, DicomStudy, DicomImage
from .BrowserController import BrowserController
from .osirix_utils import Osirix, OsirixService

__all__ = [
            "Osirix",
           "OsirixService",
           "ViewerController",
           "DCMPix",
           "ROI",
           "VRController",
            "BrowserController",
           "DicomSeries",
           "DicomStudy",
           "DicomImage",
           "Wait",
            "GrpcException",
            "WaitException",
            "OsirixServiceException"]

def osirix():
    # Checks which operating system
    # print(platform.system())
    port = ""
    domain = ""
    with open(r'/Users/admintmun/Library/Application Support/OsiriXGRPC/server_configs.json') as file:
        server_configs_dict = json.load(file)
        for item in server_configs_dict:
            if (item["active"] == "YES"):
                port = item["port"]
                domain = item["ipaddress"] + ":"
                break

    if (port == "" or domain == ""):
        raise Exception("No port or domain listed in the server configuration file.")
    # address
    channel_opt = [('grpc.max_send_message_length', 512 * 1024 * 1024),
                   ('grpc.max_receive_message_length', 512 * 1024 * 1024)]
    osirix_service = OsirixService(channel_opt=channel_opt, domain=domain, port=port).get_service()
    osirix = Osirix(osirix_service)
    return osirix