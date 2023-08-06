from . import crawler_data_processor_pb2_grpc as importStub

class DataProcessorService(object):

    def __init__(self, router):
        self.connector = router.get_connection(DataProcessorService, importStub.DataProcessorStub)

    def crawlerConnect(self, request, timeout=None):
        return self.connector.create_request('crawlerConnect', request, timeout)

    def sendEvent(self, request, timeout=None):
        return self.connector.create_request('sendEvent', request, timeout)

    def sendMessage(self, request, timeout=None):
        return self.connector.create_request('sendMessage', request, timeout)