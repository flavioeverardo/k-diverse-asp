#script(python)
import clingo
"""
Get answer sets with distance k on fixpoints
"""

""" Distance """
def distance(l1, l2):
    l3 = list(set(l1) & set(l2)) # Intersect
    l4 = list(set(l1)-set(l3))   # Difference
    l5 = list(set(l2)-set(l3))   # Difference
    return len(l4)+len(l5)

class Propagator:
    def __init__(self, k):
        self.__states = []
        self.__literals = []
        self.__k = k

    """
    Init Method 
    """
    def init(self, init):
        Propagator.__max_dist = 0
        init.check_mode = clingo.PropagatorCheckMode.Fixpoint
        
        for thread_id in range(len(self.__states), init.number_of_threads):
            self.__states.append([])

        for atom in init.symbolic_atoms:
            lit = init.solver_literal(atom.literal)
            value = init.assignment.value(lit)
            if lit not in self.__literals and init.assignment.value(lit) is None:
                self.__literals.append(lit)
        print("number of unassigned literals: %s"%len(self.__literals))

    """
    Check Method and calculate distances on partial assignments (fixpoints)
    """            
    def check(self, control):
        state = self.__states[control.thread_id]
        literals = sorted(self.__literals)
        k = self.__k
        false_lits = []
        total_assignment = True
        diverse = True
        
        if not state:
            ## Check assignments
            answer = []
            for lit in literals:
                value = control.assignment.value(lit)
                if value is True:
                    if lit not in answer:
                        answer.append(lit)
                elif value is None:
                    total_assignment = False
                    break
            if answer not in state and total_assignment:
                state.append(answer)
       
        else:
            answer = []
            ## Check assignments
            for lit in literals:
                value = control.assignment.value(lit)
                if value is True:
                    if lit not in answer:
                        answer.append(lit)
                elif value is False or value is None:
                    if lit not in false_lits:
                        false_lits.append(-lit)
            
            ## If an answer set is already given
            if state:
                for assignment in state:
                    if assignment != answer:
                        d = distance(assignment, answer)
                        if d > Propagator.__max_dist:
                            Propagator.__max_dist = d
                        if d < k:
                            diverse = False
                            if not control.add_nogood(answer+false_lits):
                                return
                if diverse:
                    if answer not in state:
                        state.append(list(answer))

def main(control):
    models = []
    total = 0
    k = int(str(control.get_const("k")))
    control.ground([("base", [])])
    control.register_propagator(Propagator(k))

    control.solve(None, lambda model: models.append(model.symbols(shown=True)))

    d = Propagator._Propagator__max_dist
    print("")
    print("Max distance between two answer sets: %s"%d)

    print("")
    for i in range(len(models)):
        for j in range(i+1,len(models)):
            partial = distance(models[i], models[j])
            print("Distance between %s and %s = %s"%(models[i], models[j], partial))
            total += partial
    print("Total distance: %s"%total) 
#end.
%
#const k=2.
