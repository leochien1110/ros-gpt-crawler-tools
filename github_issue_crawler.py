import os
import json
import argparse
import datetime
from tqdm import tqdm
from github import Github

# Load configuration
with open('config.json', 'r') as config_file:
    config = json.load(config_file)
ACCESS_TOKEN = config['ACCESS_TOKEN']
REPO_NAME = config['REPO_NAME']
timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
OUTPUT_FILE = './notes/'+REPO_NAME+'_'+timestamp+'.md'    # Output file name

def parse_args():
    parser = argparse.ArgumentParser(description="Fetch and save GitHub issues based on state and keyword filtering.")
    # help message: python github_issue_crawler.py -k "bug" "feature" -s "open" -o "output.md"
    parser.add_argument("-k", "--keywords", nargs='+', help="Keywords to filter issues by. If not provided, all issues are fetched.")
    parser.add_argument("-s", "--state", default="open", choices=['open', 'closed', 'all'], help="State of the issues to fetch: open, closed, or all. Default is 'open'.")
    parser.add_argument("-o", "--output", default=OUTPUT_FILE, help="Output file path. Default is './<repo_name>_<timestamp>.md'.")
    return parser.parse_args()


def fetch_issues(repo_name, state, keywords=None):
    # Authenticate with GitHub
    g = Github(ACCESS_TOKEN)
    repo = g.get_repo(repo_name)
    
    # Fetch and filter issues
    all_issues = repo.get_issues(state=state)
    if keywords:
        filtered_issues = [issue for issue in all_issues if any(keyword.lower() in issue.title.lower() or keyword.lower() in (issue.body or "").lower() for keyword in keywords)]
        return filtered_issues
    return all_issues


def save_all_issues_to_single_file(issues):
    # Ensure the output directory exists
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    
    # Calculate total number of issues for progress bar
    print("Counting number of issues... This may take a while.")
    issue_list = list(issues)
    issue_count = len(issue_list)

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as file:
        file.write("# GitHub Issues\n\n")
        file.write(f"## State: {args.state}\n\n")
        if args.keywords:
            file.write(f"## Keywords: {', '.join(args.keywords)}\n\n")
        
        for issue in tqdm(issue_list, total=issue_count, desc="Parsing issues", unit="issue"):
            issue_body = issue.body if issue.body is not None else 'No description provided.'
            file.write(f"## Issue #{issue.number}: {issue.title}\n\n")
            file.write(f"### Created at: {issue.created_at}\n\n")
            file.write("### Body:\n")
            file.write(issue_body + "\n\n")
            
            comments = issue.get_comments()
            if comments.totalCount > 0:
                file.write("### Comments:\n\n")
                for comment in comments:
                    comment_body = comment.body if comment.body is not None else 'No comment provided.'
                    file.write(f"#### {comment.user.login} commented at {comment.created_at}:\n\n")
                    file.write(comment_body + "\n\n")
            else:
                file.write("### Comments:\n\nNo comments.\n\n")
                
    return issue_count

if __name__ == "__main__":
    args = parse_args()
    issues = fetch_issues(REPO_NAME, args.state, args.keywords)
    issue_count = save_all_issues_to_single_file(issues)
    print(f'{issue_count} issues and their comments have been saved to {OUTPUT_FILE}.')