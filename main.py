"""
This program collects and processes information from
personnel log files and provides a list with ID,
name, date and time of entry or exit to the facility.
"""


from pathlib import Path


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
    :return: list with ID, name, date and time of entry or exit to the
             facility.
    """
    crew, enter, exit = read_files(path)
    d_crew, res = {}, {}


    def make_dict(k: str) -> dict:
        p = {}
        for i in enter:
            k2, dt = i.split(' |')[0], i.split(' |')[1]
            if k2 == k:
                for j in exit:
                    time = []
                    k3, dt3 = j.split(' |')[0], j.split(' |')[1]
                    if k3 == k2 and dt3.split()[0] == (dts0 := dt.split()[0]):
                        time.append(dt.split()[1])
                        time.append(dt3.split()[1])
                        p.setdefault(dts0, []).append([time[0], time[1]])
                        exit.remove(j)
                        break
        return p


    for st in crew:
        d_crew[st.split(' |')[0]] = st.split(' |')[1].replace('\n', '')
    for k, name in d_crew.items():
        res[k] = {'name': name.strip(), 'visits': make_dict(k)}
    return res


if __name__ == '__main__':
    from pprint import pprint
    pprint(main(PATH), width=100)
