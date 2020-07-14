import numpy as np
from game.Reversi import Reversi
from AI.model import Residual_CNN

class Node:

    def __init__(self, state, turn):
        self.state = state  # current board state
        self.turn = turn
        self.edges = []  # other connecting nodes bellow

    def isNotLeaf(self):
        return bool(self.edges)


class Edge:

    def __init__(self, inNode, outNode, prior, turn, action):
        self.id = inNode.state.id + '|' + outNode.state.id
        self.inNode = inNode
        self.outNode = outNode
        self.turn = turn
        self.action = action

        self.stats = {
            'N': 0,
            'W': 0,
            'Q': 0,
            'P': prior,
        }


class MCTS:

    def __init__(self, player, simulations=100, cpuct=1):
        self.player = player
        self.tree = dict()  # all explored nodes
        self.simulations = simulations
        self.cpuct = cpuct
        self.EPSILON = 0.2
        self.ALPHA = 0.8
        self.model = Residual_CNN((8, 8), (8, 8))

    def moveToLeaf(self):  # decides optimal Q and moves down accordingly

        breadcrumbs = []
        currentNode = self.root

        done = 0
        value = 0

        while currentNode.isNotLeaf():

            maxQU = -1000000

            if currentNode == self.root:
                epsilon = self.EPSILON
                nu = np.random.dirichlet([self.ALPHA] * len(currentNode.edges))
            else:
                epsilon = 0
                nu = [0] * len(currentNode.edges)

            Nb = 0
            for edge in currentNode.edges:
                Nb = Nb + edge.stats['N']

            for idx, edge in enumerate(currentNode.edges):

                U = self.cpuct * ((1 - epsilon) * edge.stats['P'] + epsilon * nu[idx]) * np.sqrt(Nb) / (1 + edge.stats['N'])

                Q = edge.stats['Q']

                if Q + U > maxQU:
                    maxQU = Q + U
                    simulationEdge = edge

            currentNode = simulationEdge.outNode
            breadcrumbs.append(simulationEdge)

        return currentNode, value, done, breadcrumbs

    def evaluateLeaf(self, leaf, value):  # implement done

        if leaf.done == 0:

            value, policy = self.get_preds(leaf.state, -leaf.turn)

            for move in Reversi.valid_moves(leaf.state, -leaf.turn):
                #newNode = Node(leaf.state.copy(), -leaf.turn, move)
                newState = leaf.state.copy()
                Reversi.move(newState, -leaf.turn, *move)
                if self.getID(newState) not in self.tree:  # redundant?
                    newNode = Node(newState, -leaf.turn)
                    #newNode.calculate_stats()
                    self.addNode(newNode)
                else:  # making multiple paths to same node? backFill?
                    newNode = self.tree[self.getID(newState)]

                newEdge = Edge(leaf, newNode, policy[move[0]][move[1]], -leaf.turn, move)
                leaf.edges.append(newEdge)
        else:
            pass

        return value

    def backFill(self, leaf, value, breadcrumbs):
        for edge in breadcrumbs:
            edge.update_stats(value * leaf.turn * self.player)  # ????????????????

    def get_preds(self, state, turn):
        modelIn = np.stack((state, np.full((8, 8), fill_value=turn, dytpe=np.int8)))
        preds = self.model.predict(modelIn)
        value = preds[0][0]
        policy = preds[1][0]
        return value, policy

    def addNode(self, node):
        self.tree[self.getID(node.state)] = node

    def getID(self, state):  # not fast
        return ''.join(map(str, state))

    def cleanTree(self):
        pass  # recursively remove dead branches to save memory after each move?

    def simulate(self):
        leaf, value, done, breadcrumbs = self.moveToLeaf()
        value = self.evaluateLeaf(leaf, value)
        self.backFill(leaf, value, breadcrumbs)

    def move(self, state):  # if to check if root in tree?
        if self.getID(state) not in self.tree:
            self.addNode(Node(state.copy(), -self.player))
        self.root = self.tree[self.getID(state)]
        for sim in range(self.simulations):
            self.simulate()
        maxQ = -1000000
        for node in self.root.edges:
            if node.stats['Q'] > maxQ:
                maxQ = node.stats['Q']
                action = node.action
        return action
