# A cloud-based command-line todo app for hackers

I wanted a todo app that 

1. Was always synced
2. No more clicking around in slow UIs on websites/phones. I wanted
   something that was always available to me very quickly. Pull down my
guake terminal, and I'm there.
3. Allowed me to estimate how much time is required for each task &
   track time spent

## Setup

I decided to have my client directly interact with a MongoDB backend in
the cloud, since that was the quickest way to get up and running.

I personally use [Mongo Lab](https://mongolab.com)'s 240MB free hosting
to sync my todos.

You need to create a `settings.py` file with two constants,
`MONGODB_URI` and `DB_NAMNE`.
[Explanation](https://github.com/mongolab/mongodb-driver-examples/blob/master/python/pymongo_simple_example.py)

If you want some other kind of backend (eg. REST), you can add it by
creating a new object that follows the interface of `MongoDataConnector`
in `helpers.py`.

I apologize that this is largely undocumented, although most functions
are self-explanatory. I will fix that when I get around to it.

## Usage

There is a simple "language" to creating tasks. @ for time estimates (I
use 30 min blocks), # for labels, {DATE} for due dates. It doesn't
matter what order you specify these things.

eg. "Email Bob back about project #freelance @1 {today}"
eg. "@2 #school {2012-8-20} Track down memory leaks in my code"

If unspecified, date defaults to "today".

For general usage, see `todo help`.

## Disclaimer

I wrote this in 2 hours, at the odd hours of 2am-4am. It is untested.
Use at your own risk, possible data loss.
