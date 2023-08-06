import os
import json
import shlex
import types
import itertools
import collections



def summary(run_script, job_paths):
    '''Print out a nice summary of the job sbatch files and the run script.'''
    print('Generated', len(job_paths), 'job scripts:')
    for p in job_paths:
        print('\t', p)
    print()

    print('To submit all jobs, run:')
    print('.', run_script)
    print()


'''

Naming Transformers

'''

_REPLACED = {
    '.': 'pt', ',': 'cm', '@': 'at', '/': 'sl', '\\': 'bs',
    ':': 'col', ';': 'sem', '<': 'lt', '>': 'gt',
    '!': 'ex', '?': 'qsn', '~': 'tld', '`': 'bkt',
    '#': 'hsh', '$': 'dol', '%': 'pct', '^': 'crt',
    '&': 'and', '+': 'pls', '=': 'eq', '-': 'dsh', '|': 'ppe',
    '[': 'sq_o', ']': 'sq_c', '(': 'pr_o', ')': 'pr_c',
    '{': 'crl_o', '}': 'crl_c',
}

_REPLACED = {k: '__{}__'.format(v.upper()) for k, v in _REPLACED.items()}

def _encode_special(x):
    '''Convert special characters into an ascii placeholder.'''
    for sp, token in _REPLACED.items():
        x.replace(sp, token)
    return x

def _decode_special(x):
    '''Reverse _encode_special. Convert ascii placeholders back into special characters.'''
    for sp, token in _REPLACED.items():
        x.replace(token, sp)
    return x

def _obliterate_special(x):
    '''Filter out special characters.'''
    return ''.join(xi if xi.isalnum() else _REPLACED.get(xi, '__') for xi in x)

def command_to_name(command):
    '''Convert a bash command into a usable job name.
    
    NOTE: This was originally to turn 'python my/script.py' into 'my.script'
          but obviously this is just a special case and I never really found
          a nice, general way to do this.
    '''
    fbase = os.path.splitext(shlex.split(command)[1])[0]
    return fbase.replace('/', '.').lstrip('.').replace(' ', '-')

def get_job_name(name, params, job_name_tpl=None, allowed=",._-"):
    '''Given a name and a dict of parameters, return a name that
    describes the job (name+params).'''
    # Define job name using the batch name and job parameters
    if params:
        params = {k: format_value_for_name(v) for k, v in params.items()}
        param_names, param_vals = list(zip(*sorted(params.items())))
        job_name_tpl = job_name_tpl or make_job_name_tpl(param_names)
        name = name + ',' + job_name_tpl.format(*param_vals, **{
            _obliterate_special(k): v for k, v in params.items()
        })
    name = ''.join(x for x in name if (x.isalnum() or x in allowed))
    return name

def make_job_name_tpl(names):
    '''Convert a list of keys into a formattable template string.'''
    # create a python format string for all parameters
    return ','.join(f'{n}-{{{_obliterate_special(n)}}}' for n in names)

def format_value_for_name(x):
    '''Convert complex objects (list, dict,) into something that works as a filename.'''
    # Format parameter values so that they are filename safe
    if isinstance(x, dict):
        return '_'.join('{}-{}'.format(k, v) for k, v in sorted(dict.items()))
    if isinstance(x, (list, tuple, set)):
        return '({})'.format(','.join(map(str, x)))
    return x


'''

Parameter Expansion

'''
NOTHING = object()

def expand_grid(params, ignore=NOTHING):
    '''
    e.g.
    params = [
        ('latent_dim', [1,2,4]),
        (('a', 'b'), [ (1, 3), (2, 5) ]),
        ('lets_overfit', (True,))
    ]
    assert list(expand_grid(params)) == [
        {'latent_dim': 1, 'a': 1, 'b': 3, 'lets_overfit': True},
        {'latent_dim': 1, 'a': 2, 'b': 5, 'lets_overfit': True},
        {'latent_dim': 2, 'a': 1, 'b': 3, 'lets_overfit': True},
        {'latent_dim': 2, 'a': 2, 'b': 5, 'lets_overfit': True},
        {'latent_dim': 4, 'a': 1, 'b': 3, 'lets_overfit': True},
        {'latent_dim': 4, 'a': 2, 'b': 5, 'lets_overfit': True},
    ]
    '''
    return list(_iter_expand_grid(params))

def _iter_expand_grid(params):
    if isinstance(params, (list, tuple)):
        params, param_literals = split_cond(lambda x: isinstance(x, dict), params, [False, True])
        yield from param_literals
    
    param_names, param_grid = tuple(zip(*(
        params.items() if isinstance(params, dict) else params))) or ([], [])

    if param_grid:
        for ps in itertools.product(*param_grid):
            yield expand_paired_params(zip(param_names, ps))

def expand_paired_params(params, ignore=NOTHING):
    '''Flatten tuple dict key/value pairs
    e.g.
    assert (expand_paired_params([
            ('latent_dim', 2),
            (('a', 'b'), (1, 2)),
            ('lets_overfit', True)
        ])
        == {'latent_dim': 1, 'a': 1, 'b': 2, 'lets_overfit': True})
    '''
    return {n: v for n, v in unpack(params) if v is not ignore}

def unpack(params):
    '''Flatten tuple dict key/value pairs
    e.g.
    assert (
        expand_paired_params([
            ('latent_dim', 2),
            (('a', 'b'), (1, 2)),
            ('lets_overfit', True)
        ])
        == {'latent_dim': 1, 'a': 1, 'b': 2, 'lets_overfit': True})
    '''
    params = params.items() if isinstance(params, dict) else params
    for n, v in params:
        if isinstance(n, tuple):
            # ((a, b), (1, 2)) =>
            for ni, vi in zip(n, v):
                yield ni, vi
        else:
            yield n, v


def as_chunks(lst, n=1):
    return [lst[i:i + n] for i in range(0, len(lst), n)]


def split_cond(cond, lst, keys=None):
    '''Split a list based on a condition.'''
    res = {k: [] for k in keys or []}
    for x in lst:
        k = cond(x)
        if keys and k not in keys:
            continue
        if k not in res:
            res[k] = []
        res[k].append(x)
    return [res[k] for k in keys or sorted(res)]

'''

Misc / template utils

'''

def make_executable(file_path):
    '''Grant permission to execute a file.'''
    # https://stackoverflow.com/a/30463972
    mode = os.stat(file_path).st_mode
    mode |= (mode & 0o444) >> 2
    os.chmod(file_path, mode)

def maybe_backup(path, prefix='~'):
    '''Backup a path if it exists.'''
    # create backup
    if path.exists():
        bkp_previous_path = path.prefix(prefix).next_unique(1)
        os.rename(path, bkp_previous_path)
        print('moved existing', path, 'to', bkp_previous_path)



def prettyjson(value):
    '''Pretty-print data using json.'''
    return json.dumps(value, sort_keys=True, indent=4) if value else ''


def prefixlines(text, prefix='# '):
    '''Prefix each line. Can be used to comment a block of text.'''
    return ''.join(prefix + l for l in text.splitlines(keepends=True))


def dict_merge(*ds, depth=-1, **kw):
    '''Recursive dict merge.

    Arguments:
        *ds (dicts): dicts to be merged.
        depth (int): the max depth to be merged.
        **kw: extra keys merged on top of the final dict.

    Returns:
        merged (dict).
    '''
    def merge(dicta, dictb, depth=-1):
        '''Recursive dict merge.

        Arguments:
            dicta (dict): dict to be merged into.
            dictb (dict): merged into dicta.
        '''
        for k in dictb:
            if (depth != 0 and k in dicta
                    and isinstance(dicta[k], dict)
                    and isinstance(dictb[k], collections.Mapping)):
                dict_merge(dicta[k], dictb[k], depth=depth - 1)
            else:
                dicta[k] = dictb[k]

    mdict = {}
    for d in ds + (kw,):
        merge(mdict, d, depth=depth)
    return mdict


def flatten(args, cls=(list, tuple, set, types.GeneratorType)):
    '''Flatten iterables into a flat list.'''
    if isinstance(args, cls):
        return [a for arg in args for a in flatten(arg)]
    return [args]
'''

Argument

'''

class Factory:
    '''This class makes subclasses easily queriable using ``Cls.__children__()``.
    This returns a dictionary of the lowercase class name and class as key/value.
    This can also strip off common prefixes/suffixes making it easy to for users
    to lookup. 

    .. code-block:: python
        
        class Args(Factory): pass
        class FireArgs(Args): pass
        class ArgparseArgs(Args): pass

        assert Args.__children__() == {'fireargs': FireArgs, 'argparseargs': ArgparseArgs}
        assert Args.__children__(suffix='args') == {'fire': FireArgs, 'argparse': ArgparseArgs}

        clses = Args.__children__(suffix='args')
        clses.get('fire')

    '''
    @classmethod
    def __children__(cls, prefix='', suffix=''):
        return {
            stripstr(c.__name__.lower(), prefix, suffix): c
            for c in all_subclasses(cls)
            if not c.__name__.startswith('_')}

def all_subclasses(cls):
    '''Return all recursive subclasses of a class.'''
    return set(cls.__subclasses__()).union(
        s for c in cls.__subclasses__() for s in all_subclasses(c))

def shlex_repr(v):
    '''Prepare a variable for bash. This will serialize the object using json 
    and then quote the variable if it contains any spaces/bash-specific characters.
    '''
    # v = repr(v)
    v = json.dumps(v)
    # if v is a quoted string, remove the quotes
    if len(v) >= 2 and v[0] == v[-1] and v[0] in '"\'':
        v = v[1:-1]
    return shlex.quote(v) # only quote if necessary (has spaces or bash chars)

def escape(txt, chars='"\''):
    '''Escape certain characters from a string. By default, it's quotes.'''
    for c in chars:
        txt = txt.replace(c, '\\' + c)
    return txt



def stripstr(text, prefix='', suffix=''):
    '''Strip a prefix and/or suffix from a string.'''
    text = text[len(prefix):] if prefix and text.startswith(prefix) else text
    text = text[:-len(suffix)] if suffix and text.endswith(suffix) else text
    return text


def singularity_command(overlay, sif):
    wrap = 'singularity exec --nv --overlay {}:ro {}  bash -c ". /ext3/env.sh; {{}}"'.format(overlay, sif)
    def cmd(cmd):
        return wrap.format(escape(cmd, '\"'))
    return cmd


def get_available_tensorflow_cuda_versions():
    '''Load the tensorflow-cuda lookup table.'''
    # https://www.tensorflow.org/install/source#gpu
    import csv
    with open(os.path.join(os.path.dirname(__file__), 'cuda_versions.csv'), 'r') as f:
        rows = list(csv.DictReader(f, delimiter='\t'))
    return { d['Version'].split('-')[-1]: {
        'cuda': d['CUDA'], 'cudnn': d['cuDNN'], 
        'python': d["Python version"].split(', ')
    } for d in rows }

def find_tensorflow_cuda_version(version, latest=False):
    '''Given a tensorflow version, lookup the correct'''
    import fnmatch
    versions = get_available_tensorflow_cuda_versions()
    version = str(version).split('.')[:2]
    version = '.'.join(version + ['*']*(3 - len(version)))
    matched = sorted([v for v in versions if fnmatch.fnmatch(v, version)])
    if not matched:
        raise ValueError('No value matching {!r}'.format(version))
    matched = matched[-1 if latest else 0]
    return dict(versions[matched], version=matched)

if __name__ == '__main__':
    import fire
    fire.Fire()