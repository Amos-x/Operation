

class Node(object):
    # def __init__(self,key):
    #     self.key = key

    def __eq__(self, other):
        if not other:
            return False
        return self.key == other.key


if __name__ == '__main__':
    a = [1,2]
    b = [1,2,3]
    print(a.__lt__(b))
    print(a < b)