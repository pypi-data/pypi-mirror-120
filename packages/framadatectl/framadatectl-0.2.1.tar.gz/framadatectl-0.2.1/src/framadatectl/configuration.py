import email
import datetime
import pathlib
import smtplib
import yaml

from .commands import COMMANDS_DICT


class JobCondition:

    def __init__(self, yaml_data):
        self._name = yaml_data['condition']

    def get_name(self):
        return self._name

    def check(self, framadate):
        raise Exception('Internal error: method should be overloaded')


class JobConditionSlots(JobCondition):

    def __init__(self, yaml_data):
        JobCondition.__init__(self, yaml_data)
        self._slots = 'all-slots'
        self._less = None
        self._more = None
        if 'slots' in yaml_data.keys():
            self._slots = yaml_data['slots']
        if 'less' in yaml_data.keys():
            self._less = yaml_data['less']
        if 'more' in yaml_data.keys():
            self._more = yaml_data['more']

    def check(self, framadate):
        dates = framadate.get_dates(self._slots)
        for date in dates:
            votes = framadate.get_votes(date)
            if (self._less is not None and
                    len(votes) < self._less):
                return True
            if (self._more is not None and
                    len(votes) > self._more):
                return True
        return False


class JobAction:

    def __init__(self, yaml_data):
        self._name = yaml_data['action']

    def run(self):
        raise Exception('Internal error: method should overloaded')


class JobActionCommand(JobAction):

    def __init__(self, yaml_data):
        JobAction.__init__(self, yaml_data)
        self._command = yaml_data['command']
        self._subcommand = yaml_data['subcommand']

    def run(self, config, framadate, args):
        func = COMMANDS_DICT[self._command]['subcommands'][
            self._subcommand]['func']
        return func(config, framadate, args)


class JobActionEmail(JobAction):

    def __init__(self, yaml_data):
        JobAction.__init__(self, yaml_data)
        self._slot = yaml_data['slot']
        self._content = yaml_data['content']

    def run(self, config, framadate, args):
        if self._slot == 'next-slot':
            date = framadate.get_next_slot()[0]
        else:
            date = datetime.date.fromisoformat(self._slot)
        votes_str = framadate.get_votes_names(date)
        missing_votes = 'N/A'
        exceeding_votes = 'N/A'
        if config.get_votes_min() is not None:
            missing_votes = max(config.get_votes_min() - len(votes_str), 0)
        if config.get_votes_max() is not None:
            exceeding_votes = max(len(votes_str) - config.get_votes_max(), 0)
        email_args = {
            'date': date,
            'nb_votes': len(votes_str),
            'min_votes': config.get_votes_min(),
            'max_votes': config.get_votes_max(),
            'missing_votes': missing_votes,
            'exceeding_votes': exceeding_votes,
            'votes': ', '.join(map(str, votes_str)),
        }
        e = email.message_from_bytes(
            self._content.format_map(email_args).encode('utf-8')
        )
        s = smtplib.SMTP(config.get_smtp_host())
        s.send_message(e)
        return True


class JobActionBackup(JobAction):

    def __init__(self, yaml_data):
        JobAction.__init__(self, yaml_data)
        self._slots = 'all-slots'
        self._mode = 'w'
        if 'slots' in yaml_data.keys():
            self._slots = yaml_data['slots']
        if 'mode' in yaml_data.keys():
            self._mode = yaml_data['mode']
        self._filepath = yaml_data['filepath']

    def run(self, config, framadate, args):
        path = pathlib.Path(self._filepath)
        if not path.is_absolute():
            path = pathlib.Path(str(config.get_config_dir()) + '/' +
                                self._filepath)
        with path.open(mode=self._mode, encoding='utf-8') as f:
            for date in framadate.get_slots(self._slots):
                votes_names = framadate.get_votes_names(date)
                votes_str = '\n'.join(map(str, votes_names))
                f.write(f'# {date}\n{votes_str}\n')


class Job:

    def __init__(self, yaml_data):
        self._id = yaml_data['id']
        self._conditions = []
        self._actions = []
        if 'condition' in yaml_data.keys():
            for cond in yaml_data['condition']:
                if cond['condition'] == 'slots':
                    self._conditions.append(JobConditionSlots(cond))
                else:
                    raise Exception(f'Unsupported condition name: '
                                    f'{cond["condition"]}')
        if 'action' in yaml_data.keys():
            for action in yaml_data['action']:
                if action['action'] == 'command':
                    self._actions.append(JobActionCommand(action))
                elif action['action'] == 'email':
                    self._actions.append(JobActionEmail(action))
                elif action['action'] == 'backup':
                    self._actions.append(JobActionBackup(action))
                else:
                    raise Exception(f'Unsupported action name: '
                                    f'{action["action"]}')

    def get_id(self):
        return self._id

    def conditions(self, framadate):
        for cond in self._conditions:
            if not cond.check(framadate):
                return False
        return True

    def actions(self, config, framadate, args):
        ret = True
        for action in self._actions:
            ret = action.run(config, framadate, args) and ret
        return ret

    def run(self, config, framadate, args):
        if self.conditions(framadate):
            return self.actions(config, framadate, args)


class Configuration:

    def __init__(self, yaml_path=None,
                 url=None, votes_min=None, votes_max=None,
                 quiet=None):
        """Initialize the configuration from a YAML file (if given)."""
        self._yaml_path = yaml_path
        self._url = None
        self._votes_min = None
        self._votes_max = None
        self._quiet = False     # Default value
        self._jobs = {}
        if yaml_path is not None:
            yaml_data = yaml.safe_load(yaml_path.open('r'))
            if 'configuration' in yaml_data.keys():
                yaml_configuration = yaml_data['configuration']
                if 'url' in yaml_configuration.keys():
                    self._url = yaml_configuration['url']
                if 'votes' in yaml_configuration.keys():
                    yaml_votes = yaml_configuration['votes']
                    if 'min' in yaml_votes.keys():
                        self._votes_min = int(yaml_votes['min'])
                    if 'max' in yaml_votes.keys():
                        self._votes_max = int(yaml_votes['max'])
                if 'quiet' in yaml_configuration.keys():
                    self._quiet = bool(yaml_configuration['quiet'])
                if 'email' in yaml_configuration.keys():
                    yaml_email = yaml_configuration['email']
                    self._smtp_host = yaml_email['smtp_host']
            if 'job' in yaml_data.keys():
                self._load_jobs(yaml_data['job'])
        if url is not None:
            self._url = url
        if votes_min is not None:
            self._votes_min = votes_min
        if votes_max is not None:
            self._votes_max = votes_max
        if quiet is not None:
            self._quiet = quiet

    def _load_jobs(self, yaml_data):
        for job in yaml_data:
            self._jobs[job['id']] = Job(job)

    def get_config_dir(self):
        return self._yaml_path.parent

    def get_url(self):
        return self._url

    def get_votes_min(self):
        return self._votes_min

    def get_votes_max(self):
        return self._votes_max

    def get_quiet(self):
        return self._quiet

    def get_smtp_host(self):
        return self._smtp_host

    def get_job(self, id):
        if id in self._jobs:
            return self._jobs[id]
        else:
            raise Exception('Unknown job ID')
