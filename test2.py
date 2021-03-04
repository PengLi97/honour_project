from CardType import *
import copy
import numpy as np
# t = []
# p = np.array([1,2])
# Q = np.array([1,2,3])
# print(np.vstack([p,Q]))
# p = np.vstack([p,[3,3]])
# t = np.vstack([p,[4,3]])
# v = np.vstack([t,t])
# print(v)
# print("---",v[0][0])
# a = np.array([1,2,3,4,5,6])
# a = np.reshape(a,(len(a),1))
# print(a)
# t = np.hstack((v, a))
# t = t[t[:, 1].argsort()]
# print(t)
# print(t[-1][2])
# print(type([]))
pre_single = [CardType(3, 'club', 'image/' + 'club' + '3' + '.jpg')]
a = CardType(2, 'dimond', '-')

print(type(a),type(pre_single[0]))
# test = np.load('DNAlandlord.npy')
# print(test)
# a = np.array([[0, 1, 2],
#               [0, 2, 4],
#               [0, 3, 6]])
# print(a)
# print(np.where(a < 4, a, -1))  # -1 is broadcast
