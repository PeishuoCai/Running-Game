# running for 180 mins straight = 180*3 health, else +1
# textbook = 2 health/min
# resting = no hedon gain
# if tired: running and textbook = -2 hedon
# if not tired: running = +2 hedon for first 10 mins, -2 for after 10 mins, textbook = +1 for first 20 mins, -1 for after 20 mins
# if star, then same activity +3 hedon for 10 mins, if switch or restart, +0 hedon
# if 3 star in 2 hours, +0 hedon


def initialize():
    '''Initializes the global variables needed for the simulation.
    Note: this function is incomplete, and you may want to modify it'''
    global cur_hedons, cur_health
    global cur_star
    global cur_star_activity
    global bored_with_stars
    global activity_done

    cur_hedons = 0
    cur_health = 0
    cur_star = True
    cur_star_activity = ""
    bored_with_stars = False
    activity_done = []


def check_tired():
    '''this functions checks if the player is tired. If yes, it returns True, if no, it returns False'''
    if len(activity_done) <= 120:
        if activity_done.count("resting") + activity_done.count("resting*") +  activity_done.count("*")== len(activity_done):
            return False
        return True
    elif activity_done[-120:].count("resting") + activity_done[-120:].count("resting*") + activity_done[-120:].count("*")== 120:
        return False
    elif len(activity_done) == 0:
        return False
    return True



def star_can_be_taken(activity):
    global cur_star
    if len(activity_done) <= 120 and activity_done.count("running*") + activity_done.count("resting*") + activity_done.count("textbooks*") + activity_done.count("*") >= 3 or len(activity_done) >= 120 and activity_done[-120:].count("running*") + activity_done[-120:].count("resting*") + activity_done[-120:].count("textbooks*") + activity_done[-120:].count("*") >= 3:
        cur_star = False
        return False
    elif len(activity_done) == 0:
        return False
    elif (activity_done[-1] == "resting*" or activity_done[-1] == "textbooks*" or activity_done[-1] == "running*" or activity_done[-1] == "*") and cur_star_activity == activity:
        return True
    return False


def perform_activity(activity, duration):
    global activity_done
    global cur_hedons
    global cur_health

    cur_hedons += estimate_hedons_delta(activity, duration) + use_star(activity, duration)
    cur_health += estimate_health_delta(activity, duration)
    activity_done.extend(activity for i in range(duration))


def use_star(activity, duration):
    if star_can_be_taken(activity) and cur_star:
        if duration < 10:
            return duration*3
        else:
            return 30
    return 0

def estimate_hedons_delta(activity, duration):
    if activity == "resting":
        return 0
    if not check_tired():
        if activity == "running":
            if duration <= 10:
                return duration*2
            return (20 - (duration-10)*2)
        else:
            if duration <= 20:
                return duration
            return (20 - (duration-20))
    else:
        return (duration*(-2))

def estimate_health_delta(activity, duration):
    if activity == "resting":
        return 0
    if activity == "running":
        if check_tired():
            if activity_done[-1] == "running" or activity_done[-1] == "running*":
                n_count = 0
                while activity_done[-(n_count + 1)] == "running" or activity_done[-(n_count + 1)] == "running*":
                    n_count += 1
                    if n_count == len(activity_done):
                        break
                duration_in_a_row = duration + n_count
            else:
                duration_in_a_row = duration
                n_count = 0
            if duration_in_a_row <= 180:
                return duration*3
            elif duration_in_a_row > 180 and n_count >= 180:
                return duration
            elif duration_in_a_row > 180 and n_count < 180:
                return ((180 - n_count)*3 + duration-(180-n_count))
            return (180*2 + duration)
        elif duration <= 180:
            return duration*3
        return (180*2 + duration)
    if activity == "textbooks":
        return duration*2


def get_cur_hedons():
    return cur_hedons

def get_cur_health():
    return cur_health

def offer_star(activity):
    global activity_done
    global cur_star_activity
    cur_star_activity = activity
    if len(activity_done) != 0:
        activity_done[-1] += "*"
    else:
        activity_done.append("*")

def most_fun_activity_minute():
    running = estimate_hedons_delta("running", 1) + use_star("running", 1)
    textbooks = estimate_hedons_delta("textbooks", 1) + use_star("textbooks", 1)
    resting = 0
    activity = [running, "running", textbooks, "textbooks", resting, "resting"]
    most_fun = max(running, textbooks, resting)
    for i in range (3):
        if activity[2*i] == most_fun:
            return activity[2*i+1]


if __name__ == '__main__':
    initialize()
    perform_activity("running", 30)
    print(get_cur_hedons())            #-20 = 10 * 2 + 20 * (-2)
    print(get_cur_health())            #90 = 30 * 3
    print(most_fun_activity_minute())  #resting
    perform_activity("resting", 30)
    offer_star("running")
    print(most_fun_activity_minute())  #running
    perform_activity("textbooks", 30)
    print(get_cur_health())            #150 = 90 + 30*2
    print(get_cur_hedons())            #-80 = -20 + 30 * (-2)
    offer_star("running")
    perform_activity("running", 20)
    print(get_cur_health())            #210 = 150 + 20 * 3
    print(get_cur_hedons())            #-90 = -80 + 10 * (3-2) + 10 * (-2)
    perform_activity("running", 170)
    print(get_cur_health())            #700 = 210 + 160 * 3 + 10 * 1
    print(get_cur_hedons())            #-430 = -90 + 170 * (-2)

