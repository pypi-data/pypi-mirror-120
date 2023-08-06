import datetime


def print_slot(config, framadate, date):
    votes_names = framadate.get_votes_names(date)
    votes_str = ', '.join(map(str, votes_names))
    if config.get_quiet():
        print(f'{date.isoformat()}: [{votes_str}]')
    else:
        print(f'{date.isoformat()}: [{votes_str}] '
              f'({len(votes_names)} vote(s))')


def print_slot_check(config, framadate, date):
    ret = True
    votes = framadate.get_votes(date)
    if (config.get_votes_min() is not None and
            len(votes) < config.get_votes_min()):
        mystr = f'{date.isoformat()}: KO'
        if not config.get_quiet():
            mystr += (f' ({config.get_votes_min() - len(votes)} '
                      'missing vote(s))')
        ret = False
    elif (config.get_votes_max() is not None and
          len(votes) > config.get_votes_max()):
        mystr = f'{date.isoformat()}: KO'
        if not config.get_quiet():
            mystr += f'{len(votes) - config.get_votes_max()} extra vote(s)'
        ret = False
    else:
        mystr = f'{date.isoformat()}: OK'
        if not config.get_quiet():
            mystr += f' ({len(votes)} vote(s))'
    print(mystr)
    return ret


def print_vote(config, framadate, vote):
    vote_dates = [date.isoformat() for date in vote.get_dates()]
    vote_dates_str = ', '.join(map(str, vote_dates))
    print(f'{vote.get_name()}: [{vote_dates_str}]')


def show_slot(config, framadate, args):
    print_slot(config, framadate, args.date)


def show_all_slots(config, framadate, args):
    for date in framadate.get_all_slots():
        print_slot(config, framadate, date)


def show_next_slots(config, framadate, args):
    for date in framadate.get_next_slots():
        print_slot(config, framadate, date)


def show_next_slot(config, framadate, args):
    date = framadate.get_next_slot()[0]
    print_slot(config, framadate, date)


def show_votes(config, framadate, args):
    for vote in framadate.get_votes():
        print_vote(config, vote)


def check_slot(config, framadate, args):
    if print_slot_check(config, framadate, args.date):
        return 0
    else:
        return 1


def check_all_slots(config, framadate, args):
    ret = True
    for date in framadate.get_all_slots():
        ret = print_slot_check(config, framadate, date) and ret
    if ret:
        return 0
    else:
        return 1


def check_next_slots(config, framadate, args):
    ret = True
    for date in framadate.get_next_slots():
        ret = print_slot_check(config, framadate, date) and ret
    if ret:
        return 0
    else:
        return 1


def check_next_slot(config, framadate, args):
    date = framadate.get_next_slots()[0]
    if print_slot_check(config, framadate, date):
        return 0
    else:
        return 1


def add_slot(config, framadate, args):
    date = args.date
    framadate.add_slot(date)
    if not config.get_quiet():
        print(f'{date.isoformat()}: added')


def delete_old_slots(config, framadate, args):
    for date in framadate.get_old_slots():
        framadate.delete_slot(date)
        if not config.get_quiet():
            print(f'{date.isoformat()}: deleted')


def delete_vote(config, framadate, args):
    framadate.delete_vote(args.vote)
    if not config.get_quiet():
        print(f'{args.vote}: deleted')


def delete_empty_votes(config, framadate, args):
    deleted_votes = framadate.delete_empty_votes()
    for v in deleted_votes:
        print(f'{v}: deleted')


def run_job(config, framadate, args):
    job = config.get_job(args.id)
    return job.run(config, framadate, args)


COMMANDS_DICT = {
    'show': {
        'help': 'Show poll results',
        'subcommands': {
            'slot': {
                'func': show_slot,
                'help': 'Show results for a given date',
                'args': [
                    {'name': 'date',
                     'help': 'Date slot in ISO format (YYYY-MM-DD)',
                     'type': datetime.date.fromisoformat},
                ],
            },
            'all-slots': {
                'func': show_all_slots,
                'help': 'Show results for all dates',
            },
            'next-slots': {
                'func': show_next_slots,
                'help': 'Show results for all coming dates',
            },
            'next-slot':  {
                'func': show_next_slot,
                'help': 'Show results for the next coming date',
            },
            'votes': {
                'func': show_votes,
                'help': 'Show all votes',
            },
        },
    },
    'check': {
        'help': 'Check poll results',
        'subcommands': {
            'slot': {
                'func': check_slot,
                'help': 'Check results for a given date',
                'args': [
                    {'name': 'date',
                     'help': 'Date slot in ISO format (YYYY-MM-DD)',
                     'type': datetime.date.fromisoformat},
                ],
            },
            'all-slots': {
                'func': check_all_slots,
                'help': 'Check results for all dates',
            },
            'next-slots': {
                'func': check_next_slots,
                'help': 'Check results for all coming dates',
            },
            'next-slot': {
                'func': check_next_slot,
                'help': 'Check results for the next coming date',
            },
        },
    },
    'add': {
        'help': 'Add new date slots',
        'subcommands': {
            'slot': {
                'func': add_slot,
                'help': 'Add a new date slot',
                'args': [
                    {'name': 'date',
                     'help': 'Date slot in ISO format (YYYY-MM-DD)',
                     'type': datetime.date.fromisoformat},
                ],
            },
        },
    },
    'delete': {
        'help': 'Delete date slots',
        'subcommands': {
            'old-slots': {
                'func': delete_old_slots,
                'help': 'Delete all past dates from the poll',
            },
            'vote': {
                'func': delete_vote,
                'help': 'Delete a vote',
                'args': [
                    {'name': 'vote',
                     'help': 'Name of the vote',
                     'type': str},
                ],
            },
            'empty-votes': {
                'func': delete_empty_votes,
                'help': 'Delete all empty votes from the poll',
            },
        },
    },
    'job': {
        'func': run_job,
        'help': 'Run a job from a config file',
        'args': [
            {'name': 'id',
             'help': 'Job ID from a given config file',
             'type': str},
        ],
    },
}
