# terragit

terragit is a Python package allow access to the GitLab server API , detect changes of each commit and execute terragrunt commands into changed  folders

#### precondition
install python-gitlab package:
``pip install python-gitlab``
#### Installation
``pip install terragit``
#### Start-up

for all commands you need to add  gitlab token  and gitlab url flags in order to access to your private projects: \
{-t} {--gitlab_token } gitlab token wihch allow to access to your gitlab account \
{-u} {--gitlab_url}  gitlab url  : default "https://gitlab.com" \

##### terragit {plan|validate|changes|apply|output}

{-d} {--destroy}: to indicate if it is destroy  make plan a plan destroy and make apply a destroy\
{-c} {--commit_id}: commit id\
{-mrid} { --mr_id}: merge id\
{-dir} {--directory}: directory\
{-p} {--project_id}: project id\
{-v} {-verbose}: to indicate if output will exit on the console  and in log folder too\

##### terragit {docs}

{-p} {--project_id}: project id\
{-m} {--module} : for docs module\
{-l} {--live} : for live infra\
{-o} {--output} : output path : default {"./"}\