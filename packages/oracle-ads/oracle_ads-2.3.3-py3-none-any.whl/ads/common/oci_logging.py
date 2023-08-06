import datetime
import logging
import time
from typing import Union

import oci
from ads.common.oci_mixin import OCIModelMixin, OCIWorkRequestMixin
from ads.common.oci_resource import OCIResource

logger = logging.getLogger(__name__)


class OCILoggingModelMixin(OCIModelMixin, OCIWorkRequestMixin):
    """Base model for representing OCI logging resources managed through oci.logging.LoggingManagementClient.
    This class should not be initialized directly. Use a sub-class (OCILogGroup or OCILog) instead.
    """

    @classmethod
    def from_name(cls, display_name: str) -> Union["OCILogGroup", "OCILog"]:
        """Obtain an existing OCI logging resource by using its display name.
        OCI log group or log resource requires display name to be unique.

        Parameters
        ----------
        display_name : str
            Display name of the logging resource (e.g. log group)

        Returns
        -------
        An instance of logging resource, e.g. OCILogGroup, or OCILog.

        """
        items = cls.list_resource()
        for item in items:
            if item.display_name == display_name:
                return item
        return None

    @classmethod
    def init_client(cls, **kwargs) -> oci.logging.LoggingManagementClient:
        """Initialize OCI client
        """
        return cls._init_client(client=oci.logging.LoggingManagementClient, **kwargs)

    @property
    def client(self) -> oci.logging.LoggingManagementClient:
        """ """
        return super().client

    def create_async(self):
        """Creates the OCI logging resource asynchronously.
        Sub-class should implement this method with OCI Python SDK and return the response from the OCI PythonSDK.

        """
        raise NotImplementedError()

    def create(self):
        """Creates a new resource with OCI service synchronously.
        This method will wait for the resource creation to be succeeded or failed.

        Each sub-class should implement the create_async() method with the corresponding method in OCI SDK
            to create the resource.

        Raises
        ------
        NotImplementedError
            when user called create but the create_async() method is not implemented.

        oci.exceptions.RequestException
            when there is an error creating the resource with OCI request.

        """
        wait_for_states = ("SUCCEEDED", "FAILED")
        success_state = "SUCCEEDED"

        res = self.create_async()
        # Wait for the work request to be completed.
        if "opc-work-request-id" in res.headers:
            opc_work_request_id = res.headers.get("opc-work-request-id")
            res_work_request = self.wait_for_work_request(
                opc_work_request_id,
                wait_for_state=wait_for_states,
                wait_interval_seconds=1,
            )
            # Raise an error if the failed to create the resource.
            if res_work_request.data.status != success_state:
                raise oci.exceptions.RequestException(f"Failed to create {self.__class__.__name__}.\n" + str(res.data))
            self.id = res_work_request.data.resources[0].identifier
            logger.debug("Created %s: %s", self.__class__.__name__, self.id)

        else:
            # This will likely never happen as OCI SDK will raise an error if the HTTP request is not successful.
            raise oci.exceptions.RequestException(
                f"opc-work-request-id not found in response headers: {res.headers}"
            )
        self.sync()
        return self

    def sync(self):
        """ """
        raise NotImplementedError()


class OCILogGroup(OCILoggingModelMixin, oci.logging.models.LogGroup):
    """Represents the OCI Log Group resource.

    Using ``OCILogGroup`` to create a new log group.
    OCI requires display_name to be unique and it cannot contain space.
    >>> log_group = OCILogGroup(display_name="My_Log_Group").create()
    Once created, access the OCID and other properties
    >>> log_group.id # The OCID is None before the log is created.
    >>> None
    Create a log resource within the log group
    >>> log_group.id # OCID will be available once the log group is created
    Access the property
    >>> log_group.display_name
    Create logs within the log group
    >>> log = log_group.create_log("My custom access log")
    >>> log_group.create_log("My custom prediction log")
    List the logs in a log group. The following line will return a list of OCILog objects.
    >>> logs = log_group.list_logs()
    Delete the resource
    >>> log_group.delete()
    """

    def create_async(self):
        """Creates a new LogGroup asynchronously with OCI logging service"""
        return self.client.create_log_group(self.to_oci_model(oci.logging.models.CreateLogGroupDetails))

    def sync(self):
        """ """
        self.update_from_oci_model(self.client.get_log_group(self.id).data)

    def create_log(self, display_name: str, **kwargs):
        """Create a log (OCI resource) within the log group.

        Parameters
        ----------
        display_name : str
            The display name of the log
        **kwargs :


        Returns
        -------
        OCILog
            An instance of OCILog

        """
        return OCILog(
            display_name=display_name,
            log_group_id=self.id,
            compartment_id=self.compartment_id,
            **kwargs
        ).create()

    def list_logs(self, **kwargs) -> list:
        """Lists all logs within the log group.

        Parameters
        ----------
        **kwargs :
            keyword arguments for filtering the results.
            They are passed into oci.logging.LoggingManagementClient.list_logs()

        Returns
        -------
        list
            A list of OCILog

        """
        items = oci.pagination.list_call_get_all_results(self.client.list_logs, self.id, **kwargs).data
        return [OCILog.from_oci_model(item) for item in items]

    def delete(self):
        """Deletes the log group and the logs in the log group."""
        logs = self.list_logs()
        for log in logs:
            logger.debug("Deleting OCI Log: %s", log.id)
            log.delete()
        logger.debug("Deleting OCI log group: %s", self.id)
        self.client.delete_log_group(self.id)
        return self


class OCILog(OCILoggingModelMixin, oci.logging.models.Log):
    """Represents the OCI Log resource.
    
    Usage: (OCI requires display_name to be unique and it cannot contain space)
    >>> log = OCILog.create(display_name="My_Log", log_group_id=LOG_GROUP_ID)
    Usually it is better to create a log using the create_log() method in OCILogGroup.
    >>> log.delete() # Delete the resource
    Get a log object from OCID
    >>> oci_log = OCILog.from_ocid("ocid1.log.oc1.iad.amaaaaaav66vvnia3h4o6otedz4lz23zex6z2pei6yjqszb7zdfswaa5srca")
    Stream the logs from an OCI Data Science Job run to stdout
    >>> oci_log.stream(source="ocid1.datasciencejobrun.oc1.iad.aaaaaaaah36pjirpd7n3ym3wu3nimhb6b4ljznsahlkzqidhy2bxermrjk2a")
    Gets the most recent 10 logs
    >>> oci_log.tail(10)
    """
    def __init__(self, log_type : str = "CUSTOM", **kwargs) -> None:
        """Initializes an OCI log model locally.
        The resource is not created in OCI until the create() or create_async() method is called.
        """
        if "logType" not in kwargs:
            kwargs["log_type"] = log_type
        super().__init__(**kwargs)
        self._search_client = None

    @classmethod
    def _get(cls, ocid):
        """
        """
        compartment_id = OCIResource.get_compartment_id(ocid)
        log_groups = OCILogGroup.list_resource(compartment_id=compartment_id)
        for log_group in log_groups:
            oci_logs = log_group.list_logs()
            for oci_log in oci_logs:
                if oci_log.id == ocid:
                    return oci_log
        return None

    def create_async(self):
        """Creates a new Log with OCI logging service"""
        return self.client.create_log(self.log_group_id, self.to_oci_model(oci.logging.models.CreateLogDetails))

    def sync(self):
        """ """
        self.update_from_oci_model(self.client.get_log(self.log_group_id, self.id).data)

    def delete(self):
        """Delete the log"""
        self.client.delete_log(self.log_group_id, self.id)
        return self

    @property
    def search_client(self):
        """ """
        if not self._search_client:
            self._search_client = self._init_client(client=oci.loggingsearch.LogSearchClient)
        return self._search_client

    @staticmethod
    def format_datetime(dt: datetime.datetime) -> str:
        """Converts datetime object to RFC3339 date time format in string

        Parameters
        ----------
        dt: datetime.datetime :
            

        Returns
        -------

        """
        return dt.isoformat()[:-3] + "Z"
    
    def search(self, source, time_start=None, time_end=None, limit=100, sort_by="'time'", sort_order="ASC"):
        """

        Parameters
        ----------
        source :
            
        time_start :
             (Default value = None)
        time_end :
             (Default value = None)
        limit :
             (Default value = 100)
        sort_by :
             (Default value = "'time'")
        sort_order :
             (Default value = "ASC")

        Returns
        -------

        """
        # Default time_start and time_end
        if time_start is None:
            time_start = datetime.datetime.utcnow() - datetime.timedelta(days=14)
        if time_end is None:
            time_end = datetime.datetime.utcnow()

        # Converts datetime objects to RFC3339 format
        if isinstance(time_start, datetime.datetime):
            time_start = self.format_datetime(time_start)
        if isinstance(time_end, datetime.datetime):
            time_end = self.format_datetime(time_end)

        search_details = oci.loggingsearch.models.SearchLogsDetails(
            # time_start cannot be more than 14 days older
            time_start=time_start,
            time_end=time_end,
            # https://docs.oracle.com/en-us/iaas/Content/Logging/Reference/query_language_specification.htm
            # Double quotes must be used for "<log_stream>" after search
            # Single quotes must be used for the string in <where_expression>
            # source = <OCID> is not allowed but source = *<OCID> works
            search_query=f'SEARCH "{self.compartment_id}/{self.log_group_id}/{self.id}" '
                f'| WHERE source = \'*{source}\' | SORT BY {sort_by} {sort_order}',
            # is_return_field_info=True
        )
        return self.search_client.search_logs(search_details, limit=limit).data.results

    def tail(self, source, limit=100):
        """

        Parameters
        ----------
        source :
            
        limit :
             (Default value = 100)

        Returns
        -------

        """
        logs = self.search(source, limit=limit, sort_order='DESC')
        # print([log.data.get("datetime") for log in logs])
        # print([log.data.get("time") for log in logs])
        logs = [log.data for log in logs]
        logs = sorted(logs, key=lambda x: x.get("datetime"))
        return [{
            "id": log.get("id"),
            "message": log.get("logContent").get("data").get("message")
            } for log in logs]

    def stream(self, source: str, interval: int=3, stop_condition: callable = None, batch_size: int = 100):
        """Streams logs to console/terminal until stop_condition() returns true.

        Parameters
        ----------
        source : str
        interval : int
            The time interval between sending each request to pull logs from OCI logging service (Default value = 3)
        stop_condition : callable
            A function to determine if the streaming should stop. (Default value = None)
            The log streaming will stop if the function returns true.
        batch_size : int
            (Default value = 100)
            The number of logs to be returned by OCI in each request
            This basically limits the number logs streamed for each interval
            This number should be large enough to cover the messages generated during the interval
            However, Setting this to a large number will decrease the performance
            This method calls the the tail

        """
        # Use a set to store the IDs of the printed messages
        printed = set()
        exception_count = 0
        while True:
            try:
                logs = self.tail(source, batch_size)
            except Exception:
                exception_count += 1
                if exception_count > 20:
                    raise
                else:
                    time.sleep(interval)
                    continue
            for log in logs:
                if log.get("id") not in printed:
                    print(log.get("message"))
                    printed.add(log.get("id"))
            if stop_condition and stop_condition():
                return
            time.sleep(interval)
