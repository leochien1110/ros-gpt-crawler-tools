# GitHub Issue Crawler for ChatGPT Bots

This script fetches issues from a GitHub repository and saves them in Markdown format, with support for keyword and state filters. It was initially designed to aid in creating ChatGPT bots that can answer queries based on GitHub issues, aiding in model training.

An example of its application is the [Robo Advisor](https://chat.openai.com/g/g-njWAeq2iF-robo-advisor) bot, trained on ROS 2 repository issues. However, additional data sources may be required for comprehensive model training.

## Features

- Fetch issues from any GitHub repository.
- Filter issues by keywords.
- Select issues based on their state (open, closed, or all).
- Save all relevant issue information, including comments, into a single Markdown file.

## Prerequisites

Before you run this script, you need to have Python installed on your machine. Additionally, you will need a GitHub Personal Access Token with permissions to access repositories.

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/leochien1110/github-issue-crawler.git
   cd github-issue-crawler
   ```
1. Install the required Python libraries:
    ```bash
    pip install -r requirements.txt
    ```

## Generate GitHub Personal Access Token
> :bulb: Without a GitHub access token, you will be limited to a lower rate limit for API requests.
Generate a personal access token from your GitHub account:

Go to **GitHub** -> **Settings** -> **Developer settings** -> **Personal access tokens** -> **Generate new token**.
Make sure to select the scopes or permissions you want to grant this token, such as repo for repository access. If you're unsure, select public repo.

Copy the generated token and use it in the configuration step. Save this token secure and do not share it publicly.

## Configuration
Edit the config.json file by replacing `your_access_token_here` and `owner/repository` with your personal GitHub access token and the target repository.

```json
{
    "ACCESS_TOKEN": "your_access_token_here",
    "REPO_NAME": "owner/repository"
}
```


## Usage
Run the script using the following command:

```bash
python github_issue_crawler.py --state [open|closed|all] --keywords [keyword1 keyword2 ...] --output [output_file.md]
```
The arguments are all optional:

`-s, --state`: The state of the issues to fetch (open, closed, or all). Default is 'open'.

`-k, --keywords`: A list of keywords to filter the issues. This is optional.

`-o, --output`: The output file where the issues will be saved in Markdown format. Default is 'issues.md'.

By default, the collected document will be saved under `notes/owner/repository_timestamp.md`. The timestamp is added to the filename to avoid overwriting existing files.

## Contributing
Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are greatly appreciated.

1. Fork the Project
2. Create your Feature Branch (git checkout -b feature/AmazingFeature)
3. Commit your Changes (git commit -m 'Add some AmazingFeature')
4. Push to the Branch (git push origin feature/AmazingFeature)
5. Open a Pull Request

> :warning: Don't forget to hide the information in `config.json` before committing your changes.

## License
Distributed under the MIT License. See LICENSE for more information.

Contact
leochien1110@gmail.com

Project Link: https://github.com/leochien1110/github-issue-crawler

