import pathspec


def match_file(path, patterns):
    spec = pathspec.PathSpec.from_lines(
            pathspec.patterns.GitWildMatchPattern, 
            patterns
        )
    return spec.match_file(path)
    
    
patterns = ['node_modules/', '*.txt', '*.pyc']
path = 'node_modules/dan/sam/script'
print(match_file(path, []))