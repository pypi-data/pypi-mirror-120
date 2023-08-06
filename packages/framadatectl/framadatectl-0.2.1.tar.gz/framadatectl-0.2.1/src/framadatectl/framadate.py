import base64
import csv
import datetime
import io
import re
import requests
from bs4 import BeautifulSoup

from .vote import Vote


class Framadate:

    _http_headers = {'Accept-Language': 'en-US'}

    def __init__(self, url):
        self._url = url
        self._admin = False     # whether _url is an admin URL
        self._slots = None      # Map {datetime.date: [Vote]}
        self._votes = None      # Map {str: Vote}
        self.fetch()

    def _get_exportcsv_url(self):
        m = re.fullmatch(r'''(https{0,1}://.+)/(\w+)/admin''',
                         self._url)
        if m is not None:
            self._admin = True
            return '%s/exportcsv.php?admin=%s' % (m.group(1), m.group(2))

        m = re.fullmatch(r'''(https{0,1}://.+)/(\w+)''',
                         self._url)
        if m is not None:
            return '%s/exportcsv.php?poll=%s' % (m.group(1), m.group(2))

        raise Exception('%s is not a valid Framadate URL' %
                        self._url)

    def fetch(self):
        """Fetch and parse the Framadate CSV file."""
        exportcsv_url = self._get_exportcsv_url()
        r = requests.get(exportcsv_url, headers=self._http_headers)
        if r.status_code != 200:
            raise Exception('HTTP GET %s returned a status code of %d' %
                            (exportcsv_url, r.status_code))
        csvio = io.StringIO(r.text, newline='')
        reader = csv.DictReader(csvio, dialect=csv.unix_dialect)
        reader.fieldnames[0] = 'name'
        for i in range(1, len(reader.fieldnames) - 1):
            date = datetime.datetime.strptime(reader.fieldnames[i],
                                              '%Y-%m-%d').date()
            reader.fieldnames[i] = date

        self._slots = {}
        self._votes = {}
        for date in reader.fieldnames[1:-1]:
            self._slots[date] = []
        for record in reader:
            vote_name = record['name']
            if len(vote_name) == 0:
                continue
            vote_dates = []
            for date in reader.fieldnames[1:-1]:
                if record[date] == 'Yes':
                    vote_dates.append(date)
            if vote_name in self._votes:
                raise Exception(f'Internal error: {vote_name} should not '
                                'exist in votes')
            vote = Vote(self, vote_name, vote_dates)
            self._votes[vote_name] = vote
            for date in vote_dates:
                self._slots[date].append(vote)

    def _fetch_html(self):
        """Fetch and parse the Framadate HTML page.

        This function is needed for advanced operations like deleting a vote.
        """
        r = requests.get(self._url, headers=self._http_headers)
        if r.status_code != 200:
            raise Exception('HTTP GET %s returned a status code of %d' %
                            (self._url, r.status_code))
        soup = BeautifulSoup(r.text, 'html.parser')
        vote_regexp = re.compile(r'''^Remove line: (.+)$''')
        for v in soup.find_all('a', class_='btn btn-default btn-sm',
                               title=vote_regexp):
            m = vote_regexp.fullmatch(v['title'])
            if m is None:
                raise Exception('Unexpected error: %s is not a valid title' %
                                v['title'])
            vote_name = m.group(1)
            if vote_name not in self._votes:
                raise Exception('Unexpected error: %s cannot be found in the '
                                'votes dict' % vote_name)
            self._votes[vote_name]._set_delete_url(v['href'])

    def get_slots(self, filter='all-slots'):
        """Return a list of filtered dates."""
        filters_map = {
            'all-slots': self.get_all_slots,
            'next-slots': self.get_next_slots,
            'next-slot': self.get_next_slot,
            'old-slots': self.get_old_slots,
        }
        return filters_map[filter]()

    def get_all_slots(self):
        """Return an array of all dates of the Framadate."""
        res = [date for date in self._slots.keys()]
        res.sort()
        return res

    def get_next_slots(self):
        """Return an array of future dates of the Framadate."""
        today = datetime.date.today()
        return [d for d in self.get_all_slots() if d >= today]

    def get_next_slot(self):
        """Return a one date item array of the next date of the Framadate."""
        return self.get_next_slots()[:1]

    def get_old_slots(self):
        """Return an array of old dates of the Framadate."""
        today = datetime.date.today()
        return [d for d in self.get_all_slots() if d < today]

    def get_votes(self, date=None):
        """Return the list of votes for a given date."""
        if date is None:
            return self._votes.values()
        else:
            return self._slots[date]

    def get_votes_names(self, date):
        """Return the list of votes name for a given date."""
        res = [vote.get_name() for vote in self.get_votes(date)]
        res.sort()
        return res

    def add_slot(self, date):
        """Add a new date slot into the Framadate."""
        if not self._admin:
            raise Exception('Adding slots requires a Framadate admin url')
        if date in self._slots.keys():
            raise Exception(f'Slot {date:%Y%m%d} cannot be added since it '
                            'already exists')
        r = requests.post(self._url, headers=self._http_headers,
                          data={'newdate': date.isoformat(),
                                'newmoment': '',
                                'confirm_add_column': ''})
        if r.status_code != 200:
            raise Exception('HTTP POST %s returned a status code of %d' %
                            (self._url, r.status_code))
        self._slots[date] = []

    def _get_delete_url(self, date):
        dt = datetime.datetime.combine(date, datetime.time.min)
        b64 = base64.b64encode('{t:.0f}@'.format(t=dt.timestamp()).encode())
        dtid = b64.decode().rstrip('=')
        return f'{self._url}/action/delete_column/{dtid}'

    def delete_slot(self, date):
        """Delete a date slot from the Framadate."""
        if not self._admin:
            raise Exception('Deleting slots requires a Framadate admin url')
        if date not in self._slots.keys():
            raise Exception(f'Slot {date:%Y%m%d} cannot be deleted since it '
                            'does not exist')
        delete_url = self._get_delete_url(date)
        r = requests.get(delete_url, headers=self._http_headers)
        if r.status_code != 200:
            raise Exception('HTTP GET %s returned a status code of %d' %
                            (delete_url, r.status_code))
        self._slots.pop(date)

    def delete_vote(self, vote_name):
        """Search for a vote and delete it from the Framadate."""
        vote = self._votes[vote_name]
        vote.delete()

    def delete_empty_votes(self):
        """Search for empty votes and delete them."""
        ret = []
        for vote in [vote for vote in self._votes.values()
                     if len(vote.get_slots()) == 0]:
            vote.delete()
            ret.append(vote.get_name())
        return ret

    def _forget_vote(self, vote):
        """Internal function to pop a vote from internal data."""
        self._votes.pop(vote.get_name())
        for date in vote.get_slots():
            votes = self._slots[date]
            for i in range(0, len(votes)):
                if votes[i] == vote:
                    votes.pop(i)
