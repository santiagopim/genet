#!/usr/bin/env python
################################################################################
# $Id: class_node.py,v 1.4 2010/01/18 00:32:22 santiagopm Exp $
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

"""
Define base class `node' with the minimal attributes as abstract 
attributes.

Every element in the network has:

* level: topological level, ISO level, layer, ...
* id: its own identifier.
* idtype: what kind of element is.
* idparent: from which element is a child.
* parentlevel: the level from where the parent is.

"""
class node:
    """
    Simple class with basic attributes.

    @param level id
    @param idparent id
    @param parentlevel id
    @param idtype id
    """
    def __init__(self, level, idparent, parentlevel, idtype):
        self.id = None
        self.level = level
        self.idparent = idparent
        self.parentlevel = parentlevel
        self.idtype = idtype
    
    def store(self, db):
        """
        Stores data in db. 

        @param db is the database object.
        @returns the node id.
        TODO write log with db statements.
        """
        # Uniformly define the tablename level.
        tag_level = genet_global.tagName(self.level)

        # If the node already exists.
        if self.id:

            # Update the nodes table.            
            st1 = ("UPDATE gn_" + tag_level + "_nodes SET " 
                "idtype = " + str(self.idtype) + " " 
                "WHERE id = " + str(self.id) + ";")
            db.query(st1)

            # Update the tree table.
            st2 = ("UPDATE gn____tree SET " 
                "idparent = " + str(self.idparent) + ", " 
                "parentlevel = " + str(self.parentlevel) + ", " 
                "childlevel = " + str(self.level) + " " 
                "WHERE idchild = " + str(self.id) + ";")
            db.query(st2)

            return self.id

        # If the node does not exist.
        else:
            
            # Insert the node into the table.
            st1 = ("INSERT INTO gn_" + tag_level + "_nodes(idtype) " 
                "VALUES(" 
                + str(self.idtype) + ") " 
                "RETURNING id;")
            self.id = db.query(st1).getresult()[0][0]

            # Insert the node into the tree.
            st2 = ("INSERT INTO gn____tree(idparent, idchild, "
                   "parentlevel, childlevel) " 
                "VALUES (" 
                + str(self.idparent) + ", " 
                + str(self.id) + ", " 
                + str(self.parentlevel) + ", " 
                + str(self.level) + ");")
            db.query(st2)

            return self.id

