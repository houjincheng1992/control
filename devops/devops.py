# coding=utf-8
import os
import re

# import xlrd, xlwt

import matlab
import matlab.engine

class AISSig():
    def createAISSig(self):
        path = "../devops/AISSig"
        signum = 10
        obtime = 12
        conflictNum = 2
        totalratio = 1
        channelnum = 1
        os.chdir('../ais_testmodule/')
        eng = matlab.engine.start_matlab()
        for powdiff in range(0, 15):
            for EbN0 in range(1, 2):
                try:
                    # print 'success'
                    #sig.create(float(powdiff), float(signum), float(conflictNum), float(totalratio), float(channelnum), float(EbN0), path)
                    eng.test(float(obtime), float(powdiff), float(signum), float(conflictNum), float(totalratio), float(channelnum), float(EbN0), path)
                    # print 'success'
                except Exception as exp:
                    # print "powdiff: %s  EbN0: %s" %(powdiff, EbN0)
                    msg = "CreateAisSig error:'\n'powdiff: %s  EbN0: %s" %(powdiff, EbN0)
                    # print exp
                    error.add_error_msg(msg + ':' + str(exp))
                #eng.test(powdiff, signum, conflictNum, totalratio, channelNum, EbN0, path))
        os.chdir('../devops/')
        eng.quit()
sig = AISSig()

class Demo():
    def antDemo(self):
        file_list = os.listdir('./AISSig')
        current = os.getcwd()
        aissig = os.path.join(current, './AISSig')
        os.chdir('../singleantv2.0.1/')
        eng = matlab.engine.start_matlab()
        for file_name in file_list:
            if file_name == '.' or file_name == '..' or file_name == '.DS_Store':
                continue
            sigpath = os.path.join(aissig, file_name)
            try:
                eng.Main(sigpath)
            except Exception as exp:
                msg = "antDemo error: '\n'filename: %s" %(file_name)
                error.add_error_msg(msg + ':' + str(exp))
        eng.quit()
        os.chdir('../devops/')
demo = Demo()

def getdataparam(filename):
    pattern = re.compile(r'^AIS(Data)_h\d+_t\d+_v\d+_e(\d+)_p(\d+)')
    # pattern = re.compile(r'^AISData_h\d+_t\d+_v\d+_e(\d+)_p(\d+)')
    match = pattern.match(filename)
    print filename
    if match:
        return match.groups()
    return None

class Analysis():
    def check(self):
        res = {}
        file_list = os.listdir('./AISSig')
        current = os.getcwd()
        aissig = os.path.join(current, './AISSig')
        os.chdir('../checkprob/conflictcheck')
        eng = matlab.engine.start_matlab()
        for file_name in file_list:
            if file_name == '.' or file_name == '..' or file_name == '.DS_Store':
                continue
            sigpath = os.path.join(aissig, file_name) + '/'
            resultpath = os.path.join(sigpath, 'demodResult_1ant/')
            filename = os.listdir(sigpath)
            # print filename
            for k in filename:
                data = getdataparam(k)
                print data
                if not data or not data[0]:
                    continue
                dataname = os.path.join(sigpath, k)
                # print 'start_matlab'
                try:

                    prob = eng.detectProbability(resultpath, k, sigpath)
                except Exception as exp:
                    msg = "prob error:'\n'filename: %s" % k
                    os.chdir("../")
                    error.add_error_msg(msg + ':' + str(exp))
                    os.chdir('./conflictcheck')
                if not res.has_key(int(data[1])):
                    res[int(data[1])] = {}
                if not res[int(data[1])].has_key(int(data[2])):
                    res[int(data[1])][int(data[2])] = prob
        eng.quit()
        os.chdir('../../devops/')
        print res
        return res
anay = Analysis()


def genXlsFormat(result):
    """
    TODO: from txt gen xls
    """
    try:
        ft = open('./checkprob_result/result.txt', 'w+')
    except Exception as exp:
        msg = "genxlsFormat error:'\n'" + str(exp)
        error.add_error_msg(msg)
    #for eb, value in result.iteritems():
    #    for po, pr in value.iteritems():
    items = result.items()
    items.sort()
    for eb, v in items:
        it = v.items()
        it.sort()
        for po, pr in it:
            context = str(eb) + " " + str(po) + " " + str(pr) + '\n'
            ft.write(context)
            print eb, po, pr
    ft.close()


class error_msg():
    def add_error_msg(self, msg, *args, **kwargs):
        if not os.path.exists('../devops/error.txt'):
            fe = open('../devops/error.txt', 'w')
            fe.close()
        fe = open('../devops/error.txt', 'a')
        context = str(msg) + '\r\n'
        fe.write(context)
        for item in args:
            context_item = str(item) + '\r\n'
            fe.write(context_item)
        fe.close()
error = error_msg()



if __name__ == '__main__':
    sig.createAISSig()
    demo.antDemo()
    res = anay.check()
    genXlsFormat(res)
