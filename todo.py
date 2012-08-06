#!/usr/bin/python
import sys
import os
import helpers
import pickle
import tempfile
from termcolor import colored
from datetime import datetime, date
from subprocess import call
import parsedatetime.parsedatetime as pdt
import parsedatetime.parsedatetime_consts as pdc



task_store = helpers.MongoDataConnector()

date_consts = pdc.Constants()
date_parser = pdt.Calendar(date_consts)

EDITOR = os.environ.get('EDITOR','vim')

try:
    f = open("/tmp/todo_pickle")
    task_tmp = pickle.load(f)
    f.close()
except:
    task_tmp = None

def extract_date(struct_time):
    return date(struct_time.tm_year, struct_time.tm_mon, struct_time.tm_mday)

def parse_new_task(task_str, today=False):
    """
    @ for estimated pomodoro count
    {date} for due date
    # for label
    """
    est_count = 0 
    labels = []
    due = datetime.now().date()
    text = ''
    notes = ''

    for word in task_str.split():
        if word.startswith("@"):
            est_count = int(word[1:])
        elif word.startswith("#"):
            labels.append(word[1:])
        elif word.startswith("{") and word.endswith("}"):
            due = extract_date(date_parser.parse(word[1:-1])[0])
        else:
            text += (word + " ")

    return {'text': text.strip(),
            'labels': labels,
            'est_count': est_count,
            'count': 0,
            'due': str(due),
            'notes': notes,
            'today': today,
            'done': False}

def parse_date(date_str):
    return datetime.strptime(date_str, "%Y-%m-%d").date()

def format_task(index, task):
    print_str = "[{0}]    ".format(index)
    now = datetime.now().date()
    due = parse_date(task['due'])
    if now > due:
        print_str += colored("{due}    ".format(**task), "red")
    elif now < due:
        print_str += colored("{due}    ".format(**task), "blue")
    else:
        print_str += colored("{due}    ".format(**task), "yellow")
    print_str += colored("{0}/{1}    ".format(task['count'], task['est_count']), "cyan")
    print_str += "{text}    ".format(**task)
    for label in task['labels']:
        print_str += colored("#{0} ".format(label), "green")
    return print_str

def list_tasks(params):
    print
    mapper = {}
    incomplete = task_store.get_incomplete_tasks()
    today = []
    rest = []
    for task in incomplete:
        if task['today']:
            today.append(task)
        else:
            rest.append(task)
    today = sorted(today, key=lambda x: (parse_date(x['due']), x['text'].lower()))
    rest = sorted(rest, key=lambda x: (parse_date(x['due']), x['text'].lower()))
    i = 0
    for task in today:
        mapper[str(i)] = task["_id"]
        print format_task(i, task)
        i += 1
    print "\n---\n"
    for task in rest:
        mapper[str(i)] = task["_id"]
        print format_task(i, task)
        i += 1
    f = open("/tmp/todo_pickle", "w")
    pickle.dump(mapper, f)
    f.close()
    print

def list_done(params):
    print
    mapper = {}
    completed = task_store.get_completed_tasks()
    completed = sorted(completed, reverse=True, key=lambda x: (parse_date(x['due']), x['text'].lower()))
    i = 0
    for task in completed:
        mapper[str(i)] = task["_id"]
        print format_task(i, task)
        i += 1
    f = open("/tmp/todo_pickle", "w")
    pickle.dump(mapper, f)
    f.close()
    print

def create_new_task(params, today):
    task_str = params[0]
    task_store.insert_task(parse_new_task(task_str, today))
    list_tasks([])

def make_today(params):
    task_ids = [task_tmp[task_num] for task_num in params]
    for task_id in task_ids:
        task_store.set_task_by_id(task_id, {"today": True})
    list_tasks([])

def make_later(params):
    task_ids = [task_tmp[task_num] for task_num in params]
    for task_id in task_ids:
        task_store.set_task_by_id(task_id, {"today": False})
    list_tasks([])

def make_done(params):
    task_ids = [task_tmp[task_num] for task_num in params]
    for task_id in task_ids:
        task_store.set_task_by_id(task_id, {"done": True})
    list_tasks([])

def record_pomo(params):
    task_num = params[0]
    if len(params) > 1:
        inc_num = int(params[1])
    else:
        inc_num = 1
    task_id = task_tmp[task_num]
    task_store.inc_task_field_by_id(task_id, {"count": inc_num})
    print format_task(-1, task_store.get_task_by_id(task_id))

def delete_task(params):
    task_num = params[0]
    try:
        print "Sure del {0}?".format(task_num)
        raw_input()
    except (KeyboardInterrupt, EOFError):
        print "Aborted..."
        list_tasks([])
        return
    task_id = task_tmp[task_num]
    task_store.remove_task_by_id(task_id)
    list_tasks([])


def edit_notes(params, view=True):
    task_num = params[0]
    task_id = task_tmp[task_num]
    task = task_store.get_task_by_id(task_id)
    content = task['notes']
    if not view:
        with tempfile.NamedTemporaryFile(suffix=".tmp") as temp:
          temp.write(content)
          temp.flush()
          call([EDITOR, temp.name])
          content = temp.read()
          temp.seek(0)
          content = temp.read()
          task_store.set_task_by_id(task_id, {"notes": content})
        list_tasks([])
    else:
        print content

def parse_options(args):
    action = args[0]
    params = args[1:]
    if action == "new":
        create_new_task(params, today=False)
    elif action == "newtoday" or action == "newt":
        create_new_task(params, today=True)
    elif action == "ls" or action == "list":
        list_tasks(params)
    elif action == "pomo":
        record_pomo(params)
    elif action == "today":
        make_today(params)
    elif action == "later":
        make_later(params)
    elif action == "del":
        delete_task(params)
    elif action == "done":
        make_done(params)
    elif action == "old":
        list_done(params)
    elif action == "edit":
        edit_notes(params, False)
    elif action == "view":
        edit_notes(params, True)
    elif action == "help":
        print_help()

def print_help():
    print "new <task_str>\n\t create a new task"
    print "newtoday <task_str>\n\t create a new task for today (shorthand: newt)"
    print "list\n\t list tasks (shorthand: ls)"
    print "pomo <task_num> <n>\n\t record n timeunits spent no <task_num>, default n=1"
    print "today <task_nums>\n\t move one or more tasks to the today section, split by space"
    print "later <task_nums>\n\t move one or more tasks out of the today section, split by space"
    print "done <task_nums>\n\t mark one or more tasks ask done, split by space"
    print "del <task_num>\n\t delete task, any key to confirm, ctrl+c or ctrl+d to quit"
    print "old\n\t show completed tasks"
    print "edit <task_num>\n\t edit notes for task in text editor, any key to confirm save after quitting"
    print "view <task_num>\n\t view notes for task"

if __name__ == "__main__":
    parse_options(sys.argv[1:])
