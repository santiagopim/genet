#!/usr/bin/env python
################################################################################
# $Id: test_data.py,v 1.2 2008/11/30 22:48:34 santiagopm Exp $
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

from model import class_edge 
from model import class_node
from model.db_connection import db

##
# Insert data.
#
N001 = class_node.node(1, 0, 0, 2)
print N001.store(db)

N002 = class_node.node(1, 0, 0, 2)
print N002.store(db)

N003 = class_node.node(1, 0, 0, 2)
print N003.store(db)
N003.idtype = 4
print N003.store(db)

E001 = class_edge.edge(1, N001.id, N002.id, 0, 0, 3)
print E001.store(db)

E002 = class_edge.edge(1, N002.id, N003.id, 0, 0, 3)
print E002.store(db)

E003 = class_edge.edge(1, N003.id, N001.id, 0, 0, 3)
print E003.store(db)

E004 = class_edge.edge(1, N001.id, N002.id, 0, 0, 3)
print E004.store(db)

for r in db.query("SELECT * FROM gn_01_nodes").dictresult():
    print 'id %(id)s, idtype %(idtype)s' % r

for r in db.query("SELECT * FROM gn_01_edges").dictresult():
    print 'id %(id)s, idnA %(idna)s, idnB %(idnb)s, idtype %(idtype)s' % r
