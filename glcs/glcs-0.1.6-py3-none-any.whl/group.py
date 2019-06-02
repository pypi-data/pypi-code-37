# -*- coding: utf-8 -*-
"""GroupManager and Group class."""
from glcs import group


class GroupManager:
    """Handles common Group manipulation tasks like retrieving, searching, and
    deleting of groups.
    """

    def __init__(self, gl):
        """Pass the gitlab instance to the GroupManager instance."""
        self.gl = gl

    def create(self, name=None, parent=None, or_die=None):
        if self.group_exists(name, parent):
            return or_die
        grp = or_die
        groupattrs = {
            'name': name,
            'path': name
        }
        if parent is not None:
            groupattrs['parent_id'] = parent.id
            groupattrs['path'] = name
        grp = self.gl.groups.create(groupattrs)
        if grp == or_die:
            return grp
        return group.Group(grp)

    def delete(self, name=None, id=None, or_die=False):
        if id is not None:
            self.gl.groups.delete(id)
            return True
        if name is not None:
            grp = self.get(name=name)
            grp.delete()
            return True
        return or_die

    def group_exists(self, name=None, parent=None):
        assert name is not None, "Need to pass a group name"
        parent_id = None
        if parent is not None:
            parent_id = parent.id
        groups = self.gl.groups.list(search=name)
        if not groups:
            return False
        else:
            if parent_id is None:
                return True
            else:
                for grp in groups:
                    if grp.parent_id == parent_id:
                        return True
        return False

    def get(self, name=None, id=None, parent_id=None):
        """Return the group with the given name, or Not Found"""
        groups = None
        if id is not None:
            grp = self.gl.groups.get(id)
            grp = group.Group(group)
            return grp
        if name is not None:
            groups = self.gl.groups.list(search=name)
            if groups:
                if parent_id is None:
                    grp = group.Group(groups[0])
                    return grp
                for g in groups:
                    if g.parent_id == parent_id:
                        grp = grp.Group(g)
                        return grp
                return None
            else:
                return None
        return None


class Group:
    """Handles common functions on a python-gitlab group object."""

    def __init__(self, groupobj):
        """Get or create a group with the supplied name and parent."""
        # define instance variables
        self.group = groupobj
        self.parent_id = groupobj.parent_id
        self.name = groupobj.name
        self.members = {}
        self.id = groupobj.id
        self.projects = groupobj.projects
        self.subgroups = groupobj.subgroups.list()
        # populate group member dictionary for easy member access by username
        mem = groupobj.members.list()
        for member in mem:
            self.members[member.id] = member

    def list_members(self):
        """Return the list of members in the group."""
        return self.group.members.list()

    def get_member(self, memberid):
        """Return the group member with the given id, or None if not found."""
        return self.group.members.get(memberid)

    def is_member(self, member):
        """Return True if member exists, False otherwise."""
        if member.id in self.members:
            return True
        return False

    def add_member(self, user, access):
        """Return True member can be added, False if already a member."""
        if self.is_member(user):
            return False
        member = self.group.members.create({'user_id': user.id,
                                            'access_level': access})
        self.members[member.id] = member
        return True

    def remove_member(self, user):
        """Return False if the member couldn't be removed, else True."""
        if not self.is_member(user):
            return False
        self.group.members.delete(user.id)
        return True

    def get_name(self):
        """Return the name of the current group."""
        return self.group.name

    def list_subgroups(self):
        """Return the subgroups of the group."""
        return self.subgroups

    def get_subgroups_as_groups(self):
        """Get the list of subgroups as Group objects (not SubGroup)."""
        realsubgroups = []
        for subgroup in self.subgroups:
            group = self.groupmanager.get(id=subgroup.id)
            realsubgroups.append(group)
        return realsubgroups
