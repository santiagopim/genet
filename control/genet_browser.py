#!/usr/bin/env python
################################################################################
# $Id: genet_browser.py,v 1.11 2010/02/01 23:58:42 santiagopm Exp $
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
"""
Related to paths and interlevel chains.

Should use the 'networkx' module, getting graph from db and working with it.
"""
from control import genet_global 
from model.db_connection import db

def listLevels(level=None):
    """List levels from db.

    If level is passed returns from that level only, all are returned if not.

    @param level from which gets information
    @returns list the levels
    """
    st = "SELECT id, description FROM gn____levels;"
    if level is not None:
        st = st[:-1] + " WHERE id = " + str(level) + ";"
    return db.query(st).getresult()

def listNodeTypes(level=None):
    """List node types from db.

    If level is passed returns from that level only, all are returned if not.

    @param level from which the node types are
    @returns list the node types
    """
    st = "SELECT id, description FROM gn____node_types;"
    if level is not None:
        st = st[:-1] + " WHERE level = " + str(level) + ";"
    return db.query(st).getresult()

def listEdgeTypes(level=None):
    """List edge types from db.

    If level is passed returns from that level only, all are returned if not.
    
    @param level from which the edge types are
    @returns list the node types
    """
    st = "SELECT id, description FROM gn____edge_types;"
    if level is not None:
        st = st[:-1] + " WHERE level = " + str(level) + ";"
    return db.query(st).getresult()

def listNodesId(level=None, node_type=None):
    """List nodes from db.

    If level is passed returns from that level only, if node type 
    is passed returns of that type only. If not all are returned.

    @param level from which the nodes are
    @param node_type
    @returns list the nodes
    """
    list_nodes = []

    if level is None:
        st = "SELECT id FROM gn____levels;"
        list_levels = db.query(st).getresult()
        for i in list_levels:
            tag_level = genet_global.tagName(i[0])
            st = "SELECT id, idtype FROM gn_" + tag_level + "_nodes;"
            if node_type is not None:
                st = st[:-1] + " WHERE idtype = " + str(node_type) + ";"
            list_nodes += db.query(st).getresult()
    else:
        tag_level = genet_global.tagName(level)
        st = "SELECT id, idtype FROM gn_" + tag_level + "_nodes;"
        if node_type is not None:
            st = st[:-1] + " WHERE idtype = " + str(node_type) + ";"
        list_nodes = db.query(st).getresult()

    return list_nodes

def listNodesAtt(level, node_type):
    """List node attributes from db.

    Returns data from all nodes from level and type passed.

    @param level from which the nodes are
    @param node_type
    @returns list the nodes
    """
    list_nodes = []

    tag_level = genet_global.tagName(level)
    tag_type = genet_global.tagName(node_type)

    st = ("SELECT * "
          "FROM gn_" + tag_level + "_nodes_type_" + tag_type + ";")
    list_nodes = db.query(st).getresult()

    return list_nodes
