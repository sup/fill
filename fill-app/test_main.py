# Copyright 2015 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import main
import unittest

class MainTest(unittest.TestCase):
    
    def setUp(self):
        self.app = main.app.test_client()

    def test_app_health(self):
        rv = self.app.get('/health')
        assert rv.data == 'OK'

if __name__ == '__main__':
    unittest.main()

