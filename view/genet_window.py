#!/usr/bin/env python
################################################################################
# $Id: genet_window.py,v 1.18 2010/02/01 23:58:42 santiagopm Exp $
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
Interface.

Has one tab for every work:

* Admin tab: create levels and types.
* Create tab: create nodes into the network. Must declare type of node and 
parent in which the node is embebed.
* Connect tab: connects nodes.
* Browse tab: shows network graphs (uses networkx, graphviz, ...).
"""

## TODO My emacs needs this
import sys
if '/home/santiago/workspace/genet' not in sys.path:
    sys.path.append('/home/santiago/workspace/genet')
##

import gtk
import gtk.glade
import pygtk

from control import genet_browser
from control import genet_creator 
from control import genet_global

#from model import class_edge 
#from model import class_node
#from model.db_connection import db

from view import genet_treemodels
        
class GenetWindow(gtk.Window):
    def __init__(self):
        """
        The window.
        
        """
        gladefile = "genet.glade"
        windowname = "genet"
        self.wTree = gtk.glade.XML (gladefile, windowname)
        
        # Fill tree views.
        ##
        # Browse tree
        tree = self.wTree.get_widget("treeview_browser")
        model = genet_treemodels.BrowseNodesTreeModel()
        tree.set_model(model)
    
        cell = gtk.CellRendererText()

        # Ids column should disapear in production version
        column00 = gtk.TreeViewColumn("Id", cell, text=0)
        column00.set_clickable(True)
        tree.append_column(column00)

        column01 = gtk.TreeViewColumn("Level", cell, text=1)
        column01.set_clickable(True)
        tree.append_column(column01)

        column02 = gtk.TreeViewColumn("Attribute", cell, text=2)
        column02.set_clickable(True)
        tree.append_column(column02)

        tree.set_expander_column(tree.get_column(1))

        ##
        # Connect nodes A tree
        tree = self.wTree.get_widget("treeview_conn_nodes_A")
        model = genet_treemodels.ConnectNodesTreeModel()
        tree.set_model(model)
    
        cell = gtk.CellRendererText()

        # Ids column should disapear in production version
        column00 = gtk.TreeViewColumn("Id", cell, text=0)
        column00.set_clickable(True)
        tree.append_column(column00)

        column01 = gtk.TreeViewColumn("Level", cell, text=1)
        column01.set_clickable(True)
        tree.append_column(column01)

        column02 = gtk.TreeViewColumn("Attribute", cell, text=2)
        column02.set_clickable(True)
        tree.append_column(column02)

        tree.set_expander_column(tree.get_column(1))

        ##
        # Connect nodes B tree
        tree = self.wTree.get_widget("treeview_conn_nodes_B")
        model = genet_treemodels.ConnectNodesTreeModel()
        tree.set_model(model)
    
        cell = gtk.CellRendererText()

        # Ids column should disapear in production version
        column00 = gtk.TreeViewColumn("Id", cell, text=0)
        column00.set_clickable(True)
        tree.append_column(column00)

        column01 = gtk.TreeViewColumn("Level", cell, text=1)
        column01.set_clickable(True)
        tree.append_column(column01)

        column02 = gtk.TreeViewColumn("Attribute", cell, text=2)
        column02.set_clickable(True)
        tree.append_column(column02)

        tree.set_expander_column(tree.get_column(1))

        ##
        # Connect nodes edge types tree
        tree = self.wTree.get_widget("treeview_conn_nodes_edge_types")
        model = genet_treemodels.ConnectNodesEdgeTypesTreeModel()
        tree.set_model(model)
    
        cell = gtk.CellRendererText()

        # Ids column should disapear in production version
        column00 = gtk.TreeViewColumn("Id", cell, text=0)
        column00.set_clickable(True)
        tree.append_column(column00)

        column01 = gtk.TreeViewColumn("Type", cell, text=1)
        column01.set_clickable(True)
        tree.append_column(column01)

        column02 = gtk.TreeViewColumn("", cell, text=2)
        column02.set_clickable(True)
        tree.append_column(column02)

        tree.set_expander_column(tree.get_column(1))

        ##
        # Create node types tree
        tree = self.wTree.get_widget("treeview_create_node_types")
        model = genet_treemodels.CreateNodeTypesTreeModel()
        tree.set_model(model)
    
        cell = gtk.CellRendererText()

        # Ids column should disapear in production version
        column00 = gtk.TreeViewColumn("Id", cell, text=0)
        column00.set_clickable(True)
        tree.append_column(column00)

        column01 = gtk.TreeViewColumn("Level", cell, text=1)
        column01.set_clickable(True)
        tree.append_column(column01)

        column02 = gtk.TreeViewColumn("Type", cell, text=2)
        column02.set_clickable(True)
        tree.append_column(column02)

        tree.set_expander_column(tree.get_column(1))

        ##
        # Create node parents tree
        tree = self.wTree.get_widget("treeview_create_node_parents")
        model = genet_treemodels.CreateNodeParentsTreeModel()
        tree.set_model(model)
    
        cell = gtk.CellRendererText()

        # Ids column should disapear in production version
        column00 = gtk.TreeViewColumn("Id", cell, text=0)
        column00.set_clickable(True)
        tree.append_column(column00)

        column01 = gtk.TreeViewColumn("Level", cell, text=1)
        column01.set_clickable(True)
        tree.append_column(column01)

        column02 = gtk.TreeViewColumn("Type", cell, text=2)
        column02.set_clickable(True)
        tree.append_column(column02)

        tree.set_expander_column(tree.get_column(1))

        ##
        # Admin levels tree
        tree = self.wTree.get_widget("treeview_admin_levels")
        model = genet_treemodels.AdminTreeModel()
        tree.set_model(model)
    
        cell = gtk.CellRendererText()

        # Ids column should disapear in production version
        column00 = gtk.TreeViewColumn("Id", cell, text=0)
        column00.set_clickable(True)
        tree.append_column(column00)

        column01 = gtk.TreeViewColumn("Level", cell, text=1)
        column01.set_clickable(True)
        tree.append_column(column01)

        column02 = gtk.TreeViewColumn("Type", cell, text=2)
        column02.set_clickable(True)
        tree.append_column(column02)

        tree.set_expander_column(tree.get_column(1))

        # Declare actions dictionary.
        dic = {
            # Browse tab.
            "on_button_browser_draw_level_clicked" : 
            self.button_browser_draw_level_clicked,
            "on_button_browser_draw_tree_clicked" : 
            self.button_browser_draw_tree_clicked,

            # Connect nodes tab.
            "on_button_conn_nodes_clicked" :
                self.button_conn_nodes_clicked,
            "on_button_conn_nodes_refresh_clicked" :
                self.button_conn_nodes_refresh_clicked,
            
            # Create tab.
            "on_button_create_node_clicked" :
                self.button_create_node_clicked,
            
            # Admin tab.
            "on_button_create_level_clicked" : 
            self.button_create_level_clicked,
            "on_button_drop_item_clicked" : 
            self.button_drop_item_clicked,
            "on_button_create_node_type_clicked" :
                self.button_create_node_type_clicked,
            "on_button_create_edge_type_clicked" :
                self.button_create_edge_type_clicked,
            "on_button_admin_reset_clicked" :
                self.button_admin_reset_clicked,
            "on_genet_destroy" : (gtk.main_quit) }
        self.wTree.signal_autoconnect(dic)
        return

    ############################################################################
    # Browse tab.
    #
    def button_browser_draw_level_clicked(self, widget):
        print 'Level Clicked!'

    def button_browser_draw_tree_clicked(self, widget):
        print 'Tree Clicked!'
        
    ############################################################################
    # Connect nodes tab.
    #
    def button_conn_nodes_clicked(self, widget):
        """Connects nodes selected left and right with an edge type.
        
        The edge type is taken from the edge types tree.
        """
        # TODO all interface flow must be loaded by steps, selecting node A,
        # then edge type and then node B.
        # Get node A level
        root_values = self.get_tree_selected_root_values("treeview_conn_nodes_A")
        level_id = root_values[0]

        # Load edge types in this level
        tree = self.wTree.get_widget("treeview_conn_nodes_edge_types")
        tree.get_model().reload(int(level_id))
        tree.expand_all()
        
        # Get type
#        type_values = self.get_tree_selected_values("treeview_conn_nodes_edge_types")
#        type_id = type_values[0]

    def button_conn_nodes_refresh_clicked(self, widget):
        """ Refresh trees from data model.
        """
        self.tree_refresh("treeview_conn_nodes_A")
        self.tree_refresh("treeview_conn_nodes_edge_types")
        self.tree_refresh("treeview_conn_nodes_B")

    ############################################################################
    # Create tab.
    #
    def button_create_node_clicked(self, widget):
        # Get level
        root_values = self.get_tree_selected_root_values("treeview_create_node_types")
        level_id = root_values[0]

        # Get type
        type_values = self.get_tree_selected_values("treeview_create_node_types")
        type_id = type_values[0]

        # Get parent level
        parent_root_values = self.get_tree_selected_root_values("treeview_create_node_parents")
        parentlevel_id = parent_root_values[0]

        # Get parent
        parent_values = self.get_tree_selected_values("treeview_create_node_parents")
        parent_id = parent_values[0]

        # Get attributes
        att01 = self.wTree.get_widget("entry_create_node_att").get_text()
        attributes = att01,

        # Create node
        # TODO When there is no parent, parentlevel should be its own level
        # and parent id should be 0.
        genet_creator.createNode(level_id, parent_id, 
                                 parentlevel_id, type_id, attributes)

        # Refresh tree
        self.tree_refresh("treeview_create_node_types")
        self.tree_refresh("treeview_create_node_parents")

    ############################################################################
    # Admin tab.
    #
    def button_create_level_clicked(self, widget):
        """Create a level in the network.
        """
        # Get description
        description = self.wTree.get_widget("entry_admin_level").get_text()

        # Create level
        genet_creator.createLevel(description)

        # Refresh tree
        self.tree_refresh("treeview_admin_levels")

    def button_create_node_type_clicked(self, widget):
        """Create a node type.

        Gets the level in which to create the node type from any selected
        item in the tree.
        """
        # Get level
        root_values = self.get_tree_selected_root_values("treeview_admin_levels")
        level_id = root_values[0]

        # Get description
        description = self.wTree.get_widget("entry_admin_type").get_text()

        # Create type
        genet_creator.createNodeType(level_id, description)

        # Refresh tree
        self.tree_refresh("treeview_admin_levels")

    def button_create_edge_type_clicked(self, widget):
        """Create an edge type.

        Gets the level in which to create the edge type from any selected
        item in the tree.
        """
        # Get level
        root_values = self.get_tree_selected_root_values("treeview_admin_levels")
        level_id = root_values[0]

        # Get description
        description = self.wTree.get_widget("entry_admin_type").get_text()

        # Create type
        genet_creator.createEdgeType(level, description)

        # Refresh tree
        self.tree_refresh("treeview_admin_levels")

    def button_drop_item_clicked(self, widget):
        """Purge selected item.

        Gets the item to delete from selection tree.
        """
        values = self.get_tree_selected_values("treeview_admin_levels")

        values_id = values[0]
        values_type = values[2]

        if values_type == "Edge":
            genet_creator.dropEdgeType(values_id)
        elif values_type == "Node":
            genet_creator.dropNodeType(values_id)
        elif values_type == "":
            genet_creator.dropLevel(values_id)
        else:
            # TODO raise exception. Never should be here.
            print "*** Error in code ***"

        # Refresh tree
        self.tree_refresh("treeview_admin_levels")

    def button_admin_reset_clicked(self, widget):
        genet_global.restartDatabase()
        
        # Refresh tree
        self.tree_refresh("treeview_admin_levels")

    ############################################################################
    # Auxiliary functions.
    #
    def main(self):
        gtk.main()

    def get_tree_selected_root_values(self, tree_widget):
        """Get all information from the root of the selected row in the tree.
        """
        tree = self.wTree.get_widget(tree_widget)
        tree_selection = tree.get_selection()
        tree_selection_model = tree_selection.get_selected()[0]
        tree_selection_iter = tree_selection.get_selected()[1]
        tree_n_columns = tree_selection_model.get_n_columns()
        
        # Get the root from selection. Could be in root now, so root iter is
        # the actually selected iter.
        root_iter = tree_selection_iter
        parent_iter = tree_selection_model.iter_parent(root_iter)
        while parent_iter is not None:
            root_iter = parent_iter
            parent_iter = tree_selection_model.iter_parent(parent_iter)

        values = ()
        for c in range(tree_n_columns):
            values += tree_selection_model.get(root_iter, c)

        return values

    def get_tree_selected_values(self, tree_widget):
        """Get all information from the selected row in the tree.
        """
        tree = self.wTree.get_widget(tree_widget)
        tree_sel = tree.get_selection()
        tree_sel_model, tree_sel_iter = tree_sel.get_selected()
        tree_n_columns = tree_sel_model.get_n_columns()
        
        values = ()
        for c in range(tree_n_columns):
            values += tree_sel_model.get(tree_sel_iter, c)

        return values

    def tree_refresh(self, tree_widget):
        """Refresh tree data without forget selection.
        """
        tree = self.wTree.get_widget(tree_widget)
        tree_sel = tree.get_selection()
        tree_sel_model, tree_sel_iter = tree_sel.get_selected()
        
        # Save selected item or path
        tree_sel_path = (0,)
        if tree_sel_iter is not None:
            tree_sel_path = tree_sel_model.get_path(tree_sel_iter)

        # Refresh data, reload data into model
        tree.get_model().reload()

        # Expand old selection
        tree.expand_to_path(tree_sel_path)
        #tree_sel.select_path(tree_sel_path)

if __name__ == '__main__':
    app = GenetWindow()
    app.main()
