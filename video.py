import cv2
import numpy as np
import os

class Video:

    def __init__(self, name, video):
        self.name = name
        self.video = video
        self.frame_array = []
        self.film = []
        os.makedirs("tmp/" + self.name + "/keyframes")

    def treatement(self):
        cap = cv2.VideoCapture(self.video)
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

        self.size = (len(self.film[0][0]), len(self.film[0]))
        return self.frame_array

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
            out = cv2.VideoWriter('tmp/' + self.name + '/output.avi', cv2.VideoWriter_fourcc(*'XVID'), 30, self.size)
            for image in data:
                out.write(self.film[image])
            out.release()
            return True

        return False