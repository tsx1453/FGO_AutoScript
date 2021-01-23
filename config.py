import os

project_path = os.path.split(os.path.realpath(__file__))[0]
capture_output_path = os.path.join(project_path, "captures")
template_img_path = os.path.join(project_path, "template")
match_result_save_path = os.path.join(project_path, "match_results")

if not os.path.exists(capture_output_path):
    os.mkdir(path=capture_output_path)

if not os.path.exists(match_result_save_path):
    os.mkdir(path=match_result_save_path)

if __name__ == '__main__':
    all_path, all_name = [], []
    for file in os.listdir(template_img_path):
        path = os.path.join(template_img_path, file)
        if os.path.isfile(path):
            all_path.append(path)
            all_name.append(file.split(".")[0])
    with open(os.path.join(project_path, "resources.py"), mode="w") as f:
        for i in range(0, len(all_path)):
            f.write("{} = '{}'\n".format(all_name[i], all_path[i]))
