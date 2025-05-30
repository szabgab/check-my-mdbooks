import os

checks = {
    "MDBOOK_VERSION": "0.4.44",
    "EMBEDIFY_VERSION": "0.2.12",
    "ALERTS_VERSION": "0.7.0",
}

def check_repo(base_dir, repo_url):


    
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
                for field, expected_value in checks.items():
                    if f" {field}:" in row:
                        row = row.rstrip()
                        value = row.split(":")[-1].strip()
                        if value != expected_value:
                            print(f"Mismatch in {file_name}: field {field}\nexpected value: {expected_value}\n  actual value: {value}")
                            
                        #print(f"field {field} expected value: {expected_value} actual value: {value}")


def main():
    base_dir = os.path.dirname(os.getcwd())
    print(f"base_dir: {base_dir}")
    for repo_url in [
        "https://github.com/szabgab/rust.code-maven.com/"
    ]:
        check_repo(base_dir, repo_url)


main()
