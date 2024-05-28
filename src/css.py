# -*- coding: utf-8 -*-
'''
@File    :   css.py
@Time    :   2024/05/03 17:08:55
@Author  :   Krisnile 
@Desc    :   None
'''


# Copy from LLaMA-Factory's project UI's CSS

CSS = r"""
.modal-box {
  position: fixed !important;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%); /* center horizontally */
  max-width: 1000px;
  max-height: 750px;
  overflow-y: auto;
  background-color: var(--input-background-fill);
  flex-wrap: nowrap !important;
  border: 2px solid black !important;
  z-index: 1000;
  padding: 10px;
}
"""
