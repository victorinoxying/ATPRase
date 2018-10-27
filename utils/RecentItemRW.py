import os
class RecentItemRW(object):
    path = 'data\\recent_use_item.txt'
    # �������ļ��ж�ȡ�������Ŀ·��
    @staticmethod
    def read_recent_items():
        result = []
        if not os.path.exists(RecentItemRW.path):
            return result

        fileStream = open(RecentItemRW.path, 'r')
        for line in fileStream.readlines():
            if line == '\n':
                continue
            itemInfo = line.split(' ')
            result.append(itemInfo[1])
        fileStream.close()
        return result

    # д�������ļ�
    @staticmethod
    def write_recent_items(infoList):
        fileStream = open(RecentItemRW.path, 'w+')
        for i in range(len(infoList)):
            if i == 0:
                fileStream.write(str(i) + ' ' + infoList[i])
            else:
                fileStream.write('\n' + str(i) + ' ' + infoList[i])
        fileStream.close()
