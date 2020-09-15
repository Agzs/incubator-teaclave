#!/usr/bin/env python3

# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

import sys

from teaclave import (AuthenticationService, FrontendService,
                      AuthenticationClient, FrontendClient)
from utils import (AUTHENTICATION_SERVICE_ADDRESS, FRONTEND_SERVICE_ADDRESS,
                   AS_ROOT_CA_CERT_PATH, ENCLAVE_INFO_PATH, USER_ID,
                   USER_PASSWORD)


class BuiltinPrintfExample:
    def __init__(self, user_id, user_password):
        self.user_id = user_id
        self.user_password = user_password

    def printf(self, message="Hello, Teaclave!"):
        print("AUTHENTICATION_SERVICE_ADDRESS = ", AUTHENTICATION_SERVICE_ADDRESS)
        print("AS_ROOT_CA_CERT_PATH = ", AS_ROOT_CA_CERT_PATH)
        print("ENCLAVE_INFO_PATH = ", ENCLAVE_INFO_PATH)
        client = AuthenticationService(
            AUTHENTICATION_SERVICE_ADDRESS, AS_ROOT_CA_CERT_PATH,
            ENCLAVE_INFO_PATH).connect().get_client()

        print("[+] registering user")
        client.user_register(self.user_id, self.user_password)

        print("[+] login")
        token = client.user_login(self.user_id, self.user_password)

        client = FrontendService(FRONTEND_SERVICE_ADDRESS,
                                 AS_ROOT_CA_CERT_PATH,
                                 ENCLAVE_INFO_PATH).connect().get_client()
        metadata = {"id": self.user_id, "token": token}
        client.metadata = metadata

        print("[+] registering function")
        function_id = client.register_function(
            name="builtin-printf",
            description="Native Printf Function",
            executor_type="builtin",
            arguments=["message"])

        print("[+] creating task")
        task_id = client.create_task(function_id=function_id,
                                     function_arguments={"message": message},
                                     executor="builtin")
        print("function_id = ", function_id)
        print("message = ", message)
        print("task_id = ", task_id)

        print("[+] invoking task")
        print("task_id = ", task_id)
        client.invoke_task(task_id)

        print("[+] getting result")
        print("task_id = ", task_id)
        result = client.get_task_result(task_id)
        print("[+] done")

        return bytes(result)


def main():
    print("user_id = ", USER_ID)
    print("user_password = ", USER_PASSWORD)
    example = BuiltinPrintfExample(USER_ID, USER_PASSWORD)
    if len(sys.argv) > 1:
        message = sys.argv[1]
        rt = example.printf(message)
    else:
        rt = example.printf()

    print("[+] function return: ", rt)


if __name__ == '__main__':
    main()
