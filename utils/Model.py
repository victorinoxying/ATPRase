import os


class Model(object):
    def __init__(self):
        self.__ModelDict = {}

    # 判断此model类的存储字典是否为空
    def IsEmpty(self):
        if self.__ModelDict:
            return False
        else:
            return True

    # 以下均为接口函数，直接调用,用于匹配现有实体的信息和已存模式的信息
    # 输入：信息矩阵
    # 输出：现有实体多出来的节点名（类型set）
    def matchSource(self, InfoArray):
        return self.__matchNodeList('source', InfoArray)

    def matchBranch(self, InfoArray):
        return self.__matchNodeList('branch', InfoArray)

    def matchLcc(self, InfoArray):
        return self.__matchNodeList('lcc', InfoArray)

    def matchLightning(self, InfoArray):
        return self.__matchNodeList('lightning', InfoArray)

    def matchSwitch(self, InfoArray):
        return self.__matchNodeList('switch', InfoArray)

    # 以下均为接口函数，直接调用
    # 输入：信息矩阵
    def saveSource(self, InfoArray):
        self.__saveInDict('source', InfoArray)

    def saveBranch(self, InfoArray):
        self.__saveInDict('branch', InfoArray)

    def saveLcc(self, InfoArray):
        self.__saveInDict('lcc', InfoArray)

    def saveLightning(self, InfoArray):
        self.__saveInDict('lightning', InfoArray)

    def saveSwitch(self, InfoArray):
        self.__saveInDict('switch', InfoArray)

    # 将model信息存入文本文件
    def saveInTxt(self, filePath):
        fileName = filePath + '_Model_Info.txt'
        fileStream = open(fileName, 'w+')

        for key, value in self.__ModelDict.items():
            fileStream.write('%12s' % str(key))
            for i in value:
                fileStream.write('|')
                for j in i:
                    fileStream.write(j + ' ')
            fileStream.write('\n')
        fileStream.close()

        # 清空字典
        self.__ModelDict.clear()

    # 判断txt文件是否存在
    def IsfileExist(self, filePath):
        fileName = filePath + '_Model_Info.txt'
        return os.path.exists(fileName)

    # 从txt中读出字典
    # 输入：txt文件路径
    def readFromTxt(self, filePath):
        if not self.IsfileExist(filePath):
            return
        fileName = filePath + '_Model_Info.txt'
        fileStream = open(fileName, 'r')
        self.__ModelDict.clear()
        for line in fileStream.readlines():
            EntityArray = []
            lineArray = line.split('|')
            EntityName = str(lineArray[0]).strip()
            lineArray.pop(0)
            # 这是哪个sb加的一句：
            # lineArray.pop()
            for element in lineArray:
                nodeArray = element.split(' ')
                for i in nodeArray:
                    str(i).strip()
                    if i == '' or i == '\n':
                        nodeArray.remove(i)
                EntityArray.append(nodeArray)
            self.__ModelDict[EntityName] = EntityArray
        if self.IsEmpty():
            return
        else:
            return self.__ModelDict

    # 删除本地存储的模式信息
    def removeModelTxt(self, filePath):
        fileName = filePath + '_Model_Info.txt'
        if self.IsfileExist(filePath):
            os.remove(fileName)
            return True
        else:
            return False

    # 匹配某个实体的节点名是否一致的实现函数
    # 输出：不匹配的set
    def __matchNodeList(self, entityName, toMatchList):
        return Model.diffList(entityName, self.__ModelDict[entityName])

    @staticmethod
    def diffList(owner, compare):
        """
        对比两个list，返回owner中compare没有的项
        :param owner:
        :param compare:
        :return:
        """
        nodeSet = set()
        toMatchNodeSet = set()
        for nodeName in owner:
            if nodeSet != '':
                nodeSet.add(nodeName[0])
        for nodeName in compare:
            if nodeName != '':
                toMatchNodeSet.add(nodeName)
        return nodeSet - toMatchNodeSet

    # 将模式矩阵存入字典的实现函数
    def __saveInDict(self, entityType, InfoArray):
        self.__ModelDict[entityType] = InfoArray


if __name__ == '__main__':
    model = Model()
    a = [['dasModel', 's_1'], ['sdasmlds', 'i_2_9'], ['teset', '8_9']]
    b = [['asdsad', 's_1'], ['frefrfg', 'i_2_9'], ['mnjhj', '8_9']]
    model.saveBranch(a)
    model.saveLightning(b)
    print(model.IsEmpty())
    model.saveInTxt(r'D:\dataatp\model')
    modelRead = Model()
    modelRead.readFromTxt(r'D:\dataatp\model')
    setttt = modelRead.matchBranch(['asdsad', 'frefrfg', 'mnjhj'])
    print(setttt)
