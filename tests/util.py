# Reference:
# https://github.com/aws/aws-xray-sdk-python/blob/aed8e43fc03e68c0d012a6a6e11a2e859b0bf247/tests/util.py

import threading

from aws_xray_sdk.core.emitters.udp_emitter import UDPEmitter
from aws_xray_sdk.core.recorder import AWSXRayRecorder
from aws_xray_sdk.core.sampling.sampler import DefaultSampler
from aws_xray_sdk.core.utils.compat import PY35


class StubbedEmitter(UDPEmitter):

    def __init__(self, daemon_address='127.0.0.1:2000'):
        super(StubbedEmitter, self).__init__(daemon_address)
        self._local = threading.local()

    def send_entity(self, entity):
        setattr(self._local, 'cache', entity)

    def pop(self):
        if hasattr(self._local, 'cache'):
            entity = self._local.cache
        else:
            entity = None

        self._local.__dict__.clear()
        return entity


class StubbedSampler(DefaultSampler):

    def start(self):
        pass


def get_new_stubbed_recorder():
    """
    Returns a new AWSXRayRecorder object with emitter stubbed
    """
    if not PY35:
        recorder = AWSXRayRecorder()
    else:
        from aws_xray_sdk.core.async_recorder import AsyncAWSXRayRecorder
        recorder = AsyncAWSXRayRecorder()

    recorder.configure(emitter=StubbedEmitter(), sampler=StubbedSampler())
    return recorder
