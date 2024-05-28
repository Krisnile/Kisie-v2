@echo off
SET envName=kisie-create
SET workingDir=.\src\

CALL conda activate %envName%
echo ��ǰ�����conda�����ǣ�%CONDA_DEFAULT_ENV%

CD /D %workingDir%

REM ����������
SET pythonServerScript=-m llama_cpp.server --host 0.0.0.0 --model ..\model\Meta-Llama-3-8B-GGUF\Meta-Llama-3-8B-Instruct.Q2_K.gguf --n_ctx 2048 --n_gpu_layers 28
start /B python %pythonServerScript%

REM �ȴ�����������
timeout /t 10 /nobreak

REM ����ͼ�λ�����
echo ����ͼ�λ�����
SET pythonUIScript=app.py
start python %pythonUIScript%
