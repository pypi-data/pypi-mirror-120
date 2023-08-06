#!/usr/bin/env python3

# foopylint: disable=no-value-for-parameter

from typing import List, Tuple, Dict, Any

from unittest import mock, TestCase

import radical.utils as ru


# --------------------------------------------------------------------------
#
class TestServer(ru.zmq.Server):

    def __init__(self):

        ru.zmq.Server.__init__(self)

        self.register_request('test_0', self._test_0)
        self.register_request('test_1', self._test_1)
        self.register_request('test_2', self._test_2)
        self.register_request('test_3', self._test_3)
        self.register_request('test_4', self._test_4)


    def _test_0(self) -> str:
        return 'default'


    def _test_1(self, foo: Any = None) -> Any:
        return foo


    def _test_2(self, foo: Any,
                      bar: Any) -> List[Any]:
        return [foo, bar]


    def _test_3(self, foo: Any,
                      bar: Any = 'default') -> Dict[str, Any]:
        return {'foo': foo,
                'bar': bar}


    def _test_4(self, *args, **kwargs) -> List[Any]:
        return list(args) + list(kwargs.values())


# ------------------------------------------------------------------------------
#
class TestZMQServer(TestCase):

    # --------------------------------------------------------------------------
    #
    @mock.patch('radical.utils.zmq.server.Logger')
    @mock.patch('radical.utils.zmq.server.Profiler')
    def test_server(self, mocked_profiler, mocked_logger):

        s = TestServer()

        try:
            s.start()
            self.assertIsNotNone(s.addr)

            c = ru.zmq.Client(url=s.addr)
            self.assertEqual(c.url, s.addr)

            with self.assertRaisesRegex(RuntimeError, 'no command'):
                c.request('')

            with self.assertRaisesRegex(RuntimeError, 'command .* unknown'):
                c.request('no_registered_cmd')

            with self.assertRaisesRegex(RuntimeError,
                    '.* _test_0.* takes 1 positional argument'):
                c.request('test_0', None)

            ret = c.request('test_0')
            self.assertIsInstance(ret, str)
            self.assertEqual(ret, 'default')

            ret = c.request('test_1', 'foo')
            self.assertIsInstance(ret, str)
            self.assertEqual(ret, 'foo')

            ret = c.request('test_1', ['foo', 'bar'])
            self.assertIsInstance(ret, list)
            self.assertEqual(ret, ['foo', 'bar'])

            ret = c.request('test_1')
            self.assertEqual(ret, None)

            ret = c.request('test_2', 'foo', 'bar')
            self.assertIsInstance(ret, list)
            self.assertEqual(ret, ['foo', 'bar'])

            ret = c.request('test_3', 'foo')
            self.assertIsInstance(ret, dict)
            self.assertEqual(ret, {'foo': 'foo', 'bar': 'default'})

            ret = c.request('test_3', foo='foo', bar='bar')
            self.assertIsInstance(ret, dict)
            self.assertEqual(ret, {'foo': 'foo', 'bar': 'bar'})

            ret = c.request('test_3', 'foo', bar='bar')
            self.assertIsInstance(ret, dict)
            self.assertEqual(ret, {'foo': 'foo', 'bar': 'bar'})

            ret = c.request('test_3', 'foo', 'bar')
            self.assertIsInstance(ret, dict)
            self.assertEqual(ret, {'foo': 'foo', 'bar': 'bar'})

            ret = c.request('test_4', 'foo', 'bar')
            self.assertIsInstance(ret, list)
            self.assertEqual(ret, ['foo', 'bar'])

            ret = c.request('test_4', 'foo', ['bar'])
            self.assertIsInstance(ret, list)
            self.assertEqual(ret, ['foo', ['bar']])

            c.close()

        finally:
            s.stop()
            s.wait()


# ------------------------------------------------------------------------------
#
if __name__ == '__main__':

    tc = TestZMQServer()
    tc.test_server()


# ------------------------------------------------------------------------------


