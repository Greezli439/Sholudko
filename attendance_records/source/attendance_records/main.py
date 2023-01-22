"""
This program collects and processes information from
personnel log files and provides a list with ID,
name, date and time of entry or exit to the facility.
"""


from pathlib import Path


PATH = '/home/mykhailo/Hillel/Final_Project/Sholudko/data'
CREW_FILENAME = 'crew.txt'
ENTRANCE_FILENAME = 'entrance.log'
EXIT_FILENAME = 'exit.log'


def read_files(path: str) -> tuple:
    """
    Read data from logfiles and write data to a file.
    :param path: log file
    :return: tuple with dict and list
    """
    path = Path(path)
    with open(path / CREW_FILENAME) as cf, \
            open(path / ENTRANCE_FILENAME) as enf, \
            open(path / EXIT_FILENAME) as exf:
        crew = cf.readlines()
        enter = enf.readlines()
        exit = exf.readlines()
    return crew, enter, exit


def make_dict(id_crew: str, enter: list, exit_f) -> dict:
    """
    Make dict for day enter/exit
    :param id_crew: dict with id and name.
    :param enter: list with id and enter datetime.
    :param exit_f: list with id and exit datetime.
    :return:
    """
    day_visits = {}
    for i in enter:
        id_enter, time_enter = i.split(' |')[0], i.split(' |')[1]
        if id_enter != id_crew:
            continue
        for j in exit_f:
            id_exit, time_exit = j.split(' |')[0], j.split(' |')[1]
            date, time = time_enter.split()[0], []
            if id_exit == id_enter and time_exit.split()[0] == date:
                time.append(time_enter.split()[1])
                time.append(time_exit.split()[1])
                day_visits.setdefault(date, []).append([time[0], time[1]])
                exit_f.remove(j)
                break
    return day_visits

def main(path: str) -> dict:
    """
    :param path: Tuple with dict and list.
    :return: list with ID, name, date and time of entry or exit to the
             facility.
    """
    crew, enter, exit_f = read_files(path)
    d_crew, res = {}, {}

    for st in crew:
        d_crew[st.split(' |')[0]] = st.split(' |')[1].replace('\n', '')
    for id_crew, name in d_crew.items():
        res[id_crew] = {
            'name': name.strip(),
            'visits': make_dict(id_crew, enter, exit_f)
        }
    return res


if __name__ == '__main__':
    from pprint import pprint
    pprint(main(PATH), width=100)

