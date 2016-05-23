# coding = utf-8

from tasks import matlab_create_ves_distri
class test():

    def test_distri(self, payload):
        payload = {
            "action": "distri",
            "Lat": 23,
            "Lon": 34,
            "Height": 600,
            "VesNum": 500,
            "Mode": 0,
            "distri_id": "distri",
            "Obtime": 12,
            "partable_id": "partablewfslvjoiw",
            "timetable_id": "timetablewf232fsl",
            "aisdata_id": "aisdata23fwf32f",
            "signal_id": "signalw2wf32f"
            }
        matlab_create_ves_distri(payload)

if __name__ == '__main__':
    # payload = {'action': "distri",
    #            "Lat": 23,
    #            "Lon": 34,
    #            "Height": 600,
    #            "VesNum": 500,
    #            "Mode": 0,
    #            "distri_id": "distri",
    #            "Obtime": 12,
    #            "partable_id": "partablewfslvjoiw",
    #            "timetable_id": "timetablewf232fsl",
    #            "aisdata_id": "aisdata23fwf32f",
    #            "signal_id": "signalw2wf32f"
    #            }
    test = test()
    test.test_distri()