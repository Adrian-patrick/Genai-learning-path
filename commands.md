General project workflow:

create a repo on github

clone repo locally : git clone repo_link

start working 

Important commands:

tracking files : git add . or file name

commiting changes : git commit -m "message"

pushing changes to remote : git push origin branch_name

new branch : git branch branch_name

switching branch : git switch branch_name

see remote changes in local(update branch) : git pull origin branch_name

view branches : git branch

view all branches : git branch -a

delete branch : git branch -d branch_name

modify branch name : (first switch to branch) git branch -m new_branch_name

see commit history : git log --oneline

apply old commit or specific commit : git cherry-pick commit_id

return to previous version without commiting : git switch commit_id

check status always : git status

updating main while your in diff branch(only individual branch) : git switch feature_branch -> git rebase main 

before pushing : git pull --rebase origin main

Good practices :

clean commit messages

making small commits 

not commiting secrets

using pull requests

Example workflow :

git checkout main
git pull origin main

git checkout -b feature/new-ui

# work...
git add .
git commit -m "Add new UI layout"

git push origin feature/new-ui






