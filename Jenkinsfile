pipeline {
    agent { label 'jenkins-agent' }

    parameters {
        choice(name: 'ENVIRONMENT', choices: ['stg', 'prod'])
        choice(name: 'TEST_SUITE', choices: [
            'all',
            '00_Login',
            '01_Dashboard',
            '02_Users',
            '03_Program_Type',
            '04_Patient_Groups',
            '05_Activities',
            '06_Workflow_and_Tasks',
            '07_Facility_Availability',
            '09_Scheduled_Appointments',
            '10_Search_Patients',
            '12_Add_Patient',
            '13_User_Dashboard'
        ])
        string(name: 'SINGLE_FEATURE_FILE', defaultValue: '', description: 'Enter single feature file path relative to features/all_features/')
        choice(name: 'PARALLEL_PROCESSES', choices: ['1','2','3','4','5'])
        choice(name: 'PARALLEL_SCHEME', choices: ['feature','scenario'])
        choice(name: 'HEADLESS_MODE', choices: ['true','false'])
        choice(name: 'REPORT_TYPE', choices: ['consolidated', 'current'])
        string(name: 'TEST_TAGS', defaultValue: '')
    }

    environment {
        TMPDIR = "/tmp"
        DISABLE_ALLURE_REPORTS = "true"
    }

    stages {

        stage('Setup') {
            steps {
                checkout scm
                sh 'mkdir -p Reports/screenshots Reports/features configuration'
            }
        }

        // ✅ ONLY ADDITION — restore previous allure results for cumulative
        stage('Restore Previous Allure Results') {
            when { expression { params.REPORT_TYPE == 'consolidated' } }
            steps {
                copyArtifacts(
                    projectName: currentBuild.projectName,
                    selector: lastSuccessful(),
                    filter: 'Reports/cumulative-results/**',
                    target: '.',
                    optional: true
                )
            }
        }

        stage('Inject Config') {
            steps {
                withCredentials([file(credentialsId: 'stg-ngpepv2-config', variable: 'CONFIG_FILE')]) {
                    sh 'cp $CONFIG_FILE configuration/config.ini'
                }
                sh 'cp conf_behavex.cfg .behavex'
            }
        }

        stage('Install Python Deps') {
            steps {
                sh '''
                  python3 -m venv venv
                  venv/bin/pip install --upgrade pip
                  venv/bin/pip install -r requirements.txt
                '''
            }
        }

        stage('Run BehaveX') {
            steps {
                script {

                    def suite = params.TEST_SUITE ?: 'all'

                    def featurePath = params.SINGLE_FEATURE_FILE?.trim()
                        ? "features/all_features/${params.SINGLE_FEATURE_FILE}"
                        : (suite == 'all'
                            ? "features/all_features"
                            : "features/all_features/${suite}")

                    def tagArg = params.TEST_TAGS?.trim()
                        ? "--tags ${params.TEST_TAGS}"
                        : "--tags ~@wip"

                    catchError(buildResult: 'UNSTABLE', stageResult: 'UNSTABLE') {

                        sh """
                          export TMPDIR=/tmp

                          venv/bin/behavex \
                            --config .behavex \
                            --define env=${params.ENVIRONMENT} \
                            --define headless=${params.HEADLESS_MODE} \
                            --parallel-processes ${params.PARALLEL_PROCESSES} \
                            --parallel-scheme ${params.PARALLEL_SCHEME} \
                            ${tagArg} \
                            ${featurePath}
                        """
                    }

                    // ✅ YOUR EXISTING ALLURE HELPER — UNTOUCHED
                    if (params.REPORT_TYPE == 'consolidated') {
                        sh '''
                          venv/bin/python -c "from utils.ui.allure_helper import AllureHelper; AllureHelper.accumulate_results()"
                          venv/bin/python -c "from utils.ui.allure_helper import AllureHelper; AllureHelper.setup_executor_and_environment_info()"
                        '''
                    } else {
                        sh '''
                          venv/bin/python -c "from utils.ui.allure_helper import AllureHelper; AllureHelper.setup_executor_and_environment_info()"
                        '''
                    }
                }
            }
        }

        stage('Publish Allure') {
            steps {
                script {
                    def resultsPath = params.REPORT_TYPE == 'consolidated'
                        ? 'Reports/cumulative-results'
                        : 'Reports/features'

                    allure([
                        includeProperties: false,
                        results: [[path: resultsPath]],
                        reportBuildPolicy: 'ALWAYS'
                    ])
                }
            }
        }
    }

    post {
        always {
            // ✅ ONLY ADDITION — preserve results so next build can accumulate
            archiveArtifacts artifacts: 'Reports/cumulative-results/**', allowEmptyArchive: true
            cleanWs()
        }

        success { echo '✅ All tests passed' }
        unstable { echo '⚠ Some tests failed — cumulative updated' }
        failure { echo '❌ Infrastructure failure' }
    }
}
