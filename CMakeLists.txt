# cmake_minimum_required(VERSION <specify CMake version here>)
project(LiveCodeBenchPro)

set(CMAKE_CXX_STANDARD 14)

include_directories(.)
include_directories(.idea)
include_directories(bert-base-uncased-mrpc)

add_executable(LiveCodeBenchPro
        .idea/copyright/Influence_IPM_LLC.xml
        .idea/inspectionProfiles/Project_Default.xml
        .idea/.gitignore
        .idea/encodings.xml
        .idea/LiveCodeBenchPro.iml
        .idea/misc.xml
        .idea/modules.xml
        .idea/workspace.xml
        bert-base-uncased-mrpc/bert-base-uncased-mrpc/huggingface_Intel_bert-base-uncased-mrpc_v1/.gitignore
        bert-base-uncased-mrpc/bert-base-uncased-mrpc/huggingface_Intel_bert-base-uncased-mrpc_v1/bert_ov.json
        bert-base-uncased-mrpc/bert-base-uncased-mrpc/huggingface_Intel_bert-base-uncased-mrpc_v1/bert_qdq_amd.json
        bert-base-uncased-mrpc/bert-base-uncased-mrpc/huggingface_Intel_bert-base-uncased-mrpc_v1/bert_qdq_qnn.json
        bert-base-uncased-mrpc/bert-base-uncased-mrpc/huggingface_Intel_bert-base-uncased-mrpc_v1/inference_sample.ipynb
        bert-base-uncased-mrpc/bert-base-uncased-mrpc/huggingface_Intel_bert-base-uncased-mrpc_v1/model_project.config
        bert-base-uncased-mrpc/bert-base-uncased-mrpc/huggingface_Intel_bert-base-uncased-mrpc_v1/README.md
        bert-base-uncased-mrpc/bert-base-uncased-mrpc/huggingface_Intel_bert-base-uncased-mrpc_v1/requirements.txt
        bert-base-uncased-mrpc/bert-base-uncased-mrpc/huggingface_Intel_bert-base-uncased-mrpc_v1/user_script.py
        bert-base-uncased-mrpc/bert-base-uncased-mrpc/model_lab.workspace.config
        "LiveCodeBench Pro Paper.pdf")
