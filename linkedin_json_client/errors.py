class LinkedInApiJsonClientError(ValueError):
    def __init__(self, error_json, *args, **kwargs):
        """
        JSON Errors look like
        {
          "errorCode": 0,
          "message": "Access to posting messages denied.",
          "requestId": "KPA3JXNBAJ",
          "status": 403,
          "timestamp": 1346269248747
        }
        """
        msg = 'LinkedIn request failed at %(timestamp)s with status '\
              '%(status)s. The error code was %(errorCode)s and message is '\
              '"%(message)s".'
        super(LinkedInApiJsonClientError, self).__init__(msg % error_json)