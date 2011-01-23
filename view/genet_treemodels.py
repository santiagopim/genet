#!/usr/bin/env python
################################################################################
# $Id: genet_treemodels.py,v 1.4 2010/02/01 23:58:42 santiagopm Exp $
################################################################################
# Copyright (c) 2008, 2009, 2010 Santiago Paya Miralta <santiagopm::wanadoo.es>
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

import gtk
import gobject

from control import genet_browser

################################################################################
# Browse nodes tree
#
class BrowseNodesTreeModel(gtk.TreeStore):
    """Tree model to browse network nodes.

    The tree presents the nodes to see heritage. 

    |> level id, level name, ""
    |  > node type id, node type name, "Node"
    |    > node id, node id, node att
    """
    def __init__(self):
        gtk.TreeStore.__init__(self,
                               gobject.TYPE_STRING, 
                               gobject.TYPE_STRING,
                               gobject.TYPE_STRING)
        self.load()
    
    def load(self):
        list_levels = genet_browser.listLevels()
    
        for i in list_levels:
            iter_level = self.append(None)
            self.set(iter_level, 0, i[0], 1, i[1], 2, "")
        
            # Fill children with this level nodetypes
            list_node_types = genet_browser.listNodeTypes(i[0])
            for j in list_node_types:
                iter_node_type = self.append(iter_level)
                self.set(iter_node_type, 0, j[0], 1, j[1], 2, "Node")
            
                # Fill children with this level & type nodes
                list_nodes = genet_browser.listNodesAtt(i[0], j[0])
                for k in list_nodes:
                    iter_node = self.append(iter_node_type)
                    self.set(iter_node, 0, k[0], 1, k[0], 2, k[1])

    def reload(self):
        self.clear()
        self.load()

################################################################################
# Connect nodes tree
#
class ConnectNodesTreeModel(gtk.TreeStore):
    """Tree model to select node for connect each others.

    The tree presents the nodes to select the connect one.

    |> level id, level name, ""
    |  > node type id, node type name, "Node"
    |    > node id, node id, node att
    """
    def __init__(self):
        gtk.TreeStore.__init__(self,
                               gobject.TYPE_STRING, 
                               gobject.TYPE_STRING,
                               gobject.TYPE_STRING)
        self.load()
    
    def load(self):
        list_levels = genet_browser.listLevels()
    
        for i in list_levels:
            iter_level = self.append(None)
            self.set(iter_level, 0, i[0], 1, i[1], 2, "")
        
            # Fill children with this level nodetypes
            list_node_types = genet_browser.listNodeTypes(i[0])
            for j in list_node_types:
                iter_node_type = self.append(iter_level)
                self.set(iter_node_type, 0, j[0], 1, j[1], 2, "Node")
            
                # Fill children with this level & type nodes
                list_nodes = genet_browser.listNodesAtt(i[0], j[0])
                for k in list_nodes:
                    iter_node = self.append(iter_node_type)
                    self.set(iter_node, 0, k[0], 1, k[0], 2, k[1])

    def reload(self):
        self.clear()
        self.load()

################################################################################
# Connect nodes edge types tree
#
class ConnectNodesEdgeTypesTreeModel(gtk.TreeStore):
    """Tree model to select edge type for connect nodes.

    The tree presents the edge types that may be used to connect nodes.

    |> level id, level name, ""
    |  > edge type id, edge type name, ""
    """
    def __init__(self):
        gtk.TreeStore.__init__(self,
                               gobject.TYPE_STRING, 
                               gobject.TYPE_STRING,
                               gobject.TYPE_STRING)
        self.load()
    
    def load(self, level=None):
        list_levels = genet_browser.listLevels(level)
    
        for i in list_levels:
            iter_level = self.append(None)
            self.set(iter_level, 0, i[0], 1, i[1], 2, "")
        
            # Fill children with this level edgetypes
            list_edge_types = genet_browser.listEdgeTypes(i[0])
            for j in list_edge_types:
                iter_edge_type = self.append(iter_level)
                self.set(iter_edge_type, 0, j[0], 1, j[1], 2, "")
            
    def reload(self, level=None):
        self.clear()
        self.load(level)

################################################################################
# Create node types tree
#
class CreateNodeTypesTreeModel(gtk.TreeStore):
    """Tree model to select type in nodes creation.

    The tree presents the node types to select the desired type to create, then
    another tree presents all nodes in levels which can be parent.

    |> level id, level name, ""
    |  > node type id, node type name, "Node"
    """
    def __init__(self):
        gtk.TreeStore.__init__(self,
                               gobject.TYPE_STRING, 
                               gobject.TYPE_STRING,
                               gobject.TYPE_STRING)
        self.load()
    
    def load(self):
        list_levels = genet_browser.listLevels()
    
        for i in list_levels:
            iter_level = self.append(None)
            self.set(iter_level, 0, i[0], 1, i[1], 2, "")
        
            # Fill children with this level nodetypes
            list_node_types = genet_browser.listNodeTypes(i[0])
            for j in list_node_types:
                iter_node_type = self.append(iter_level)
                self.set(iter_node_type, 0, j[0], 1, j[1], 2, "Node")
            
    def reload(self):
        self.clear()
        self.load()

################################################################################
# Create node parents tree
#
class CreateNodeParentsTreeModel(gtk.TreeStore):
    """Tree model to select node parent in nodes creation.

    The tree presents the nodes to select the desired parent to the
    creating node.

    |> level id, level name, ""
    |  > node type id, node type name, "Node"
    |    > node id, node att, ""
    """
    def __init__(self):
        gtk.TreeStore.__init__(self,
                               gobject.TYPE_STRING, 
                               gobject.TYPE_STRING,
                               gobject.TYPE_STRING)
        self.load()
    
    def load(self):
        list_levels = genet_browser.listLevels()
    
        for i in list_levels:
            iter_level = self.append(None)
            self.set(iter_level, 0, i[0], 1, i[1], 2, "")
        
            # Fill children with this level nodetypes
            list_node_types = genet_browser.listNodeTypes(i[0])
            for j in list_node_types:
                iter_node_type = self.append(iter_level)
                self.set(iter_node_type, 0, j[0], 1, j[1], 2, "Node")
            
                # Fill children with this level & type nodes
                list_nodes = genet_browser.listNodesId(i[0], j[0])
                for k in list_nodes:
                    iter_node = self.append(iter_node_type)
                    self.set(iter_node, 0, k[0], 1, k[1], 2, "")

    def reload(self):
        self.clear()
        self.load()

################################################################################
# Admin tree
#
class AdminTreeModel(gtk.TreeStore):
    """Tree model to select and admin levels, node types or edge types.

    The tree presents levels and types. Can select any item to delete or add
    stuff.

    |> level id, level name, ""
    |  > node type id, node type name, "Node"
    |  > edge type id, edge type name, "Edge"
    """
    def __init__(self):
        gtk.TreeStore.__init__(self,
                               gobject.TYPE_STRING, 
                               gobject.TYPE_STRING,
                               gobject.TYPE_STRING)
        self.load()
    
    def load(self):
        list_levels = genet_browser.listLevels()
    
        for i in list_levels:
            iter_level = self.append(None)
            self.set(iter_level, 0, i[0], 1, i[1], 2, "")
        
            # Fill children with this level nodetypes and edgetypes
            list_node_types = genet_browser.listNodeTypes(i[0])
            for j in list_node_types:
                iter_node_type = self.append(iter_level)
                self.set(iter_node_type, 0, j[0], 1, j[1], 2, "Node")
            
            list_edge_types = genet_browser.listEdgeTypes(i[0])
            for k in list_edge_types:
                iter_edge_type = self.append(iter_level)
                self.set(iter_edge_type, 0, k[0], 1, k[1], 2, "Edge")

    def reload(self):
        self.clear()
        self.load()

