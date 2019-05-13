#!/usr/bin/env python
# import wx
# # an observable calls callback functions when the data has changed
# #o = Observable()
# #def func(data):
# # print "hello", data
# #o.addCallback(func)
# #o.set(1)
# # --| "hello", 1
# class Observable:
#     def __init__(self, initialValue=None):
#         self.data = initialValue
#         self.callbacks = {}
#
#     def addCallback(self, func):
#         self.callbacks[func] = 1
#
#     def delCallback(self, func):
#         del self.callback[func]
#
#     def _docallbacks(self):
#         for func in self.callbacks:
#             func(self.data)
#
#     def set(self, data):
#         self.data = data
#         self._docallbacks()
#
#     def get(self):
#         return self.data
#
#     def unset(self):
#         self.data = None
#
# class Model:
#     def __init__(self):
#         self.myMoney = Observable(0)
#
#     def addMoney(self, value):
#         self.myMoney.set(self.myMoney.get() + value)
#
#     def removeMoney(self, value):
#         self.myMoney.set(self.myMoney.get() - value)
#
#
# class View(wx.Frame):
#     def __init__(self, parent):
#         wx.Frame.__init__(self, parent, title="Main View")
#         sizer = wx.BoxSizer(wx.VERTICAL)
#         text = wx.StaticText(self, label="My Money")
#         ctrl = wx.TextCtrl(self)
#         sizer.Add(text, 0, wx.EXPAND | wx.ALL)
#         sizer.Add(ctrl, 0, wx.EXPAND | wx.ALL)
#         ctrl.SetEditable(False)
#         self.SetSizer(sizer)
#         self.moneyCtrl = ctrl
#
#     def SetMoney(self, money):
#         self.moneyCtrl.SetValue(str(money))
#
#
# class ChangerWidget(wx.Frame):
#     def __init__(self, parent):
#         wx.Frame.__init__(self, parent, title="Main View")
#         sizer = wx.BoxSizer(wx.VERTICAL)
#         self.add = wx.Button(self, label="Add Money")
#         self.remove = wx.Button(self, label="Remove Money")
#         sizer.Add(self.add, 0, wx.EXPAND | wx.ALL)
#         sizer.Add(self.remove, 0, wx.EXPAND | wx.ALL)
#         self.SetSizer(sizer)
#
# class Controller:
#     def __init__(self, app):
#         self.model = Model()
#         self.view1 = View(None)
#         self.view2 = ChangerWidget(self.view1)
#         self.MoneyChanged(self.model.myMoney.get())
#         self.view2.add.Bind(wx.EVT_BUTTON, self.AddMoney)
#         self.view2.remove.Bind(wx.EVT_BUTTON, self.RemoveMoney)
#         self.model.myMoney.addCallback(self.MoneyChanged)
#         self.view1.Show()
#         self.view2.Show()
#
#     def AddMoney(self, evt):
#         self.model.addMoney(10)
#
#     def RemoveMoney(self, evt):
#         self.model.removeMoney(10)
#
#     def MoneyChanged(self, money):
#         self.view1.SetMoney(money)
#
# app = wx.App(False)
# controller = Controller(app)
# app.MainLoop()

# def generate_all_points(points, size):
#     from itertools import combinations
#
#     all_combinations = combinations(points, size)
#     return (list(all_combinations))
#
# def generate_4points(points):
#
#     all_4points = generate_all_points(points, 4)
#     print (len(all_4points))
#     print ("ALL POINTS -\t", points)
#     for item in all_4points:
#         print(item)
#     for point_set in all_4points:
#
#         to_remove = list(set(points).difference(set(point_set)))
#         for item in all_4points:
#             if (len(set(to_remove).difference(item)) == 0):
#                 all_4points.remove(item)
#
#         print ("Main -\t", point_set, "\nTo Remove -\t", to_remove)
#         #all_4points.remove(list(set(points).difference(set(point_set))))
#     print (len(all_4points))
#
# points = [(1, 2), (4, 5), (223, 456), (111, 345), (123, 4), (23, 89), (999, 888), (895, 569)]
# generate_4points(points)

#

# import numpy as np
# from numpy import array
#
# a = array([[11, 12, 13], [21, 22, 23], [31, 32, 33]])
# print('\na =',a.shape, '\n', a)
#
# b = array([0, 1, 2])
# print('\nb =',b.shape, '\n', b)
#
#
# try:
#     c = a[range(2), b]
#     print('\nc =',c.shape, '\n', c)
# except IndexError:
#     print('2 too small')
# try:
#     c = a[range(4), b]
#     print('\nc =',c.shape, '\n', c)
# except IndexError:
#     print('4 too big')
# try:
#     d = array([0, 1, 2, 3])
#     c = a[range(2), d]
#     print('\nc =',c.shape, '\n', c)
# except IndexError:
#     print('4 too big')
# try:
#     d = array([0, 1])
#     c = a[range(4), d]
#     print('\nc =',c.shape, '\n', c)
# except IndexError:
#     print('2 too small')
#
# print('\n3 is the correct number')
# c = a[range(3), b]
# print('\nc =',c.shape, '\n', c)
#

# c = a + b
# print(c.shape)
# print(c)
# print()

# c = a * b
# print(c.shape)
# print(c)
# print()

# print([range(2),b])
# c = a[range(2),b]
# print([range(2),b])
# c = a[b,range(3)]

# n = 100
# j = 0 # must be >= 0
# i = 0 # must be >= 0
# Z = np.random.random((n + i,n + j))
# y = np.arange(n)
# print(Z[:2,:2])
# print(Z[range(2),:2])
# print(Z.shape)
# print(y.shape)
# Z[range(n), y]
# #from numpy import array
#

# Z = np.random.random((7,6))
# y = np.arange(6)
# print(Z.shape)
# print(y.shape)
# #Z[range(10),y]
# print(Z[range(6),y])

#Z[range(500), y]
# import itertools
# from multiprocessing import Pool
# import os
#
# def combinations(inputs):
#     combi = list(itertools.combinations(inputs, 5))
#     pool = Pool(len(combi))
#     outputs = pool.map(evaluate, combi)
#     return outputs
#
#
# def evaluate(input):
#     return ['processed by {0}'.format(os.getpid()), input]
#
#
# a = [[2,2],[4,3],[5,1],[6,3],[7,2],[12,4],[12,2]]
# b = combinations(a)
# for i in b:
#     print(i)


# import multiprocessing
# import os
# import itertools
#
#
# def evaluate(input):
#     t = os.getpid()
#     return [input, t]
#
# def combinations(inputs):
#     pool = multiprocessing.Pool(21)
#     combi = list(itertools.combinations(inputs, 5))
#     outputs=pool.map(evaluate, combi) #[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21])
#     return outputs
#
# a = [[2,2],[4,3],[5,1],[6,3],[7,2],[12,4],[12,2]]
# a = [1,2,3,4,5,6,7]
#
# if __name__ == '__main__':
#     b = combinations(a)
#     for i in b: print(i)

# import time
# import sys
# from multiprocessing import Process
# import multiprocessing
# import itertools
#
#
# def combinations(inputs):
#     pool = multiprocessing.Pool()
#     # combi = list(itertools.combinations(inputs, 5))
#     combi = [1, 2 , 3, 4, 5, 6, 7]
#     outputs = pool.map(evaluate, combi)
#     return outputs
#
#
# numb = 0
#
#
# def evaluate(input):
#     global numb
#     print('+', input, numb)
#     time.sleep(float(input) / 10.)
#     numb += 1
#     n = numb
#     print('*', input, n)
#     time.sleep(float(input) / 10.)
#     print('-', input, n)
#     return [input, n]
#
# # a = [1, 2 , 3, 4, 5, 6]
# a = [1, 2 , 3, 4, 5, 6, 7]
# a = [['a'],['b'],['c'],['d'],['e'],['f'],['g']]
# #a = [[2,2],[4,3],[5,1],[6,3],[7,2],[12,4],[12,2]]
# b = combinations(a)
# for i in b:
#   print(i)