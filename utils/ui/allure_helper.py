import os
import base64
import allure
import shutil
import subprocess
import platform
import json
from datetime import datetime
from allure_commons.types import AttachmentType

from utils.logger import printf
from utils.utils import get_current_time
from utils.ui.config_reader import is_allure_enabled


class AllureHelper:
    ALLURE_RESULTS_DIR = "Reports/features"
    CUMULATIVE_RESULTS_DIR = "Reports/cumulative-results"

    @staticmethod
    def assign_feature_suite(context, feature):
        """Assign parent suite from folder name (for reference - tags must be in Gherkin for Allure Behave)."""
        # Determine parentSuite from folder
        feature_path = feature.filename
        folder_name = os.path.basename(os.path.dirname(feature_path))
        parts = folder_name.split('_')
        if len(parts) > 1 and parts[0].isdigit():
            parent_suite = ''.join(word.capitalize() for word in parts[1:])
        else:
            parent_suite = folder_name.replace('_', '').title()

        feature.tags.append(f"allure.label.parentSuite:{parent_suite}")

        # Store for reference
        feature.parent_suite = parent_suite

    @staticmethod
    def assign_scenario_suite(context, scenario):
        """Assign suite labels (for reference - tags must be in Gherkin for Allure Behave)."""
        # ParentSuite is always from feature (folder)
        parent_suite = getattr(scenario.feature, 'parent_suite', 'DefaultSuite')

        # Determine suite from scenario tags
        if 'smoke' in scenario.tags:
            suite = 'smoke'
        elif 'regression' in scenario.tags:
            suite = 'regression'
        else:
            # Check for other tags (excluding allure tags)
            other_tags = [tag for tag in scenario.tags if not tag.startswith('allure.')]
            if other_tags:
                suite = other_tags[0]  # Use first non-allure tag
            else:
                suite = 'regression'  # Default

        sub_suite = scenario.name.strip().replace(' ', '_')
        
        scenario.tags.append(f"allure.label.parentSuite:{parent_suite}")
        scenario.tags.append(f"allure.label.suite:{suite}")
        scenario.tags.append(f"allure.label.subSuite:{sub_suite}")

    @staticmethod
    def assign_scenario_tags_for_feature(context, feature):
        """Assign Allure suite labels for all scenarios in a feature."""
        for scenario in feature.scenarios:
            # ParentSuite is always from feature (folder)
            parent_suite_sc = getattr(scenario.feature, 'parent_suite', 'DefaultSuite')

            # Determine suite from scenario tags
            if 'smoke' in scenario.tags:
                suite = 'Smoke'
            elif 'regression' in scenario.tags:
                suite = 'Regression'
            else:
                # Check for other tags (excluding allure tags)
                other_tags = [tag for tag in scenario.tags if not tag.startswith('allure.')]
                if other_tags:
                    suite = other_tags[0].capitalize()  # Capitalize first non-allure tag
                else:
                    suite = 'Regression'  # Default

            sub_suite = scenario.name.strip().replace(' ', '_')

            scenario.tags.append(f"allure.label.parentSuite:{parent_suite_sc}")
            scenario.tags.append(f"allure.label.suite:{suite}")
            scenario.tags.append(f"allure.label.subSuite:{sub_suite}")

    @staticmethod
    def attach_failure(driver, step):
        """Attach screenshot + URL if a step fails."""
        if step.status != 'failed':
            return

        current_url, screenshot_png = None, None
        try:
            current_url = driver.current_url
            screenshot_png = driver.get_screenshot_as_png()
        except Exception as e:
            printf(f"Failed to retrieve current URL during failure attachment: {e}")

        try:
            if screenshot_png and current_url:
                base64_image = base64.b64encode(screenshot_png).decode('utf-8')
                html_content = f"""
                    <div>
                        <p><strong>Current URL:</strong>
                        <a href="{current_url}" target="_blank">{current_url}</a></p>
                        <img src="data:image/png;base64,{base64_image}"
                        alt="Screenshot" style="max-width: 100%; height: auto;">
                    </div>
                """
                allure.attach(html_content, name=f"failed_step_{get_current_time()}",
                              attachment_type=AttachmentType.HTML)
            elif screenshot_png:
                allure.attach(screenshot_png, name=f"failed_step_{get_current_time()}",
                              attachment_type=AttachmentType.PNG)
            elif current_url:
                allure.attach(f"Current URL: {current_url}",
                              name=f"failed_step_{get_current_time()}_url.txt",
                              attachment_type=AttachmentType.TEXT)
        except Exception as e:
            printf(f"Allure attachment failed (likely in CI environment): {e}")

    @staticmethod
    def merge_history(allure_results_dir, allure_report_dir):
        """Preserve allure history between runs."""
        history_src = os.path.join(allure_report_dir, 'history')
        history_dst = os.path.join(allure_results_dir, 'history')

        if os.path.exists(history_src):
            os.makedirs(allure_results_dir, exist_ok=True)
            if os.path.exists(history_dst):
                for item in os.listdir(history_src):
                    s = os.path.join(history_src, item)
                    d = os.path.join(history_dst, item)
                    if os.path.isdir(s):
                        shutil.copytree(s, d, dirs_exist_ok=True)
                    else:
                        shutil.copy2(s, d)
            else:
                shutil.copytree(history_src, history_dst)

    @staticmethod
    def setup_allure_folders():
        """Create necessary folders for Allure reporting."""
        if not is_allure_enabled():
            printf("Allure reporting is disabled - skipping folder setup")
            return

        try:
            os.makedirs("Reports", exist_ok=True)
            os.makedirs(AllureHelper.ALLURE_RESULTS_DIR, exist_ok=True)
            printf("Allure folders created successfully")

            # Generate executor and environment info for local runs
            AllureHelper.setup_executor_and_environment_info()
        except Exception as e:
            printf(f"Exception occurred while creating Allure folders: {e}")

    @staticmethod
    def setup_executor_and_environment_info():
        """Generate executor.json and environment.properties files for Allure reporting."""

        try:
            # Use cumulative-results for Jenkins, features for local
            results_dir = AllureHelper.CUMULATIVE_RESULTS_DIR if os.getenv("JENKINS_HOME") else AllureHelper.ALLURE_RESULTS_DIR
            os.makedirs(results_dir, exist_ok=True)

            # --- Executor Info --- (skip for Jenkins as it's auto-generated)
            if not os.getenv("JENKINS_HOME"):
                executor_info = {
                    "name": platform.node(),  # system/computer hostname
                    "type": "local",
                    "buildName": f"Run {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                    "buildOrder": "1",
                    "buildUrl": "",
                    "reportName": "Allure Report - Local",
                }

                with open(os.path.join(results_dir, "executor.json"), "w", encoding="utf-8") as f:
                    json.dump(executor_info, f, indent=2)

            # --- Environment Info ---
            env_info = {
                "OS": platform.system(),
                "OS Version": platform.version(),
                "Platform": platform.platform(),
                "Processor": platform.processor(),
                "Python Version": platform.python_version(),
            }

            # Add Jenkins-specific environment info
            if os.getenv("JENKINS_HOME"):
                jenkins_env = {
                    "Jenkins.Build.Number": os.getenv("BUILD_NUMBER", ""),
                    "Jenkins.Job.Name": os.getenv("JOB_NAME", ""),
                    "Jenkins.Build.URL": os.getenv("BUILD_URL", ""),
                    "Jenkins.Environment": os.getenv("CI_ENVIRONMENT", ""),
                    "Jenkins.Headless": os.getenv("HEADLESS_MODE", ""),
                    "Jenkins.Timestamp": os.getenv("TIMESTAMP", ""),
                }
                env_info.update(jenkins_env)

            with open(os.path.join(results_dir, "environment.properties"), "w", encoding="utf-8") as f:
                for k, v in env_info.items():
                    f.write(f"{k}={v}\n")

            printf("Executor and environment information files generated successfully")
        except Exception as e:
            printf(f"Exception occurred while generating executor/environment info: {e}")

    @staticmethod
    def accumulate_results():
        """Accumulate current run results (JSON + attachments) into cumulative directory."""
        try:
            current_results_dir = AllureHelper.ALLURE_RESULTS_DIR
            cumulative_dir = AllureHelper.CUMULATIVE_RESULTS_DIR

            os.makedirs(cumulative_dir, exist_ok=True)

            copied_count = 0
            if os.path.exists(current_results_dir):
                for file in os.listdir(current_results_dir):
                    src = os.path.join(current_results_dir, file)
                    dst = os.path.join(cumulative_dir, file)
                    if os.path.isfile(src):
                        shutil.copy2(src, dst)
                        copied_count += 1

            printf(f"Accumulated {copied_count} result & attachment files into cumulative directory")
            return True
        except Exception as e:
            printf(f"Error accumulating results: {e}")
            return False

    @staticmethod
    def clear_cumulative_results():
        """Clear the cumulative result's directory."""
        try:
            cumulative_dir = AllureHelper.CUMULATIVE_RESULTS_DIR
            if os.path.exists(cumulative_dir):
                shutil.rmtree(cumulative_dir)
                printf("Cumulative results cleared")
            else:
                printf("Cumulative results directory does not exist")
            return True
        except Exception as e:
            printf(f"Error clearing cumulative results: {e}")
            return False

    @staticmethod
    def generate_cumulative_report():
        """Generate Allure report from cumulative results with history."""
        if not is_allure_enabled():
            printf("Allure reporting is disabled - skipping cumulative report generation")
            return

        try:
            cumulative_dir = AllureHelper.CUMULATIVE_RESULTS_DIR
            allure_report_dir = "Reports/allure-report"

            # Ensure cumulative directory exists and has results
            if not os.path.exists(cumulative_dir):
                printf("No cumulative results found - run tests first")
                return

            json_files = [f for f in os.listdir(cumulative_dir) if f.endswith('.json')]
            if not json_files:
                printf("No result files in cumulative directory")
                return

            # Merge history
            AllureHelper.merge_history(cumulative_dir, allure_report_dir)

            cmd = f"allure generate {cumulative_dir} -o {allure_report_dir} --clean"
            printf(f"Generating cumulative Allure report with command: {cmd}")
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

            if result.returncode == 0:
                printf("Cumulative Allure report generated successfully")
                printf(f"View the report by running: allure open {allure_report_dir}")
                printf(f"Report includes {len(json_files)} test results from accumulated runs")
            else:
                printf(f"Error generating cumulative Allure report: {result.stderr}")
                printf(f"Command output: {result.stdout}")
        except Exception as e:
            printf(f"Exception occurred while generating cumulative Allure report: {e}")

    @staticmethod
    def generate_report():
        """Run allure generate command (legacy method for backward compatibility)."""
        if not is_allure_enabled():
            printf("Allure reporting is disabled - skipping report generation")
            return

        try:
            allure_results_dir = AllureHelper.ALLURE_RESULTS_DIR
            allure_report_dir = "Reports/allure-report"
            AllureHelper.merge_history(allure_results_dir, allure_report_dir)

            cmd = f"allure generate {allure_results_dir} -o {allure_report_dir} --clean"
            printf(f"Generating Allure report with command: {cmd}")
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

            if result.returncode == 0:
                printf("Allure report generated successfully")
                printf(f"View the report by running: allure open {allure_report_dir}")
            else:
                printf(f"Error generating Allure report: {result.stderr}")
                printf(f"Command output: {result.stdout}")
        except Exception as e:
            printf(f"Exception occurred while generating Allure report: {e}")