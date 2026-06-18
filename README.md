# OV Package Builder
### Build OpenVINO packages in a Docker container

## Usage
```yaml
services:
  ...
  ov_builder:
    container_name: ov_builder
    image: ghcr.io/droans/ov-builder:latest
    restart: never
    volumes:
      - /path/to/outputs:/output
```

## Environment Variables

| Variable                   | Type | Description                                                              | Default                        | Note |
|----------------------------|------|--------------------------------------------------------------------------|--------------------------------|------|
| UPDATE_OPENVINO            | int  | Update OpenVINO (1: Update, 0: Skip)                                     | 1                              |      |
| OPENVINO_GIT_REMOTE        | str  | Remote repo to use for the OV source                                     | openvinotoolkit/openvino       |      |
| OPENVINO_GIT_BRANCH        | str  | Branch to use for the OV source                                          | master                         | 2    |
| OPENVINO_GIT_PR            | int  | PR to use for the OV source                                              | unset                          | 2    |
| OPENVINO_GIT_PR_USE_MERGED | int  | Whether to merge PR with master or use current head for the OV source    | 1                              |      |
| OPENVINO_BUILD_TYPE        | str  | Build type to use for OpenVINO                                           | ocl                            | 1,3  |
| OPENVINO_BUILD_FILE        | str  | Build script to use for OpenVINO                                         | unset                          | 1,3  |
| UPDATE_GENAI               | int  | Update GenAI (1: Update, 0: Skip)                                        | 1                              |      |
| GENAI_GIT_REMOTE           | str  | Remote repo to use for the GenAI source                                  | openvinotoolkit/openvino.genai |      |
| GENAI_GIT_BRANCH           | str  | Branch to use for the GenAI source                                       | master                         | 2    |
| GENAI_GIT_PR               | int  | PR to use for the GenAI source                                           | unset                          | 2    |
| GENAI_GIT_PR_USE_MERGED    | int  | Whether to merge PR with master or use current head for the GenAI source | 1                              |      |
| UPDATE_TOKENIZERS          | int  | Update Tokenizers (1: Update, 0: Skip)                                   | 1                              |      |
| OUTPUT_DIR                 | str  | Container directory to save wheels                                       | /output                        |      |
| USE_DATED_FOLDERS          | int  | Save wheels to dated subdirectories                                      | 1                              | 4    |
| SAVE_UPDATE_CONFIG         | int  | Save the config used to generate the wheels                              | 1                              |      |
| LOG_LEVEL                  | str  | Logging level to use.                                                    | info                           | 5    |

##### Notes
1. Options: ocl, ocl-debug, ze, ze-debug, sycl, sycl-debug. Some options may not be enabled yet.
2. When `OPENVINO_BUILD_TYPE` and `OPENVINO_BUILD_FILE` are both provided, `OPENVINO_BUILD_FILE` will take priority.
3. When `XXX_GIT_PR` and `XXX_GIT_BRANCH` are both provided, `XXX_GIT_PR` will take priority.
4. Date format used is "`%Y-%m-%d_%H:%M:%S"`
5. Options: debug, info, warn, error, critical, fatal
