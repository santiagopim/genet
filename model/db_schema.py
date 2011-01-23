#!/usr/bin/env python
################################################################################
# $Id: db_schema.py,v 1.9 2010/02/01 23:58:42 santiagopm Exp $
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

from db_connection import db

################################################################################
# Schema tables.
#
def fillSchema():
    """
    Start the db schema. Must be ran only once because restarts the master
    sequence and the type tables.
    """

    ##
    # All identifiers of networks elements has the same sequence source.
    # 
    st = """
    CREATE SEQUENCE "gn____ids_seq" 
      INCREMENT 1 
      MINVALUE 100000000 
      NO MAXVALUE 
      NO CYCLE;
    """
    ret = st, db.query(st)
    
    ##
    # All other elements, not in network, has another sequence source.
    #
    st = """
    CREATE SEQUENCE "gn____aux_seq"
      INCREMENT 1
      MINVALUE 1
      NO MAXVALUE
      NO CYCLE;
    """
    ret = ret, st, db.query(st)
    
    ##
    # Levels directory.
    # 
    st = """
    CREATE TABLE "gn____levels" (
        "id" integer NOT NULL DEFAULT nextval('gn____aux_seq'),
        "description" varchar(126)
    ) WITH (OIDS = FALSE);
    ALTER TABLE "gn____levels" 
        ADD CONSTRAINT "gn____levels_pk" 
        PRIMARY KEY("id");
    """
    ret = ret, st, db.query(st)

    ##
    # Out from basic schema all tables are referenced by this ones.
    #
    st = """
    CREATE TABLE "gn____node_types" (
        "id" integer NOT NULL DEFAULT nextval('gn____aux_seq'),
        "level" integer,
        "tablename" varchar(63), -- pg NAMEDATALEN is 63 currently.
        "description" varchar(126)
    ) WITH (OIDS = FALSE);
    ALTER TABLE "gn____node_types" 
        ADD CONSTRAINT "gn____node_types_pk" 
        PRIMARY KEY("id");
    ALTER TABLE "gn____node_types" 
        ADD CONSTRAINT "gn____node_types_level" 
        FOREIGN KEY ("level")
        REFERENCES "gn____levels"("id") 
        ON UPDATE CASCADE ON DELETE CASCADE;
    
    CREATE TABLE "gn____edge_types" (
        "id" integer NOT NULL DEFAULT nextval('gn____aux_seq'),
        "level" integer,
        "tablename" varchar(63), -- pg NAMEDATALEN is 63 currently.
        "description" varchar(126)
    ) WITH (OIDS = FALSE);
    ALTER TABLE "gn____edge_types" 
        ADD CONSTRAINT "gn____edge_types_pk" 
        PRIMARY KEY("id");
    ALTER TABLE "gn____edge_types" 
        ADD CONSTRAINT "gn____edge_types_level" 
        FOREIGN KEY ("level")
        REFERENCES "gn____levels"("id") 
        ON UPDATE CASCADE ON DELETE CASCADE;
    """
    ret = ret, st, db.query(st)

    ##
    # The tree relates between levels.
    # 
    st = """
    CREATE TABLE "gn____tree" (
        "idparent" integer,
        "idchild" integer,
        "parentlevel" integer,
        "childlevel" integer
    ) WITH (OIDS = FALSE);
    -- Child has only one parent.
    ALTER TABLE "gn____tree" 
        ADD CONSTRAINT "gn____tree_pk" 
        PRIMARY KEY("idchild");
    ALTER TABLE "gn____tree" 
        ADD CONSTRAINT "gn____tree_parentlevel" 
        FOREIGN KEY ("parentlevel")
        REFERENCES "gn____levels"("id") 
        ON UPDATE CASCADE ON DELETE CASCADE;
    ALTER TABLE "gn____tree" 
        ADD CONSTRAINT "gn____tree_childlevel" 
        FOREIGN KEY ("childlevel")
        REFERENCES "gn____levels"("id") 
        ON UPDATE CASCADE ON DELETE CASCADE;
    -- Can not constraint idparent and idchild
    -- to id nodes because do not know about
    -- their levels.
    -- TODO Constraint id from nodes.
    """
    ret = ret, st, db.query(st)
    
    # Return all outputs from queries.
    return ret

#def emptySchema():
#    """
#    Deletes all schematic tables.
#
#    """
#    st = """
#    DROP SEQUENCE IF EXISTS "gn____ids_seq" CASCADE;
#    DROP SEQUENCE IF EXISTS "gn____aux_seq" CASCADE;
#    DROP TABLE IF EXISTS "gn____tree" CASCADE;
#    DROP TABLE IF EXISTS "gn____levels" CASCADE;
#    DROP TABLE IF EXISTS "gn____node_types" CASCADE;
#    DROP TABLE IF EXISTS "gn____edge_types" CASCADE;
#    """
#    return st, db.query(st)

################################################################################
# Level tables.
#
def createLevelTables(level):
    """
    Tables schema. Create one level in datastore.

    @param level is the level identifier string.
    """
    st = """
    CREATE TABLE "gn_""" + level + """_nodes" (
        "id" integer NOT NULL DEFAULT nextval('gn____ids_seq'),
        "idtype" integer
    ) WITH (OIDS = FALSE);
    ALTER TABLE "gn_""" + level + """_nodes" 
        ADD CONSTRAINT "gn_""" + level + """_nodes_id" 
        PRIMARY KEY("id");
    ALTER TABLE "gn_""" + level + """_nodes" 
        ADD CONSTRAINT "gn_""" + level + """_nodes_fkey_type" 
        FOREIGN KEY ("idtype")
        REFERENCES "gn____node_types"("id") 
        ON UPDATE RESTRICT ON DELETE RESTRICT;

    CREATE TABLE "gn_""" + level + """_edges" (
        "id" integer NOT NULL DEFAULT nextval('gn____ids_seq'),
        "idna" integer,
        "idnb" integer,
        "idtype" integer
    ) WITH (OIDS = FALSE);
    ALTER TABLE "gn_""" + level + """_edges" 
        ADD CONSTRAINT "gn_""" + level + """_edges_id" 
        PRIMARY KEY("id");
    ALTER TABLE "gn_""" + level + """_edges" 
        ADD CONSTRAINT "gn_""" + level + """_edges_fkey_topoA" 
        FOREIGN KEY ("idna")
        REFERENCES "gn_""" + level + """_nodes"("id") 
        ON UPDATE RESTRICT ON DELETE RESTRICT;
    ALTER TABLE "gn_""" + level + """_edges" 
        ADD CONSTRAINT "gn_""" + level + """_edges_fkey_topoB" 
        FOREIGN KEY ("idnb") 
        REFERENCES "gn_""" + level + """_nodes"("id") 
        ON UPDATE RESTRICT ON DELETE RESTRICT;
    ALTER TABLE "gn_""" + level + """_edges" 
        ADD CONSTRAINT "gn_""" + level + """_edges_fkey_type" 
        FOREIGN KEY ("idtype")
        REFERENCES "gn____edge_types"("id") 
        ON UPDATE RESTRICT ON DELETE RESTRICT;
    """
    return st, db.query(st)

def dropLevelTables(level):
    """
    The level tables dropping deletes all network elements in the level.

    @param level is the level identifier string.
    """
    st = """
    DROP TABLE IF EXISTS "gn_""" + level + """_nodes" CASCADE;
    DROP TABLE IF EXISTS "gn_""" + level + """_edges" CASCADE;
    """
    return st, db.query(st)

def createNodeTypeTable(level, tablename):
    """
    TODO
    """
    st = """
    CREATE TABLE """ + tablename + """ (
        "idnode" integer,
        "attribute01" varchar(32)
    ) WITH (OIDS = FALSE);
    ALTER TABLE """ + tablename + """ 
        ADD CONSTRAINT """ + tablename + """_id 
        PRIMARY KEY("idnode");
    ALTER TABLE """ + tablename + """
        ADD CONSTRAINT """ + tablename + """_fkey_type 
        FOREIGN KEY ("idnode")
        REFERENCES gn_""" + level + """_nodes("id") 
        ON UPDATE RESTRICT ON DELETE RESTRICT;
    """
    return st, db.query(st)
    
def createEdgeTypeTable(level, tablename):
    """
    TODO
    """
    st = """
    CREATE TABLE """ + tablename + """ (
        "idedge" integer,
        "atribute01" varchar(32)
    ) WITH (OIDS = FALSE);
    ALTER TABLE """ + tablename + """ 
        ADD CONSTRAINT """ + tablename + """_id 
        PRIMARY KEY("idedge");
    ALTER TABLE """ + tablename + """
        ADD CONSTRAINT """ + tablename + """_fkey_type 
        FOREIGN KEY ("idedge")
        REFERENCES gn_""" + level + """_edges("id") 
        ON UPDATE RESTRICT ON DELETE RESTRICT;
    """
    return st, db.query(st)

