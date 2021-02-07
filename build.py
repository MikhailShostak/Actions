import os, subprocess, pathlib

def mkdir(*args):
    path = os.path.join(ROOT_DIR, *args)
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)
    return path

def run(*args):
    print(' '.join(*args))
    subprocess.run(*args)

def build_library(title, header_dir, source_dir, source_extensions):
    obj_dir = mkdir('build', 'obj', title)
    run(['clang', '-working-directory', obj_dir, '-I'+os.path.join(ROOT_DIR, title, header_dir), '-c'] + [os.path.join(ROOT_DIR, title, source_dir, e) for e in source_extensions])
    run(['llvm-ar', 'rc', os.path.join(LIB_DIR, title), os.path.join(obj_dir, '*.o')])

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
INCLUDE_DIR = mkdir('build', 'include')
LIB_DIR = mkdir('build', 'lib')

build_library('yaml-cpp', 'include', 'src', ['*.cpp'])
build_library('fmt', 'include', 'src', ['*.cc'])
