import os
import json
import argparse
import datetime
from tqdm import tqdm
from github import Github

ACCESS_TOKEN = os.getenv('GITHUB_TOKEN')
timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

class GitHubIssueCrawler:
    # constructor
    def __init__(self):
        self.outfile = None
    
    def fetch_issues(self, repo_name, state, keywords=None):  
        print(f'Fetching issues from {repo_name}, state: {state}')
          
        # Authenticate with GitHub
        g = Github(ACCESS_TOKEN)
        repo = g.get_repo(repo_name)
        
        # setup output file in case outfile is not provided
        keywords_str = '_'.join(keywords) + '_' if keywords else ''
        self.outfile = f'./notes/{repo_name}_{keywords_str}{timestamp}.md'    # Output file name
        
        # Fetch and filter issues
        all_issues = repo.get_issues(state=state)
        if keywords:
            print(f'Filtering issues by keywords: {keywords}...')
            filtered_issues = [issue for issue in all_issues if any(keyword.lower() in issue.title.lower() or keyword.lower() in (issue.body or "").lower() for keyword in keywords)]
            return filtered_issues
        
        return all_issues

    def save_all_issues_to_single_file(self, issues, args):
        # Ensure the output directory exists
        outfile = args.outfile if args.outfile else self.outfile
        os.makedirs(os.path.dirname(outfile), exist_ok=True)
        
        # Calculate total number of issues for progress bar
        print("Counting number of issues... This may take a while.")
        issue_list = list(issues)
        issue_count = len(issue_list)

        with open(outfile, 'w', encoding='utf-8') as file:
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
    parser = argparse.ArgumentParser(description="Fetch and save GitHub issues based on state and keyword filtering.")
    parser.add_argument("-r", "--repo", help="[owner]/[repo] Name of the repository to fetch issues from. e.g. 'ros2/rclpy'")
    parser.add_argument("-s", "--state", default="closed", choices=['open', 'closed', 'all'], help="State of the issues to fetch: open, closed, or all. Default is 'closed'.")
    parser.add_argument("-k", "--keywords", nargs='+', help="Keywords to filter issues by. If not provided, all issues are fetched.")
    parser.add_argument("-o", "--outfile", help="Optional output file name. Default is '[repo]_[timestamp].md'.")
    args = parser.parse_args()
    
    crawler = GitHubIssueCrawler()
    issues = crawler.fetch_issues(args.repo, args.state, args.keywords)
    issue_count = crawler.save_all_issues_to_single_file(issues, args)
    print(f'{issue_count} issues and their comments have been saved to {crawler.outfile}.')
