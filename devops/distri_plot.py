# coding=utf-8
import os
import matlab.engine

def distri_plot():
    dirName_trans = '../distri_plot/transAnt'
    dirName_rec = '../distri_plot/recAnt'
    power_control_min = -114
    power_control_max = -90
    triangle_ant_min = 0
    triangle_ant_max = 48
    data_plot_path = '../devops/plot&Data'
    os.chdir("../distri_plot")
    eng = matlab.engine.start_matlab()
    sate_height_list = [1010]
    for index in sate_height_list:
        sate_height = index
        try:
            eng.distriPlot(float(sate_height), dirName_trans, dirName_rec, float(power_control_min), float(power_control_max), float(triangle_ant_min), float(triangle_ant_max), data_plot_path)
        except Exception as exp:
            msg = "plot error:'\n'sate_height_%s" % sate_height
            print msg
            print exp
    eng.quit()
if __name__ == '__main__':
    distri_plot()