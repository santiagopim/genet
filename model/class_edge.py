#!/usr/bin/env python
################################################################################
# $Id: class_edge.py,v 1.5 2010/02/01 23:58:42 santiagopm Exp $
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
Define base class `edge' with the minimal attributes as abstract 
attributes.

Every element in the network has:

* level: topological level, ISO level, layer, ...
* id: its own identifier.
* idtype: what kind of element is.
* idparent: from which element is a child.
* parentlevel: the level from where the parent is.

And in linear (edges) elements that connects two puntual (nodes) elements
there are:

* idnA: one side connection point id.
* idnB: other side id.

"""

from control import genet_global

class edge:
    """
    Simple class with basic attributes.
    
    The the edge itself, 'idnA' and 'idnB' should be from the same level, 
    this is resolved at execution time from an intelligent interface, but
    the schema does not restricts.

    TODO Schema could restrict. Since nodes has id only if they are in 
    the db, one may check theirs levels. Need db reference.

    """
    def __init__(self, level, idnA, idnB, idparent, parentlevel, idtype):
        self.id = None
        self.level = level
        self.idnA = idnA
        self.idnB = idnB
        self.idparent = idparent
        self.parentlevel = parentlevel
        self.idtype = idtype

#        # Check idnA and idnB are on the correct level. They must exist.
#        tag_level = genet_global.tagName(self.level)
#        st = "SELECT id " \
#            "FROM gn_" + tag_level + "_nodes " \
#            "WHERE id = " + self.idnA + ";"
#        if db.query(st).getresult()[0][0] != idnA:
#            return
#
#        st = "SELECT id " \
#            "FROM gn_" + tag_level + "_nodes " \
#            "WHERE id = " + self.idnB + ";"
#        if db.query(st).getresult()[0][0] != idnB:
#            return

    def store(self, db):
        """
        Stores data in db. 

        @param db is the database object.
        @returns the SQL statement and edge id.
        """
        # Uniformly define the tablename level.
        tag_level = genet_global.tagName(self.level)

        # If the edge already exists.
        if self.id:

            # Update the edges table.
            st1 = ("UPDATE gn_" + tag_level + "_edges SET " 
                "idnA = " + str(self.idnA) + ", " 
                "idnB" + str(self.idnB) + ", " 
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

        # If the edge does not exist.
        else:

            # Insert the edge into the table.
            st1 = ("INSERT INTO gn_" + tag_level + "_edges(idna, idnb, idtype) " 
                "VALUES(" 
                + str(self.idnA) + ", " 
                + str(self.idnB) + ", " 
                + str(self.idtype) + ") " 
                "RETURNING id;")
            self.id = db.query(st1).getresult()[0][0]

            # Insert the node into the tree.
            st2 = ("INSERT INTO gn____tree(idparent, idchild, "
                   "parentlevel, childlevel) " 
                "VALUES(" 
                + str(self.idparent) + ", " 
                + str(self.id) + ", " 
                + str(self.parentlevel) + ", " 
                + str(self.level) + ");")
            db.query(st2)

            return self.id
        
