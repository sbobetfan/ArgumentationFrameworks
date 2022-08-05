def compute_labelling(all_relations, all_args):
    print(all_relations)
    in_args = set()
    out_args = set()

    count = 1
    while True:
        print("Count: " + str(count))
        x = len(in_args)
        y = len(out_args)
        tmp_ins = set()
        tmp_outs = set()

        # IN ARGUMENTS:
        for arg in all_args:
            attackers = set()
            labelled_args = in_args.union(out_args)
            if arg not in labelled_args:
                for n, p in all_relations:
                    if p == arg:
                        attackers.add(n)
                if len(attackers) == 0:
                    tmp_ins.add(arg)
                if len(attackers) > 0:
                    if attackers.issubset(out_args):
                        tmp_ins.add(arg)

        # OUT ARGUMENTS
        for arg in all_args:
            attackers = set()
            labelled_args = in_args.union(out_args)
            if arg not in labelled_args:
                for n, p in all_relations:
                    if p == arg:
                        attackers.add(n)
                for att in attackers:
                    if att in tmp_ins:
                        tmp_outs.add(arg)


        count+=1
        in_args |= tmp_ins
        out_args |= tmp_outs
        print("IN Arguments: " + str(in_args))
        print("OUT Arguments: " + str(out_args))

        # if unchanged at end of iteration
        if x == len(in_args) and y == len(out_args):
            break

    undec_args = all_args-(in_args.union(out_args))
    print("UNDEC Arguments: " + str(undec_args))
    print("Grounded Labelling: (" + str(in_args) + ", " + str(out_args) + ", " + str(undec_args) + ")")
    labelling = [(in_args, out_args, undec_args)]
    return labelling
