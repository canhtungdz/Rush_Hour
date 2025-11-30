import vehicle, solver, pygame, threading, copy


class Vehicles:
    def __init__(self, size_game):
        self.vehicles = {

        }
        self.size_game = size_game
        self.moved = []
        self.cells = [[0] * size_game for _ in range(size_game)]
        self.solution = []
        self.hint_mode = False
        self.calculating = False



    def add_vehicle(self, size,versus,initial):
        if self.check_add_vehicle_valid(size, versus, initial):
            self.vehicles[len(self.vehicles) + 1] = vehicle.Vehicle(size,versus,initial)
        self.update_cells()

    def check_add_vehicle_valid(self, size, versus, initial):
        if not (0 <= abs(versus) <= self.size_game and 0 <= initial <= self.size_game and abs(initial) + size - 1 <= self.size_game):
            return False
        if versus > 0:
            for col in range(initial, initial + size):
                if self.cells[versus - 1][col - 1] != 0:
                    return False
            return True
        else:
            for row in range(initial, initial + size ):
                if self.cells[row - 1][-versus - 1] != 0:
                    return False
            return True
    def len(self):
        return len(self.vehicles)

    def get_vehicle(self, index):
        return self.vehicles.get(index)
    
    def check_move_valid(self, vehicle, step):
        pos_last = self.vehicles[vehicle].get_pos_last()
        size_vehicle = self.vehicles[vehicle].size
        versus_vehicle = self.vehicles[vehicle].versus
        
        if versus_vehicle > 0:
            if step > 0:
                if pos_last + size_vehicle - 1 + step > self.size_game:
                    return False
                for col_cell in range(pos_last + size_vehicle, pos_last + size_vehicle + step):
                    if not self.cells[versus_vehicle - 1][col_cell - 1] == 0:
                        return False
                return True
            else:
                if pos_last + step < 1:
                    return False
                for col_cell in range(pos_last + step, pos_last):
                    if not self.cells[versus_vehicle - 1][col_cell - 1] == 0:
                        return False
                return True
        else :
            if step > 0:
                if pos_last + size_vehicle - 1 + step > self.size_game:
                    return False
                for row_cell in range(pos_last + size_vehicle, pos_last + size_vehicle + step):
                    if not self.cells[row_cell - 1][-versus_vehicle - 1] == 0:
                        return False
                return True
            else :
                if pos_last + step < 1:
                    return False
                for row_cell in range(pos_last + step, pos_last):
                    if not self.cells[row_cell - 1][-versus_vehicle - 1] == 0:
                        return False
                return True

    def move(self,vehicle, step):
        if self.check_move_valid(vehicle, step):
            self.vehicles[vehicle].add_move(step)
            self.moved.append(vehicle)
            self.update_cells()
            
            if getattr(self, 'solution', None):
                next_move = self.solution[0]
                # Check if the move matches the vehicle in the hint
                if next_move[0] == vehicle:
                    # Calculate remaining steps needed
                    # next_move[1] is the total steps in the hint
                    # step is the steps just moved
                    
                    # We need to be careful about direction.
                    # If hint is +2, and we moved +1, remaining is +1.
                    # If hint is -2, and we moved -1, remaining is -1.
                    # If hint is +2, and we moved -1 (wrong direction), remaining is +3? 
                    # Or should we just strictly follow the hint.
                    
                    # Let's assume the user is trying to follow the hint.
                    remaining = next_move[1] - step
                    
                    if remaining == 0:
                        self.solution.pop(0)
                    else:
                        # Update the hint with remaining steps
                        self.solution[0] = (vehicle, remaining)
                else:
                    # User moved a different vehicle.
                    # Do NOT clear the solution. Keep the hint for the correct vehicle.
                    pass

    def update_cells(self):
        self.cells = [[0] * self.size_game for _ in range(self.size_game)]
        for vehicle_name in self.vehicles.keys():
            vehicle = self.vehicles.get(vehicle_name)
            if vehicle.versus > 0:
                for col_cell in range(vehicle.get_pos_last(), vehicle.get_pos_last() + vehicle.size):
                    self.cells[vehicle.versus - 1][col_cell - 1] = vehicle_name
            else :
                for row_cell in range(vehicle.get_pos_last(), vehicle.get_pos_last() + vehicle.size):
                    self.cells[row_cell - 1][-vehicle.versus - 1] = vehicle_name

    #reset
    def restart_game(self):
        for vehicle in self.vehicles.values():
            vehicle.reset_vehicle()
        self.update_cells()
        self.reset_hints()

    def reset_game(self):
        self.vehicles.clear()
        self.update_cells()
        self.reset_hints()

    def reset_hints(self):
        self.solution = []
        self.hint_mode = False
        self.calculating = False

    def pop_last_vehicle(self):
        if len(self.vehicles) > 0:
            self.vehicles.popitem()

    def back_move(self):
        if len(self.moved) > 0:
            self.vehicles[self.moved.pop()].back_move()
            self.update_cells()

    def solve(self):
        self.hint_mode = True
        self.calculate_solution(silent=False)

    def calculate_solution(self, silent=False):
        if getattr(self, 'calculating', False):
            return
            
        self.calculating = True
        # Create a deepcopy of self to pass to the thread
        # We only need the essential state for the solver
        # But Vehicles object might be complex to deepcopy if it has pygame surfaces etc.
        # Luckily Vehicles seems to only have data.
        
        # However, deepcopying 'self' might be risky if it has references to other things.
        # Let's try to deepcopy. If it fails (like before), we might need a lighter copy.
        # The previous RecursionError was likely due to self.solution containing reference to something or just depth.
        # We cleared self.solution before solving, which helped.
        
        # We need to pass a state that the solver can use.
        # The solver takes a 'state' object which is a Vehicles instance.
        
        try:
            # Create a lightweight copy or just deepcopy if safe
            # To be safe, let's clear solution on the copy or just pass self and be careful?
            # No, passing self to thread is bad because main thread modifies it.
            
            # Let's try deepcopying but ensure we don't copy unnecessary things.
            # Actually, we can just create a new Vehicles object and populate it.
            pass
        except:
            pass
            
        thread = threading.Thread(target=self._run_solver, args=(silent,))
        thread.start()

    def _run_solver(self, silent):
        # We need a snapshot of the current state.
        # Since deepcopy might be unstable, let's manually reconstruct the state for the solver.
        # Solver needs: size_game, vehicles (with positions).
        
        try:
            # Create a dummy state object for the solver
            state_copy = Vehicles(self.size_game)
            state_copy.vehicles = copy.deepcopy(self.vehicles)
            state_copy.update_cells()
            
            sol = solver.RushHourSolver(state_copy)
            solution = sol.solver()
            
            if solution is None:
                if not silent:
                    print("No solution")
                self.solution = []
            else:
                if not silent:
                    print("Steps: ", len(solution))
                self.solution = solution
        except Exception as e:
            print(f"Solver thread error: {e}")
        finally:
            self.calculating = False

    def update(self):
        pass
