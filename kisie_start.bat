@echo off
SET envName=kisie-create
SET workingDir=.\src\

CALL conda activate %envName%
echo 当前激活的conda环境是：%CONDA_DEFAULT_ENV%

CD /D %workingDir%

REM 启动服务器
SET pythonServerScript=-m llama_cpp.server --host 0.0.0.0 --model ..\model\Meta-Llama-3-8B-GGUF\Meta-Llama-3-8B-Instruct.Q2_K.gguf --n_ctx 2048 --n_gpu_layers 28
start /B python %pythonServerScript%

REM 等待服务器启动
timeout /t 10 /nobreak

REM 启动图形化界面
echo 启动图形化界面
SET pythonUIScript=app.py
start python %pythonUIScript%
