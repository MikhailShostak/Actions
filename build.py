import os, subprocess, pathlib

ROOT = os.path.dirname(os.path.abspath(__file__))

def mkdir(*args):
    path = os.path.join(ROOT, *args)
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)
    return path

def run(*args):
    print(' '.join(*args))
    subprocess.run(*args)

def build_library(title, header_dir, source_dir, source_extensions):
    obj_dir = mkdir('build', 'obj', title)
    run(['clang', '-working-directory', obj_dir, '-I'+os.path.join(ROOT, title, header_dir), '-c'] + [os.path.join(ROOT, title, source_dir, e) for e in source_extensions])
    run(['llvm-ar', 'rc', os.path.join(obj_dir, title), os.path.join(obj_dir, '*.o')])

mkdir('build', 'include')
mkdir('build', 'lib')

build_library('yaml-cpp', 'include', 'src', ['*.cpp'])
