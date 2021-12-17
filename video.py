import cv2
import numpy as np
import os
import uuid
import json

class Video:

    def __init__(self, video, name=uuid.uuid1(), frame_array=[], film=[]):
        self.name = str(name)
        self.video = video
        self.frame_array = frame_array
        self.film = film
        self.progress = 0
        os.makedirs("tmp/" + self.name + "/keyframes", exist_ok=True)

    def treatement(self):
        cap = cv2.VideoCapture(self.video)
        length_video = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        diff_array_value = []
        ret, prev_frame = cap.read()
        self.film.append(prev_frame)
        while ret:
            ret, curr_frame = cap.read()
            if ret:
                diff = cv2.absdiff(curr_frame, prev_frame)
                non_zero_count = np.count_nonzero(diff)
                diff_array_value.append(non_zero_count)
                self.film.append(curr_frame)
                prev_frame = curr_frame
                self.progress += (1/(2*length_video))*100

        p_frame_thresh = max(diff_array_value) - 0.04 * max(diff_array_value)

        plot_new_value = []
        stopper = 0
        for i in range(1, len(self.film)):
            diff = cv2.absdiff(self.film[i], self.film[i - 1])
            non_zero_count = np.count_nonzero(diff)
            plot_new_value.append(non_zero_count)
            if non_zero_count > p_frame_thresh and stopper > 30:
                stopper = 0
                cv2.imwrite("tmp/" + self.name + "/keyframes/" + str(i) + ".jpg", self.film[i])
                self.frame_array.append(i)
                #for j in range(i, i + 30):
                #    if (j < len(self.film)):
                #        self.frame_array.append(j)
            stopper += 1
            self.progress += (1 / (2 * length_video))*100

        self.size = (len(self.film[0][0]), len(self.film[0]))

        returned_value = {}
        returned_value['data'] = []

        for frame in self.frame_array:
            returned_value['data'].append({
                'id': frame,
                'time_code': frame/30,
                'img': "tmp/" + self.name + "/keyframes/" + str(frame) + ".jpg",
                'checked': True
            })

        return returned_value

    def save_ressource(self, keyframes=[]):
        data = []
        if keyframes == []: #ALL
            for frame in self.frame_array:
                data.append(frame)
                for j in range(frame, frame + 30):
                    if (j < len(self.film)):
                        data.append(j)
        else:
            for frame in keyframes:
                data.append(frame)
                for j in range(frame, frame + 30):
                    if (j < len(self.film)):
                        data.append(j)

        if len(data) > 0:
            out = cv2.VideoWriter('tmp/' + self.name + '/output.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 30, self.size)
            for image in data:
                out.write(self.film[image])
            out.release()
            return True

        return False

    def add_manualy_keyFrame_from_time_code(self, time_code):
        """inutile"""
        time_code = int(time_code) * 30
        img = self.film[time_code]
        cv2.imwrite("tmp/" + self.name + "/keyframes/" + str(time_code) + ".jpg", img)
        return "tmp/" + self.name + "/keyframes/" + str(time_code) + ".jpg"

    def from_time_code(self, time_code):
        time_code = int(time_code) * 30
        return "tmp/" + self.name + "/keyframes/" + str(time_code) + ".jpg"

    def getProgress(self):
        return self.progress

    def export(self):
        return (self.name, self.video, self.frame_array)

    