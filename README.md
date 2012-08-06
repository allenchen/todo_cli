# A cloud-based command-line todo app for hackers

I wanted a todo app with these qualities

1. Was always synced
2. A fast UI. I want to spend less time managing my tasks, and more time
   doing them.
3. Allowed me to estimate how much time is required for each task &
   track time spent
4. I like to go through my todos and pick what to get done at the start
   of the day. 

Most apps either fell short on (2) or didn't have all of (1, 3, 4). So I
figured I would build my own. I went with the fastest UI I could think
of - none at all.

## Setup

I decided to have my client directly interact with a MongoDB backend in
the cloud, since that was the quickest way to get up and running.

I personally use [Mongo Lab](https://mongolab.com)'s 240MB free hosting
to sync my data. As long as I have this db setup correctly, all
computers are instantly synced.

You need to create a `settings.py` file with two constants,
`MONGODB_URI` and `DB_NAMNE`.
[Explanation](https://github.com/mongolab/mongodb-driver-examples/blob/master/python/pymongo_simple_example.py).

If you want some other kind of backend (eg. REST), you can add it by
creating a new object that follows the interface of `MongoDataConnector`
in `helpers.py`.

I apologize that this is largely undocumented, although most functions
are self-explanatory. I will fix that when I get around to it.


## Usage

There is a simple "language" to creating tasks. @ for time estimates (I
use 30 min blocks), # for labels, {DATE} for due dates. It doesn't
matter what order you specify these things. If unspecified, date defaults to "today".

eg. "Email Bob back about project #freelance @1 {today}"

eg. "@2 #school {2012-8-20} Track down memory leaks in my code"

`todo ls` lists the current tasks (top is today, then incomplete). After
you run this command, each task is identified by a number. You can then
perform operations using this identifier, eg `todo done <task_num>`.
You can also add any textual notes to a task through `todo edit
<task_num>`.

See `todo help` for all commands and their usage.

## Disclaimer

I wrote this in 2 hours, at the odd hours of 2am-4am. It is untested.
Use at your own risk, possible data loss.
