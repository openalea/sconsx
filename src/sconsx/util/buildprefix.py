

def fix_custom_buildprefix(env, standardprefix = 'build-scons'):
    """ 
        A function that create a symlink in case build_prefix is different from standardprefix. 
        Usefull to make the link with python setup.py configuration.
        Args:
        env (SCons.environment or str): The actual prefix.
        standardprefix (str): The name of the standart prefix used by setup.py.
    """
    import os, shutil
    if os.name == 'posix' :
        if type(env) == str:
            prefix = env
        else:
            # A 
            prefix = env['build_prefix']
        if os.path.basename(prefix) != standardprefix:
            if os.path.exists(standardprefix):
                if os.path.isdir(standardprefix) and not os.path.islink(standardprefix): 
                    shutil.rmtree(standardprefix)
                else: 
                    os.remove(standardprefix)
            os.symlink(prefix, standardprefix)

