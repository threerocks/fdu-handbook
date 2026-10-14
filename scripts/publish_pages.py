"""Publish the already-reviewed static site to the repository's gh-pages branch."""
from pathlib import Path
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'dist/site'


def git(*arguments, cwd=ROOT, capture=False):
    return subprocess.run(['git', *arguments], cwd=cwd, text=True, check=True,
                          stdout=subprocess.PIPE if capture else None).stdout


if not (SITE / 'index.html').is_file() or not (SITE / 'downloads/fdu-handbook.pdf').is_file():
    raise SystemExit('Build the website and PDF before publishing.')

remote_url = git('remote', 'get-url', 'origin', capture=True).strip()
author_name = git('config', 'user.name', capture=True).strip()
author_email = git('config', 'user.email', capture=True).strip()
existing_branch = git('ls-remote', '--heads', 'origin', 'gh-pages', capture=True).strip()

with tempfile.TemporaryDirectory(prefix='fdu-pages-') as directory:
    checkout = Path(directory)
    git('init', '--initial-branch=gh-pages', cwd=checkout)
    git('config', 'user.name', author_name, cwd=checkout)
    git('config', 'user.email', author_email, cwd=checkout)
    git('remote', 'add', 'origin', remote_url, cwd=checkout)
    if existing_branch:
        git('fetch', '--depth=1', 'origin', 'gh-pages', cwd=checkout)
        git('checkout', '-B', 'gh-pages', 'FETCH_HEAD', cwd=checkout)
    for entry in checkout.iterdir():
        if entry.name != '.git':
            shutil.rmtree(entry) if entry.is_dir() else entry.unlink()
    shutil.copytree(SITE, checkout, dirs_exist_ok=True)
    (checkout / '.nojekyll').touch()
    git('add', '--all', cwd=checkout)
    changes = git('status', '--porcelain', cwd=checkout, capture=True)
    if not changes:
        print('The published site already matches the local build.')
    else:
        source_commit = git('rev-parse', '--short', 'HEAD', capture=True).strip()
        git('commit', '-m', f'Publish handbook site from {source_commit}', cwd=checkout)
        git('push', 'origin', 'HEAD:gh-pages', cwd=checkout)
