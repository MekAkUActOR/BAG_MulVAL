#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 14:53:49 2020

@author: hongxing
"""

import sys
from xml.dom.minidom import parse
from graphviz import Digraph
import xlrd
from itertools import combinations,permutations


# 图的节点结构
class Node:
    def __init__(self, ID, fact, metric, TYPE):
        self.id = ID
        self.fact = fact
        self.metric = metric
        self.type = TYPE
        self.cve = ''
        self.prior = []
        self.next = []
        self.priarc = []
        self.nexarc = []
        self.D = 0
        self.rate = 0.9
        self.flag = 0
        self.tempnext = []

    def CVSS(self, AV, AC, AU):
        self.rate = AV * AC * AU
        self.D = 1 / self.rate


# 边结构
class Edge:
    def __init__(self, src, dst):
        self.src = src
        self.dst = dst
        self.rate = 1
        self.fact = ''
        self.subg = 0


# 图结构
class Graph:
    def __init__(self):
        self.nodgrp = []  # 图的所有节点集合
        self.arcgrp = []  # 图的边集合
        self.attacker = []  # 攻击起点集合
        self.aim = []  # 攻击目标集合
        self.rate = 1  # 攻击路径相对概率

    def dcopy(self, graph):
        self.nodgrp = graph.nodgrp.copy()
        self.arcgrp = graph.arcgrp.copy()
        self.attacker = graph.attacker.copy()
        self.aim = graph.aim.copy()
        self.rate = graph.rate


class Stack:
    '''栈'''

    # 构造一个栈的容器
    def __init__(self):
        self.__list = []

    def PUSH(self, item):
        '''添加一个新的元素到栈顶'''
        self.__list.append(item)

    def POP(self):
        '''弹出栈顶元素'''
        return self.__list.pop()

    def peek(self):
        '''返回栈顶元素'''
        if self.__list:
            return self.__list[-1]
        return None

    def isnot_empty(self):
        '''判断栈是否为空'''
        return self.__list != []

    def size(self):
        '''返回栈的的元素个数'''
        return len(self.__list)

    def clr(self):
        '''清空栈'''
        return self.__list.clear()

    def copy(self):
        '''返回栈体'''
        return self.__list.copy()

    def dcopy(self, l):
        '''直接拷贝一个list为栈体'''
        self.__list = l.copy()

    def remove(self, nod):
        '''去除栈体中某个节点'''
        while nod in self.__list:
            self.__list.remove(nod)


def readXML(path):
    '''读取XML文件生成有向图'''
    domTree = parse(path)
    rootNode = domTree.documentElement
    print(rootNode.nodeName)

    arcs = rootNode.getElementsByTagName("arcs")
    vertices = rootNode.getElementsByTagName("vertices")

    arclist = arcs[0].getElementsByTagName("arc")
    vertexlist = vertices[0].getElementsByTagName("vertex")

    graph = Graph()

    for vertex in vertexlist:
        ID = vertex.getElementsByTagName("id")[0].childNodes[0].data
        fact = vertex.getElementsByTagName("fact")[0].childNodes[0].data
        metric = vertex.getElementsByTagName("metric")[0].childNodes[0].data
        TYPE = vertex.getElementsByTagName("type")[0].childNodes[0].data
        nod = Node(ID, fact, metric, TYPE)
        graph.nodgrp.append(nod)

    for arc in arclist:
        dst = arc.getElementsByTagName("src")[0].childNodes[0].data
        src = arc.getElementsByTagName("dst")[0].childNodes[0].data
        ar = Edge(src, dst)
        graph.arcgrp.append(ar)

    return graph


def DigraphAnalysis(graph, aim):
    '''解析图，将图的边与节点关联，节点相互关联并分类'''
    for nod in graph.nodgrp:
        for arc in graph.arcgrp:
            if arc.src == nod.id:
                for node in graph.nodgrp:
                    if node.id == arc.dst:
                        nod.next.append(node)
                nod.nexarc.append(arc)
            elif arc.dst == nod.id:
                for node in graph.nodgrp:
                    if node.id == arc.src:
                        nod.prior.append(node)
                nod.priarc.append(arc)
                arc.subg = nod.id
                if nod.type == 'AND':
                    arc.fact = 'and'
                elif nod.type == 'OR':
                    arc.fact = 'or'

    for nod in graph.nodgrp:
        if nod.type == 'LEAF':
            if nod.fact.find('vulExists') != -1:
                fact = nod.fact
                fact = fact.split(',')
                if fact[1] == 'vulID':
                    nod.cve = fact[1]
                else:
                    cve = fact[1].split('\'')
                    nod.cve = cve[1]
            elif nod.fact.find('attacker') != -1:
                graph.attacker.append(nod)
        elif aim == '_':
            if nod.type == 'OR':
                graph.aim.append(nod)
        elif aim != '':
            if nod.fact.find(aim) != -1:
                if nod.type == 'OR':
                    graph.aim.append(nod)

    tempGnodgrp = graph.nodgrp.copy()
    tempGattacker = graph.attacker.copy()
    for nod in tempGnodgrp:
        if nod.type == 'LEAF':
            tempid = 1
            while len(nod.next) > 1:
                node = Node(str(tempid) + '|' + nod.id, nod.fact, nod.metric, nod.type)
                tempnext = nod.next.pop()
                node.next.append(tempnext)
                tempNnexarc = nod.nexarc.copy()
                for arc in tempNnexarc:
                    if arc.dst == tempnext.id:
                        nod.nexarc.remove(arc)
                        arc.src = str(tempid) + '|' + nod.id
                        node.nexarc.append(arc)
                tempnext.prior.remove(nod)
                tempnext.prior.append(node)
                graph.nodgrp.append(node)
                if nod in tempGattacker:
                    graph.attacker.append(node)
                tempid = tempid + 1


def CVSSCal(cveid):
    '''根据CVE查询AV、AC、AU'''
    file = './mulvala2b/src/cveid.xls'
    data = xlrd.open_workbook(file)
    table = data.sheets()[0]
    cve = table.col_values(0)
    av = table.col_values(2)
    ac = table.col_values(3)
    au = table.col_values(4)

    try:
        result = cve.index(cveid)
    except:
        print('Unknown vulnerability.', cveid)
        return 1.0, 0.71, 0.704
    else:
        if av[result] == 'N':
            AV = 1.0
        elif av[result] == 'A':
            AV = 0.646
        else:
            AV = 0.359
        if ac[result] == 'L':
            AC = 0.71
        elif ac[result] == 'M':
            AC = 0.61
        else:
            AC = 0.35
        if au[result] == 'N':
            AU = 0.704
        elif au[result] == 'S':
            AU = 0.56
        else:
            AU = 0.45
        return AV, AC, AU


def elimAND(graph, nod):
    '''删除一个AND节点'''
    tempnods = nod.next.copy()
    temp = nod.next.copy()
    for node in temp:
        node.prior.remove(nod)
        nod.next.remove(node)
    temp = nod.prior.copy()
    for node in temp:
        if node.type == 'LEAF':
            graph.nodgrp.remove(node)
            node.next.remove(nod)
            nod.prior.remove(node)
        else:
            node.next.remove(nod)
            nod.prior.remove(node)

    for arc in (nod.priarc + nod.nexarc):
        graph.arcgrp.remove(arc)
    graph.nodgrp.remove(nod)

    for temp in tempnods:
        if temp.prior:
            pass
        else:
            graph = elimOR(graph, temp)

    return graph


def elimFollOR(graph, nod):
    '''删除一个OR节点的所有子节点'''
    temp = nod.next.copy()
    for node in temp:
        graph = elimAND(graph, node)

    return graph


def elimOR(graph, nod):
    '''删除一个OR节点'''
    graph = elimFollOR(graph, nod)
    graph.nodgrp.remove(nod)

    return graph


def Dye(nod):
    '''标记一个AND区域'''
    for nd in nod.prior:
        nd.flag = 1


def seekCir(stack):
    '''在一个list中寻找一个环路'''
    cir = []
    exist = 0
    temp = Stack()
    temp.dcopy(stack)
    flag = temp.peek()
    if flag.type == 'AND':
        cir.append(flag)
    temp.POP()
    while temp.isnot_empty():
        check = temp.peek()
        if check.type == 'AND':
            cir.append(check)
        temp.POP()
        if check == flag:
            exist = 1
            break

    return cir, exist


def cutCir(graph, cir):
    '''通过去除攻击难度最大的AND节点来消除含圈路径'''
    tempMax = cir[0]
    graph = elimAND(graph, tempMax)

    return graph


def DFScut(graph, leaf):
    '''深度优先搜索所有可能路径并消除含圈路径'''
    stack = Stack()
    stack.PUSH(leaf)
    while stack.isnot_empty():
        if stack.peek().tempnext:
            temp = stack.peek().tempnext[-1]
            stack.peek().tempnext.pop()
            if temp.type == 'AND':
                Dye(temp)
            stack.PUSH(temp)
            cir, exist = seekCir(stack)
            if exist:
                graph = cutCir(graph, cir)
                for node in stack.copy():
                    if node not in graph.nodgrp:
                        stack.remove(node)
        else:
            stack.POP()

    return graph


def elimCir(graph, aim):
    '''消除含圈路径'''
    temp = graph.nodgrp.copy()
    if aim == '_':
        pass
    else:
        for nod in temp:
            if nod.fact == aim:
                graph = elimFollOR(graph, nod)

    for nod in graph.nodgrp:
        if nod.type == 'LEAF':
            if nod.cve:
                AV, AC, AU = CVSSCal(nod.cve)
                nod.CVSS(AV, AC, AU)
        if nod.type == 'AND':
            nod.rate = 1

    for node in graph.nodgrp:
        node.tempnext = node.next.copy()
    temp = graph.attacker.copy()
    for node in temp:
        for nod in node.next:
            Dye(nod)
        graph = DFScut(graph, node)
    temp = graph.nodgrp.copy()
    for node in temp:
        if (node.type == 'LEAF') & (node.flag == 0):
            for nod in node.next:
                Dye(nod)
            graph = DFScut(graph, node)

    return graph


def InitExceptStack(graph, stack):
    '''初始化已标记主路径外的所有节点标记'''
    for nod in graph.nodgrp:
        if nod not in stack.copy():
            nod.flag = 0
            nod.tempnext = nod.next.copy()


# 先找到一条主线，再将路上所有节点的祖先节点全部包含进来
def eatAcient(graph, subgraph, node):
    '''将路上所有节点的祖先节点全部包含进来'''
    if node.prior:
        for nod in node.prior:
            if nod.flag == 0:
                if nod.type == 'LEAF':
                    subgraph.nodgrp.append(nod)
                    nod.flag = 1
                else:
                    subsubgraphs = []
                    for attacker in graph.attacker:
                        graph_copy = Graph()
                        graph_copy.dcopy(graph)
                        subsubgraphs = subsubgraphs + TargetedDFS(graph_copy, attacker, nod)
                    for fragment in subsubgraphs:
                        for nd in fragment:
                            subgraph.nodgrp.append(nd)


def TargetedDFS(graph, attacker, terminal):
    '''深度优先搜索找到所有攻击路径'''
    stack = Stack()
    InitExceptStack(graph, stack)
    stack.PUSH(attacker)
    attacker.flag = 1
    subgraphlist = []
    while stack.isnot_empty():
        if stack.peek().tempnext:
            temp = stack.peek().tempnext[-1]
            stack.peek().tempnext.pop()
            temp.flag = 1
            stack.PUSH(temp)
        else:
            temp = stack.peek()
            if temp.type == 'OR':
                if temp == terminal:
                    subgraph = Graph()
                    subgraph.aim.append(temp)
                    subgraph.attacker.append(attacker)
                    subgraph.nodgrp = stack.copy()
                    temp = subgraph.nodgrp.copy()
                    for nod in temp:
                        if nod.type == 'AND':
                            eatAcient(graph, subgraph, nod)
                    subgraph.nodgrp = list(set(subgraph.nodgrp))
                    subgraphlist.append(subgraph)
            stack.POP()
            InitExceptStack(graph, stack)

    return subgraphlist


def OrBayesian(node, parents, subgraph):
    rates = []
    for nod in parents:
        rates.append(RateCal(nod, subgraph))
    rate = 0
    i = 0
    a = []
    while i < len(rates):
        a.append(i)
        i = i + 1
    i = 0
    while i < len(rates):
        rates_temp = []
        for b in combinations(a, i):
            for j in b:
                rates_temp.append(1 - rates[j])
            for j in a:
                if j not in b:
                    rates_temp.append(rates[j])
            rate_temp = 1
            for rat in rates_temp:
                rate_temp = rate_temp * rat
            rate = rate + rate_temp
        i = i + 1
    rate = rate * node.rate
    return rate

def AndBayesian(node, parents, subgraph):
    rate = node.rate
    for nod in parents:
        rate = rate * RateCal(nod, subgraph)
    return rate


def RateCal(node, subgraph):
    '''递归计算攻击路径相对概率'''
    if node.type == 'LEAF':
        return node.rate
    elif node.type == 'OR':
        parents = []
        for nod in node.prior:
            if nod in subgraph.nodgrp:
                parents.append(nod)
        rate = OrBayesian(node, parents, subgraph)
        return rate
    else:
        rate = AndBayesian(node, node.prior, subgraph)
        return rate


def BayesianAnalysis(graph):
    '''得到所有攻击路径及其相对概率'''
    attack_pathlist = []
    for nod in graph.aim:
        for attacker in graph.attacker:
            attack_pathlist.append(TargetedDFS(graph, attacker, nod))

    for sublist in attack_pathlist:
        for sub in sublist:
            for nod in sub.nodgrp:
                for arc in nod.priarc:
                    for node in sub.nodgrp:
                        if node.id == arc.src:
                            sub.arcgrp.append(arc)

    for sublist in attack_pathlist:
        for subgraph in sublist:
            for nod in subgraph.aim:
                subgraph.rate = RateCal(nod, subgraph)

    return attack_pathlist


def dotGener(graph):
    dot = Digraph(comment='This is a attack_graph.', name="Bayesian Attack Graph")
    dot.node("Bayesian Attack Graph", "Bayesian Attack Graph", shape='tripleoctagon', color='blue')
    for nod in graph.nodgrp:
        if nod.type == 'LEAF':
            dot.node(nod.id, nod.id + ":" + nod.fact + ":" + nod.metric, shape='box')
        elif nod.type == 'OR':
            dot.node(nod.id, nod.id + ":" + nod.fact + ":" + nod.metric, shape='diamond')
        elif nod.type == 'AND':
            dot.node(nod.id, nod.id + ":" + nod.fact + ":" + nod.metric, shape='ellipse')
    for arc in graph.arcgrp:
        dot.edge(arc.src, arc.dst, label=arc.fact + ':' + arc.subg)

    return dot


def seekMpath(sublist):
    '''找到相对攻击概率最大的攻击路径'''
    temp = sublist.copy()
    tempMax = temp[-1]
    temp.pop()
    while temp:
        fol = temp[-1]
        temp.pop()
        if tempMax.rate <= fol.rate:
            tempMax = fol

    return tempMax


def resultGener(attack_pathlist):
    dot = Digraph(comment='This is the result.', name="cluster_Attack_Paths")
    dot.attr(compound='true')
    dot.node("Attack Paths", "Bayesian Attack Paths", shape='tripleoctagon', color='blue')
    # i = 64
    i = 0
    for sublist in attack_pathlist:
        sdot = Digraph(name='cluster_Series' + ':' + str(i + 1))
        sdot.attr(compound='true')
        for subgraph in sublist:
            i = i + 1
            if subgraph.rate == seekMpath(sublist).rate:
                subdot = Digraph(graph_attr={"style": 'filled', "color": 'lightgrey'},
                                 node_attr={"style": "filled", "color": "cadetblue1"},
                                 name="cluster_rate" + ":" + str(i))
            else:
                subdot = Digraph(name='cluster_rate' + ':' + str(i))
            for nod in subgraph.nodgrp:
                if nod.type == 'LEAF':
                    subdot.node(str(i) + '|' + nod.id, nod.id + ":" + nod.fact + ":" + nod.metric, shape='box')
                elif nod.type == 'OR':
                    subdot.node(str(i) + '|' + nod.id, nod.id + ":" + nod.fact + ":" + nod.metric, shape='diamond')
                elif nod.type == 'AND':
                    subdot.node(str(i) + '|' + nod.id, nod.id + ":" + nod.fact + ":" + nod.metric, shape='ellipse')
            for arc in subgraph.arcgrp:
                subdot.edge(str(i) + '|' + arc.src, str(i) + '|' + arc.dst, label=arc.fact + ':' + arc.subg)
            subdot.node("Rate" + str(i), "Relative Rate:" + str(subgraph.rate), shape='doubleoctagon', color='magenta')
            for nod in subgraph.aim:
                subdot.edge(str(i) + '|' + nod.id, "Rate" + str(i), arrowhead='dot', style='dashed')
            sdot.subgraph(subdot)
        dot.subgraph(sdot)

    return dot


def isAimExist(graph, aim):
    flag = True
    for nod in graph.nodgrp:
        if nod.type == 'OR':
            if nod.fact.find(aim) != -1:
                flag = False
    if (aim == '') | (aim == '_'):
        flag = False

    return flag


def ObservList(attack_pathlist):
    for sublist in attack_pathlist:
        print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
        for sub in sublist:
            print('-------------------------------------------')
            for nod in sub.nodgrp:
                print(nod.id, ':', nod.fact)
            print('-------------------------')
            for arc in sub.arcgrp:
                print(arc.src, '->', arc.dst)
            print('-------------------------------------------')


def aimSel():
    aimlist = []
    path = "./mulvala2b/src/mulvalsrc/AttackGraph.xml"
    try:
        graph = readXML(path)
        for nod in graph.nodgrp:
            if nod.type == 'OR':
                aimlist.append(nod.fact)
    except:
        return aimlist
    else:
        return aimlist

def A2B(aim):
    path2 = "./mulvala2b/src/mulvalsrc/AttackGraph.xml"
    graph = readXML(path2)
    if isAimExist(graph, aim):
        print("Aim doesn't exist!")
        return 1
    DigraphAnalysis(graph, aim)
    graph = elimCir(graph, aim)
    attack_pathlist = BayesianAnalysis(graph)
    ObservList(attack_pathlist)

    dot = dotGener(graph)
    print(dot.source)
    dot.render('./mulvala2b/src/mulvalsrc/output-graph.dot')
    
    result = resultGener(attack_pathlist)
    print(result.source)
    result.render('./mulvala2b/src/mulvalsrc/result.dot')
    return 0
