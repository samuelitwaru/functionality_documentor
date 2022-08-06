import pathspec
from urllib.parse import urlparse
import pathlib
import github
import os

END_CHOICES = [('FRONT', 'FRONT'), ('BACK', 'BACK')]

def match_file(path, patterns):
    spec = pathspec.PathSpec.from_lines(
            pathspec.patterns.GitWildMatchPattern, 
            patterns
        )
    return spec.match_file(path)


def get_path_from_url(self, url):
    return urlparse(url).path.strip('/')

def get_url_path(url):
    return urlparse(url).path.strip('/')


def dot_notation(path):
    path = pathlib.Path(path)
    return '.'.join(path.with_suffix('').parts)


def create_gist(token, repo_name, file_path):
    g = github.Github(token)
    repo = g.get_repo(repo_name)
    file_content = repo.get_contents(file_path)
    content = file_content.decoded_content.decode()
    user = g.get_user()
    file_name = os.path.basename(file_path)
    gist = user.create_gist(
        public=False, 
        files={file_name: github.InputFileContent(content)},
        description=file_path
    )
    return gist

def delete_gist(token, gist_id):
    g = github.Github(token)
    user = g.get_user()
    gists = user.get_gists()
    filtered_gist = list(filter(lambda gist: gist.id==gist_id, gists))
    if len(filtered_gist):
        gist = filtered_gist[0]
        gist.delete()