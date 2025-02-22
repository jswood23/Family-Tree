import openpyxl
import subprocess
from dbscripts import * # all functions relating to the sqlite3 database
from person_init import * # all functions relating to the Person object

excel_path = r"C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE"
file_path = r"C:\Users\ASHil\PycharmProjects\Family-Tree\family-tree-data.xlsx"
people = []
person_name_dict = {}
person_id_dict = {}


def show_kids(person):
    for child in person.children:
        print(child)


def print_table():
    for person in people:
        print((f"{'ID:'} {person.parse_id} \t {'Name:'} {person.first_name} {person.last_name} \t "
              f"{'Class of '}{person.class_year}").expandtabs(15))


def get_person_by_id(person_id):
    if person_id == '':
        pass
    else:
        person_id = int(person_id)
        for person in people:
            if person.parse_id == person_id:
                print(person.first_name, person.last_name, 'class of', person.class_year)
                return person
    print("No person found with ID:", person_id)
    print()
    return None


def get_person_by_last():
    print()
    print('*****************************************')
    print('Enter 9 to go back')
    print('NOTE: Input is case sensitive')
    people_list = []

    while True:
        print()
        get = input('Enter last name: ')
        if get == '9':
            print('*****************************************')
            break

        else:
            for person in people:
                if person.last_name == get:
                    print(f"Parse ID for {person.first_name} {person.last_name}: {person.parse_id}")
                    people_list.append(person)

            if len(people_list) == 0:
                print("No people found with last name:", get)


def get_person_by_year(person_year):
    people_list = []
    person_year = int(person_year)

    for person in people:
        if person.class_year == person_year:
            print(f"{person.first_name} {person.last_name}")
            people_list.append(person)

    if not people_list:
        print(f"No people found with class of {person_year}")

    return people_list


def path_selection():
    global file_path, excel_path

    while True:
        print()
        print('Enter the path to either your EXCEL.EXE or the family-tree-data.xlsx')
        print('You will select which path it is in the next step')
        new_path = input('Enter path: ')
        raw_path = r"{}".format(new_path)
        print()
        print(f"Path: {raw_path}")
        selected = input('[1] Set path for EXCEL.EXE \n[2] Set path for family-tree-data.xlsx '
                         '\n[3] Change input \n[9] Go back \nInput choice: ')

        match selected:
            case'1':
                excel_path = raw_path
                print()
                break

            case '2':
                file_path = raw_path
                print()
                break

            case '3':
                print()

            case '9':
                print()
                break


def data_menu():
    print('***************** Data ******************')
    while True:
        global people

        print('Select action:')
        print('[1] Print table')
        print('[2] Open Excel')
        print('[3] Re-parse data')
        print('[4] Edit paths')
        print('[5] Display paths')
        print('[9] Go back')
        selected = input('Input choice: ')

        match selected:
            case '1':
                print()
                print_table()
                print()

            case '2':
                try:
                    subprocess.Popen([excel_path, file_path])
                    print('For changes to take effect you MUST close Excel AND then re-parse the data')
                    print()
                except Exception:
                    print('Error, verify correct paths')
                    print()

            case '3':
                clear_db_people()
                people, person_name_dict, person_id_dict = initialize_people()
                print()

            case '4':
                path_selection()

            case '5':
                print()
                print(f'Path to EXCEL.EXE: {excel_path}')
                print(f'Path to family-tree-data.xlsx: {file_path:}')
                print()

            case '9':
                print('*****************************************')
                print()
                break

            case '':
                print()


def search_menu():
    print('**************** Search *****************')
    while True:
        print('Select search criterion:')
        print('[1] ID')
        print('[2] Last name')
        print('[3] Class year')
        print('[9] Go back')
        selected = input('Input choice: ')

        match selected:
            case '1':
                print()
                get_person_by_id(input('Enter ID: '))

            case '2':
                get_person_by_last()
                print()

            case '3':
                print()
                print('*****************************************')
                get_person_by_year(input('Enter class year: '))
                print('*****************************************')

            case '9':
                print('*****************************************')
                print()
                break

            case '':
                print()
        print()


def relationships_menu():
    print('************* Relationships *************')
    while True:
        print('Select action:')
        print('[1] Immediate family')
        print('[2] Show all descendants')
        print('[3] Show all ancestors')
        print('[9] Go back')

        selected = input('Input choice: ')

        match selected:
            case '1':
                show_relationships()
            case '2':
                show_descendants()
            case '3':
                show_ancestors()
            case '9':
                print('*****************************************')
                print()
                break
        print()


def credits_menu():
    print('**************** Credits ****************')
    print('Historians: \t Tanner Hansard \'23 and Chris Huser \'22'.expandtabs(10))
    print('Traditions Chairs: \t Owen Dunston \'23, Aidan Hill \'23, and Liam Stevens \'23'.expandtabs(10))
    print('Vice President: \t Miles Baker \'23'.expandtabs(10))
    print('Comp Sci Major: \t Joshua Wood \'23'.expandtabs(10))
    print('*****************************************')
    print()


def print_nested_list(nested_list, output_length):
    ancestors = []
    def is_last_in_list(place, parent_list_length):
        return place[len(place)-1] >= parent_list_length - 1
    def getEl (place):
        ancestors.clear()
        ancestors.append(False)
        element = nested_list
        parent_list_length = len(nested_list)
        for i, index in enumerate(place):
            if index >= len(element): raise StopIteration
            if isinstance(element, list): parent_list_length = len(element)
            element = element[index]
            ancestors.append(False if is_last_in_list(place[0:i+1], parent_list_length) else True)
        return(element, parent_list_length)
        
    PIPE = " │" + ' ' * (output_length - 2)
    ELBOW = " └─" + '─' * (output_length - 2)
    TEE = " ├─" + '─' * (output_length - 2)
    SPACE = ' ' * (output_length)
    place = []
    keepGoing = True
    try:
        while keepGoing:
            element, parent_list_length = getEl(place)
            while isinstance(element, list):
                element = element[0]
                place.append(0)
                if isinstance(element, list): parent_list_length = len(element)

            # print element
            last_in_list = is_last_in_list(place, parent_list_length)
            pipes = ""
            for ancestor in ancestors[0:len(ancestors)-1]:
                if ancestor:
                    pipes += PIPE
                else:
                    pipes += SPACE
            # isCorner = last_in_list
            isCorner = True # always print elbows
            thisLine = pipes + (ELBOW if isCorner else TEE) + str(element)
            print(pipes + PIPE)
            print(thisLine)

            while last_in_list:
                # if at the end of the parent list, then remove the last element
                place.pop(len(place)-1)
                if not place:
                    keepGoing = False
                    break
                element, parent_list_length = getEl(place)
                last_in_list = is_last_in_list(place, parent_list_length)

            # increment the new last element by one
            if keepGoing and not last_in_list: place[len(place)-1] += 1
    except StopIteration:
        print("StopIteration exception raised.", place)
        pass


def create_rec_list(this_person, direction, depth, maxDepth):
    nodes = this_person.children if direction == "DOWN" else this_person.parents if direction == "UP" else []
    if nodes and depth < maxDepth:
        node_list = [person_name_dict[this_person.parse_id]]
        for node in nodes:
            node_list.append(create_rec_list(person_id_dict[node], direction, depth + 1, maxDepth))
        return node_list
    else:
        return person_name_dict[this_person.parse_id]


def show_ancestors():
    print()
    subject = int(input('Enter person ID: '))
    maxDepth = input('How many generations of ancestors? ')
    print()

    subject = person_id_dict[subject]
    print("Showing ancestors for", subject.first_name + ' ' + subject.last_name)
    rl = create_rec_list(subject, "UP", 0, (int(maxDepth) if maxDepth else 1000))
    print_nested_list(rl, 5)
    print('*****************************************')
    print()


def show_descendants():
    print()
    subject = int(input('Enter person ID: '))
    maxDepth = input('How many generations of descendants? ')
    print()

    print('*****************************************')
    subject = person_id_dict[subject]
    print("Showing descendants for", subject.first_name + ' ' + subject.last_name)
    rl = create_rec_list(subject, "DOWN", 0, (int(maxDepth) if maxDepth else 1000))
    print_nested_list(rl, 5)
    print('*****************************************')
    print()


def show_relationships():
    print()
    subject = int(input('Enter person ID: '))
    print()
    subject = person_id_dict[subject]

    tense = 'old man' if len(subject.parents) == 1 else 'old men'
    print(f'{subject.first_name} {subject.last_name}\'s {tense}:')
    for parent in subject.parents:
        if parent:
            print(person_name_dict[parent])

    print(f'\n{subject.first_name} {subject.last_name}\'s buffo:')
    for child in subject.children:
        if child:
            print(person_name_dict[child])

    print()


def main():
    print('Welcome to the Singing Cadet family tree project! Here you can lookup any recorded member to see their '
          'family tree!')
    print('Github Repo: https://github.com/ASHill11/Family-Tree')
    print()
    while True:
        print('*************** Main Menu ***************')
        print('[1] Search')
        print('[2] Relationships')
        print('[7] Data')
        print('[8] Credits')
        print('[9] Exit')
        selected = input('Input choice: ')
        print()

        match selected:
            case '1':
                search_menu()

            case '2':
                relationships_menu()

            case '7':
                data_menu()

            case '8':
                credits_menu()

            case '9':
                exit()

people, person_name_dict, person_id_dict = initialize_people()
main()
