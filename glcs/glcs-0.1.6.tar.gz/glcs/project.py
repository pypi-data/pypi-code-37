# -*- coding: utf-8 -*-
"""ProjectManager and Project classes."""
from .student import Student


class ProjectManager:
    """Contains a set of functions for manipulating projects."""

    def __init__(self, gl):
        """Create a ProjectManager instance."""
        self.gl = gl
        ProjectManager.gitlab_instance = gl

    def get(self, id=None):
        """Get the GitLab project with the given ID."""
        pass

    def list(self, archived=None, visbility=None, owned=None, starred=None,
             search=None):
        """Get a list of GitLab projects matching the criteria."""
        pass

    def create(self, settings=None):
        """Create a GitLab project with the supplied settings."""
        pass

    def delete(self, id=None):
        """Delete a GitLab project with the given ID."""
        pass

    def import_project(self, file=None, name=None):
        """Import a GitLab project into the current server."""
        pass


class Project:
    """Contains a set of functions for manipulating a specific project."""

    def __init__(self, project_obj):
        """Create a Project instance."""
        self.project_obj = project_obj

    def snippets(self, enabled=None):
        """Enable or disable project snippets."""
        if enabled:
            self.enable_snippets()
        else:
            self.disable_snippets()

    def enable_snippets(self):
        """Enable project snippets."""
        self.project_obj.snippets_enabled = 1
        self.update()

    def disable_snippets(self):
        """Disable project snippets."""
        self.project_obj.snippets_enabled = 0
        self.update()

    def update(self):
        """Update the project on the server to match this project."""
        self.project_obj.save()

    def delete(self):
        """Delete this project."""
        self.project_obj.delete()

    def create_fork(self, options=None):
        """Create a fork of this project with the given options."""
        return self.project_obj.forks.create(options)

    def list_forks(self):
        """Get a list of the projects forked from this project."""
        return self.project_obj.forks.list()

    def used_languages(self):
        """Get a list of languages used in this project (percentages)."""
        return self.project_obj.languages()

    def star(self):
        """Star this project."""
        self.project_obj.star()

    def unstar(self):
        """Unstar this project."""
        self.project_obj.unstar()

    def archive(self):
        """Archive this project."""
        self.project_obj.archive()

    def unarchive(self):
        """Unarchive this project."""
        self.project_obj.unarchive()

    def housekeeping(self):
        """Perform housekeeping on this project."""
        self.project_obj.housekeeping()

    def repo_tree(self, path=None, ref=None):
        """Get the repository tree for this project given the path and ref."""
        if path is not None and ref is not None:
            return self.project_obj.repository_tree(path=path, ref=ref)
        elif path is not None and ref is None:
            return self.project_obj.repository_tree(path=path)
        elif path is None and ref is not None:
            return self.project_obj.repository_tree(ref=ref)
        else:
            return self.project_obj.repository_tree()

    def repo_blob(self, forItem=None):
        """Get the repository blob for the given item."""
        pass

    def repo_archive(self, sha=None):
        """Get the repository archive for the given sha."""
        pass

    def snapshot(self):
        """Get a snapshot of the project."""
        pass

    def compare_branches(self, b1=None, b2=None):
        """Compare two branches within the project."""
        pass

    def compare_tags(self, t1=None, t2=None):
        """Compare two tags within the project."""
        pass

    def compare_commits(self, c1=None, c2=None):
        """Compare two commits within the project."""
        pass

    def contributors(self):
        """Get a list of contributors to the project."""
        pass

    def list_users(self, search=None):
        """Get a list of users of the project."""
        pass

    def export(self, options):
        """Export this project."""
        pass
