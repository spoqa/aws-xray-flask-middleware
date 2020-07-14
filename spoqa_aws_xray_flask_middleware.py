try:
    import urllib.parse as urlparse
except ImportError:
    import urlparse

from aws_xray_sdk.core.models import http
from aws_xray_sdk.ext.flask.middleware import XRayMiddleware as OrigMiddleware
from flask import request

__all__ = 'XRayMiddleware',


class XRayMiddleware(OrigMiddleware):
    def _before_request(self):
        super(XRayMiddleware, self)._before_request()

        req = request._get_current_object()

        if self.in_lambda_ctx:
            segment = self._recorder.current_subsegment()
        else:
            segment = self._recorder.current_segment()

        if req.url_rule:
            path = req.url_rule.rule
        else:
            path = req.path
        url = urlparse.urljoin('//{}/'.format(segment.name), path)

        segment.put_http_meta(http.URL, str(url))
        segment.put_annotation(http.URL, str(req.base_url))
