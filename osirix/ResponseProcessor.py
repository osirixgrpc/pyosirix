import datetime
from typing import Tuple, Dict

import sys
import numpy as np
from numpy import ndarray

from osirix.Exceptions import GrpcException

# sys.path.append("../../src/python")
import osirix.pb2.osirix_pb2 as osirix_pb2
import osirix.pb2.dicomstudy_pb2 as dicomstudy_pb2

#TODO break the responseprocessor into smaller parts
class ResponseProcessor(object):
    """
    Class that processes all the gRPC response to extract the information required from it
    to build the pyOsirix objects
    """

    def __init__(self) -> None:
        # print("Response Processor Started")
        pass

    def process_basic_response(self, response) -> None:
        """
        Checks whether the status of the response is success or not
        Args:
            response: response returned by Osirix service for the request made

        Returns:
             None
        """
        if (response.status.status == 1):
            pass
        else:
            raise GrpcException("No response")

    # What should be the type of the response? It is the response classes in the protobufs
    def process_displayed_2d_viewers(self, response) -> Tuple[osirix_pb2.OsirixDisplayed2DViewersResponse, ...]:
        """
         Extract displayed viewer controllers from the response
         Args:
             response: response returned by Osirix service for the request made

        Returns:
             Tuple containing osirixrpc_uid of displayed 2d viewers for BrowserController
        """

        viewers_tuple : Tuple[osirix_pb2.OsirixDisplayed2DViewersResponse, ...] = ()

        for viewer_controller in response.viewer_controllers:

            viewers_tuple = viewers_tuple + (viewer_controller,)

        return viewers_tuple

    def process_displayed_vr_controllers(self, response) -> Tuple[osirix_pb2.OsirixDisplayedVRControllersResponse, ...]:
        """
         Extract displayed VR controllers from the response

         Args:
             response: response returned by Osirix service for the request made

         Returns:
             Tuple containing osirixrpc_uid of displayed VR Controllers for BrowserController
        """

        vr_controllers_tuple : Tuple[osirix_pb2.OsirixDisplayedVRControllersResponse, ...] = ()

        for vr_controller in response.vr_controllers:

            vr_controllers_tuple = vr_controllers_tuple + (vr_controller,)

        return vr_controllers_tuple

    def process_modality(self, response) -> str:
        """
         Extract modality from the response

         Args:
             response: response returned by Osirix service for the request made

         Returns:
             str : modality
        """
        if (response.status.status == 1):

            return response.modality
        else:
            raise GrpcException("No response")

    def process_name(self, response) -> str:
        """
         Extract name from the response

         Args:
             response: response returned by Osirix service for the request made

         Returns:
             str : name
        """
        if (response.status.status == 1):

            return response.name
        else:
            raise GrpcException("No response")

    def process_title(self, response) -> str:
        """
         Extract title from the response

         Args:
             response: response returned by Osirix service for the request made

         Returns:
            str: title
        """
        if (response.status.status == 1):

            return response.title
        else:
            # print("No title response")
            raise GrpcException("No response")

    def process_wlww(self, response):
        """
         Extract wlww from the response

         Args:
             response: response returned by Osirix service for the request made

         Returns:
             int: wl
             int: ww
        """
        if (response.status.status == 1):

            return response.wl, response.ww
        else:
            raise GrpcException("No response")

    def process_no_images(self, response) -> int:
        """
         Extract number of images from the response

         Args:
             response: response returned by Osirix service for the request made

         Returns:
             int : number of images
        """
        if (response.status.status == 1):

            return response.no_images
        else:
            raise GrpcException("No response")

    #DicomStudy
    def process_datetime(self, response: dicomstudy_pb2.DicomStudyDateResponse) -> datetime.datetime:
        """
         Extract datetime from the response

         Args:
             response: response returned by Osirix service for the request made

         Returns:
             datetime : date and time
        """
        if (response.status.status == 1):
            datetime_output : datetime.datetime = datetime.datetime(response.year,
                                       response.month,
                                       response.day,
                                       response.hour,
                                       response.minute,
                                       response.second
                                   )
            return datetime_output
        else:
            raise GrpcException("No response for datetime")

    def process_dob_datetime(self, response: dicomstudy_pb2.DicomStudyDateOfBirthResponse) -> datetime.datetime:
        """
         Extract date of birth of patient from the response

         Args:
             response: response returned by Osirix service for the request made

         Returns:
             datetime : date of birth of patient for study
         """
        if (response.status.status == 1):
            datetime_output : datetime.datetime = datetime.datetime(response.year,
                                       response.month,
                                       response.day
                                   )
            return datetime_output
        else:
            raise GrpcException("No response for datetime")

    def process_institution_name(self, response) -> str:
        """
         Extract institution name from the response

         Args:
             response: response returned by Osirix service for the request made

         Returns:
             str : institution name for study
        """
        if (response.status.status == 1):

            return response.institution_name
        else:
            raise GrpcException("No response")

    def process_study_modality(self, response) -> str:
        """
         Extract modalities of the study from the response

         Args:
             response: response returned by Osirix service for the request made
         Returns:
             str : modalities for study
        """
        if (response.status.status == 1):

            return response.modalities
        else:
            raise GrpcException("No response")



    # def process_series_modality(self, response) -> str:
    #     if (response.status.status == 1):
    #
    #         return response.modality
    #     else:
    #         raise GrpcException("No response")

    def process_patient_id(self, response) -> str:
        """
         Extract patient id from the response

         Args:
             response: response returned by Osirix service for the request made

         Returns:
             str : patient id for study
        """
        if (response.status.status == 1):

            return response.patient_id
        else:
            raise GrpcException("No response")

    def process_patient_uid(self, response) -> str:
        """
         Extract patient uid from the response

         Args:
             response: response returned by Osirix service for the request made

         Returns:
             str : patient uid for study
        """
        if (response.status.status == 1):

            return response.patient_uid
        else:
            raise GrpcException("No response")

    def process_patient_sex(self, response) -> str:
        """
         Extract patient's sex from the response

         Args:
             response: response returned by Osirix service for the request made

         Returns:
             str : patient sex for study
        """
        if (response.status.status == 1):

            return response.patient_sex
        else:
            raise GrpcException("No response")

    def process_performing_physician(self, response) -> str:
        """
         Extract performing physician from the response

         Args:
             response: response returned by Osirix service for the request made

         Returns:
             str : performing physician for study
        """
        if (response.status.status == 1):

            return response.performing_physician
        else:
            raise GrpcException("No response")

    def process_referring_physician(self, response) -> str:
        """
         Extract referring physician from the response

         Args:
             response: response returned by Osirix service for the request made

         Returns:
             str : referring physician for study
        """
        if (response.status.status == 1):

            return response.referring_physician
        else:
            raise GrpcException("No response")

    # def process_series_name(self, response):
    #     if (response.status.status == 1):
    #
    #         return response.name
    #     else:
    #         raise GrpcException("No response")

    def process_study_study_name(self, response) -> str:
        """
         Extract name of the study from the response

         Args:
             response: response returned by Osirix service for the request made

         Returns:
             str : study name for study
        """
        if (response.status.status == 1):

            return response.study_name
        else:
            raise GrpcException("No response")

    def process_study_instance_uid(self, response) -> str:
        """
         Extract study instance uid from the response

         Args:
             response: response returned by Osirix service for the request made

         Returns:
             str : instance uid for study
        """
        if (response.status.status == 1):

            return response.study_instance_uid
        else:
            raise GrpcException("No response")


    def process_paths(self, response) -> Tuple[str, ...]:
        """
         Extract paths from the response

         Args:
             response: response returned by Osirix service for the request made
         Returns:
             Tuple containing file paths for study in str

        """
        if (response.status.status == 1):

            return tuple(response.paths)
        else:
            raise GrpcException("No response")

    def process_images(self, response):
        """
         Extract images from the response

         Args:
             response: response returned by Osirix service for the request made

         Returns:
             osirixrpc_uid of images for study
        """
        if (response.status.status == 1):

            images_tuple = ()

            for image in response.images:
                # print(series.osirixrpc_uid)
                # images_tuple = images_tuple + (image.osirixrpc_uid,)
                images_tuple = images_tuple + (image,)

            return images_tuple
        else:
            raise GrpcException("No response")

    def process_num_files(self, response) -> int:
        """
         Extract number of files from the response

         Args:
             response: response returned by Osirix service for the request made

         Returns:
             int : number of files for study

        """
        if (response.status.status == 1):

            return response.no_files
        else:
            raise GrpcException("No response")

    def process_study_series(self, response):
        """
         Extract the all the series that are a part of the study from the response

         Args:
             response: response returned by Osirix service for the request made

         Returns:
             osirixrpc_uid of all the series for study
         """
        if (response.status.status == 1):
            series_tuple = ()

            for series in response.series:
                # print(series.osirixrpc_uid)
                # series_tuple = series_tuple + (series.osirixrpc_uid,)
                series_tuple = series_tuple + (series,)

            return series_tuple
        else:
            raise GrpcException("No response")

    # Dicom Series
    def process_series_description(self, response) -> str:
        """
         Extract series description from the response

         Args:
             response: response returned by Osirix service for the request made

         Returns:
             str: series description for series
        """
        if (response.status.status == 1):

            return response.series_description
        else:
            raise GrpcException("No response")

    def process_series_instance_uid(self, response) -> str:
        """
         Extract series instance uid from the response

         Args:
             response: response returned by Osirix service for the request made

        Returns:
             str: instance uid for series
        """
        if (response.status.status == 1):

            return response.series_instance_uid
        else:
            raise GrpcException("No response")

    def process_series_sop_class_uid(self, response) -> str:
        """
         Extract series sop class uid from the response

         Args:
             response: response returned by Osirix service for the request made

         Returns:
             str: sop class uid for series
        """
        if (response.status.status == 1):

            return response.series_sop_class_uid
        else:
            raise GrpcException("No response")

    def process_series_previous_series(self, response):
        """
         Extract previous series in the study from the response

         Args:
             response: response returned by Osirix service for the request made
         Returns:
             osirixrpc_uid of previous series for image

        """
        if (response.status.status == 1):

            # return response.previous_series.osirixrpc_uid
            return response.previous_series
        else:
            raise GrpcException("No response")

    def process_series_next_series(self, response):
        """
         Extract next series in the study from the response

         Args:
             response: response returned by Osirix service for the request made

         Returns:
             osirixrpc_uid of next series for image
        """
        if (response.status.status == 1):

            # return response.next_series.osirixrpc_uid
            return response.next_series
        else:
            raise GrpcException("No response")

    def process_series_study(self, response):
        """
         Extract the study that the series belongs to from the response

         Args:
             response: response returned by Osirix service for the request made

         Returns:
             osirixrpc_uid of study for image

        """
        if (response.status.status == 1):

            # return response.study.osirixrpc_uid
            return response.study
        else:
            raise GrpcException("No response")

    def process_series_sorted_image(self, response):
        """
         Extract sorted images of the series from the response

         Args:
             response: response returned by Osirix service for the request made

         Returns:
             Tuple containing osirixrpc_uid of sorted images for image
        """
        if (response.status.status == 1):
            sorted_image_tuple = ()

            for sorted_image in response.sorted_images:
                sorted_image_tuple = sorted_image_tuple + (sorted_image,)
                # sorted_image_tuple = sorted_image_tuple + (sorted_image.osirixrpc_uid,)

            return sorted_image_tuple
        else:
            raise GrpcException("No response")

    # Dicom Image
    def process_image_instance_number(self, response) -> int:
        """
         Extract iamge instance number from the response

         Args:
             response: response returned by Osirix service for the request made
         Returns:
             int: instance number for image

        """
        if (response.status.status == 1):

            return response.instance_number
        else:
            raise GrpcException("No response")

    # def process_image_modality(self, response) -> str:
    #     if (response.status.status == 1):
    #
    #         return response.modality
    #     else:
    #         raise GrpcException("No response")

    def process_image_number_of_frames(self, response) -> int:
        """
         Extract number of frames in the image from the response

         Args:
             response: response returned by Osirix service for the request made

         Returns:
             int: number of frames for image

        """
        if (response.status.status == 1):

            return response.number_of_frames
        else:
            raise GrpcException("No response")

    def process_image_slice_location(self, response) -> float:
        """
         Extract slice location of the image from the response

         Args:
             response: response returned by Osirix service for the request made

         Returns:
             float: slice location for image
        """
        if (response.status.status == 1):

            return response.slice_locations
        else:
            raise GrpcException("No response")

    def process_image_series(self, response):
        """
         Extract series that the image belongs to from the response

         Args:
             response: response returned by Osirix service for the request made
         Returns:
             osirixrpc_uid of series for image

        """
        if (response.status.status == 1):

            # return response.series.osirixrpc_uid
            return response.series
        else:
            raise GrpcException("No response")

    def process_image_height(self, response) -> int:
        """
         Extract height of the image from the response

         Args:
             response: response returned by Osirix service for the request made

         Returns:
             int: height for image
        """
        if (response.status.status == 1):

            return response.height
        else:
            raise GrpcException("No response")

    def process_image_width(self, response) -> int:
        """
         Extract width of the image from the response

         Args:
             response: response returned by Osirix service for the request made

         Returns:
             int: width for image
        """
        if (response.status.status == 1):

            return response.width
        else:
            raise GrpcException("No response")

    def process_image_sop_instance_uid(self, response) -> str:
        """
         Extract sop instance uid of the image from the response

         Args:
             response: response returned by Osirix service for the request made

         Returns:
             str: sop class instance uid for image

        """
        if (response.status.status == 1):

            return response.sop_instance_uid
        else:
            raise GrpcException("No response")

    def process_image_complete_path(self, response) -> str:
        """
         Extract complete path of the image from the response

         Args:
             response: response returned by Osirix service for the request made

        Returns:
             str: complete path for image

        """
        if (response.status.status == 1):

            return response.path_name
        else:
            raise GrpcException("No response")

    # VR Controller

    # def process_vr_title(self, response) -> str:
    #     if (response.status.status == 1):
    #
    #         return response.title
    #     else:
    #         # print("No title response")
    #         raise GrpcException("No response")

    def process_vr_style(self, response) -> str:
        """
         Extract style of VR controller from the response

         Args:
             response: response returned by Osirix service for the request made
         Returns:
             int: style for VRController
        """
        if (response.status.status == 1):

            return response.style
        else:
            raise GrpcException("No response")

    def process_vr_rendering_mode(self, response) -> str:
        """
         Extract rendering mode of VR controller from the response

         Args:
             response: response returned by Osirix service for the request made

         Returns:
             int: rendering mode for VRController

        """
        if (response.status.status == 1):

            return response.rendering_mode
        else:
            raise GrpcException("No response")

    # def process_vr_wlww(self, response):
    #     if (response.status.status == 1):
    #
    #         return response.wl, response.ww
    #     else:
    #         raise GrpcException("No response")

    def process_blending_controller(self, response):
        """
         Extract blending controller from the response

         Args:
             response: response returned by Osirix service for the request made

         Returns:
             osirixrpc_uid for ViewerController
        """
        if (response.status.status == 1):

            # return response.viewer_controller.osirixrpc_uid
            return response.viewer_controller

        else:
            raise GrpcException("No response")

    def process_viewer_2d(self, response):
        """
         Extract 2D viewer from the response

         Args:
             response: response returned by Osirix service for the request made

         Returns:
             osirixrpc_uid for ViewerController
        """
        if (response.status.status == 1):

            # return response.viewer_controller.osirixrpc_uid
            return response.viewer_controller

        else:
            raise GrpcException("No response")

    # Viewer Controller
    # def process_viewer_wlww(self, response):
    #     if (response.status.status == 1):
    #
    #         return response.wl, response.ww
    #     else:
    #         raise GrpcException("No response")

    # def process_viewer_modality(self, response):
    #     if (response.status.status == 1):
    #
    #         return response.modality
    #     else:
    #         raise GrpcException("No response")

    # def process_viewer_title(self, response):
    #     if (response.status.status == 1):
    #
    #         return response.title
    #     else:
    #         raise GrpcException("No response")

    def process_viewer_idx(self, response) -> int:
        """
         Extract idx of the ViewerController from the response

         Args:
             response: response returned by Osirix service for the request made

         Returns:
             int : idx
        """
        if (response.status.status == 1):

            return response.idx
        else:
            raise GrpcException("No response")

    def process_viewer_movie_idx(self, response) -> int:
        """
         Extract movie_idx of the ViewerController from the response

         Args:
             response: response returned by Osirix service for the request made

         Returns:
             int : movie idx
        """
        if (response.status.status == 1):

            return response.movie_idx
        else:
            raise GrpcException("No response")

    def process_pix_list(self, response):
        """
         Extract DCMPix associated with the ViewerController from the response

         Args:
             response: response returned by Osirix service for the request made
         """
        if (response.status.status == 1):
            dcm_pix_tuple = ()

            for pix in response.pix:
                # dcm_pix_tuple = dcm_pix_tuple + (pix.osirixrpc_uid,)
                dcm_pix_tuple = dcm_pix_tuple + (pix,)

            return dcm_pix_tuple
        else:
            raise GrpcException("No response")

    #DCMPix

    def process_is_rgb(self, response) -> bool:
        """
         Extract whether the DCMPix is rgb or not from the response

         Args:
             response: response returned by Osirix service for the request made
         Returns:
             bool : is_rgb

        """
        if (response.status.status == 1):

            return response.is_rgb
        else:
            raise GrpcException("No response")

    def process_pix_convert_to_rgb_bw(self, response) -> None:
        """
          Process the response from conversion the DCMPix to rgb or bw

          Args:
              response: response returned by Osirix service for the request made
          Returns:
              None

         """
        if (response.status.status == 1):

            pass
        elif (response.status.status == 0):
            # 0 response code is the current overall failure code so there could be many reasons for failures.
            # In this case, if the image is already rgb/bw, it would be 0
            print("Image is already RGB or BW")
        else:
            raise GrpcException("No response")

    def process_pix_shape(self, response) -> Tuple[int, int]:
        """
         Extract shape of DCMPix from the response

         Args:
             response: response returned by Osirix service for the request made
         Returns:
             Tuple containing shape information (rows and columns)
        """
        if (response.status.status == 1):

            return (response.rows, response.columns)
        else:
            raise GrpcException("No response")

    def process_pix_spacing(self, response) -> Tuple[float, float]:
        """
         Extract spacing of DCMPix from the response

         Args:
             response: response returned by Osirix service for the request made
         Returns:
             Tuple containing spacing information (rows and columns)
        """
        if (response.status.status == 1):

            return (response.spacing_rows, response.spacing_columns)
        else:
            raise GrpcException("No response")

    def process_pix_origin(self, response) -> Tuple[float, float, float]:
        """
         Extract origin of DCMPix from the response

         Args:
             response: response returned by Osirix service for the request made

         Returns:
             Tuple containing origin information (rows, columns, values) in float
        """
        if (response.status.status == 1):

            return (response.origin_rows, response.origin_columns, response.origin_slices)
        else:
            raise GrpcException("No response")

    def process_pix_orientation(self, response) -> Tuple[float, ...]:
        """
         Extract orientation of DCMPix from the response

         Args:
             response: response returned by Osirix service for the request made
         Returns:
             Tuple containing orientations of DCMPix in float
        """
        if (response.status.status == 1):
            tuple : Tuple[float, ...] = ()
            for orientation in response.orientation:
                tuple = tuple + (orientation,)

            return tuple
        else:
            raise GrpcException("No response")

    def process_pix_slice_location(self, response) -> float:
        """
        Extract slice location of DCMPix from the response

        Args:
            response: response returned by Osirix service for the request made
        Returns:
             float : slice location
        """
        if (response.status.status == 1):

            return response.slice_location
        else:
            raise GrpcException("No response")

    def process_pix_source_file(self, response) -> str:
        """
         Extract source file of the DCMPix from the response

         Args:
             response: response returned by Osirix service for the request made
         Returns:
             str : source file
        """
        if (response.status.status == 1):

            return response.source_file
        else:
            raise GrpcException("No response")

    def process_pix_image(self, response) -> ndarray:
        """
         Extract underlying image data of the DCMPix from the response

         Args:
             response: response returned by Osirix service for the request made

         Returns:
             ndarray : image data
         """
        if (response.status.status == 1):

            if response.is_argb:
                image_array = np.array(response.image_data_argb).reshape(response.rows, response.columns, 4)
                return image_array
            else:
                image_array = np.array(response.image_data_float).reshape(response.rows, response.columns)
                return image_array

        else:
            raise GrpcException("No response")

    def process_pix_compute_roi(self, response) -> Dict[str, float]:
        """
         Compute the ROI information of the DCMPix from the response

         Args:
             response: response returned by Osirix service for the request made

         Returns:
             Dict containing the ROI statistics such as mean

         """
        if (response.status.status == 1):
            roi_dict = {
                'mean': response.mean,
                'total': response.total,
                'std_dev': response.std_dev,
                'min': response.min,
                'max': response.max,
                'skewness': response.skewness,
                'kurtosis': response.kurtosis
            }
            return roi_dict
        else:
            raise GrpcException("No response")

    def process_pix_roi_map(self, response) -> ndarray:
        """
         Extract ROI map of DCMPix from the response

         Args:
            response: response returned by Osirix service for the request made

         Returns:
            ndarray : roi map
        """
        if (response.status.status == 1):
            roi_map_array = np.array(response.map).reshape(response.rows, response.columns)
            return roi_map_array
        else:
            raise GrpcException("No response")

    def process_pix_roi_values(self, response) -> Tuple[ndarray, ndarray, ndarray]:
        """
         Extract the ROI values of the DCMPix from the response

         Args:
            response: response returned by Osirix service for the request made

         Returns:
            Tuple containing ndarray for rows, columns and values of ROI
        """
        if (response.status.status == 1):
            rows = np.array(response.row_indices)
            columns = np.array(response.column_indices)
            values = np.array(response.values)
            return (rows, columns, values)
        else:
            raise GrpcException("No response")

    # ROI
    # def process_roi_name(self, response) -> str:
    #     if (response.status.status == 1):
    #
    #         return response.name
    #     else:
    #         raise GrpcException("No response")

    def process_roi_color(self, response) -> Tuple[int, int, int]:
        """
         Extract color of ROI from the response

         Args:
            response: response returned by Osirix service for the request made

         Returns:
            Tuple containing red, green, blue values in int

        """
        if (response.status.status == 1):

            return (response.r, response.g, response.b)
        else:
            raise GrpcException("No response")

    def process_roi_opacity(self, response) -> float:
        """
         Extract opacity of ROI from the response

         Args:
            response: response returned by Osirix service for the request made

         Returns:
            float : opacity
        """
        if (response.status.status == 1):

            return response.opacity
        else:
            raise GrpcException("No response")

    def process_roi_thickness(self, response) -> float:
        """
         Extract thickness of ROI from the response

         Args:
            response: response returned by Osirix service for the request made

         Returns:
            float : thickness
        """
        if (response.status.status == 1):

            return response.thickness
        else:
            raise GrpcException("No response")

    def process_roi_pix(self, response) -> str:
        """
         Extract DCMPix associated with the ROI from the response

         Args:
            response: response returned by Osirix service for the request made

         Returns:
             str : pix osirixrpc_id
        """
        if (response.status.status == 1):

            return response.pix
        else:
            raise GrpcException("No response")

    def process_roi_points(self, response) -> ndarray:
        """
         Extract points of the ROI from the response

         Args:
            response: response returned by Osirix service for the request made

         Returns:
             ndarray : roi points
        """
        if (response.status.status == 1):

            points = []
            for i in range(len(response.points)):
                points.append([response.points[i].x, response.points[i].y])
            points = np.array(points)

            return points
        else:
            raise GrpcException("No response")

    def process_roi_type(self, response) -> str:
        """
         Extract the type of the ROI from the response

         Args:
            response: response returned by Osirix service for the request made

         Returns:
             str : type of roi
        """
        if (response.status.status == 1):

            return response.type
        else:
            raise GrpcException("No response")

    #ViewerController

    #BrowserController

    # def process_browser_database_selection(self, response):
    #     """
    #      Extract all the study/series that are present in the Osirix browser from the response
    #
    #      Args:
    #          response: response returned by Osirix service for the request made
    #      """
    #     if (response.status.status == 1):
    #
    #         series_tuple : Tuple[DicomSeries, ...] = ()
    #         study_tuple : Tuple[DicomStudy, ...] = ()
    #
    #         for series in response.series:
    #             series_tuple = series_tuple + (series,)
    #
    #         for study in response.studies:
    #             study_tuple = study_tuple + (study,)
    #
    #         return (study_tuple, series_tuple)
    #     else:
    #         raise GrpcException("No response")














