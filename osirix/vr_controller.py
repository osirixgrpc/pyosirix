import warnings
from typing import Tuple

import numpy

import osirixgrpc.viewercontroller_pb2 as viewercontroller_pb2
import osirixgrpc.vrcontroller_pb2 as vrcontroller_pb2
import osirixgrpc.roivolume_pb2 as roivolume_pb2
from osirix.response_processor import ResponseProcessor
from osirix.viewer_controller import ViewerController


class ROIVolume:
    """
    A class representing the 3D volume ROI contained within a 3D render window.
    """
    def __init__(self,
                 pb2_object: roivolume_pb2,
                 osirix_service):
        self.pb2_object = pb2_object
        self.osirix_service = osirix_service

    @property
    def texture(self) -> bool:
        """ The texture of the ROI volume as a bool.
        """
        response = self.osirix_service.ROIVolumeTexture(self.pb2_object)
        if response.status == 0:
            warnings.warn("Invalid ROI Volume")
            return None
        return response.texture

    @texture.setter
    def texture(self, texture: bool):
        """ The texture of the ROI volume as a bool.
        """
        request = roivolume_pb2.ROIVolumeSetTextureRequest(roi=self.pb2_object,
                                                           texture=texture)
        response = self.osirix_service.ROIVolumeSetTexture(request)
        if not response.status == 1:
            warnings.warn("Could not set ROIVolume texture")

    @property
    def visible(self) -> bool:
        """ The visibility of the ROI volume as a bool.
        """
        response = self.osirix_service.ROIVolumeVisible(self.pb2_object)
        if response.status == 0:
            warnings.warn("Invalid ROI Volume")
            return None
        return response.visible

    @property
    def name(self) -> str:
        """ The name of the ROI volume.
        """
        response = self.osirix_service.ROIVolumeName(self.pb2_object)
        if response.status == 0:
            warnings.warn("Invalid ROI Volume")
            return None
        return response.name

    @property
    def color(self) -> Tuple[float, float, float]:
        """ The color of the ROI volume as a (r, g, b) tuple (each channel in range 0-1)
        """
        response = self.osirix_service.ROIVolumeColor(self.pb2_object)
        if response.status == 0:
            warnings.warn("Invalid ROI Volume")
            return None
        return response.r, response.g, response.b

    @color.setter
    def color(self, color: Tuple[int, int, int]):
        """ The color of the ROI volume as a (r, g, b) tuple (each channel in range 0-1)
        """
        # Check the input
        if not len(color) == 3:
            raise ValueError("Color must have 3 elements")
        if numpy.any(numpy.array(color) < 0):
            raise ValueError("RGB values must be >= 0")
        if numpy.any(numpy.array(color) > 1):
            raise ValueError("RGB values must be <= 1")

        request = roivolume_pb2.ROIVolumeSetColorRequest(roi=self.pb2_object,
                                                         r=color[0],
                                                         g=color[1],
                                                         b=color[2])
        response = self.osirix_service.ROIVolumeSetColor(request)
        if not response.status == 1:
            warnings.warn("Could not set ROIVolume color")

    def volume(self) -> float:
        """ The volume of the ROI volume

        Returns:
            volume: float
        """
        response = self.osirix_service.ROIVolumeVolume(self.pb2_object)
        if response.status == 0:
            warnings.warn("Invalid ROI Volume")
            return None
        return response.volume

    @property
    def opacity(self) -> float:
        """ The opacity of the ROI volume in the range 0-1
        """
        response = self.osirix_service.ROIVolumeOpacity(self.pb2_object)
        if response.status == 0:
            warnings.warn("Invalid ROI Volume")
            return None
        return response.opacity

    @opacity.setter
    def opacity(self, opacity: float):
        """ The opacity of the ROI volume in the range 0-1
        """
        if opacity < 0 or opacity > 1:
            raise ValueError("Opacity must be in range 0-1")
        request = roivolume_pb2.ROIVolumeSetOpacityRequest(roi=self.pb2_object,
                                                           opacity=opacity)
        response = self.osirix_service.ROIVolumeSetOpacity(request)
        if not response.status == 1:
            warnings.warn("Could not set ROIVolume opacity")

    @property
    def factor(self) -> float:
        """ The factor of the ROI volume in the range 0-1
        """
        response = self.osirix_service.ROIVolumeFactor(self.pb2_object)
        if response.status == 0:
            warnings.warn("Invalid ROI Volume")
            return None
        return response.factor

    @opacity.setter
    def factor(self, factor: float):
        """ The factor of the ROI volume in the range 0-1
        """
        if factor < 0 or factor > 1:
            raise ValueError("Factor must be in range 0-1")
        request = roivolume_pb2.ROIVolumeSetFactorRequest(roi=self.pb2_object,
                                                          factor=factor)
        response = self.osirix_service.ROIVolumeSetFactor(request)
        if not response.status == 1:
            warnings.warn("Could not set ROIVolume factor")


class VRController:
    """
    Class representing the properties and methods to communicate with the Osirix service through
    gRPC for a VRController
    """
    def __init__(self,
                 osirixrpc_uid: str,
                 osirix_service):
        self.osirixrpc_uid = osirixrpc_uid
        self.osirix_service = osirix_service
        self.response_processor = ResponseProcessor()

    @property
    def rendering_mode(self) -> str:
        """
          Process gRPC request to retrieve the rendering mode for VRController

          Returns:
            str : rendering mode
        """
        response_vr_rendering_mode = self.osirix_service.VRControllerRenderingMode(self.osirixrpc_uid)
        rendering_mode = self.response_processor.process_vr_rendering_mode(response_vr_rendering_mode)
        return rendering_mode

    @rendering_mode.setter
    def rendering_mode(self, rendering_mode: str) -> None:
        """
          Process gRPC request to set the rendering mode for the VRController

          Args:
            str: rendering mode

          Returns:
            None
        """
        request = vrcontroller_pb2.VRControllerSetRenderingModeRequest(vr_controller=self.osirixrpc_uid, rendering_mode=rendering_mode)
        response = self.osirix_service.VRControllerSetRenderingMode(request)
        self.response_processor.process_basic_response(response)

    @property
    def style(self) -> str:
        """
          Process gRPC request to retrieve the style for the VRController

          Returns:
            str : style
        """
        response_vr_style = self.osirix_service.VRControllerStyle(self.osirixrpc_uid)
        style = self.response_processor.process_vr_style(response_vr_style)
        return style

    @property
    def title(self) -> str:
        """
          Process gRPC request to retrieve the title for the VRController

          Returns:
            str : title
        """
        response_vr_title = self.osirix_service.VRControllerTitle(self.osirixrpc_uid)
        title = self.response_processor.process_title(response_vr_title)
        return title

    @property
    def wlww(self) -> Tuple[float, float]:
        """
          Process gRPC request to retrieve the wlww for the VRController

          Returns:
            Tuple containing wl and ww in float
        """
        response_vr_wlww = self.osirix_service.VRControllerWLWW(self.osirixrpc_uid)
        vr_wl, vr_ww = self.response_processor.process_wlww(response_vr_wlww)
        return vr_wl, vr_ww

    @wlww.setter
    def wlww(self, wlww: Tuple[float, float]) -> None:
        """
          Process gRPC request to set the wlww for the VRController

          Args:
            Tuple[float, float]: wlww

          Returns:
            None
        """
        wl, ww = wlww
        request = vrcontroller_pb2.VRControllerSetWLWWRequest(vr_controller=self.osirixrpc_uid, wl=wl, ww=ww)
        response = self.osirix_service.VRControllerSetWLWW(request)
        self.response_processor.process_basic_response(response)

    def blending_controller(self) -> ViewerController:
        """
          Process gRPC request to retrieve the blending controller for the VRController

          Returns:
            ViewerController
        """
        response_blending_controller = self.osirix_service.VRControllerBlendingController(self.osirixrpc_uid)
        blending_controller = self.response_processor.process_blending_controller(response_blending_controller)
        blending_controller_obj = ViewerController(blending_controller, self.osirix_service)
        return blending_controller_obj

    def viewer_2d(self) -> ViewerController:
        """
          Process gRPC request to retrieve the 2D viewer for the VRController

          Returns:
            ViewerController
        """
        response_viewer_2d = self.osirix_service.VRControllerViewer2D(self.osirixrpc_uid)
        viewer_2d = self.response_processor.process_viewer_2d(response_viewer_2d)
        viewer_2d_obj = ViewerController(viewer_2d, self.osirix_service)
        return viewer_2d_obj

    def roi_volumes(self) -> Tuple[ROIVolume, ...]:
        """
        Return the ROIVolume instances stored within the VR controller.

         Returns:
           Tuple[ROIVolume, ...]
        """
        roi_volumes = ()
        response_roi_volumes = self.osirix_service.VRControllerROIVolumes(self.osirixrpc_uid)
        for roi_volume in response_roi_volumes.roi_volumes:
            roi = ROIVolume(roi_volume, self.osirix_service)
            roi_volumes = roi_volumes + (roi,)
        return roi_volumes

    def hide_roi_volume(self, roi_volume: ROIVolume):
        """
        Hide the given ROI volume
        """
        request = vrcontroller_pb2.VRControllerHideROIVolumeRequest(vr_controller=self.osirixrpc_uid,
                                                                    roi_volume=roi_volume.pb2_object)
        response = self.osirix_service.VRControllerHideROIVolume(request)
        if response.status.status == 0:
            raise Exception("Error: %s" % response.status.message)

    def display_roi_volume(self, roi_volume: ROIVolume):
        """
        Display the given ROI volume
        """
        request = vrcontroller_pb2.VRControllerDisplayROIVolumeRequest(vr_controller=self.osirixrpc_uid,
                                                                       roi_volume=roi_volume.pb2_object)
        response = self.osirix_service.VRControllerDisplayROIVolume(request)
        if response.status.status == 0:
            raise Exception("Error: %s" % response.status.message)

    def needs_display_update(self):
        response = self.osirix_service.VRControllerNeedsDisplayUpdate(self.osirixrpc_uid)
        if response.status.status == 0:
            raise Exception("Error: %s" % response.status.message)


