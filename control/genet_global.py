#!/usr/bin/env python
################################################################################
# $Id: genet_global.py,v 1.7 2010/01/19 23:28:14 santiagopm Exp $
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
Start the schema creating the roles and the database in the DBMS as superuser,
in psql:

CREATE ROLE genetuser LOGIN;
CREATE DATABASE genet OWNER genetuser;
\connect genet
DROP SCHEMA public CASCADE;
CREATE SCHEMA public AUTHORIZATION genetuser;
CREATE ROLE santiago LOGIN;
GRANT genetuser TO santiago;

genet_global.restartDatabase() or 'Reset' button.

"""
from model.db_connection import db
from model import db_schema

##
# *** DANGER *** *** DANGER *** *** DANGER *** *** DANGER *** *** DANGER *** 
# Deletes all the database data tables.
# *** DANGER *** *** DANGER *** *** DANGER *** *** DANGER *** *** DANGER *** 
def restartDatabase():
    """
    *** DANGER *** *** DANGER *** *** DANGER *** *** DANGER *** *** DANGER *** 
    Restarts all the database.
    *** DANGER *** *** DANGER *** *** DANGER *** *** DANGER *** *** DANGER *** 

    """
    st = ("DROP SCHEMA public CASCADE;" 
        "CREATE SCHEMA public AUTHORIZATION genet;")
    ret = st, db.query(st)
    ret = ret, db_schema.fillSchema()
    return ret

##
# *** DANGER *** *** DANGER *** *** DANGER *** *** DANGER *** *** DANGER *** 
# Inconsistent calls to db from this application if changed with no restart.
# *** DANGER *** *** DANGER *** *** DANGER *** *** DANGER *** *** DANGER *** 
def tagName(input):
    """
    Tags uniformly database elements. Padded on the left with zeros.

    # *** DANGER *** *** DANGER *** *** DANGER *** *** DANGER *** *** DANGER *** 
    # Inconsistent calls to db from this application if changed with no restart.
    # *** DANGER *** *** DANGER *** *** DANGER *** *** DANGER *** *** DANGER *** 
    
    """
    return str(input).zfill(2)
