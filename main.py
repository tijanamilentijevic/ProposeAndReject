import numpy as np
import matplotlib.pyplot as plt


class Node:
    def __init__(self, node_id, node_b):
        self.id = node_id
        self.b = node_b
        self.connected_nodes = []  # for each node, non-null entries
        self.accepted_nodes = []  # the list of accepted proposals
        self.received_proposals = []
        self.proposed_node = None

    def is_done(self):  # can this node send new proposals
        if self.b > 0 and len(self.connected_nodes) > 0:
            return False
        return True


def create_entries():
    if log: print("Start creating Entries:")
    for i in range(n):
        node = Node(i, b)  # the making of nodes
        nodes.append(node)
    for i in range(n):
        current_node = find_node(i)
        for j in range(n):
            if matrix[i][j] > 0:
                current_node.connected_nodes.append(find_node(j))
                if log: print("Node {} has non-null entry with Node {}".format(current_node.id, find_node(j).id))


def find_node(key):
    for i in nodes:
        if i.id == key:
            return i
    raise ValueError('Node %d could not be found in nodes', key)


def check_done():  # check for each node if it can send proposals
    for node in nodes:
        if not node.is_done():
            return False
    return True


def send_entries():
    finished = False
    round = 1  # iteration
    communication_round = 0
    while not finished:
        if log: print("Proposalround {}".format(round))
        communication_round += 2 * l
        for node in nodes:
            if not node.is_done():
                node.connected_nodes.sort(key=lambda x: matrix[node.id, x.id], reverse=True)  # sort entries
                proposed_node = node.connected_nodes[0]  # choose the biggest entry
                node.connected_nodes.pop(0)
                node.proposed_node = proposed_node
                proposed_node.received_proposals.append(node)  # proposal sent
                node.b -= 1  # node is tentative, waiting for acceptance
                if log: print("Node {} proposes to {}".format(node.id, proposed_node.id))
        if log: print("Examinationround {}".format(round))
        sent_proposals = False
        max_proposals = 0
        max_accepted_proposals = 0
        for node in nodes:
            accepted_proposals = 0
            if log: print("Node {}(b = {}) receives proposals from: ".format(node.id, node.b), end='')
            if len(node.received_proposals) > max_proposals:
                max_proposals = len(node.received_proposals)
            for prop in node.received_proposals:
                if log: print("{}, ".format(prop.id), end='')
            if log: print('')
            if len(node.received_proposals) > 0 and node.b > 0:
                combined_list = []  # for examination
                for proposer in node.received_proposals:
                    combined_list.append([proposer, matrix[proposer.id][node.id] + matrix[node.id][proposer.id]])
                combined_list.sort(key=lambda x: x[1], reverse=True)  # sort received proposals
                while len(combined_list) > 0 and node.b > 0:
                    accepted_node = combined_list[0][0]
                    if accepted_node in node.accepted_nodes:
                        combined_list.pop(0)
                    else:
                        if accepted_node == node.proposed_node:
                            node.b += 1
                        node.b -= 1
                        if log: print("Node {} accepts node {}".format(node.id, accepted_node.id))
                        accepted_node.accepted_nodes.append(node)  # add the corresponding node to accepted nodes
                        node.accepted_nodes.append(accepted_node)
                        accepted_proposals += 1
                        if not sent_proposals:
                            communication_round += 2 * l
                            sent_proposals = True
                        combined_list.pop(0)
                for i in combined_list:  # if proposal not accepted
                    i[0].b += 1
                if max_accepted_proposals < accepted_proposals:
                    max_accepted_proposals = accepted_proposals
            node.received_proposals = []
        communication_round += max_proposals - 1
        communication_round += max_accepted_proposals - 1
        finished = check_done()
        round += 1
    return communication_round


def entry_communication_probability(p, entry):  # deciding which entry stays and which is 0
    k = np.random.rand()
    if k > p:
        return 0
    else:
        return entry


def create_matrix():
    old_sum = 0
    new_sum = 0
    for i in range(len(matrix)):
        for j in range(len(matrix[1])):
            if i == j:
                matrix[i][j] = 0
            else:
                matrix[i][j] = entry_communication_probability(p, matrix[i][j])
            old_sum = old_sum + matrix[i][j]
    for i in range(len(matrix)):
        for j in range(len(matrix[1])):
            if matrix[i][j] != 0:
                matrix[i][j] = matrix[i][j] / old_sum
            new_sum = new_sum + matrix[i][j]  # new_sum sums up to 1 in the end


if __name__ == "__main__":
    n = int(input("Enter the size of the matrix:"))
    p = float(input("Enter the probability that two nodes communicate with each other (form 0.x):"))
    b = int(input("Enter the degree of DAN:"))
    l = int(input("Enter the number of levels that fattree contains:"))
    logs = input("Would you like a printed output of the algorithm? y/n ")
    #logs = "n"
    if logs == "y":
        log = True  # for printing
    else:
        log = False
    """
    p=0.2
    cr_avg1 = 0
    cr_avg2 = 0
    cr_avg3 = 0
    data1 = []
    data2 = []
    data3 = []
    # print("n = {}, p = {}, b = {}, l = {}".format(n, p, b, l))
    prob = [0.2,0.3,0.4]
    for pe in prob:
        p=pe
        print("n = {}, p = {}, b = {}, l = {}".format(n, p, b, l))
        for i in range(3):
            nodes = []  # array of elements from class Node
            matrix = np.random.rand(n, n)
            proposals = np.zeros((n, n))
            create_matrix()
            if log: print(matrix)
            create_entries()
            CR = send_entries()
            if pe == 0.2:
                cr_avg1 += CR
                data1.append(CR)
            elif pe == 0.3:
                cr_avg2 += CR
                data2.append(CR)
            else:
                cr_avg3 += CR
                data3.append(CR)
            print('finished {}'.format(i))
    """
    nodes = []  # array of elements from class Node
    matrix = np.random.rand(n, n)
    proposals = np.zeros((n, n))
    create_matrix()
    if log: print(matrix)
    create_entries()
    send_entries()
    if log:
        for k in nodes:
            print("Node {} has connection to: ".format(k.id), end='')
            for j in k.accepted_nodes:
                print("{}, ".format(j.id), end='')
            print('')
    """
    # print("Communication Rounds: {}".format(CR))
    print("Za l=3: {}, za l=4: {}, za l=5: {} ".format(cr_avg1, cr_avg2, cr_avg3))
    # names = ['p = 0.2', 'p = 0.3', 'p = 0.4', 'p = 0.5', 'p = 0.6', 'p = 0.7']
    # plt.bar(names, [round(cr_avg1 / 100), round(cr_avg2 / 100), round(cr_avg3 / 100), round(cr_avg4 / 100), round(cr_avg5 / 100), round(cr_avg6 / 100)])
    data = [data1, data2, data3]

    fig = plt.figure(figsize=(10, 7))

    fig1, ax1 = plt.subplots()
    ax1.boxplot(data)
    ax1.set_title(
        'Repetitions of the modified version of \n the "Propose and Reject" algorithm \n with n = 1024, p = 0.2 and b = 4')
    ax1.set_ylabel('Average number of communication rounds')
    # ax = fig.add_axes([0, 0, 1, 1])
    # bp = ax.boxplot(data)
    # plt.ylabel('Average number of communication rounds')
    plt.show()
    """

