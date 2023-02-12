import random
import matplotlib.pyplot as plt

def dis(p1, p2):
    distant = 0
    for index in range(len(p1)):
        distant += (p1[index]-p2[index])*(p1[index]-p2[index])
    return distant

class LVQ:
    def __init__(self):
        self.data = []
        self.label = []
        self.ClassCenter = []
        self.ClassLabel = []
        self.ClassNum = 0

    def Train(self, classNum = 3, classLabel = [], raito = 0.1, turn = 10000, data = [], label = []):
        self.data = data
        self.label = label
        self.ClassLabel = classLabel
        self.ClassNum = classNum
        dataSet = {}
        vis = {}
        for index in range(len(data)):
            if label[index] not in dataSet.keys():
                dataSet[label[index]] = []
                vis[label[index]] = []
            dataSet[label[index]].append(data[index])
            vis[label[index]].append(False)
        #初始化中心数组
        for index in range(classNum):
            while True:
                pos = random.randint(0, len(dataSet[self.ClassLabel[index]])-1)
                if not vis[self.ClassLabel[index]][pos]:
                    vis[self.ClassLabel[index]][pos] = True
                    self.ClassCenter.append(dataSet[self.ClassLabel[index]][pos])
                    break
        for index in range(turn):
            pos = random.randint(0, len(data)-1)
            distant = dis(self.ClassCenter[0], data[pos])
            cPos = 0
            for i in range(classNum):
                if dis(self.ClassCenter[i], data[pos]) < distant:
                    cPos = i
                    distant = dis(self.ClassCenter[i], data[pos])
            diff = []
            for i in range(len(data[pos])):
                diff.append(raito*(data[pos][i]-self.ClassCenter[cPos][i]))
            if label[pos] == self.ClassLabel[cPos]:
                for i in range(len(self.ClassCenter[cPos])):
                    self.ClassCenter[cPos][i] += diff[i]
            else:
                for i in range(len(self.ClassCenter[cPos])):
                    self.ClassCenter[cPos][i] -= diff[i]

    def Predict(self, data):
        distant = dis(data, self.ClassCenter[0])
        res = self.ClassLabel[0]
        pos = 0
        for index in range(self.ClassNum):
            if dis(data, self.ClassCenter[index]) < distant:
                distant = dis(data, self.ClassCenter[index])
                res = self.ClassLabel[index]
                pos = index
        return res, pos


if __name__ == "__main__":
    lvq = LVQ()
    datas = [[0.697, 0.460], [0.774, 0.376], [0.634, 0.264], [0.608, 0.318],
             [0.556, 0.215], [0.403, 0.237], [0.481, 0.149], [0.437, 0.211],
             [0.666, 0.091], [0.243, 0.267], [0.245, 0.057], [0.343, 0.099],
             [0.639, 0.161], [0.657, 0.198], [0.360, 0.370], [0.593, 0.042],
             [0.719, 0.103], [0.359, 0.188], [0.339, 0.241], [0.282, 0.257],
             [0.748, 0.232], [0.714, 0.346], [0.483, 0.312], [0.478, 0.437],
             [0.525, 0.369], [0.751, 0.489], [0.532, 0.472], [0.473, 0.376],
             [0.725, 0.445], [0.446, 0.459]]
    labels = ['c1', 'c1', 'c1', 'c1', 'c1', 'c1', 'c1', 'c1', 'c2', 'c2',
              'c2', 'c2', 'c2', 'c2', 'c2', 'c2', 'c2', 'c2', 'c2', 'c2',
              'c2', 'c1', 'c1', 'c1', 'c1', 'c1', 'c1', 'c1', 'c1', 'c1',
              'c1', 'c1', 'c1', 'c1', 'c1', 'c1', 'c1', 'c1', 'c1', 'c1']
    marks = ['or', 'ob', 'og', 'ok', '^r', '+r', 'sr', 'dr', '<r', 'pr']
    lvq.Train(classNum=5, classLabel=['c1','c2','c2','c1','c1'],turn=100, data=datas, label=labels)
    for d in datas:
        r, p = lvq.Predict(d)
        plt.plot(d[0], d[1], marks[p] , markersize=5)
    plt.show()
