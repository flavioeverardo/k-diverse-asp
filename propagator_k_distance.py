#script(python)
import clingo
"""
Get answer sets with distance k during propagation.
"""

""" Distance """
def distance(l1, l2):
    l3 = list(set(l1) & set(l2)) # Intersect
    l4 = list(set(l1)-set(l3))   # Difference
    l5 = list(set(l2)-set(l3))   # Difference
    return len(l4)+len(l5)

class Propagator:
    def __init__(self, k):
        self.__answers  = []        
        self.__states   = []
        self.__partial  = []
        self.__literals = []
        self.__k = k

    """
    Init Method 
    """
    def init(self, init):
        Propagator.__max_dist = 0
        init.check_mode = clingo.PropagatorCheckMode.Total
        
        for thread_id in range(len(self.__states), init.number_of_threads):
            self.__answers.append([])
            self.__states.append([])
            self.__partial.append([])

            for atom in init.symbolic_atoms:
                lit = init.solver_literal(atom.literal)
                value = init.assignment.value(lit)
                if lit not in self.__states[thread_id] and init.assignment.value(lit) is None:
                    init.add_watch( lit)
                    init.add_watch(-lit)
                    self.__states[thread_id].append(lit)
                    self.__literals.append(lit)
        print("number of unassigned literals: %s"%len(self.__literals))

    """
    Propagate method and calculate distances on partial assignments
    """
    def propagate(self, control, changes):
        answers  = self.__answers[control.thread_id]
        state    = self.__states[control.thread_id]
        partial  = self.__partial[control.thread_id]
        k        = self.__k        
        diverse  = True

        if answers:        
            for lit in changes:
                value = control.assignment.value(abs(lit))
                if value is True and abs(lit) not in partial:
                    partial.append(abs(lit))
                    state.remove(abs(lit))
                    
            for assignment in answers:
                if assignment != partial:
                    d = distance(assignment, partial)
                if d > Propagator.__max_dist:
                    Propagator.__max_dist = d
                if d < k:
                    diverse = False
                    false_lits = list([-x for x in state])
                    if not control.add_nogood(partial+false_lits):
                        return
            if diverse:
                if partial not in answers:
                    answers.append(list(partial))

    """
    Undo method to update state
    """
    def undo(self, thread_id, assignment, undo):
        state    = self.__states[thread_id]
        partial  = self.__partial[thread_id]

        for lit in undo:
            if abs(lit) not in state and abs(lit) in partial:
                partial.remove(abs(lit))
                state.append(abs(lit))

    """
    Check Method just to get the first answer set. No other functionalities implemented here
    """
    def check(self, control):
        answers  = self.__answers[control.thread_id]
        state    = self.__states[control.thread_id]
        partial  = self.__partial[control.thread_id]
        literals = sorted(self.__literals)

        if not answers:
            for lit in literals:
                value = control.assignment.value(lit)
                if value:
                    state.remove(lit)
                    partial.append(lit)
            answers.append(list(partial))            
        
def main(control):
    models = []
    total = 0
    k = int(str(control.get_const("k")))
    v = False
    if str(control.get_const("v")) == "true":
        v = True
    control.ground([("base", [])])    
    control.register_propagator(Propagator(k))

    if v:
        control.solve(None, lambda model: models.append(model.symbols(shown=True)))
    else:
        control.solve()
    
    d = Propagator._Propagator__max_dist
    print ""
    print "Max distance between two answer sets:", d

    if v:
        print ""
        for i in range(len(models)):
            for j in range(i+1,len(models)):
                partial = distance(models[i], models[j])
                print "Distance between %s and %s = %s"%(models[i], models[j], partial)
                total += partial
        print "Total distance: %s"%total

#clingo k-distance.py test3.lp --sign-def=rnd --sign-fix --rand-freq=1 --seed=$RANDOM --enum-mode=record 0 -c k=3 -c n=15 -c v=true
#end.
%
#const k=2.
#const v="False".
