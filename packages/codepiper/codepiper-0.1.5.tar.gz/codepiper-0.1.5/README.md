# codepiper 

This tool provides some utilities for working with AWS CodePipeline:

* `watch` - monitor a pipeline for executions and also follow CodeBuild logs
* `rollback`- rollback a stage of a pipeline to a prior execution 

![](codepiper.gif)

# Watch

To monitor all active executions for a pipeline:

`codepiper watch -p my-pipeline-name` 

To monitor a pipeline along with logs from CodeBuild:

`codepiper watch -p my-pipeline-name -f` 

To monitor one specific execution for a pipeline:

`codepiper watch -p my-pipeline-name -e 20b20f00-f63d-4b05-8921-20a4fc16090e` 

# Rollback

To rollback a pipeline stage to last successful execution:

`codepiper rollback -p my-pipeline-name -s Production` 

To rollback a pipeline stage to a specific commit id:

`codepiper rollback -p my-pipeline-name -s Production -c af32c18` 

To rollback a pipeline stage and watch logs

`codepiper rollback -p my-pipeline-name -s Production -f`

# Installation

`pip install codepiper`

# Limitations

* `$CODEBUILD_RESOLVED_SOURCE_VERSION` is unavailable since the CodeBuild execution is not initiated via CodePipeline. The workaround for this is to use [CodePipeline Variables](https://docs.aws.amazon.com/codepipeline/latest/userguide/reference-variables.html) to pass the `CommitId` from source stage as a user defined environment variable to your CodeBuild project.
