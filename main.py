from pathlib import Path

"""
This program collects and processes information from 
personnel log files and provides a list with ID,
name, date and time of entry or exit to the facility.
"""

PATH = '/home/mykhailo/Hillel/Final_Project/Sholudko/venv/'
CREW_FILENAME = 'crew.txt'
ENTRANCE_FILENAME = 'entrance.log'
EXIT_FILENAME = 'exit.log'


def read_files(path: str) -> tuple:
    """
    Read data from logfiles and write data to a file.
    :param path: log file
    :return: tuple with dict and list
    """
    path = Path(path) / 'data'
    with open(path / CREW_FILENAME) as cf, \
        open(path / ENTRANCE_FILENAME) as enf, \
        open(path / EXIT_FILENAME) as exf:
        crew = cf.readlines()
        enter = enf.readlines()
        exit = exf.readlines()
    return crew, enter, exit


def main(path: str) -> dict:
    """
    :param path: Tuple with dict and list.
    :return: list with ID, name, date and time of entry or exit to the facility.
    """
    crew, enter, exit = read_files(path)
    d_crew, res, d_res = {}, {}, {}
    for i in crew:
        d_crew[i.split(' |')[0]] = i.split(' |')[1].replace('\n', '')
    for k, name in d_crew.items():
        p_res = {}
        for i in enter:
            k2, dt = i.split(' |')[0], i.split(' |')[1]
            if k2 == k:
                for j in exit:
                    k3, dt3 = j.split(' |')[0], j.split(' |')[1]
                    if k3 == k2 and j.split(' |')[1].split()[0] == i.split(' |')[1].split()[0]:
                        p_res.setdefault(dt.split()[0], []).append([i.split(' |')[1].split()[1],
                                                                    j.split(' |')[1].split()[1]])
                        exit.remove(j)
                        break
        res[k] = {'name': name.strip(), 'visits': p_res}
    return res


if __name__ == '__main__':
    from pprint import pprint
    pprint(main(PATH), width=100)
