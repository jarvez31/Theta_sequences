import random
from shapely.geometry import LineString, LinearRing, box, Point, Polygon
import matplotlib.pyplot as plt
import pickle
import numpy as np

sq1_env = box(-0.1, -0.5, 1.1, 0.5)
k1_env = list(sq1_env.exterior.coords)
env = [[m[0] for m in k1_env ], [m[1] for m in k1_env ]]

# params to choose from
steps = [2000, 1000, 1500] # steps to be chosen from for stopping and moving 
dt = 0.002  # sampling rate
speed_lis = [0.4, 0.2, 0.6] # list for multiple speeds

v = []
cyclen = [0]
n_steps = 0
t_len = 1
num_cycles = 30

for i in range(num_cycles):
    sum_v = 0
    while sum_v <= t_len:
        st2 = random.choice(steps)
        s_temp2 = [0]*st2
        st = random.choice(steps)
        speed = random.choice(speed_lis)
        s_temp = [speed]*st
        sum_v = sum_v + speed*st*dt
        v = v + s_temp2 + s_temp
        n_steps = n_steps + st + st2
    diff = int((sum_v - t_len)/(speed*dt))
    # print(diff)
    if diff != 0:
        del v[-1*(diff+1):-1]
    st2 = random.choice(steps)
    s_temp2 = [0]*st2
    v = v + s_temp2
    n_steps = n_steps + st2 - diff
    # print(sum_v)
    sum_v = t_len

    while sum_v>=0:
        st2 = random.choice(steps)
        s_temp2 = [0]*st2
        st = random.choice(steps)
        speed = random.choice(speed_lis)
        s_temp = [-1*speed]*st
        sum_v = sum_v - speed*st*dt
        v = v + s_temp2 + s_temp
        n_steps = n_steps + st + st2 
    diff = int(sum_v/(dt*speed))
    if diff != 0:
        del v[diff-1:-1]

    st2 = random.choice(steps)
    s_temp2 = [0]*st2
    v = v + s_temp2
    n_steps = n_steps + st2 - abs(diff)
    # cyclen.append(n_steps)
    cyclen.append(len(v))
    # print(sum_v)

x = [] 
x0 = 0
for i in v:
    x0 = x0 + i*dt
    x.append(x0)
plt.plot(range(len(v)), x[-len(v):])
plt.show()
y = [0]*len(x) # n variance


vel = []
speed = []
for i in range(1,len(x)):
    v0 = np.sqrt(((x[i] - x[i-1])**2) + ((y[i] - y[i-1])**2))/dt
    v1 = x[i] - x[i-1]
    speed.append(v0)
    vel.append(v1)
plt.plot(range(len(vel)), vel)
plt.suptitle("velocity profile")
plt.show()

theta_real_deg = [0]*len(vel)
for i in range(len(theta_real_deg)):
    if x[i+1]-x[i]<0:
        theta_real_deg[i] = 180
    elif x[i+1]-x[i]>0:
        theta_real_deg[i] = 0
    else:
        theta_real_deg[i] = theta_real_deg[i-1]

plt.scatter(range(len(theta_real_deg)), theta_real_deg)

plt.show()
pos = np.column_stack((np.asarray(x), np.asarray(y)))
traj_name = "traj_1.pk1"
d = {'x':list(x), 'y':list(y), 'speed':list(speed), 'vel':vel, 'theta': list(theta_real_deg), 'env': env, 'pos':pos, "cyclen":cyclen} #, 'obj': small_box}
with open(traj_name, 'wb') as f:
    pickle.dump(d, f)
