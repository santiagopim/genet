#!/usr/bin/env python
################################################################################
# $Id: test_networkx.py,v 1.4 2010/01/07 23:48:48 santiagopm Exp $
################################################################################
# Copyright (c) 2008 Santiago Paya Miralta <santiagopm::wanadoo.es>
#
# This file is part of mine.
#
# Mine is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
################################################################################

import pylab as P
import networkx as NX
from model.db_connection import db

################################################################################
# Level 01
#
G01 = NX.MultiGraph(name='Level 01')

for r in db.query("SELECT * FROM gn_01_edges").dictresult():
    G01.add_edges_from([(r['idna'], r['idnb'], r['id'])])
    
# May be there are isolated nodes.
for r in db.query("SELECT * FROM gn_01_nodes").dictresult():
    G01.add_node(r['id'])

print 'G01 nodes:', G01.nodes()
print 'G01 edges:', G01.edges()

pos = NX.spring_layout(G01)
NX.draw_networkx(G01, pos)
P.show()

P.savefig("genet_L1.png")
print "Wrote genet_L1.png"

#################################################################################
## Level 1
##
#G101 = NX.MultiGraph(name='Infrastructure')
#
#for e in genet.EL01:
#    print e.idnA.id, e.idnB.id, e.id
#    G101.add_edge(e.idnA.id, e.idnB.id, e.id)
#
## May be there are isolated nodes.
#for n in genet.NL01:
#    print n.id
#    G101.add_node(n.id)
#
#print 'G101 nodes:', G101.nodes()
#print 'G101 edges:', G101.edges()
#
#pos = NX.spring_layout(G101)
#NX.draw_networkx(G101, pos)
#P.show()
#
#P.savefig("genet_L101.png")
#print "Wrote genet_L101.png"
#
#################################################################################
## Fancy draw & DOT
##
#G102 = NX.MultiGraph(name='Infrastructure')
#
#for e in genet.EL01:
#    print e.idnA.id, e.idnB.id, e.id
#    G102.add_edges_from([(e.idnA.id, e.idnB.id, e)])
#
## May be there are isolated nodes.
#for n in genet.NL01:
#    print n.id
#    G102.add_node(n.id)
#
#pos = NX.spring_layout(G102)
#NX.draw_networkx_nodes(G102, pos, node_color='g', node_size=500)
#NX.draw_networkx_edges(G102, pos, width=8.0, alpha=0.5, edge_color='g')
#labels={}
#labels[G102.nodes()[0]]='$\pi$'
#labels[G102.nodes()[1]]='$\mu$'
#labels[G102.nodes()[2]]='$\epsilon$'
#NX.draw_networkx_labels(G102, pos, labels=labels, 
#                        font_color='w', font_family='sans-serif', 
#                        font_size=12)
#P.show()
#
#P.savefig("genet_L102.png")
#print "Wrote genet_L102.png"
#
#"""
#With the dot file can do in the system:
#$ neato -Tpng file.dot > file.png
#$ eog file.png
#"""
#NX.write_dot(G102,"genet_L102.dot")
#print "Wrote genet_L102.dot"
#
#################################################################################
## Paths
##
#"""
#The Dijkstra algorithms seems not to support multiedge graphs, because
#the NX._Graph.get_edge() function returns a list.
#
#Line 438 in /var/lib/python-support/python2.5/networkx/path.py, function
#single_source_dijkstra(G,source,target), should be:
#
#...
#if G.multiedges:
#    vw_dist = dist[v] + reduce(min, G.get_edge(v,w))
#else:
#    vw_dist = dist[v] + G.get_edge(v,w)
#...
#
#or may be defining an appropiate function get_edge(v, w) depending on
#the multiedges property before the loooop. 
#
#Example:
#
#>>> l = [0.23, 7, 0.1]
#>>> print reduce(min, l)
#0.1
#
#"""
#G103 = NX.MultiGraph(name='Infrastructure')
#
#for e in genet.EL01:
#    # When creating the graph with edges (dont worry about isolated nodes)
#    # the information passed is the edges' weight. 
#    print e.idnA.id, e.idnB.id, e.id
#    G103.add_edge(e.idnA.id, e.idnB.id, e.iddown.len)

paths = NX.single_source_shortest_path_length(G01, G01.nodes()[0], 1000)
print paths

paths = NX.single_source_shortest_path(G01, G01.nodes()[0], 1000)
print paths

path = NX.shortest_path(G01, 
                        G01.nodes()[0], 
                        G01.nodes()[NX.number_of_nodes(G01)-1])
print path

paths = NX.single_source_dijkstra_path_length(G01, G01.nodes()[0])
print paths
print 'The', G01.edges()[0], 'weight is:', G01.edges()[0][2]

paths = NX.single_source_dijkstra_path(G01, G01.nodes()[0])
print paths

