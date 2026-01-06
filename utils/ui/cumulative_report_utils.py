#!/usr/bin/env python3
"""
Utility script for managing cumulative Allure reports locally.
Provides commands to clear cumulative results and generate reports.
"""

import sys
import os
from utils.logger import printf
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.ui.allure_helper import AllureHelper

def main():
    if len(sys.argv) < 2:
        printf("Usage: python cumulative_report_utils.py <command>")
        printf("Commands:")
        printf("  clear    - Clear cumulative results")
        printf("  generate - Generate cumulative report")
        printf("  status   - Show cumulative results status")
        return

    command = sys.argv[1].lower()

    if command == "clear":
        AllureHelper.clear_cumulative_results()
    elif command == "generate":
        AllureHelper.generate_cumulative_report()
    elif command == "status":
        cumulative_dir = "Reports/cumulative-results"
        if os.path.exists(cumulative_dir):
            json_files = [f for f in os.listdir(cumulative_dir) if f.endswith('.json')]
            printf(f"Cumulative results directory exists with {len(json_files)} result files")
            if json_files:
                printf("Recent files:")
                for f in sorted(json_files, key=lambda x: os.path.getmtime(os.path.join(cumulative_dir, x)), reverse=True)[:5]:
                    printf(f"  {f}")
        else:
            printf("Cumulative results directory does not exist")
    else:
        printf(f"Unknown command: {command}")

if __name__ == "__main__":
    main()