import os

exclude_dirs = (
    '.hg',
    '.git',
    '.svn',
    'node_modules',
    '__pycache__',
)


def djangoplus_find_staticfiles(cwd, app_paths, cmdline=False):
    templates = set()
    project_paths = []

    app_paths = app_paths.split(',')

    for file in os.listdir(cwd):
        path = os.path.join(cwd, file)

        if file[0] == '.' or not os.path.isdir(path) or file in exclude_dirs:
            continue

        if path not in app_paths and not os.path.exists(os.path.join(path, '__init__.py')):
            continue

        if path not in app_paths:
            project_paths.append(path)

    static_paths = set()
    for i, path in enumerate(app_paths):
        if path.startswith('tpl|'):
            continue
        elif path.startswith('sta|'):
            path = path[4:]
        elif os.path.split(path)[-1] == 'static':
            pass
        else:
            path = os.path.join(path, 'static')
            if not os.path.exists(path):
                path = ''

        if not path or path in static_paths:
            continue
        static_paths.add(path)

        for root, dirs, files in os.walk(path):
            directory = root[len(path)+1:]
            if directory:
                templates.add('%s/' % directory)
            templates.update(os.path.join(root, x)[len(path)+1:] for x in files)

    for path in project_paths:
        for root, dirs, files in os.walk(path):
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            parts = root.split(os.path.sep)
            if 'static' not in parts:
                continue

            i = parts.index('static')
            i += sum(len(x) for x in parts[:i+1]) + 1
            directory = root[i:]
            if directory:
                templates.add('%s/' % directory)
            templates.update(os.path.join(root, x)[i:] for x in files)

    templates = list(sorted(templates, key=lambda x:
                            (len(x.split(os.path.sep)), x)))

    try:
        import vim  # noqa F811
        vim.command('let s:staticfiles_cache = %s' % repr(templates).replace("u'", "'").replace("\\\\", "/"))
    except ImportError:
        print('\n'.join(templates))


if __name__ == "__main__":
    try:
        import vim  # noqa F401
    except ImportError:
        djangoplus_find_staticfiles(os.getcwd(), '', 1)
