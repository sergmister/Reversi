import numpy as np
from game.Reversi import Reversi


class Node:

    def __init__(self, state, turn, action):
        self.state = state  # current board state
        self.turn = turn  # turn of the last play
        self.action = action  # action of the last play
        self.done = 0
        self.edges = []  # other connecting nodes bellow
        self.stats = {
            'N': 0,  # number of visits
            'W': 0,  # total value of next state
            'Q': 0,  # mean value of next state
        }

    def calculate_stats(self):
        game_over, white_total, black_total = Reversi.check_board(self.state, self.turn)
        if game_over:
            if white_total == black_total:
                value = 1
            elif white_total > black_total:
                value = self.turn * 100
                self.done = 1
            elif white_total < black_total:
                value = self.turn * -100
                self.done = 1
        else:
            if self.turn == 1:
                value = white_total / black_total
            elif self.turn == -1:
                value = black_total / white_total
        self.update_stats(value)

    def update_stats(self, value):
        self.stats['N'] += 1
        self.stats['W'] += value
        self.stats['Q'] = self.stats['W'] / self.stats['N']

    def isNotLeaf(self):
        return bool(self.edges)


class basic_MCTS:

    def __init__(self, player, simulations=100, cpuct=1):
        self.player = player
        self.tree = dict()  # all explored nodes
        self.simulations = simulations
        self.cpuct = cpuct

    def moveToLeaf(self):  # decides optimal Q and moves down accordingly

        breadcrumbs = []
        currentNode = self.root

        while currentNode.isNotLeaf():
            maxQ = -1000000
            for node in currentNode.edges:
                Q = node.stats['Q']
                if Q > maxQ:
                    maxQ = Q
                    simulationNode = node

            currentNode = simulationNode
            breadcrumbs.append(simulationNode)

        return currentNode, breadcrumbs

    def evaluateLeaf(self, leaf):  # implement done
        if leaf.done == 0:
            for move in Reversi.valid_moves(leaf.state, -leaf.turn):
                newNode = Node(leaf.state.copy(), -leaf.turn, move)
                Reversi.move(newNode.state, newNode.turn, *move)
                if self.getID(newNode.state) not in self.tree:  # redundant?
                    newNode.calculate_stats()
                    self.addNode(newNode)
                    leaf.edges.append(newNode)
                else:  # making multiple paths to same node? backFill?
                    leaf.edges.append(self.tree[self.getID(newNode.state)])
                    del newNode
        else:
            pass

    def backFill(self, leaf, breadcrumbs):
        value = leaf.stats['W']
        for node in breadcrumbs:
            node.update_stats(value)

    def addNode(self, node):
        self.tree[self.getID(node.state)] = node

    def getID(self, state):  # not fast
        return ''.join(map(str, state))

    def simulate(self):
        leaf, breadcrumbs = self.moveToLeaf()
        self.evaluateLeaf(leaf)
        self.backFill(leaf, breadcrumbs)

    def move(self, state):  # if to check if root in tree?
        if self.getID(state) not in self.tree:
            self.addNode(Node(state.copy(), -self.player, None))
        self.root = self.tree[self.getID(state)]
        for sim in range(self.simulations):
            self.simulate()
        maxQ = -1000000
        for node in self.root.edges:
            if node.stats['Q'] > maxQ:
                maxQ = node.stats['Q']
                action = node.action
        return action



