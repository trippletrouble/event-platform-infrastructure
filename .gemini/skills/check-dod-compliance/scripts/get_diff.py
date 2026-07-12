import subprocess
import sys
import os
import argparse

def run_git_cmd(args, cwd=None):
    try:
        res = subprocess.run(['git'] + args, capture_output=True, text=True, check=True, cwd=cwd)
        return res.stdout.strip()
    except subprocess.CalledProcessError as e:
        # Don't print error if it's just checking if inside work tree
        if args != ['rev-parse', '--is-inside-work-tree']:
            print(f"Error running git {' '.join(args)} in {cwd or '.'}: {e.stderr.strip()}", file=sys.stderr)
        return None

def get_base_branch(cwd=None):
    # Get list of remote branches
    remote_branches = run_git_cmd(['branch', '-r'], cwd=cwd)
    if remote_branches:
        branches = [b.strip() for b in remote_branches.split('\n')]
        candidates = [
            'origin/develop',
            'origin/developer',
            'origin/master',
            'origin/main'
        ]
        for candidate in candidates:
            if any(candidate in b for b in branches):
                return candidate
                
    # Fallback to local branches
    local_branches = run_git_cmd(['branch'], cwd=cwd)
    if local_branches:
        branches = [b.replace('*', '').strip() for b in local_branches.split('\n')]
        candidates = ['develop', 'developer', 'master', 'main']
        for candidate in candidates:
            if candidate in branches:
                return candidate
                
    return 'origin/develop' # default fallback

def get_repo_changes(repo_path, base_branch_arg=None):
    if not run_git_cmd(['rev-parse', '--is-inside-work-tree'], cwd=repo_path or None):
        return []
        
    base_branch = base_branch_arg or get_base_branch(repo_path or None)
    print(f"Analyzing repository at '{repo_path or '.'}' against base: {base_branch}")
    
    diff_output = run_git_cmd(['diff', '--name-status', f"{base_branch}...HEAD"], cwd=repo_path or None)
    
    # Also include local uncommitted/unstaged changes
    status_output = run_git_cmd(['status', '--porcelain'], cwd=repo_path or None)
    
    files_map = {} # path -> status
    
    if diff_output:
        for line in diff_output.split('\n'):
            if not line.strip():
                continue
            parts = line.split('\t')
            if len(parts) >= 2:
                status = parts[0]
                filepath = parts[-1]
                files_map[filepath] = status
                
    if status_output:
        for line in status_output.split('\n'):
            if not line.strip():
                continue
            status_part = line[:2].strip()
            filepath = line[3:].strip()
            # If renamed, parse correctly (e.g. "old -> new" or just "new")
            if " -> " in filepath:
                filepath = filepath.split(" -> ")[-1].strip()
            
            files_map[filepath] = files_map.get(filepath, status_part or 'M')
            
    files = []
    for filepath, status in files_map.items():
        full_path = os.path.join(repo_path or '', filepath)
        # Check if this path is a submodule (is a directory containing .git)
        if os.path.isdir(full_path) and os.path.exists(os.path.join(full_path, '.git')):
            print(f"Detected git submodule: {filepath}")
            sub_changes = get_repo_changes(full_path, base_branch_arg)
            for sub_f in sub_changes:
                files.append({
                    'status': sub_f['status'],
                    'path': os.path.join(filepath, sub_f['path']).replace('\\', '/')
                })
        else:
            files.append({
                'status': status,
                'path': filepath.replace('\\', '/')
            })
            
    return files

def main():
    parser = argparse.ArgumentParser(description="Get changed files against a target branch including submodules")
    parser.add_argument('--base', help="Base branch to compare against (e.g. origin/develop)")
    args = parser.parse_args()
    
    files = get_repo_changes('', args.base)
    
    # Filter and categorize files
    frontend_exts = {'.ts', '.tsx', '.js', '.jsx', '.css', '.scss', '.html'}
    
    frontend_files = []
    other_files = []
    
    for f in files:
        _, ext = os.path.splitext(f['path'])
        # If the file is under a frontend/ directory or has frontend extension
        is_frontend = 'frontend/' in f['path'] or ext in frontend_exts
        if is_frontend:
            frontend_files.append(f)
        else:
            other_files.append(f)
            
    print("\n--- Changed Files Summary ---")
    print(f"Total modified files: {len(files)}")
    print(f"Frontend files: {len(frontend_files)}")
    print(f"Backend/Other files: {len(other_files)}")
    
    print("\n[Frontend Files]")
    for f in frontend_files:
        print(f"  [{f['status']}] {f['path']}")
        
    print("\n[Backend/Other Files]")
    for f in other_files:
        print(f"  [{f['status']}] {f['path']}")

if __name__ == '__main__':
    main()
