from copy import deepcopy

def add_to_candidate_labellings(labelling):
    global candidate_labellings
    if labelling not in candidate_labellings:
        candidate_labellings.append(labelling)

def remove_duplicates(list):
    new_list = []
    for x in list:
        if x not in new_list:
            new_list.append(x)
    return new_list

labelling_to_dos = []
lock = False
current_framework = []
def compute_labelling(all_relations, all_args):
    global candidate_labellings, labelling_to_dos, lock, current_framework
    candidate_labellings = []
    # start by labelling all arguments as IN
    init_labelling = (set(),set(),set())

    for arg in all_args:
        init_labelling[0].add(arg)

    find_labellings(deepcopy(init_labelling), all_relations, 0)

    while labelling_to_dos:
        labelling_to_dos = remove_duplicates(labelling_to_dos)
        next_labelling = labelling_to_dos.pop(0)
        next_labelling = (next_labelling)
        framework = next_labelling[0]
        params = next_labelling[1]
        # if no super illegal arguments, add to candidates
        if not params:
            add_to_candidate_labellings(framework)

        for x in params:
            find_labellings(deepcopy(framework), all_relations, x)

    print("Number of preferred labellings found:")
    print(len(candidate_labellings))
    all_labellings = []
    for l in candidate_labellings:
        output = (l[0], l[1], l[2])
        print(output)
        all_labellings.append(output)

    args_to_remove = []
    for i in all_labellings:
        for j in all_labellings:
            if j[0] < i[0] and j not in args_to_remove:
                args_to_remove.append(j)

    for k in args_to_remove:
        all_labellings.remove(k)

    return all_labellings


def find_labellings(Lab, all_relations, x):
    global candidate_labellings, labelling_to_dos
    # each labelling is of the format (in_args, out_args, undec_args)

    if check_if_legally_in(Lab, all_relations):

        for labelling in candidate_labellings:
            if labelling[0] < Lab[0]:
                print("REMOVAL OF ")
                print(labelling)
                candidate_labellings.remove(labelling)

        add_to_candidate_labellings(Lab)

        print("labelling added")
        print("===================")
    else:
        if check_if_super_illegal(Lab, all_relations):
            xset = get_all_super_illegally_in_args(Lab, all_relations)

            ins = Lab[0]
            outs = Lab[1]
            undecs = Lab[2]
            print((ins, outs, undecs))

            for x in xset:
                transition_step(deepcopy(Lab), all_relations, x)

        else:
            illegal_ins = get_all_illegally_in_args(Lab, all_relations)
            for y in illegal_ins:
                transition_step(deepcopy(Lab), all_relations, y)



def check_if_legally_in(L, all_relations):
    for a,b in all_relations:
        # if b is in and a is not out then b is ILLEGALLY in
        if b in L[0] and not a in L[1]:
            return False
    return True

def check_if_legally_out(L, all_relations, arg):
    for a,b in all_relations:
        if b == arg:
            if b in L[1] and a in L[0]:
                return True
    return False

def check_if_super_illegal(L, all_relations):
    for a,b in all_relations:
            if b in L[0]:
                if a in L[0] or a in L[2]:
                    return True
    return False

def get_super_illegal_argument(L, all_relations):
    for a,b in all_relations:
            if b in L[0]:
                if a in L[0] or a in L[2]:
                    return b

def get_all_super_illegally_in_args(L, all_relations):
    super_illegal_ins = set()
    for a,b in all_relations:
        if b in L[0]:
            if a in L[0] or a in L[2]:
                super_illegal_ins.add(b)

    return super_illegal_ins

def get_all_illegally_in_args(L, all_relations):
    illegal_ins = set()
    for a,b in all_relations:
        # if b is in and a is not out then b is ILLEGALLY in
        if b in L[0] and not a in L[1]:
            illegal_ins.add(b)
    return illegal_ins

# add arg to out args, remove arg from in args
def transition_step(L, all_relations, arg):
    global labelling_to_dos
    
    print("enter transition step with arg: " + str(arg))
    L[0].remove(arg)
    L[1].add(arg)
    y = set()
    y.add(arg)
    # gather every argument attacked by arg
    for a,b in all_relations:
        if a == arg:
            y.add(b)
    # check if the attacked arguments are illegally out
    for ar in y:
        if ar in L[1]:
            if not check_if_legally_out(L, all_relations, ar):
                L[1].remove(ar)
                L[2].add(ar)
    print("New L after transition: ")
    print((L[0], L[1], L[2]))
    # find_labellings(L, all_relations, 0)
    xset = get_all_super_illegally_in_args(L, all_relations)
    labelling_to_dos.append((deepcopy(L), xset))
    return
