"""

OVERVIEW
- [x] parse tag spec and compare with latest tag
- [x] bump the version number
- [x] write changelog
- [x] append to existing changelog file
- [x] write some tests
- [x] cli options
 - [x] dry run option
- [x] commit and tag release

- [x] more test
- [x] code coverage

- [x] version this module

- [x] ci/cd with GitHub Actions
- package wheel
- publish to pypy
- cleanup directory/module structure
- other version formats
- format output from config
- create the release using github release

Unrelated
- generate a toc
- count loc
"""

import datetime
import io
import logging
import os
import re
import subprocess
import sys


SYS_NONE = 0
SYS_WIN32 = 1
SYS_LINUX = 2
SYS_PYTHON2 = 2
SYS_PYTHON3 = 3

MIN_SUPPORTED_PYTHON_MAJOR = 3
MIN_SUPPORTED_PYTHON_MINOR = 6
MIN_SUPPORTED_PYTHON_MICRO = 0

COMMIT_PATTERN = R"^g([a-z0-9]{40}) '(.*)'"

log = logging.getLogger(__name__)


def release(args):

 use_tag = args.tag
 is_debug = args.debug
 push_tags = args.push
 is_dry_run = args.dry_run
 is_preview_changelog = args.preview
 changelog_path = args.changelog_filename
 emit_changes_to_changelog = args.changelog
 use_version_file = args.version_file
 version_file = args.version_filename

 logging.basicConfig()

 if is_debug:
  log.setLevel(logging.DEBUG)
 else:
  log.setLevel(logging.INFO)

 #############################
 # note/fred: context cracking

 SYS_PLATFORM = 0
 PYTHON_VERSION_MAJOR = 0
 PYTHON_VERSION_MINOR = 0

 if 0: pass
 elif sys.platform.startswith("win32"):
  SYS_PLATFORM = SYS_WIN32
 elif sys.platform.startswith("linux"):
  SYS_PLATFORM = SYS_LINUX
 else:
  log.fatal(f"sys system '{sys.platform}' is not supported")
  exit(1)

 # todo/fred: fetch which version of the platform we are using

 assert SYS_PLATFORM

 if 0: pass
 elif sys.version_info[0] == MIN_SUPPORTED_PYTHON_MAJOR:
  # todo/fred: min micro version
  if sys.version_info[1] < MIN_SUPPORTED_PYTHON_MINOR:
   log.fatal(f"python version {sys.version_info[0]}.{sys.version_info[1]} is not supported")
   exit(1)

  if sys.version_info[1] == MIN_SUPPORTED_PYTHON_MINOR and sys.version_info[2] < MIN_SUPPORTED_PYTHON_MICRO:
   log.fatal(f"python version {sys.version_info[0]}.{sys.version_info[1]} is not supported")
   exit(1)

  PYTHON_VERSION_MAJOR = SYS_PYTHON3
  PYTHON_VERSION_MINOR = sys.version_info[1]  

 else:
  log.fatal(f"python version {sys.version_info[0]}.{sys.version_info[1]} is not supported")
  exit(1)

 log.debug(f"sys.platform={sys.platform}, python.version={PYTHON_VERSION_MAJOR}.{PYTHON_VERSION_MINOR}")

 assert PYTHON_VERSION_MAJOR == MIN_SUPPORTED_PYTHON_MAJOR
 assert PYTHON_VERSION_MINOR >= MIN_SUPPORTED_PYTHON_MINOR

 if SYS_PLATFORM == SYS_WIN32:
  req_out = subprocess.run(["where", "git"], capture_output=subprocess.PIPE)
  # log.debug(f"git found at '{req_out.stdout.decode('utf-8').rstrip()}'")
  git_found = (req_out.returncode == 0)
 elif SYS_PLATFORM == SYS_LINUX:
  is_valid, which_git = cli(["which", "git"])
  git_found = is_valid
 else:
  raise NotImplementedError("os not supported yet")

 assert git_found

 if git_found == False:
  log.fatal(f"git could not be found in path")
  exit(1)

 # todo/fred: fetch which version of git we are dealing with

 #####################################
 # note/fred: github details

 is_valid, git_remote_out = cli(["git", "remote"])
 if not is_valid:
  log.fatal("could not fetch git remote")
  exit(1)

 git_remote = git_remote_out
 log.debug("using remote '%s'", git_remote)

 is_valid, git_remote_get_url_out = cli(["git", "remote", "get-url", git_remote])
 if not is_valid:
  log.fatal("could not fetch git remote url")
  exit(1)

 git_remote_url = git_remote_get_url_out
 if not git_remote_url.startswith("https://github.com") or not git_remote_url.endswith(".git"):
  log.fatal("repo '%s' doesn't seem to be a github repository", git_remote_url)
  exit(1)

 assert len(git_remote_url) > 4
 repo_url = git_remote_url[:-4]
 log.debug("git repo url: %s", repo_url)

 #
 #############################
 # note/fred: fetch latest tag

 is_first_release = False

 now = datetime.datetime.now()
 year = now.strftime("%Y")
 month = f"{now.month}"
 log.debug("year:%s, month: %s", year, month)

 current_tag = f"{year}.{month}"
 latest_tag = current_tag

 # note/fred: here we are running a git command and parsing the output

 is_valid, git_describe_tags_out = cli(["git", "describe", "--tags", "--abbrev=0"])

 if not is_valid or lates_tag == "":
  log.warning("No tags were found -- treating as first release using tag '%s'", latest_tag)
  is_first_release = True

  release_without_tags = True
  if not release_without_tags:
    exit(1)
 
 else:
  latest_tag = git_describe_tags_out
  log.debug("latest tag: %s", latest_tag)

 #
 ##############################
 # note/fred: parse git commits

 if is_first_release:
  git_cmd = ["git", "log", "--pretty=g%H '%s'%n%bEOC"]
 else:
  git_cmd = ["git", "log", "{}..HEAD".format(latest_tag), "--pretty=g%H '%s'%n%bEOC"]

 log.debug(git_cmd)

 type_pattern = re.compile(R"(.*):(.*)")
 pattern = re.compile(COMMIT_PATTERN)

 is_valid, git_out = cli(git_cmd)
 if is_valid:

  string = io.StringIO(git_out)

  changes = parse_git_commits(string, pattern, type_pattern)
  num_commits_to_report = len(changes)

  ################################
  # note/fred: fetch new version by bumping the tag according to a given tag spec

  if num_commits_to_report > 0:
   log.debug("found %d change(s) -- bumping version", num_commits_to_report)

   ################################
   # note/fred: aggregate changes of type

   changes_pivoted = {}
   for index, commit_hash, category, subvalue, body in changes:
    
    # @speed
    if not category in changes_pivoted:
     changes_pivoted[category] = []

    changes_pivoted[category].append((commit_hash, subvalue, body))

   log.debug(changes_pivoted)

   ################################
   # note/fred: parse tag spec

   # todo/fred: we would like to have differnt types of tag specs

   if is_first_release:
    new_tag = current_tag
   else:
    if latest_tag == current_tag:
     # note/fred: if the tags are the same, we need to bump the version
     # according to the tag spec

     tag_spec_pattern = re.compile(R"(\d{4})[.](\d{1,2})([.]\d+)?")
     tag_result = tag_spec_pattern.match(latest_tag)
     if tag_result:

      tag_groups = tag_result.groups()
      log.debug(tag_groups)

      major = int(tag_groups[0])
      minor = int(tag_groups[1])
      micro = tag_groups[2]

      assert major
      assert minor

      if int(year) == major:
       if int(month) == minor:
        if micro:
         new_tag = "{}.{}".format(current_tag, str(int(micro) + 1))
        else:
         new_tag = "{}.{}".format(current_tag, str(1))
      else:
       # note/fred: in all other cases we restart the numbering
       new_tag = current_tag

       if int(year) > major:
        log.warning("year is from the future?")
       
       if (int(year) == major and int(month) > minor):
        log.warning("month is from the future?")

     else:
      log.warning("last tag does not match the tag spec, or unknown tag found -- setting a new tag")
      new_tag = current_tag

    else:
     log.debug("starting from zero")
     new_tag = current_tag

   assert new_tag

   log.debug("new tag: %s", new_tag)

   ################################
   # note/fred: maintain a version file in addition to tag

   if use_version_file and not is_dry_run:
    log.debug("emitting version file: %s", version_file)
    with open(version_file, "w") as file:
     file.write(new_tag)

   ################################
   # note/fred: read existing changelog

   if emit_changes_to_changelog:

    changelog_str = ""
    changelog_prev_content_str = ""
    changelog_header_str = ""

    is_changelog_existing = os.path.exists(changelog_path)

    if is_changelog_existing:

     log.debug("changelog '%s' exists, appending our changes", changelog_path)
     with open(changelog_path, "r") as existing_changelog:
      changelog_str = existing_changelog.read()

     (changelog_header_str,
      changelog_prev_content_str) = split_changelog_header_and_content(changelog_str, new_tag)

    else:
     log.debug("no changelog '%s' found, creating a new one", changelog_path)

     # note/fred: generate a new header
     with io.StringIO() as changelog_header:
      # changelog_header.write("<!--- generated: header -->")
      changelog_header.write("{}\n".format("# Changelog"))
      changelog_header.write("\n")
      changelog_header.write("All notable changes in this repository will be documented in this file.\n")
      changelog_header.write("\n")
      changelog_header.write("This format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),\n")
      changelog_header.write("and the project uses a calendar versioning scheme, 'year.month[.revision]'.\n")
      changelog_header.write("\n")
      changelog_header.write("## [Unreleased]\n")
      changelog_header.write("\n")
      changelog_header.flush()

      changelog_header.seek(0)
      changelog_header_str = changelog_header.read()

    datestr = now.strftime("%Y-%m-%d")
    changelog_content = generate_changelog_content(datestr, latest_tag, new_tag, repo_url, changes_pivoted, is_first_release)

    changelog_str = os.linesep.join([changelog_header_str, changelog_content, changelog_prev_content_str])

    # todo/fred: take a backup of the existing changelog just in case until we know
    # this operation worked

    if not is_dry_run:
     with open(changelog_path, "w") as new_changelog:
      new_changelog.write(changelog_str)

    if is_preview_changelog:
     print("Changelog Preview".center(80, "-"))
     print(changelog_str, end="", flush=True)
     print("-" * 80)

    #################################
    # note/fred: commit changelog

    # todo/fred: actually commit the changelog

   else:
    pass  # do nothing

   ##################################
   # note/fred: tag and push version

   git_tag_cmd = ["git", "tag", "-a", new_tag, "-m", "'version {}'".format(new_tag)]
   git_push_cmd = ["git", "push", git_remote, new_tag]

   if not is_dry_run:
    
    if use_tag:
     is_valid, git_tag_out = cli(git_tag_cmd)
     if is_valid:

      if push_tags:
       is_valid, git_push_tags_out = cli(git_push_cmd)
       if not is_valid:
        log.fatal("could not push to remote, aborting")
        exit(1)
     
     else:
      log.fatal("could not create a tag on current commit, aborting")
      exit(1)

   else:
    log.info(" ".join(git_tag_cmd))
    log.info(" ".join(git_push_cmd))

   # todo/fred: use the github api to create a release from this tag now

  else:
   log.info("no changes was parsed from the commit history, ignoring release")

 else:
  log.fatal("could not run git commant '%a', aborting", git_cmd)
  exit(1)


def cli(argument_list) -> (bool, str):
 result = subprocess.run(argument_list, capture_output=subprocess.PIPE)
 return result.returncode == 0, result.stdout.decode("utf-8").rstrip()


def parse_git_commits(string, pattern, type_pattern):

 changes = []
 num_commits = 0
 num_commits_to_report = 0

 while (1):

  line = string.readline()
  if line == "":
   break

  stripped_line = line.rstrip()
  if len(stripped_line) > 0 and stripped_line[0] == 'g':

   result = pattern.match(line)
   if result:
    commit_hash = result.group(1)
    subject = result.group(2)

    # log.debug("commit=%d hash=%s subject='%s'", num_commits, commit_hash, subject)

    num_commits += 1

    #######################
    # note/fred: parse type

    type_result = type_pattern.match(subject)
    if type_result:
     subject_type = type_result.group(1).strip()
     subject_value = type_result.group(2).strip()
     log.debug("type: '%s', value: '%s'", subject_type, subject_value)
    else:
     # note/fred: not a type
     log.debug("subject '%s' does not contain a type -- skipping", subject)
     continue;

    assert subject_type
    assert subject_value

    # todo/fred: consider max number of commits supported
    if num_commits > 99999:
     assert False

    #######################
    # note/fred: parse body

    num_lines = 0
    whole_body = ""
    while (1):
     body = string.readline().rstrip()
     num_lines += 1

     if body == "" or body == "EOC":
      break

     whole_body += body

     if num_lines > 999:
      assert False
     # todo/fred: consider max number of lines in body comment supported

    if whole_body:
     log.debug("body='%s'", whole_body)

    change = (num_commits_to_report, commit_hash, subject_type, subject_value, whole_body)
    changes.append(change)

    num_commits_to_report += 1

   else:  # if type_result:
    # note/fred: commit was somehow malformed or missing
    assert False  # todo/fred: diagnose

 return changes


def split_changelog_header_and_content(changelog_str, release_version) -> (str, str):

 changelog_prev_content_str = ""
 changelog_header_str = ""

 with io.StringIO(changelog_str) as existing_changelog:

  CHANGE_PATTERN = R"^<a name='(.*)'></a>## "
  change_pattern = re.compile(CHANGE_PATTERN)

  line = ""
  last_pos = 0
  num_lines = 0
  is_prev_tag_found_in_changelog = False
  while 1:
   
   last_pos = existing_changelog.tell()
   line = existing_changelog.readline()

   log.debug("line: %s", line)
   
   if not line:
    break

   num_lines += 1

   # note/fred: this is the first occurance of an an anchor
   if line.strip().startswith("<a name='"):

    change_result = change_pattern.match(line)
    if change_result and change_result.group(0) == release_version:
     # todo/fred: here we can provide the option to replace or append rather than error out
     log.fatal("Version '%s' already exists in the changelog", release_version)
     exit(1)

    # @bug
    # todo/fred: this last position isn't splitting the file where we want it to

    existing_changelog.seek(last_pos)
    is_prev_tag_found_in_changelog = True

    # note/fred: the rest of it is now considered old changes
    changelog_prev_content_str = existing_changelog.read()
    break

  # todo/fred: all kinds of wierd edge cases here... could we map it out visually perhaps?

  if not is_prev_tag_found_in_changelog:
   log.warning("No previous release was found in the file, appending changes to the end of the file")
   is_force_overwrite_enabled = True
   if not is_force_overwrite_enabled:
    exit(1)

  existing_changelog.seek(0)
  # @bug?
  # note/fred: there is something odd with win32 here, maybe the newlines are strange or something?
  changelog_header_str = existing_changelog.read(last_pos)

 return changelog_header_str, changelog_prev_content_str


def generate_changelog_content(datestr, prev_version, new_version, repo_url, changes_pivoted, is_first_release) -> str:


 with io.StringIO() as changelog:

  changelog.write("<a name='{0}'></a>## [{0}]".format(new_version))

  # compare string
  if not is_first_release:
   assert prev_version != new_version
   compare_url = "{}/compare/{}...{}".format(
    repo_url, prev_version, new_version
   )
   changelog.write("({})".format(compare_url))

  # date
  changelog.write(" - {}\n".format(datestr))
  changelog.write("\n")

  # changes
  for category, changes in changes_pivoted.items():
   changelog.write("### {}\n".format(category.title()))
   changelog.write("\n")

   for commit_hash, change, body in changes:
    changelog.write("* {} ([{}]({}/commit/{}))\n".format(change.capitalize(), commit_hash[:7], repo_url, commit_hash))

    if body != "":
     changelog.write("{}\n".format(body))

   changelog.write("\n")

  changelog.flush()
  changelog.seek(0)
  changelog_updates_str = changelog.read()

 return changelog_updates_str
