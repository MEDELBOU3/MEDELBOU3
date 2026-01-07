# scripts/calculate_loc.py
import os
import re
import json
import subprocess
from datetime import datetime
from collections import defaultdict

try:
    from github import Github
except ImportError:
    print("ERROR: PyGithub not installed. Install it with: pip install PyGithub")
    exit(1)

# Get GitHub token from environment
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')
USERNAME = 'MEDELBOU3'

# Configuration
MAX_REPOS = 20  # Limit repos to analyze (change to None for all repos)
SKIP_FORKS = True  # Skip forked repositories

def get_all_repositories():
    """Fetch all repositories for the user"""
    try:
        g = Github(GITHUB_TOKEN)
        user = g.get_user(USERNAME)
        repos = list(user.get_repos())
        
        if SKIP_FORKS:
            repos = [repo for repo in repos if not repo.fork]
        
        print(f"Found {len(repos)} repositories")
        return repos
    except Exception as e:
        print(f"Error fetching repositories: {e}")
        return []

def check_cloc_installed():
    """Check if cloc is installed"""
    try:
        result = subprocess.run(['cloc', '--version'], 
                              capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False

def clone_and_analyze_repo(repo):
    """Clone repository and analyze with cloc"""
    repo_name = repo.name
    clone_url = repo.clone_url
    temp_dir = f"temp_{repo_name}"
    
    try:
        # Clone repository (shallow clone for speed)
        print(f"  Cloning {repo_name}...")
        result = subprocess.run(
            ['git', 'clone', '--depth', '1', clone_url, temp_dir],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode != 0:
            print(f"  ⚠️  Failed to clone {repo_name}")
            return None
        
        # Run cloc
        print(f"  Analyzing {repo_name}...")
        result = subprocess.run(
            ['cloc', temp_dir, '--json', '--quiet'],
            capture_output=True,
            text=True,
            timeout=120
        )
        
        if result.returncode == 0 and result.stdout:
            data = json.loads(result.stdout)
            print(f"  ✅ {repo_name}: {data.get('SUM', {}).get('code', 0):,} lines")
            return data
        else:
            print(f"  ⚠️  Error analyzing {repo_name}")
            return None
            
    except subprocess.TimeoutExpired:
        print(f"  ⏱️  Timeout analyzing {repo_name}")
        return None
    except Exception as e:
        print(f"  ❌ Error processing {repo_name}: {e}")
        return None
    finally:
        # Cleanup
        if os.path.exists(temp_dir):
            subprocess.run(['rm', '-rf', temp_dir], capture_output=True)

def aggregate_statistics(all_repo_data):
    """Aggregate statistics from all repositories"""
    total_files = 0
    total_code = 0
    total_blank = 0
    total_comment = 0
    failed_repos = 0
    
    language_stats = defaultdict(lambda: {
        'files': 0,
        'code': 0,
        'comment': 0,
        'blank': 0
    })
    
    repo_loc = []
    
    for repo_name, data in all_repo_data.items():
        if not data or 'SUM' not in data:
            failed_repos += 1
            continue
            
        repo_total = data['SUM']['code']
        repo_loc.append((repo_name, repo_total))
        
        total_files += data['SUM']['nFiles']
        total_code += data['SUM']['code']
        total_blank += data['SUM']['blank']
        total_comment += data['SUM']['comment']
        
        # Aggregate by language
        for lang, stats in data.items():
            if lang not in ['header', 'SUM']:
                language_stats[lang]['files'] += stats['nFiles']
                language_stats[lang]['code'] += stats['code']
                language_stats[lang]['comment'] += stats['comment']
                language_stats[lang]['blank'] += stats['blank']
    
    # Sort
    repo_loc.sort(key=lambda x: x[1], reverse=True)
    sorted_languages = sorted(language_stats.items(), 
                             key=lambda x: x[1]['code'], 
                             reverse=True)
    
    return {
        'total_files': total_files,
        'total_code': total_code,
        'total_blank': total_blank,
        'total_comment': total_comment,
        'language_stats': sorted_languages,
        'repo_loc': repo_loc,
        'total_repos': len(all_repo_data),
        'failed_repos': failed_repos
    }

def generate_markdown_stats(stats):
    """Generate markdown statistics"""
    timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    
    md = f"""
![Total LOC](https://img.shields.io/badge/Total%20LOC-{stats['total_code']:,}-blue?style=for-the-badge)

**Last Updated:** {timestamp} UTC

<details>
<summary>📊 Detailed Statistics</summary>

# LOC Statistics - All Repositories

Generated on: {timestamp} UTC

## Summary Statistics

| Metric | Count |
|--------|-------|
| Total Repositories Processed | {stats['total_repos']} |
| Failed Repositories | {stats['failed_repos']} |
| Total Files | {stats['total_files']:,} |
| Total Lines of Code | {stats['total_code']:,} |
| Total Blank Lines | {stats['total_blank']:,} |
| Total Comment Lines | {stats['total_comment']:,} |


## Top 15 Languages by LOC

| Language | Files | Code Lines | Comment Lines | Blank Lines |
|----------|-------|------------|---------------|-------------|
"""
    
    for lang, data in stats['language_stats'][:15]:
        md += f"| {lang:15} | {data['files']:6} | {data['code']:10,} | {data['comment']:13,} | {data['blank']:11,} |\n"
    
    md += "\n## Top 20 Repositories by LOC\n\n"
    md += "| Repository | Lines of Code |\n"
    md += "|------------|---------------|\n"
    
    for repo_name, loc in stats['repo_loc'][:20]:
        md += f"| {USERNAME}/{repo_name:50} | {loc:13,} |\n"
    
    md += "\n</details>\n"
    
    return md

def update_readme(stats_markdown):
    """Update README.md with new statistics"""
    readme_path = 'README.md'
    
    if not os.path.exists(readme_path):
        print(f"❌ {readme_path} not found!")
        return False
    
    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace content between markers
    pattern = r'<!--START_LOC-->.*?<!--END_LOC-->'
    replacement = f'<!--START_LOC-->\n{stats_markdown}\n<!--END_LOC-->'
    
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    # Check if markers exist
    if '<!--START_LOC-->' not in content:
        print("⚠️  Warning: LOC markers not found in README.md")
        print("Add the following to your README.md:")
        print("<!--START_LOC-->")
        print("<!--END_LOC-->")
        return False
    
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("✅ README.md updated successfully!")
    return True

def main():
    """Main function"""
    print("=" * 60)
    print(f"📊 Starting LOC calculation for {USERNAME}")
    print("=" * 60)
    
    # Check prerequisites
    if not GITHUB_TOKEN:
        print("❌ GITHUB_TOKEN environment variable not set!")
        print("Set it with: export GITHUB_TOKEN='your_token_here'")
        return
    
    if not check_cloc_installed():
        print("❌ cloc is not installed!")
        print("Install it with:")
        print("  - Ubuntu/Debian: sudo apt-get install cloc")
        print("  - macOS: brew install cloc")
        print("  - Windows: choco install cloc")
        return
    
    # Get all repositories
    repos = get_all_repositories()
    if not repos:
        print("❌ No repositories found!")
        return
    
    # Limit repos if configured
    if MAX_REPOS:
        repos = repos[:MAX_REPOS]
        print(f"⚙️  Limited to {MAX_REPOS} repositories")
    
    print(f"\n📦 Processing {len(repos)} repositories...\n")
    
    # Analyze each repository
    all_repo_data = {}
    for i, repo in enumerate(repos, 1):
        print(f"[{i}/{len(repos)}] {repo.name}")
        data = clone_and_analyze_repo(repo)
        if data:
            all_repo_data[repo.name] = data
        print()
    
    if not all_repo_data:
        print("❌ No repositories were successfully analyzed!")
        return
    
    print("=" * 60)
    print("📈 Aggregating statistics...")
    print("=" * 60)
    
    # Aggregate statistics
    stats = aggregate_statistics(all_repo_data)
    
    # Print summary
    print(f"\n✅ Analysis complete!")
    print(f"   Total LOC: {stats['total_code']:,}")
    print(f"   Repositories: {stats['total_repos']}")
    print(f"   Languages: {len(stats['language_stats'])}")
    
    # Generate markdown
    stats_markdown = generate_markdown_stats(stats)
    
    # Update README
    print("\n📝 Updating README.md...")
    if update_readme(stats_markdown):
        print("\n🎉 LOC calculation completed successfully!")
    else:
        print("\n⚠️  LOC calculation completed but README update failed")
        print("Generated statistics:\n")
        print(stats_markdown)

if __name__ == '__main__':
    main()