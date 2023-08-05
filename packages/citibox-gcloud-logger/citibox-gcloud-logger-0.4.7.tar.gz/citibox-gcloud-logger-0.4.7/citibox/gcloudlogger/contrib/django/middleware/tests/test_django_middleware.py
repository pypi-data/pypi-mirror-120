from unittest import mock
import json

from citibox.gcloudlogger.contrib.django import DjangoMiddleware
from citibox.gcloudlogger.contrib.django.django_record_factory import DjangoRecordFactory
from citibox.gcloudlogger.src.gcloud_formatter import GCloudFormatter
from citibox.gcloudlogger.test_helpers.logger_test_case import LoggerTestCase


class EmptyResource:
    pass


class FakeResponse:
    content = json.dumps({"some_key": "some_value"})
    data = '{"some_key": "some_value"}'
    status_code = "200 Ok"

    def items(self):
        """
        Mocks django.http.response.HttpResponse.items method
        :return: dict
        """
        return {
            'header_1': 'h1',
            'header_2': 'h2'
        }


@mock.patch('citibox.gcloudlogger.contrib.django.django_record_factory.HttpRequest')
class TestDjangoMiddleware(LoggerTestCase):
    logger = None
    _formatter = GCloudFormatter
    logger_name = __name__

    def test_process_request_get_http(self, request_mock):
        request_mock.get_host.return_value = "fake_host.com"
        request_mock.path = "/fake/path"
        request_mock.method = "GET"
        request_mock.META = {
            "HTTP_HEADER_1": "header_1",
            "USER_AGENT": "cosicas_raras"
        }
        request_mock.GET.lists.return_value = [
            ("param", "value")
        ]

        django_middleware = self._create_django_middleware(request_mock=request_mock)
        result = django_middleware(request_mock)
        last_log = json.loads(self.memory_logger.last_record)

        self.assertIsInstance(result, FakeResponse)
        self.assertEquals(f'{request_mock.method} 200 Ok {request_mock.path}', last_log.get('message'))
        self.assertIn("headers", last_log.get('request'))
        self.assertIn("host", last_log)
        self.assertIn("path", last_log)
        self.assertEquals("value", last_log.get('request').get("params").get("param"))
        self.assertEquals("header_1", last_log.get('request').get("headers").get("HEADER_1"))
        self.assertEquals(json.loads(FakeResponse.content), last_log.get("response").get("body"))

    def test_process_request_post_http(self, request_mock):
        request_mock.get_host.return_value = "fake_host.com"
        request_mock.path = "/fake/path"
        request_mock.method = "POST"
        request_mock.META = {
            "HTTP_HEADER_1": "header_1"
        }
        request_mock.POST = {
            "param": "value"
        }

        django_middleware = self._create_django_middleware(request_mock=request_mock)
        result = django_middleware(request_mock)
        last_log = json.loads(self.memory_logger.last_record)

        self.assertIsInstance(result, FakeResponse)
        self.assertEquals(f'{request_mock.method} 200 Ok {request_mock.path}', last_log.get('message'))
        self.assertIn("headers", last_log.get('request'))
        self.assertIn("host", last_log)
        self.assertIn("path", last_log)
        self.assertEquals("value", last_log.get('request').get("body").get("param"))
        self.assertEquals("header_1", last_log.get('request').get("headers").get("HEADER_1"))
        self.assertEquals(json.loads(FakeResponse.content), last_log.get("response").get("body"))

    def test_process_request_post_pubsub_http(self, request_mock):
        request_mock.get_host.return_value = "fake_host.com"
        request_mock.path = "/fake/path"
        request_mock.method = "POST"
        request_mock.META = {
            "HTTP_HEADER_1": "header_1",
            "HTTP_USER_AGENT": DjangoRecordFactory.PUBSUB_USER_AGENT
        }
        request_mock.POST = {
            "message": {
                "attributes": {"attr_1": "AA"}
            }
        }

        django_middleware = self._create_django_middleware(request_mock=request_mock)
        result = django_middleware(request_mock)
        last_log = json.loads(self.memory_logger.last_record)

        self.assertIsInstance(result, FakeResponse)
        self.assertEquals(f'{request_mock.method} 200 Ok {request_mock.path}', last_log.get('message'))
        self.assertIn("headers", last_log.get('request'))
        self.assertIn("host", last_log)
        self.assertIn("path", last_log)
        self.assertEquals("AA", last_log.get("attr_1"))
        self.assertEquals("header_1", last_log.get('request').get("headers").get("HEADER_1"))
        self.assertEquals(json.loads(FakeResponse.content), last_log.get("response").get("body"))

    def test_process_request_post_pubsub_http_without_attributes(self, request_mock):
        request_mock.get_host.return_value = "fake_host.com"
        request_mock.path = "/fake/path"
        request_mock.method = "POST"
        request_mock.META = {
            "HTTP_HEADER_1": "header_1",
            "HTTP_USER_AGENT": DjangoRecordFactory.PUBSUB_USER_AGENT
        }
        request_mock.POST = {
            "message": {
                "attributes": {}
            }
        }

        django_middleware = self._create_django_middleware(request_mock=request_mock)
        result = django_middleware(request_mock)
        last_log = json.loads(self.memory_logger.last_record)

        self.assertIsInstance(result, FakeResponse)
        self.assertEquals(f'{request_mock.method} 200 Ok {request_mock.path}', last_log.get('message'))
        self.assertIn("headers", last_log.get('request'))
        self.assertIn("host", last_log)
        self.assertIn("path", last_log)
        self.assertEquals("header_1", last_log.get('request').get("headers").get("HEADER_1"))
        self.assertNotIn("attr_1", last_log)
        self.assertEquals(json.loads(FakeResponse.content), last_log.get("response").get("body"))

    def test_process_exception_logs_exception_and_trace(self, request_mock):
        exception = Exception()
        exception.args = ('Something went wrong', )

        def process_exception_wrapper(request):
            django_middleware.process_exception(request, exception)
            return FakeResponse()

        django_middleware = self._create_django_middleware(request_mock=request_mock)
        django_middleware._get_response = mock.Mock(side_effect=process_exception_wrapper)

        django_middleware(request_mock)
        last_log = json.loads(self.memory_logger.last_record)
        self.assertIn('exception', last_log)
        self.assertIn('name', last_log['exception'])
        self.assertIn('args', last_log['exception'])
        self.assertIn('traceback', last_log['exception'])
        self.assertEquals(last_log['exception']['name'], 'Exception')
        self.assertEquals(last_log['exception']['args'], ['Something went wrong', ])

    def test_django_middleware_fails_building(self, request_mock):
        with mock.patch(
                'citibox.gcloudlogger.contrib.django.middleware.django_middleware.DjangoRecordFactory',
                autospec=True
        ) as django_record_factory_mock:
            error = AttributeError("'NoneType' object has no attribute 'height'")
            django_record_factory_mock.return_value.build.side_effect = error

            django_middleware = self._create_django_middleware(request_mock=request_mock)

            django_middleware(request_mock)
            last_log = json.loads(self.memory_logger.last_record)
            self.assertIn('logger_exception', last_log)
            self.assertIn('name', last_log['logger_exception'])
            self.assertIn('args', last_log['logger_exception'])
            self.assertIn('traceback', last_log['logger_exception'])
            self.assertEquals(last_log['logger_exception']['name'], 'AttributeError')
            self.assertEquals(last_log['logger_exception']['args'], ["'NoneType' object has no attribute 'height'", ])

    def _create_django_middleware(self, request_mock=None, view_kwargs={}):
        django_middleware = DjangoMiddleware(lambda x: FakeResponse())
        django_middleware.view_kwargs = view_kwargs
        django_middleware.request = request_mock
        return django_middleware
