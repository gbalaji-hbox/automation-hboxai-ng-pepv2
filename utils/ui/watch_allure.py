import os
from livereload.server import Server

REPORT_DIR = "Reports/allure-report"


def main():
    # Skip if CI/CD
    if os.getenv("GITHUB_ACTIONS") or os.getenv("JENKINS_HOME") or os.getenv("JENKINS_HOME"):
        print("CI/CD detected. Not starting live reload.")
        return

    server = Server()
    server.watch(f"{REPORT_DIR}/**/*")  # Watch regenerated report
    print("Starting live reload at http://localhost:8084")
    server.serve(root=REPORT_DIR, port=8084, restart_delay=1, open_url_delay=1)


if __name__ == "__main__":
    main()
