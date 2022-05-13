import sys

import osirixgrpc.browsercontroller_pb2 as browsercontroller_pb2
from osirix.exceptions import GrpcException
from typing import Tuple, List
from osirix.dicom import DicomSeries, DicomStudy
from osirix.response_processor import ResponseProcessor


class BrowserController(object):
    """
    A class representing the main database window within OsiriX.
    This can be best accessed using osirix.current_browser()
    """
    def __init__(self, osirixrpc_uid, osirix_service) -> None:
        self.osirix_service = osirix_service
        self.osirixrpc_uid = osirixrpc_uid
        self.response_processor = ResponseProcessor()

    def copy_files_into_database(self, files: List[str]) -> None:
        """
        Copy files into the database of Osirix

        Args:
            files: list of files to copy into database

        Returns:
            None

        """
        request = browsercontroller_pb2.BrowserControllerCopyFilesIfNeededRequest(browser=self.osirixrpc_uid, paths=files)
        response = self.osirix_service.BrowserControllerCopyFilesIfNeeded(request)
        self.response_processor.process_basic_response(response)

    def database_selection(self) -> Tuple[Tuple[DicomStudy, ...], Tuple[DicomSeries, ...]]:
        """
        Queries the OsiriX database for the selected studies and series

        Returns:
            A Tuple containing two Tuples. The first Tuple contains all the Dicom studies and the second
            Tuple contains all the Dicom series in the database.
        """
        response = self.osirix_service.BrowserControllerDatabaseSelection(self.osirixrpc_uid)

        if response.status.status == 1:

            series_tuple = ()
            for series in response.series:
                series_obj = DicomSeries(series, self.osirix_service)
                series_tuple = series_tuple + (series_obj,)

            study_tuple = ()
            for study in response.studies:
                study_obj = DicomStudy(study, self.osirix_service)
                study_tuple = study_tuple + (study_obj,)

            return study_tuple, series_tuple
        else:
            raise GrpcException("No response")
