from __future__ import annotations
from typing import Tuple, Dict
import sys

from numpy import ndarray

# sys.path.append("./pb2")
# sys.path.append("/Users/admintmun/dev/pyosirix/osirix/pb2")
import osirix.pb2.viewercontroller_pb2 as viewercontroller_pb2
import osirix.pb2.vrcontroller_pb2 as vrcontroller_pb2
import osirix.pb2.dcmpix_pb2 as dcmpix_pb2
import osirix.pb2.roi_pb2 as roi_pb2
from osirix.Dicom import DicomSeries, DicomStudy, DicomImage
from osirix.ResponseProcessor import ResponseProcessor

class DCMPix(object):
    '''
    Class representing the properties and methods to communicate with the Osirix service through
    gRPC for DCMPix
    '''

    def __init__(self,
                 osirixrpc_uid,
                 osirix_service):
        self.response_processor = ResponseProcessor()
        self.osirixrpc_uid = osirixrpc_uid
        self.osirix_service = osirix_service

    @property
    def is_rgb(self) -> bool:
        """
        Provides boolean value whether the DCMPix is rgb
        Returns:
            bool: rgb
        """
        response_is_rgb = self.osirix_service.DCMPixIsRGB(self.osirixrpc_uid)
        self._is_rgb = self.response_processor.process_is_rgb(response_is_rgb)
        return self._is_rgb

    @property
    def slice_location(self) -> float:
        """
        Provides slice location associated with the DCMPix
        Returns:
            bool: slice location
        """
        response_slice_location = self.osirix_service.DCMPixSliceLocation(self.osirixrpc_uid)
        self._slice_location = self.response_processor.process_pix_slice_location(response_slice_location)
        return self._slice_location

    @property
    def orientation(self) -> Tuple[float]:
        """
        Provides orientation associated with the DCMPix
        Returns:
            Tuple containing orientations in float
        """
        response_orientation = self.osirix_service.DCMPixOrientation(self.osirixrpc_uid)
        self._orientation = self.response_processor.process_pix_orientation(response_orientation)

        return self._orientation

    @property
    def origin(self) -> Tuple[float]:
        """
        Provides origin (rows, columns, slices) associated with the DCMPix
        Returns:
            A Tuple containing the origin values (rows, columns, slices) in float
        """
        response_origin = self.osirix_service.DCMPixOrigin(self.osirixrpc_uid)
        self._origin = self.response_processor.process_pix_origin(response_origin)
        return self._origin

    @property
    def pixel_spacing(self) -> Tuple[float]:
        """
        Provides pixel spacing in rows and columns associated with the DCMPix
        Returns:
            A tuple containing pixel spacings (rows and columns) in float
        """
        response_spacing = self.osirix_service.DCMPixSpacing(self.osirixrpc_uid)
        self._pixel_spacing = self.response_processor.process_pix_spacing(response_spacing)

        return self._pixel_spacing

    @property
    def shape(self) -> Tuple[int]:
        """
        Provides shape (rows, columns) associated with the DCMPix
        Returns:
            Tuple containing shape (rows, columns) in float
        """
        response_pix_shape = self.osirix_service.DCMPixShape(self.osirixrpc_uid)
        self._shape = self.response_processor.process_pix_shape(response_pix_shape)
        return self._shape

    @property
    def source_file(self) -> str:
        """
         Provides source file associated with the DCMPix
         Returns:
            str: source file for DCMPix
        """
        response_pix_source_file = self.osirix_service.DCMPixSourceFile(self.osirixrpc_uid)
        self._source_file = self.response_processor.process_pix_source_file(response_pix_source_file)
        return self._source_file

    @property
    def image(self) -> ndarray:
        """
          Provides underlying image associated with the DCMPix
          Returns:
            ndarray: image data for DCMPix
        """
        response_pix_image = self.osirix_service.DCMPixImage(self.osirixrpc_uid)
        self._image = self.response_processor.process_pix_image(response_pix_image)
        return self._image

    # @image.setter - setter only allows one value so switch to using a method
    def set_image(self, image: ndarray, is_argb: bool) -> None:
        if is_argb:
            request = dcmpix_pb2.DCMPixSetImageRequest(pix=self.osirixrpc_uid, image_data_argb=image)

        else:
            request = dcmpix_pb2.DCMPixSetImageRequest(pix=self.osirixrpc_uid, image_data_float=image)

        response = self.osirix_service.DCMPixSetImage(request)
        self.response_processor.process_basic_response(response)

    def compute_roi(self, roi : ROI) -> Dict[str, float]:
        """
          Makes a gRPC request to compute ROIs of DCMPix and retrieves the statistics for the ROI in a dictionary.

          Examples:

           roi_dict = {
                'mean': ...,
                'total': ...,
                'std_dev': ...,
                'min': ...,
                'max': ...,
                'skewness': ...,
                'kurtosis': ...
            }

          Args:
            ROI: osirixrpc_uid of a ROI

          Returns:
            Dict containing the statistics of the ROI

        """
        request = dcmpix_pb2.DCMPixComputeROIRequest(pix=self.osirixrpc_uid, roi=roi.osirixrpc_uid)
        response = self.osirix_service.DCMPixComputeROI(request)
        roi_dict = self.response_processor.process_pix_compute_roi(response)

        return roi_dict

    def convert_to_bw(self) -> None:
        """
          Makes a gRPC request to convert DCMPix to black-white
          Returns:
            None
        """
        request = dcmpix_pb2.DCMPixConvertToBWRequest(pix = self.osirixrpc_uid, bw_channel = 3)
        response = self.osirix_service.DCMPixConvertToBW(request)
        self.response_processor.process_pix_convert_to_rgb_bw(response)


    def convert_to_rgb(self) -> None:
        """
          Makes a gRPC request to convert DCMPix to red-green-blue
          Returns:
            None
        """
        request = dcmpix_pb2.DCMPixConvertToRGBRequest(pix = self.osirixrpc_uid, rgb_channel = 3)
        response = self.osirix_service.DCMPixConvertToRGB(request)
        self.response_processor.process_pix_convert_to_rgb_bw(response)

    def get_map_from_roi(self, roi : ROI) -> ndarray:
        """
          Makes a gRPC request to retrieve the ROI map for the DCMPix
          Args:
            ROI: osirixrpc_uid of a ROI

          Returns:
            ndarray: ROI map
        """
        request = dcmpix_pb2.DCMPixGetMapFromROIRequest(pix=self.osirixrpc_uid, roi=roi.osirixrpc_uid)
        response = self.osirix_service.DCMPixGetMapFromROI(request)
        roi_map_array = self.response_processor.process_pix_roi_map(response)
        return roi_map_array

    def get_roi_values(self, roi : ROI) -> Tuple[ndarray]:
        """
          Makes a gRPC request to get the ROI values for the DCMPix

          Args:
            ROI: osirixrpc_uid of a ROI

          Returns:
            Tuple containing the ROI values (rows, columns, values) in ndarray
        """
        request = dcmpix_pb2.DCMPixROIValuesRequest(pix=self.osirixrpc_uid, roi=roi.osirixrpc_uid)
        response = self.osirix_service.DCMPixROIValues(request)
        roi_values = self.response_processor.process_pix_roi_values(response)

        return roi_values
    #TODO
    # Don't see their RPC in osirix.proto but can see response in dcmpix.prot
    def image_obj(self) -> DicomImage:
        """
          Makes a gRPC request to to retrieve the image obj for the DCMPix
          Returns:
              DicomImage: image for DCMPix
        """
        response_pix_dicom_image = self.osirix_service.DCMPixDicomImage(self.osirixrpc_uid)
        return DicomImage(response_pix_dicom_image, self.osirix_service)

    #TODO
    # Don't see their RPC in osirix.proto but can see response in dcmpix.prot
    def series_obj(self) -> DicomSeries:
        """
          Makes a gRPC request to to retrieve the series obj for the DCMPix
          Returns:
              DicomSeries: series for DCMPix
        """
        response_pix_dicom_series = self.osirix_service.DCMPixDicomSeries(self.osirixrpc_uid)
        return DicomSeries(response_pix_dicom_series, self.osirix_service)

    #TODO
    # Don't see their RPC in osirix.proto but can see response in dcmpix.prot
    def study_object(self) -> DicomStudy:
        """
          Makes a gRPC request to to retrieve the study obj for the DCMPix
          Returns:
              DicomStudy: study for DCMPix
        """
        response_pix_dicom_study = self.osirix_service.DCMPixDicomStudy(self.osirixrpc_uid)
        return DicomStudy(response_pix_dicom_study, self.osirix_service)

class ROI(object):
    '''
    Class representing the properties and methods to communicate with the Osirix service through
    gRPC for the ROIs in Osirix
    '''
    # osirixrpc_uid = None
    # response_processor = None
    # osirix_service = None

    def __init__(self,
                 osirixrpc_uid,
                 osirix_service):
        self.response_processor = ResponseProcessor()
        self.osirixrpc_uid = osirixrpc_uid
        self.osirix_service = osirix_service


    @property
    def color(self) -> Tuple[int, int, int]:
        """
          Makes a gRPC request to retrieve the color (r, g, b) for the ROI
          Returns:
              Tuple containing the color values (r, g, b) in int
        """
        response_roi_color = self.osirix_service.ROIColor(self.osirixrpc_uid)
        self._color = self.response_processor.process_roi_color(response_roi_color)
        return self._color

    @color.setter
    def color(self, color: Tuple[int, int, int]) -> None:
        """
          Makes a gRPC request to set the color (r, g, b) for the ROI

          Args:
            A Tuple containing the red, green, blue values for color

          Returns:
            None
        """
        r, g, b = color
        request = roi_pb2.ROISetColorRequest(roi=self.osirixrpc_uid, r=r, g=g, b=b)
        response_roi_color = self.osirix_service.ROISetColor(request)
        self.response_processor.process_basic_response(response_roi_color)

    @property
    def name(self) -> str:
        """
          Makes a gRPC request to get the name for the ROI
          Returns:
            str: name
        """
        response_roi_name = self.osirix_service.ROIName(self.osirixrpc_uid)
        self._name = self.response_processor.process_name(response_roi_name)
        return self._name

    @name.setter
    def name(self, name : str) -> None:
        """
          Makes a gRPC request to set the name for the ROI

          Args:
            str : name

          Returns:
            None
        """
        request = roi_pb2.ROISetNameRequest(roi=self.osirixrpc_uid, name=name)
        response_roi_name = self.osirix_service.ROISetName(request)
        self.response_processor.process_basic_response(response_roi_name)

    @property
    def opacity(self) -> float:
        """
          Makes a gRPC request to retrieve the opacity for the ROI

          Returns:
            float: opacity
        """

        response_roi_opacity = self.osirix_service.ROIOpacity(self.osirixrpc_uid)
        self._opacity = self.response_processor.process_roi_opacity(response_roi_opacity)
        return self._opacity

    @opacity.setter
    def opacity(self, opacity : float) -> None:
        """
          Makes a gRPC request to set the opacity for the ROI

          Args:
            float : opacity

          Returns:
            None
        """
        request = roi_pb2.ROISetOpacityRequest(roi=self.osirixrpc_uid, opacity=opacity)
        response = self.osirix_service.ROISetOpacity(request)
        self.response_processor.process_basic_response(response)

    @property
    def points(self) -> ndarray:
        """
          Makes a gRPC request to retrieve the points for the ROI

          Returns:
            ndarray: points
        """
        response_roi_points = self.osirix_service.ROIPoints(self.osirixrpc_uid)
        self._points = self.response_processor.process_roi_points(response_roi_points)
        return self._points

    # TODO
    # @points.setter
    # def points(self, points : ndarray) -> None:
    #     request = roi_pb2.ROISetPointsRequest(roi=self.osirixrpc_uid, point=points)
    #     response = self.osirix_service.SetROIPoints(request)
    #     self.response_processor.process_basic_response(response)

    @property
    def thickness(self) -> float:
        """
          Makes a gRPC request to retrieve the thickness for the ROI

          Returns:
            float: thickness
        """
        response_roi_thickness = self.osirix_service.ROIThickness(self.osirixrpc_uid)
        self._thickness = self.response_processor.process_roi_thickness(response_roi_thickness)
        return self._thickness

    @thickness.setter
    def thickness(self, thickness : float) -> None:
        """
          Makes a gRPC request to set the thickness for the ROI

          Args:
            float : thickness

          Returns:
            None
        """
        request = roi_pb2.ROISetThicknessRequest(roi=self.osirixrpc_uid, thickness=thickness)
        response = self.osirix_service.ROISetThickness(request)
        self.response_processor.process_basic_response(response)

    @property
    def pix(self) -> DCMPix:
        """
          Makes a gRPC request to retrieve the DCMPix for the ROI

          Returns:
            DCMPix : pix that ROI is drawn on
        """
        response_roi_pix = self.osirix_service.ROIPix(self.osirixrpc_uid)
        roi_pix = self.response_processor.process_roi_pix(response_roi_pix)
        self._pix = DCMPix(roi_pix, self.osirix_service)
        return self._pix

    #TODO Can't see proto message for type
    @property
    # def type(self) -> str:
    #     return self._type

    def centroid(self) -> Tuple[float, float]:
        """
          Makes a gRPC request to retrieve the centroid (x, y) for the ROI

          Returns:
            A Tuple containing centroid information (x, y)
        """
        response = self.osirix_service.ROICentroid(self.osirixrpc_uid)
        return (response.x , response.y)

    def flip_horizontally(self) -> None:
        """
          Makes a gRPC request to flip the ROI horizontally

          Returns:
            None
        """
        response = self.osirix_service.ROIFlipHorizontally(self.osirixrpc_uid)
        self.response_processor.process_basic_response(response)

    def flip_vertically(self) -> None:
        """
          Makes a gRPC request to flip the ROI vertically
          Returns:
            None
        """
        response = self.osirix_service.ROIFlipVertically(self.osirixrpc_uid)
        self.response_processor.process_basic_response(response)

    def roi_area(self) -> float :
        """
          Makes a gRPC request to retrieve the area for the ROI

          Returns:
            float : area of ROI
        """
        response = self.osirix_service.ROIArea(self.osirixrpc_uid)
        return response.area

    def roi_move(self, columns:float, rows:float) -> None:
        """
          Makes a gRPC request to move the ROI by rows and columns

          Args:
            float : columns
            float : rows

          Returns:
            None
        """
        request = roi_pb2.ROIMoveRequest(roi=self.osirixrpc_uid, columns=columns, rows=rows)
        response = self.osirix_service.ROIMove(request)
        self.response_processor.process_basic_response(response)

    def rotate(self, theta:float, center: Tuple[int, int]) -> None:
        """
          Makes a gRPC request to rotate the ROI using theta and center (x, y_

          Args:
            float : theta
            Tuple[int, int]: center

          Returns:
            None
        """
        # centroid_response = self.osirix_service.ROICentroid(self.osirixrpc_uid)
        x, y = center
        request = roi_pb2.ROIRotateRequest(roi=self.osirixrpc_uid, degrees=theta, x=x, y=y)
        response = self.osirix_service.ROIRotate(request)
        self.response_processor.process_basic_response(response)

class ViewerController(object):
    '''
    Class representing the properties and methods to communicate with the Osirix service through
    gRPC for a ViewerController
    '''

    def __init__(self, osirixrpc_uid, osirix_service):
        self.osirixrpc_uid = osirixrpc_uid
        self.osirix_service = osirix_service
        self.response_processor = ResponseProcessor()

    @property
    def idx(self) -> int:
        """
          Makes a gRPC request to retrieve the idx for the ViewerController

          Returns:
            int : idx
        """
        response_viewer_idx = self.osirix_service.ViewerControllerIdx(self.osirixrpc_uid)
        self._idx = self.response_processor.process_viewer_idx(response_viewer_idx)

        return self._idx

    @idx.setter
    def idx(self, idx=int) -> None:
        """
          Makes a gRPC request to set the idx for the ViewerController

          Args:
            int : idx

          Returns:
            None
        """
        request = viewercontroller_pb2.ViewerControllerSetIdxRequest(viewer_controller=self.osirixrpc_uid, idx=idx)
        response = self.osirix_service.ViewerControllerSetIdx(request)
        self.response_processor.process_basic_response(response)

    @property
    def modality(self) -> str:
        """
          Makes a gRPC request to retrieve the modality for the ViewerController

          Returns:
            str : modality
        """
        response_viewer_modality = self.osirix_service.ViewerControllerModality(self.osirixrpc_uid)
        self._modality = self.response_processor.process_modality(response_viewer_modality)

        return self._modality

    @property
    def movie_idx(self) -> int:
        """
          Makes a gRPC request to retrieve the movie idx for the ViewerController

          Returns:
            int : movie_idx
        """
        response_viewer_movie_idx = self.osirix_service.ViewerControllerMovieIdx(self.osirixrpc_uid)
        self._movie_idx = self.response_processor.process_viewer_movie_idx(response_viewer_movie_idx)

        return self._movie_idx

    @movie_idx.setter
    def movie_idx(self, movie_idx=int) -> None:
        """
          Makes a gRPC request to set the movie idx for the ViewerController

          Args:
            int : movie_idx

          Returns:
            None
        """
        request = viewercontroller_pb2.ViewerControllerSetMovieIdxRequest(viewer_controller=self.osirixrpc_uid, movie_idx=movie_idx)
        response = self.osirix_service.ViewerControllerSetMovieIdx(request)
        self.response_processor.process_basic_response(response)

    @property
    def title(self) -> str:
        """
          Makes a gRPC request to retrieve the title for the ViewerController

          Returns:
            str : title
        """
        response_viewer_title = self.osirix_service.ViewerControllerTitle(self.osirixrpc_uid)
        self._title = self.response_processor.process_title(response_viewer_title)

        return self._title

    @property
    def wlww(self) -> Tuple[float, float]:
        """
          Makes a gRPC request to retrieve the wlww for the ViewerController

          Returns:
            A Tuple containing wl and ww in float
        """
        response_viewer_wlww = self.osirix_service.ViewerControllerWLWW(self.osirixrpc_uid)
        viewer_wl, viewer_ww = self.response_processor.process_wlww(response_viewer_wlww)
        self._ww = viewer_ww
        self._wl = viewer_wl
        return (self._wl, self._ww)

    @wlww.setter
    def wlww(self, wlww : Tuple[float, float]) -> None:
        """
          Makes a gRPC request to set the wlww for the ViewerController

          Args:
            Tuple[float, float] : wlww

          Returns:
            None
        """
        wl, ww = wlww
        request = viewercontroller_pb2.ViewerControllerSetWLWWRequest(viewer_controller=self.osirixrpc_uid, wl=wl, ww=ww)
        response = self.osirix_service.ViewerControllerSetWLWW(request)
        self.response_processor.process_basic_response(response)

    def process_viewer_pix_list(self, response) -> Tuple[DCMPix, ...]:
        """
          Process gRPC response to retrieve the pix list for the ViewerController

          Args:
            response : response from ViewerControllerPixListResponse

          Returns:
            A Tuple containing DCMPix
        """
        pix_tuple: Tuple[DCMPix, ...] = ()
        for pix in response.pix:
            dcm_pix = DCMPix(pix, self.osirix_service)
            pix_tuple = pix_tuple + (dcm_pix,)

        return pix_tuple

    def process_viewer_roi_list(self, response) -> Tuple[ROI, ...]:
        """
          Process gRPC response to retrieve the roi list for the ViewerController

          Args:
            response : response from ViewerControllerROIListResponse

          Returns:
            A Tuple containing ROIs
        """
        roi_tuple: Tuple[ROI, ...] = ()
        for roi_slice in response.roi_slices:
            roi = ROI(roi_slice, self.osirix_service)
            roi_tuple = roi_tuple + (roi,)
        return roi_tuple

    def process_viewer_rois(self, response) -> Tuple[ROI, ...]:
        """
          Process gRPC response to retrieve the ROIs for the ViewerController

          Args:
            response : response from ViewerControllerROIsWithNameResponse/ViewerControllerSelectedROIsResponse

          Returns:
            A Tuple containing DCMPix
        """
        roi_tuple: Tuple[ROI, ...] = ()
        for roi in response.rois:
            roi = ROI(roi, self.osirix_service)
            roi_tuple = roi_tuple + (roi,)
        return roi_tuple

    def process_vr_controllers(self, response) -> Tuple[VRController, ...]:
        """
          Process gRPC response to retrieve the VR controllers for the ViewerController

          Args:
            response : response from ViewerControllerVRControllersResponse

          Returns:
            A Tuple containing VR Controllers`
        """
        vr_tuple: Tuple[VRController, ...] = ()
        for vr_controller in response.vr_controllers:
            vr_controller_obj = VRController(vr_controller, self.osirix_service)
            vr_tuple = vr_tuple + (vr_controller_obj,)
        return vr_tuple

    # # returns VC
    def blending_controller(self) -> ViewerController:
        """
          Process gRPC response to retrieve the blending controller for the ViewerController

          Returns:
            ViewerController
        """

        # Multiple VR Controllers case?
        vr_controller = self.osirix_service.ViewerControllerVRControllers(self.osirixrpc_uid).vr_controllers[0]
        response = self.osirix_service.VRControllerBlendingController(vr_controller)
        return ViewerController(response.viewer_controller, self.osirix_service)

    def close_viewer(self) -> None:
        """
          Process gRPC request to close the ViewerController

          Returns:
            None
        """
        response = self.osirix_service.ViewerControllerCloseViewer(self.osirixrpc_uid)
        self.response_processor.process_images(response)

    # returns VC
    def copy_viewer_window(self, in_4d: bool = False) -> ViewerController:
        """
          Process gRPC request to copy the viewer window for the ViewerController

          Args:
            bool : in_4d

          Returns:
            ViewerController
        """
        request = viewercontroller_pb2.ViewerControllerCopyViewerWindowRequest(viewer_controller=self.osirixrpc_uid, in_4d=in_4d)
        response = self.osirix_service.ViewerControllerCopyViewerWindow(request)
        self.response_processor.process_basic_response(response)

        return ViewerController(self.osirixrpc_uid,self.osirix_service)

    def cur_dcm(self) -> DCMPix:
        """
          Process gRPC request to retrieve current dicom pix for the ViewerController

          Returns:
            DCMPix: current dicom picture for ViewerController
        """
        pix = self.osirix_service.ViewerControllerCurDCM(self.osirixrpc_uid).pix
        dcm_pix = DCMPix(pix, self.osirix_service)
        return dcm_pix

    #TODO wait for Wait protobuf to be exposed
    # def end_wait_window(self, window: Wait):

    def is_data_volumic(self, in_4d: bool = False) -> bool:
        """
          Process gRPC request to retrieve the is_data_volumic flag for the ViewerController

          Args:
            bool : in_4d

          Returns:
            bool : whether data is volumic
        """
        request = viewercontroller_pb2.ViewerControllerIsDataVolumicRequest(viewer_controller=self.osirixrpc_uid, in_4d=in_4d)
        response = self.osirix_service.ViewerControllerIsDataVolumic(request)
        return response.in_4d

    def max_movie_index(self) -> int:
        """
          Process gRPC request to retrieve max movie idx for the ViewerController

          Returns:
            int : max movie inde
        """
        response = self.osirix_service.ViewerControllerMaxMovieIdx(self.osirixrpc_uid)
        return response.max_movie_idx

    def needs_display_update(self) -> None:
        """
          Process gRPC requqest to check whether the ViewerController needs display update

          Returns:
            None
        """
        response = self.osirix_service.ViewerControllerNeedsDisplayUpdate(self.osirixrpc_uid)
        self.response_processor.process_basic_response(response)

    def pix_list(self, movie_idx: int) -> Tuple[DCMPix, ...]:
        """
          Process gRPC response to retrieve the VR controllers for the ViewerController

          Args:
            response : response from ViewerControllerVRControllersResponse

          Returns:
            A Tuple containing VR Controllers`
        """
        request = viewercontroller_pb2.ViewerControllerPixListRequest(viewer_controller=self.osirixrpc_uid, movie_idx=movie_idx)
        response = self.osirix_service.ViewerControllerPixList(request)
        pix_tuple = self.process_viewer_pix_list(response)

        return pix_tuple

    def resample_viewer_controller(self, vc : ViewerController) -> ViewerController:
        """
          Process gRPC request to resample the ViewerController based on another fixed ViewerController

          Args:
            ViewerController : ViewerController to resameple from

          Returns:
            ViewerController
        """
        request = viewercontroller_pb2.ViewerControllerResampleViewerControllerRequest(
                                                            viewer_controller=self.osirixrpc_uid,
                                                            fixed_viewer_controller=vc.osirixrpc_uid)

        response = self.osirix_service.ViewerControllerResampleViewerController(request)
        self.response_processor.process_basic_response(response)
        return ViewerController(self.osirixrpc_uid, self.osirix_service)

    # Check ROISlice and ROI
    def roi_list(self, movie_idx:int) -> Tuple[ROI, ...]:
        """
          Process gRPC request to retrieve the list of ROIs based on movie_idx for the ViewerController

          Args:
            int: movie_idx

          Returns:
            A Tuple containing ROIs
        """
        request = viewercontroller_pb2.ViewerControllerROIListRequest(viewer_controller=self.osirixrpc_uid,
                                                                      movie_idx=movie_idx)
        response = self.osirix_service.ViewerControllerROIList(request)

        roi_tuple = self.process_viewer_roi_list(response)

        return roi_tuple


    def rois_with_name(self, name: str, movie_idx: int, in_4d: bool = False) -> Tuple[ROI, ...]:
        """
          Process gRPC request to retrieve the list of ROIs based on movie_idx for the ViewerController

          Args:
            str: name
            int: movie_idx
            bool : in_4d

          Returns:
            A Tuple containing ROIs
        """
        request = viewercontroller_pb2.ViewerControllerROIsWithNameRequest(viewer_controller=self.osirixrpc_uid,
                                                                           name=name,
                                                                           movie_idx=movie_idx,
                                                                           in_4d=in_4d)
        response = self.osirix_service.ViewerControllerROIsWithName(request)
        roi_tuple = self.process_viewer_rois(response)

        return roi_tuple

    def selected_rois(self) -> Tuple[ROI, ...]:
        """
          Process gRPC request to retrieve ROIs that are selected for the ViewerController

          Returns:
            A Tuple containing ROIs
        """
        response = self.osirix_service.ViewerControllerSelectedROIs(self.osirixrpc_uid)
        roi_tuple = self.process_viewer_rois(response)

        return roi_tuple

    #TODO implement this when the TypeResponse protobuf is exposed

    # def set_roi(self, roi: ROI, position: int, movie_idx: int) -> None:
    #     #Mask
    #     buffer_array = np.random.randn(40 * 40) > 0
    #     buffer = viewercontroller_pb2.ViewerControllerNewROIRequest.Buffer(buffer=1 * buffer_array, rows=40,
    #                                                                        columns=40)
    #
    #     r, g, b = roi.color
    #     color = viewercontroller_pb2.ViewerControllerNewROIRequest.Color(r=r, g=g, b=b)
    #     request = viewercontroller_pb2.ViewerControllerNewROIRequest(viewer_controller=self.osirixrpc_uid,
    #                                                                  movie_idx=movie_idx,
    #                                                                  position=position,
    #                                                                  itype=20,
    #                                                                  buffer=buffer,
    #                                                                  color=color,
    #                                                                  opacity=roi.opacity,
    #                                                                  name=roi.name)
    #     response = self.osirix_service.ViewerControllerNewROI(request)
    #     print(response.roi)
    #
    #     # How to decide between which ROI to create
    #
    #     #Oval
    #     rect = viewercontroller_pb2.ViewerControllerNewROIRequest.Rect(origin_x=66., origin_y=42., width=20.,
    #                                                                    height=10.)
    #     color = viewercontroller_pb2.ViewerControllerNewROIRequest.Color(r=255, g=100, b=200)
    #     request = viewercontroller_pb2.ViewerControllerNewROIRequest(viewer_controller=self.viewer_controller,
    #                                                                  movie_idx=0, position=0, itype=9,
    #                                                                  rectangle=rect, color=color, opacity=0.5,
    #                                                                  name="oval", thickness=3.0)
    #     response = self.osirix_service.ViewerControllerNewROI(request)
    #     self.assertEqual(response.status.status, 1)
    #     print(response.roi)
    #
    #     # Arrow
    #     # Points seem to go in order [head, tail]
    #     color = viewercontroller_pb2.ViewerControllerNewROIRequest.Color(r=0, g=255, b=0)
    #     points = [viewercontroller_pb2.ViewerControllerNewROIRequest.Point2D(x=66., y=42.),
    #               viewercontroller_pb2.ViewerControllerNewROIRequest.Point2D(x=99., y=24.)]
    #     request = viewercontroller_pb2.ViewerControllerNewROIRequest(viewer_controller=self.viewer_controller,
    #                                                                  points=points, movie_idx=0, position=0,
    #                                                                  itype=14, color=color, opacity=0.5,
    #                                                                  name="arrow", thickness=3.0)
    #     response = self.osirix_service.ViewerControllerNewROI(request)
    #     print(response.roi)
    #
    #     #Point
    #     rect = viewercontroller_pb2.ViewerControllerNewROIRequest.Rect(origin_x=66., origin_y=42., width=20.,
    #                                                                    height=10.)
    #     color = viewercontroller_pb2.ViewerControllerNewROIRequest.Color(r=0, g=255, b=255)
    #     request = viewercontroller_pb2.ViewerControllerNewROIRequest(viewer_controller=self.viewer_controller,
    #                                                                  rectangle=rect, movie_idx=0, position=0,
    #                                                                  itype=19, color=color, opacity=1.0,
    #                                                                  name="point", thickness=3.0)
    #     response = self.osirix_service.ViewerControllerNewROI(request)
    #     print(response.roi)
    #
    #     # A rectangle TROI
    #     rect = viewercontroller_pb2.ViewerControllerNewROIRequest.Rect(origin_x=66., origin_y=42., width=20.,
    #                                                                    height=10.)
    #     color = viewercontroller_pb2.ViewerControllerNewROIRequest.Color(r=255, g=100, b=100)
    #     request = viewercontroller_pb2.ViewerControllerNewROIRequest(viewer_controller=self.viewer_controller,
    #                                                                  rectangle=rect, movie_idx=0, position=0,
    #                                                                  itype=6, color=color, opacity=1.0, name="tROI",
    #                                                                  thickness=3.0)
    #     response = self.osirix_service.ViewerControllerNewROI(request)
    #     self.assertEqual(response.status.status, 1)
    #     print(response.roi)
    #
    #     #Text
    #     rect = viewercontroller_pb2.ViewerControllerNewROIRequest.Rect(origin_x=66., origin_y=42., width=20.,
    #                                                                    height=10.)
    #     color = viewercontroller_pb2.ViewerControllerNewROIRequest.Color(r=255, g=100, b=100)
    #     request = viewercontroller_pb2.ViewerControllerNewROIRequest(viewer_controller=self.viewer_controller,
    #                                                                  rectangle=rect, movie_idx=0, position=0,
    #                                                                  itype=13, color=color, opacity=1.0,
    #                                                                  name="Some text", thickness=3.0)
    #     response = self.osirix_service.ViewerControllerNewROI(request)
    #     print(response.roi)
    #
    #     #TTAGT
    #     points = [[50.20499802, 32.32217407], [53.27367783, 38.77323914], [64.68674469, 25.43341637],
    #               [69.71873474, 36.01180649], [41.8967247, 36.27430344], [68.91729736, 23.42099953]]
    #     points = [viewercontroller_pb2.ViewerControllerNewROIRequest.Point2D(x=p[0], y=p[1]) for p in points]
    #     print(len(points))
    #     color = viewercontroller_pb2.ViewerControllerNewROIRequest.Color(r=100, g=250, b=220)
    #     request = viewercontroller_pb2.ViewerControllerNewROIRequest(viewer_controller=self.viewer_controller,
    #                                                                  points=points, movie_idx=0, position=0,
    #                                                                  itype=29, color=color, opacity=1.0,
    #                                                                  name="tTAGT", thickness=3.0)
    #     response = self.osirix_service.ViewerControllerNewROI(request)
    #     print(response.roi)
    #
    #     #Pencil
    #     points = [[50.20499802, 32.32217407], [53.27367783, 38.77323914], [64.68674469, 25.43341637],
    #               [69.71873474, 36.01180649], [41.8967247, 36.27430344], [68.91729736, 23.42099953]]
    #     points = [viewercontroller_pb2.ViewerControllerNewROIRequest.Point2D(x=p[0], y=p[1]) for p in points]
    #     color = viewercontroller_pb2.ViewerControllerNewROIRequest.Color(r=100, g=50, b=220)
    #     request = viewercontroller_pb2.ViewerControllerNewROIRequest(viewer_controller=self.viewer_controller,
    #                                                                  points=points, movie_idx=0, position=0,
    #                                                                  itype=15, color=color, opacity=1.0,
    #                                                                  name="pencil", thickness=3.0)
    #     response = self.osirix_service.ViewerControllerNewROI(request)
    #     print(response.roi)
    #
    #     points = [viewercontroller_pb2.ViewerControllerNewROIRequest.Point2D(x=71., y=-2.), \
    #               viewercontroller_pb2.ViewerControllerNewROIRequest.Point2D(x=67., y=11.), \
    #               viewercontroller_pb2.ViewerControllerNewROIRequest.Point2D(x=90., y=9.)]
    #     color = viewercontroller_pb2.ViewerControllerNewROIRequest.Color(r=100, g=50, b=220)
    #     request = viewercontroller_pb2.ViewerControllerNewROIRequest(viewer_controller=self.viewer_controller,
    #                                                                  points=points, movie_idx=0, position=0,
    #                                                                  itype=12, color=color, opacity=1.0,
    #                                                                  name="pencil", thickness=3.0)
    #     response = self.osirix_service.ViewerControllerNewROI(request)
    #     print(response.roi)
    #
    #     # Measure
    #     points = [viewercontroller_pb2.ViewerControllerNewROIRequest.Point2D(x=71., y=-2.), \
    #               viewercontroller_pb2.ViewerControllerNewROIRequest.Point2D(x=67., y=11.)]
    #     color = viewercontroller_pb2.ViewerControllerNewROIRequest.Color(r=100, g=50, b=0)
    #     request = viewercontroller_pb2.ViewerControllerNewROIRequest(viewer_controller=self.viewer_controller,
    #                                                                  points=points, movie_idx=0, position=0,
    #                                                                  itype=5, color=color, opacity=1.0,
    #                                                                  name="measure", thickness=3.0)
    #     response = self.osirix_service.ViewerControllerNewROI(request)
    #     print(response.roi)

    #TODO No response in osirix.proto

    # def start_wait_progress_window(self, message: str, max: int) -> Wait:

    def vr_controllers(self) -> Tuple[VRController, ...]:
        """
          Process gRPC request to retrieve the VR Controllers for the ViewerController

          Returns:
            None
        """
        response = self.osirix_service.ViewerControllerVRControllers(self.osirixrpc_uid)
        vr_tuple = self.process_vr_controllers(response)

        return vr_tuple



    @classmethod
    def name(cls):
        cls.__name__

class VRController(object):
    '''
    Class representing the properties and methods to communicate with the Osirix service through
    gRPC for a VRController
    '''

    def __init__(self,
                 osirixrpc_uid : str,
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
        self._rendering_mode = self.response_processor.process_vr_rendering_mode(response_vr_rendering_mode)

        return self._rendering_mode

    @rendering_mode.setter
    def rendering_mode(self, rendering_mode : str) -> None:
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
        self._style = self.response_processor.process_vr_style(response_vr_style)

        return self._style

    @property
    def title(self) -> str:
        """
          Process gRPC request to retrieve the title for the VRController

          Returns:
            str : title
        """
        response_vr_title = self.osirix_service.VRControllerTitle(self.osirixrpc_uid)
        self._title = self.response_processor.process_title(response_vr_title)

        return self._title

    @property
    def wlww(self) -> Tuple[float, float]:
        """
          Process gRPC request to retrive the wlww for the VRController

          Returns:
            Tuple containing wl and ww in float
        """
        response_vr_wlww = self.osirix_service.VRControllerWLWW(self.osirixrpc_uid)
        vr_wl, vr_ww = self.response_processor.process_wlww(response_vr_wlww)

        return (vr_wl, vr_ww)

    @wlww.setter
    def wlww(self, wlww : Tuple[float, float]) -> None:
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


