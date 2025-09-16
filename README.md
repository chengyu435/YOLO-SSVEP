# YOLO-SSVEP
基于**YOLOv11**实现基于视觉目标追踪的多目标 SSVEP 实验范式  
核心范式为`SSVEP_YOLO`,实现多目标追踪的SSVEP范式，其中特别针对帧数显示的同步进行了改进优化  
用户可修改刷新率、检测目标数、视觉刺激频率等参数，采用的是正弦波刺激波形。  


`train`为YOLO的训练，目前采用的是基于cuda的GPU加速  
`process`为基础的YOLO识别并显示结果，包含摄像头和图片处理两种方法  
`test`为通过CV2获取摄像头画面并使用YOLO处理，保留处理结果并显示  
`SSVEP`为基于pygame的单目标SSVEP范式  
最终范式`SSVEP_YOLO`即为`test`和`SSVEP`融合得到的结果  
