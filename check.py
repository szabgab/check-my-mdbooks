import os

CHECKS = {
    "MDBOOK_VERSION": "0.4.51",   # https://github.com/rust-lang/mdBook/
    "EMBEDIFY_VERSION": "0.2.13", # https://github.com/MR-Addict/mdbook-embedify/
    "ALERTS_VERSION": "0.7.0",    # https://github.com/lambdalisue/rs-mdbook-alerts
    "LINKCHECK_VERSION": "0.7.7", # https://github.com/Michael-F-Bryan/mdbook-linkcheck
}

REPOS =[
        "https://github.com/szabgab/rust.code-maven.com/",
        "https://github.com/szabgab/mdbook.code-maven.com/",
        "https://github.com/szabgab/mdbooks.code-maven.com/",
        "https://github.com/szabgab/rust-he.code-maven.com/",
        "https://github.com/szabgab/python-he.code-maven.com/",
        "https://github.com/szabgab/c.code-maven.com/",
        "https://github.com/szabgab/exercises.code-maven.com/",
        "https://github.com/szabgab/git.code-maven.com/",
        "https://github.com/szabgab/git-he.code-maven.com/",
        "https://github.com/szabgab/groovy.code-maven.com/",
        "https://github.com/szabgab/he.code-maven.com/",
        "https://github.com/szabgab/ruby.code-maven.com/",
        "https://github.com/szabgab/web3.code-maven.com/",
        "https://github.com/szabgab/axum/",
]


def check_repo(base_dir, repo_url):
    print("-----")
    errors = 0

    
    print(f"repo_url: {repo_url}")
    repo_url = repo_url.rstrip("/")
    repo_name = repo_url.split("/")[-1]
    print(f"repo_name: {repo_name}")

    ci = os.environ.get("CI")
    print(f"CI: {ci}")
    if ci:
        result = os.system(f"git clone --depth 1 {repo_url}")
        print(f"git clone result: {result}")
        workflows_dir = os.path.join(repo_name, ".github", "workflows")
    else:
        workflows_dir = os.path.join(base_dir, repo_name, ".github", "workflows")


    print(f"workflows_dir: {workflows_dir}")
    for file_name in os.listdir(workflows_dir):
        file_path = os.path.join(workflows_dir, file_name)
        with open(file_path) as fh:
            for row in fh:
                for field, expected_value in CHECKS.items():
                    if f" {field}:" in row:
                        row = row.rstrip()
                        value = row.split(":")[-1].strip()
                        if value != expected_value:
                            print(f"Mismatch in {file_name}: field {field}\nexpected value: {expected_value}\n  actual value: {value}")
                            errors  += 1
                            
                        #print(f"field {field} expected value: {expected_value} actual value: {value}")
    return errors


def main():
    base_dir = os.path.dirname(os.getcwd())
    print(f"base_dir: {base_dir}")
    errors = 0
    for repo_url in REPOS:
        errors += check_repo(base_dir, repo_url)

    print("--------------------")
    if errors > 0:
        print(f"Found {errors} errors")
        exit(errors)
    else:
        print("Everything looks fine")

main()
