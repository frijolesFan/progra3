
        for value in domain:
            conflicts = 0
            #cuenta cuántas variables relacionadas tienen este valor en su dominio
            for constraint in const:
                if var_to_assign in constraint:
                    for other_var in constraint:
                        if other_var != var_to_assign and value in Vars[other_var]:
                            conflicts += 1
            value_scores.append((value, conflicts))