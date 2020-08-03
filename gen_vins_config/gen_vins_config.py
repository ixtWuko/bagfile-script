#! /usr/bin/env python
# -*- coding: utf-8 -*-

'''
根据 kalibr 标定的结果，产生 vins 使用的 config.yaml
只适用于 两相机 + 一个IMU 的情况
输入：联合标定产生的 yaml 文件，通常以 camchain-imucam 命名，以及产生的描述 imu 参数的 yaml 文件。
输出：用于 vins 运行的 config 文件，以及描述两相机参数的 yaml 文件。
'''

import yaml
import numpy as np
import cv2 as cv
import getopt
import sys


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "c:i:o:h", ["chainfile=", "imufile=", "outputdir=", "help"])
    except getopt.GetoptError:
        print("usage: gen_vins_config.py -c <camchain-imucam.yaml> -i <imu.yaml> -o <output dir>")
        sys.exit(2)

    chain_file = ""
    imu_file = ""
    output_dir = ""
    for opt, arg in opts:
        if opt in ("-c", "--chainfile"):
            chain_file = arg
        if opt in ("-i", "--imufile"):
            imu_file = arg
        if opt in ("-o", "--outputdir"):
            output_dir = arg
        if opt in ("-h", "--help"):
            help_str = """
                -c --chainfile <camchain-imucam.yaml>
                -i --imufile   <imu.yaml>
                -h --help
            """
            print(help_str)

    f = open(chain_file)
    chain_parameter = yaml.load(f)
    f.close()
    f = open(imu_file)
    imu_parameter = yaml.load(f)
    f.close()

    config = cv.FileStorage(output_dir + "/stereo_camera_imu.yaml", cv.FILE_STORAGE_WRITE)
    config.write('imu', 1)
    config.write('num_of_cam', 2)
    config.write('imu_topic', '\"' + str(imu_parameter["imu0"]["rostopic"]) + '\"')
    config.write('image0_topic', '\"' + str(chain_parameter["cam0"]["rostopic"]) + '\"')
    config.write('image1_topic', '\"' + str(chain_parameter["cam1"]["rostopic"]) + '\"')
    config.write('output_path', '\"/home\"')
    config.write('cam0_calib', "cam1.yaml")
    config.write('cam1_calib', "cam2.yaml")
    config.write('image_width', chain_parameter["cam0"]["resolution"][0])
    config.write('image_height', chain_parameter["cam0"]["resolution"][1])
    config.write('estimate_extrinsic', 0)
    config.write('body_T_cam0', np.array(chain_parameter["cam0"]["T_cam_imu"]))
    config.write('body_T_cam1', np.array(chain_parameter["cam1"]["T_cam_imu"]))
    config.write('multiple_thread', 1)
    config.write('max_cnt', 150)
    config.write('min_dist', 30)
    config.write('freq', 10)
    config.write('F_threshold', 1.0)
    config.write('show_track', 1)
    config.write('flow_back', 0)
    config.write('max_solver_time', 0.04)
    config.write('max_num_iterations', 8)
    config.write('keyframe_parallax', 10.0)
    config.write('acc_n', imu_parameter["imu0"]["accelerometer_noise_density"])
    config.write('acc_w', imu_parameter["imu0"]["accelerometer_random_walk"])
    config.write('gyr_n', imu_parameter["imu0"]["gyroscope_noise_density"])
    config.write('gyr_w', imu_parameter["imu0"]["gyroscope_random_walk"])
    config.write('g_norm', 9.7985)
    config.write('estimate_td', 0)
    config.write('td', 0)
    config.release()

    f = open(r"./template/cam1.yaml")
    template_cam1 = yaml.load(f)
    f.close()
    f = open(r"./template/cam2.yaml")
    template_cam2 = yaml.load(f)
    f.close()

    template_cam1["image_width"] = chain_parameter["cam0"]["resolution"][0]
    template_cam1["image_height"] = chain_parameter["cam0"]["resolution"][1]
    template_cam1["distortion_parameters"]["k1"] = chain_parameter["cam0"]["distortion_coeffs"][0]
    template_cam1["distortion_parameters"]["k2"] = chain_parameter["cam0"]["distortion_coeffs"][1]
    template_cam1["distortion_parameters"]["p1"] = chain_parameter["cam0"]["distortion_coeffs"][2]
    template_cam1["distortion_parameters"]["p2"] = chain_parameter["cam0"]["distortion_coeffs"][3]
    template_cam1["projection_parameters"]["fx"] = chain_parameter["cam0"]["intrinsics"][0]
    template_cam1["projection_parameters"]["fy"] = chain_parameter["cam0"]["intrinsics"][1]
    template_cam1["projection_parameters"]["cx"] = chain_parameter["cam0"]["intrinsics"][2]
    template_cam1["projection_parameters"]["cy"] = chain_parameter["cam0"]["intrinsics"][3]
    with open(output_dir + "/cam1.yaml", "w") as dumpfile:
        dumpfile.write("%YAML:1.0\n")
        dumpfile.write("---\n")
        dumpfile.write(yaml.dump(template_cam1, default_flow_style=False))

    template_cam2["image_width"] = chain_parameter["cam1"]["resolution"][0]
    template_cam2["image_height"] = chain_parameter["cam1"]["resolution"][1]
    template_cam2["distortion_parameters"]["k1"] = chain_parameter["cam1"]["distortion_coeffs"][0]
    template_cam2["distortion_parameters"]["k2"] = chain_parameter["cam1"]["distortion_coeffs"][1]
    template_cam2["distortion_parameters"]["p1"] = chain_parameter["cam1"]["distortion_coeffs"][2]
    template_cam2["distortion_parameters"]["p2"] = chain_parameter["cam1"]["distortion_coeffs"][3]
    template_cam2["projection_parameters"]["fx"] = chain_parameter["cam1"]["intrinsics"][0]
    template_cam2["projection_parameters"]["fy"] = chain_parameter["cam1"]["intrinsics"][1]
    template_cam2["projection_parameters"]["cx"] = chain_parameter["cam1"]["intrinsics"][2]
    template_cam2["projection_parameters"]["cy"] = chain_parameter["cam1"]["intrinsics"][3]
    with open(output_dir + "/cam2.yaml", "w") as dumpfile:
        dumpfile.write("%YAML:1.0\n")
        dumpfile.write("---\n")
        dumpfile.write(yaml.dump(template_cam2, default_flow_style=False))


if __name__ == "__main__":
    main(sys.argv[1:])