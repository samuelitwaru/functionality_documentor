import pathspec

def match_file(path, patterns):
    spec = pathspec.PathSpec.from_lines(
            pathspec.patterns.GitWildMatchPattern, 
            patterns
        )
    return spec.match_file(path)