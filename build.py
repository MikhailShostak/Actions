import os, subprocess, pathlib, shutil

def mkdir(*args):
    path = os.path.join(ROOT_DIR, *args)
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)
    return path

def run(*args):
    print(' '.join(*args))
    subprocess.run(*args)

def copytree(src, dst, symlinks=False, ignore=None):
    print('copy {} {}'.format(src, dst))
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)

def copy_headers(title, header_dir):
    copytree(os.path.join(ROOT_DIR, title, header_dir), INCLUDE_DIR)

def build_library(title, header_dir, source_dir, source_extensions):
    obj_dir = mkdir('build', 'obj', title)
    obj_files = []
    for root, subdirs, files in os.walk(os.path.join(ROOT_DIR, title, source_dir)):
        for f in files:
            if pathlib.Path(f).suffix not in source_extensions:
                continue
            
            source_file = os.path.join(root, f)
            obj_file = os.path.join(obj_dir, f + '.o')
            obj_files.append(obj_file)
            run(['clang', '-I'+os.path.join(ROOT_DIR, title, header_dir), '-c', source_file, '-o', obj_file])
    
    run(['llvm-ar', 'rc', os.path.join(LIB_DIR, title + '.a')] + obj_files)
    copy_headers(title, header_dir)

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

try:
    shutil.rmtree(os.path.join(ROOT_DIR, 'build'))
except:
    pass

INCLUDE_DIR = mkdir('build', 'include')
LIB_DIR = mkdir('build', 'lib')

build_library('yaml-cpp', 'include', 'src', ['.cpp'])
build_library('fmt', 'include', 'src', ['.cc'])
