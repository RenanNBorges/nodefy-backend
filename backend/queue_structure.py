class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class Queue:
    def __init__(self):
        self.queue = None
        self.size = 0

    def push(self, data):
        auxNode = self.queue
        if self.size != 0:
            while auxNode.next:
                auxNode = auxNode.next
            auxNode.next = Node(data)
        else:
            self.queue = Node(data)

        self.size += 1

    def pop(self):
        elem = self.queue
        if self.queue and self.queue.next:
            self.queue = self.queue.next
        elif self.queue:
            self.queue = None
        else:
            return self.queue
        self.size -= 1
        return elem.data
