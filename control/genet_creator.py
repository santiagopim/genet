#!/usr/bin/env python
################################################################################
# $Id: genet_creator.py,v 1.10 2010/02/01 23:58:42 santiagopm Exp $
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

from control import genet_global

from model import class_edge 
from model import class_node
from model import db_schema
#from model.class_edge import edge
#from model.class_node import node

from model.db_connection import db

################################################################################
# Create tables.
# 
def createLevel(description):
    """
    Create one level in the network data model. The level primary key is
    used to tag the table.

    @param description of the level.
    @returns queries statements and results.
    """
    st = ("INSERT INTO gn____levels(description) " 
        "VALUES ('" + description + "') " 
        "RETURNING id;")
    level = db.query(st).getresult()[0][0]
    tag_level = genet_global.tagName(level)
    
    # Create the layer tables.
    ret = db_schema.createLevelTables(tag_level)
    return ret

def dropLevel(level):
    """
    @param level id to delete.
    """
    # Drop the layer tables.
    tag_level = genet_global.tagName(level)
    ret = db_schema.dropLevelTables(tag_level)
    
    # Drop all type tables in the level.
    # Edges.
    st = ("SELECT id " 
        "FROM gn____edge_types " 
        "WHERE level = " + level + ";")
    ids = db.query(st).getresult()
    if len(ids):
        for i in ids:
            dropEdgeType(i[0])        

    # Nodes.
    st = ("SELECT id " 
        "FROM gn____node_types " 
        "WHERE level = " + level + ";")
    ids = db.query(st).getresult()
    if len(ids):
        for i in ids:
            dropNodeType(i[0])        

    # Delete entry into the levels table.
    st = ("DELETE FROM gn____levels " 
        "WHERE id = " + level + ";")
    ret = ret, db.query(st)
    return ret

def createEdgeType(level, description):
    """
    Create one edge type. Construct the new tablename of type with the new type.

    @param level in which the new type is added.
    @param description of the type.
    """
    st = ("INSERT INTO gn____edge_types(level, description) " 
        "VALUES (" + level + ", '" + description + "') " 
        "RETURNING ID;")
    id = db.query(st).getresult()[0][0]
    ret = st, id

    # Update tablename with the level and id.
    tag_level = genet_global.tagName(level)
    tag_id = genet_global.tagName(id)
    tablename = "gn_" + tag_level + "_edges_type_" + tag_id

    st = ("UPDATE gn____edge_types " 
        "SET tablename = '" + tablename + "' " 
        "WHERE id = " + str(id) + ";")
    ret = ret, st, db.query(st)

    # Create the table.
    ret = ret, db_schema.createEdgeTypeTable(tag_level, tablename)
    
    return ret

def dropEdgeType(edge_id):
    """
    @param edge_id the type id into the table.
    """
    st = ("SELECT tablename " 
        "FROM gn____edge_types " 
        "WHERE id = " + str(edge_id) + ";")
    tablename = db.query(st).getresult()[0][0]

    # Drop the table.
    st = "DROP TABLE IF EXISTS " + tablename + " CASCADE;"
    ret = db.query(st)

    # Delete entry into the types table.
    st = ("DELETE FROM gn____edge_types " 
        "WHERE id = " + str(edge_id) + ";")
    ret = ret, db.query(st)

    return ret
    
def createNodeType(level, description):
    """
    Create one edge type. Construct the new tablename of type with the new type.

    @param level in which the new type is added.
    @param description of the type.
    """
    st = ("INSERT INTO gn____node_types(level, description) " 
        "VALUES (" + level + ", '" + description + "') " 
        "RETURNING ID;")
    id = db.query(st).getresult()[0][0]
    ret = st, id

    # Update tablename with the level and id.
    tag_level = genet_global.tagName(level)
    tag_id = genet_global.tagName(id)
    tablename = "gn_" + tag_level + "_nodes_type_" + tag_id

    st = ("UPDATE gn____node_types " 
        "SET tablename = '" + tablename + "' " 
        "WHERE id = " + str(id) + ";")
    ret = ret, st, db.query(st)

    # Create the table.
    ret = ret, db_schema.createNodeTypeTable(tag_level, tablename)
    
    return ret
    
def dropNodeType(id):
    """
    @param id the type id into the table.
    """
    st = ("SELECT tablename " 
        "FROM gn____node_types " 
        "WHERE id = " + str(id) + ";")
    tablename = db.query(st).getresult()[0][0]

    # Drop the table.
    st = "DROP TABLE IF EXISTS " + tablename + " CASCADE;"
    ret = db.query(st)

    # Delete entry into the types table.
    st = ("DELETE FROM gn____node_types " 
        "WHERE id = " + str(id) + ";")
    ret = ret, db.query(st)

    return ret

def createNode(level_id, parent_id, parentlevel_id, type_id, attributes):
    """Create node in db.

    Uses Node class for the node creation and coding for the node type
    attributes store.

    TODO store any attributes len.

    @param level id
    @param parent id
    @param parentlevel id
    @param type id
    @param attributes tuple of node attributes
    """
    N = class_node.node(level_id, parent_id, parentlevel_id, type_id)
    node_id = N.store(db)

    tag_level = genet_global.tagName(level_id)
    tag_type =  genet_global.tagName(type_id)

    st = ("INSERT INTO gn_" + tag_level + "_nodes_type_" + tag_type +  
          " VALUES(" + str(node_id) + ", '" + attributes[0] + "');")
    db.query(st)


def connectNodes(level_id, idnA, idnB, parent_id, parentlevel_id, type_id, attributes):
    """Create edge in db.

    Uses Edge class for the edge creation and coding for the edge type
    attributes store.

    TODO store any attributes len.

    @param level id
    @param node A id
    @param node B id
    @param parent id
    @param parentlevel id
    @param type id
    @param attributes tuple of edge attributes
    """
    E = class_edge.edge(level_id, idnA, idnB, parent_id, parentlevel_id, type_id)
    edge_id = E.store(db)

    tag_level = genet_global.tagName(level_id)
    tag_type =  genet_global.tagName(type_id)

    st = ("INSERT INTO gn_" + tag_level + "_edges_type_" + tag_type +  
          " VALUES(" + str(edge_id) + ", '" + attributes[0] + "');")
    db.query(st)
    
    
