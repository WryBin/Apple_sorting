文件说明：

test/	测试集图片

train/	 训练集图片

validation/	验证集图片

apple_size.docx	人工测量的苹果尺寸值

healthy_vs_rot_1.h5	keras输出的模型文件

healthy_vs_rot_1.py	keras训练文件，为兼容树莓派环境，此处使用CPU进行训练，训练后输出模型文件

imgprocessing.py	图像处理文件

PI_environment.py	深度学习训练环境与树莓派测试环境相同

test.py	使用测试集进行判断，输出为概率值，小于0.5判断为健康果，大于0.5判断为缺陷果



