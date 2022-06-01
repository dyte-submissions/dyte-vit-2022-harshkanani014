import csv
from github import Github
import json
from progress.bar import Bar
from progress.bar import FillingSquaresBar
from progress.spinner import PieSpinner
import click
from pyfiglet import Figlet


# Function to check dependency version of nodeJS packages
# return : List
def nodejs_dependancy_version_checker(repo, dependency_name, repos, repo_link, version):
    '''
    return : List[]
    '''
    contents = repo.get_contents("package.json") # get content of package.json
    decoded_content = contents.decoded_content # decode content into readable form
    json_content = json.loads(decoded_content) # convert decoded content into json format
    dependencies = json_content['dependencies']
    # check if required dependencies present in File 
    if dependency_name not in dependencies:
        ans = [repos, repo_link, "No Dependacy found", "No version found", "No version found"]

    else:
        if dependencies[dependency_name][1:] >= version:
            ans = [repos, repo_link, dependency_name ,dependencies[dependency_name][1:], True]
        else:
            ans = [repos, repo_link, dependency_name,dependencies[dependency_name][1:], False]
    return ans

# Function to check dependency version of nodeJS packages
# return : List
def python_dependancy_version_checker(repo, dependency_name, repos, repo_link, version):
    '''
    return : List[]
    '''
    contents = repo.get_contents("requirements.txt")
    decoded_content = contents.decoded_content
    str_content = decoded_content.decode('utf-8').split() # convert decoded content into st format
    for library in str_content:
        split_index = library.index("=")
        python_library = library[:split_index]
        python_library_version = library[split_index+2:]
        if python_library==dependency_name:
            if python_library_version >= version:
                ans = [repos, repo_link, python_library , python_library_version, True]
            else:
                ans = [repos, repo_link, python_library , python_library_version, False]
            return ans
    return [repos, repo_link, "No Dependacy found", "No version found", "No version found"]


@click.group()
def messages():
  pass


# Set commands and argument for 
@click.command('check')
@click.option('--input_file', '-i')
@click.option('--dependancy_names', '-d', multiple=True)
def check_dependancy_versions(input_file, dependancy_names):
    f = Figlet(font='slant')
    print(f.renderText('Dyte SDK tool'))
    bar = FillingSquaresBar('Processing', max=23)
    # using an access token
    print("How to generate Github Token? Visit link: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token")
    print()
    github_token = input("Enter your Github token : ")
    
    g = Github(github_token)
    output_file = open("output.csv", "w")
    input_file = open(input_file, "r")
    writer = csv.writer(output_file)
    reader = csv.reader(input_file)
    line_count = 0
    data = {}
    for row in reader:
        bar.next()
        print(" " + row[0] + "File Processing")
        if line_count==0:
            pass
        else:
            data.update({row[0]:row[1]})
        line_count += 1
    # print(data)
    print("Total rows processed ", line_count)
            
    header = ["repo", "repo link", "dependacy_name", "version", "version_satisfied"]
    writer.writerow(header)
    # dependency_args = ["axios@0.23.0", "dyte-client@0.36.1", "typescript@4.1.2", "Django@4.0.1"]
    dependency_args = dependancy_names
    for each_dependecy in dependency_args:
        dependency = each_dependecy
        bar.next()
        print(" " + each_dependecy)
        # spinner.next()
        split_index = dependency.index("@")
        dependency_name = dependency[:split_index]
        version = dependency[split_index+1:]
        for repos in data:
            bar.next()
            print(" " + "Repo clone in process")
            repo_link = data[repos]
            if "/"==repo_link[-1]:
                repo_link = repo_link[19:len(repo_link)-1]
            else:
                repo_link = repo_link[19:]
            repo = g.get_repo(repo_link)
            try:
                bar.next()
                print(" checking nodejs package.json")
                result = nodejs_dependancy_version_checker(repo, dependency_name, repos, repo_link, version)
                print(result)
                writer.writerow(result)
            except:
                bar.next()
                print(' checking python requirements.txt')
                try:
                    result = python_dependancy_version_checker(repo, dependency_name, repos, repo_link, version)
                    writer.writerow(result)
                except:
                    print("File Not Found")
    print()
    print("Process completed.... 100%")
    print("output.csv file generated")
    bar.finish()

@click.command('update')
@click.option('--input_file', '-i')
@click.option('--dependancy_names', '-d', multiple=True)
def update_dependacy_version(input_file, dependancy_names):
    f = Figlet(font='slant')
    print(f.renderText('Dyte SDK tool'))
    spinner = PieSpinner('Loading ')
    bar = FillingSquaresBar('Processing', max=23)
    # using an access token
    print("How to generate Github? Visit link: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token")
    print()
    github_token = input("Enter your Github token : ")
   
    g = Github(github_token)
    output_file = open("updated_output.csv", "w")
    input_file = open(input_file, "r")
    writer = csv.writer(output_file)
    reader = csv.reader(input_file)
    line_count = 0
    data = {}
    for row in reader:
        bar.next()
        print(" " + row[0] + "File Processing")
        if line_count==0:
            pass
        else:
            data.update({row[0]:row[1]})
        line_count += 1
    # print(data)
    print("Total rows processed ", line_count)
            
    header = ["repo", "repo link", "dependacy_name", "version", "version_satisfied", "update_pr"]
    writer.writerow(header)
    # dependency_args = ["axios@0.23.0", "dyte-client@0.36.1", "typescript@4.1.2", "Django@4.0.1"]
    dependency_args = dependancy_names
    for each_dependecy in dependency_args:
        dependency = each_dependecy
        bar.next()
        print(" " + each_dependecy)
        # spinner.next()
        split_index = dependency.index("@")
        dependency_name = dependency[:split_index]
        version = dependency[split_index+1:]
        # print(dependency_name)
        for repos in data:
            bar.next()
            print(" Repo clone in process")
            repo_link = data[repos]
            if "/"==repo_link[-1]:
                repo_link = repo_link[19:len(repo_link)-1]
            else:
                repo_link = repo_link[19:]
            repo = g.get_repo(repo_link)
            try:
                bar.next()
                print(" checking nodejs package.json")
                result = nodejs_dependancy_version_checker(repo, dependency_name, repos, repo_link, version)
                if result[4]==False:
                    bar.next()
                    print(" creating PR request for " + repo_link)
                    github_user = g.get_user()
                    myfork = github_user.create_fork(repo)
                    sb = repo.get_branch('main')
                    try:
                        myfork.create_git_ref(ref='refs/heads/dependancy-update', sha=sb.commit.sha)
                    except:
                        pass
                    contents = myfork.get_contents("package.json", ref='dependancy-update')
                    decoded_content = contents.decoded_content
                    json_content = json.loads(decoded_content) # convert decoded content into json format
                    json_content['dependencies'][dependency_name] = "^"+version
                    new_content = json.dumps(json_content, indent=3)
                    pr  = myfork.update_file(contents.path, "update dependacy", new_content, contents.sha, branch="dependancy-update")

                    # updating dependency version in package-lock.json
                    contents = myfork.get_contents("package-lock.json", ref='dependancy-update')
                    decoded_content = contents.decoded_content
                    json_content = json.loads(decoded_content) # convert decoded content into json format
                    json_content['dependencies'][dependency_name] = "^"+version
                    new_content = json.dumps(json_content, indent=3)
                    pr  = myfork.update_file(contents.path, "update dependacy", new_content, contents.sha, branch="dependancy-update")
                    try:
                        pr = repo.create_pull(title="chore: updates " + dependency_name + " to " + version, 
                                                            body="Updates the version of " + dependency_name +  " from " + result[3] + " to " + version, 
                                                            head="harshkanani014:dependancy-update", 
                                                            base="main",
                                                            )
                        pr_request = pr.html_url
                        result.append(pr_request)
                    except:
                        result.append('')

                else:
                    result.append('')
                print(result)
                writer.writerow(result)
            except:
                try:
                    bar.next()
                    print(" checking python requirements.txt")
                    result = python_dependancy_version_checker(repo, dependency_name, repos, repo_link, version)
                    # print(ans)
                    if result[4]==False:
                        bar.next()
                        print(" creating PR request for " + repo_link)
                        github_user = g.get_user()
                        myfork = github_user.create_fork(repo)
                        try:
                            sb = repo.get_branch('main')
                        except:
                            sb = repo.get_branch('master')
                        try:
                            myfork.create_git_ref(ref='refs/heads/dependancy-update', sha=sb.commit.sha)
                        except:
                            pass
                        contents = myfork.get_contents("requirements.txt", ref='dependancy-update')
                        decoded_content = contents.decoded_content
                        str_content = decoded_content.decode('utf-8').split()
                        for libs in range(len(str_content)):
                            if str_content[libs]==dependency_name:
                                str_content[libs] = dependency_name+"=="+version
                                break
                        new_content = "\n".join(str_content)
                        pr  = myfork.update_file(contents.path, "update dependacy", new_content, contents.sha, branch="dependancy-update")
                        try:
                            pr = repo.create_pull(title="chore: updates " + dependency_name + " to " + version, 
                                                                body="Updates the version of " + dependency_name +  " from " + result[3] + " to " + version, 
                                                                head="harshkanani014:dependancy-update", 
                                                                base="master",
                                                                )
                            pr_request = pr.html_url
                            result.append(pr_request)
                        except:
                            result.append('')
                    else:
                        result.append('')
                    writer.writerow(result)
                except:
                    print("File Not Found/Pull request already exist")
    
    print()
    print("Process completed.... 100%")
    print("updated_output.csv file generated")
    bar.finish()


messages.add_command(check_dependancy_versions)
messages.add_command(update_dependacy_version)

messages()

















# import os
# import git
# import shutil
# import tempfile

# # Create temporary dir
# t = tempfile.mkdtemp()
# # Clone into temporary dir
# git.Repo.clone_from('https://github.com/dyte-in/backend-sample-app', t, branch='main', depth=1)
# # Copy desired file from temporary dir
# shutil.move(os.path.join(t, 'package.json'), '.')
# # Remove temporary dir
# shutil.rmtree(t)




# Github Enterprise with custom hostname
# g = Github(base_url="https://{hostname}/api/v3", login_or_token="access_token")




