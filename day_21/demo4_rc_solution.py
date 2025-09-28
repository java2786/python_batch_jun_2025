# lic policies
import threading
import time

# Global counter
# Shared resource
policy_counter = 0
counter_lock = threading.Lock()

# process agents task to increase policies
def process_lic_policiy(agent_name, policies_to_process):
    global policy_counter
    
    for i in range(policies_to_process):
        print(f"Agent {agent_name}: Processing policy {i+1}")
        
        
        # synchronised ->         
        with counter_lock:
            # Here race condition will occur
            current_count = policy_counter # read current value of shared resource
            # processing is taking time -> context switch
            time.sleep(.5) # 1s = 1000ms
            policy_counter = current_count + 1 # update shared resource
            print(f"Agent {agent_name}: Total policies processed so far: {policy_counter}")

agents = ["Kamlesh", "Nitesh", "Hitesh"]
# policies_to_process -> 5, 5, 5 => 15

agent_threads = []
policy_count = 500

for agent in agents:
    thread = threading.Thread(target=process_lic_policiy, args=(agent, policy_count))
    agent_threads.append(thread)

for thread in agent_threads:
    # start all threads
    thread.start()
    
for thread in agent_threads:
    # wait for all threads to complete -> agent task to complete
    thread.join()

print("\n\n*************\n\n")
print(f"Executed total policies: {len(agents)*policy_count}") # policy_count*3
print(f"Actual proccessed policies: {policy_counter}") # ?
