import os

capture_output_path = os.path.join(os.path.split(os.path.realpath(__file__))[0], "captures")
template_img_path = os.path.join(os.path.split(os.path.realpath(__file__))[0], "template")

if not os.path.exists(capture_output_path):
    os.mkdir(path=capture_output_path)
