# -*- coding: utf-8 -*-
# =============================================================================
# Recursively prints the tree structure of the matplotlib object
def print_tree( obj, indent ):
        print indent, type(obj)
        for child in obj.get_children():
                print_tree( child, indent + "   " )
        return
# =============================================================================