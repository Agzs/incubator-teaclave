// Licensed to the Apache Software Foundation (ASF) under one
// or more contributor license agreements.  See the NOTICE file
// distributed with this work for additional information
// regarding copyright ownership.  The ASF licenses this file
// to you under the Apache License, Version 2.0 (the
// "License"); you may not use this file except in compliance
// with the License.  You may obtain a copy of the License at
//
//   http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing,
// software distributed under the License is distributed on an
// "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
// KIND, either express or implied.  See the License for the
// specific language governing permissions and limitations
// under the License.

#[cfg(feature = "mesalock_sgx")]
use std::prelude::v1::*;

use std::convert::TryFrom;
use teaclave_types::{FunctionArguments, FunctionRuntime};

#[derive(Default)]
pub struct Printf;

#[derive(serde::Deserialize)]
struct PrintfArguments {
    message: String,
}

impl TryFrom<FunctionArguments> for PrintfArguments {
    type Error = anyhow::Error;

    fn try_from(arguments: FunctionArguments) -> Result<Self, Self::Error> {
        use anyhow::Context;
        serde_json::from_str(&arguments.into_string()).context("Cannot deserialize arguments")
    }
}

impl Printf {
    pub const NAME: &'static str = "builtin-printf";

    pub fn new() -> Self {
        Default::default()
    }

    pub fn run(
        &self,
        arguments: FunctionArguments,
        _runtime: FunctionRuntime,
    ) -> anyhow::Result<String> {
        let message = PrintfArguments::try_from(arguments)?.message;
        Ok(message)
    }
}

#[cfg(feature = "enclave_unit_test")]
pub mod tests {
    use super::*;
    use serde_json::json;
    use teaclave_runtime::*;
    use teaclave_test_utils::*;
    use teaclave_types::*;

    pub fn run_tests() -> bool {
        run_tests!(test_printf)
    }

    fn test_printf() {
        let args = FunctionArguments::from_json(json!({
            "message": "Hello Teaclave!"
        }))
        .unwrap();

        let input_files = StagedFiles::default();
        let output_files = StagedFiles::default();

        let runtime = Box::new(RawIoRuntime::new(input_files, output_files));
        let function = Printf;

        let summary = function.run(args, runtime).unwrap();
        assert_eq!(summary, "Hello Teaclave!");
    }
}