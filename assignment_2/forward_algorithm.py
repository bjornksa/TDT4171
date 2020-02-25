import numpy as np

def forward(T, O, f):
    """ Calculate next forward message from Transition model T, Sensor model O and previous f """

    f_next = O*T.getT()*f # Calculate next f
    f_next = f_next / np.sum(f_next) # Normalize vector
    return f_next


def forward_filtering(evidence):
    """ Run forward smoothing for all timesteps with given evidence """

    timesteps = len(evidence) + 1

    forward_messages = [np.matrix("0.0; 0.0") for i in range((timesteps))]
    forward_messages[0] = np.matrix("0.5; 0.5")

    transition_matrix = np.matrix("0.7 0.3; 0.3 0.7")
    sensor_matrix = np.matrix("0.9 0.0; 0.0 0.2")

    for i in range(1, timesteps):
        if evidence[i-1]:
            O = sensor_matrix
        else:
            O = 1 - sensor_matrix

        forward_messages[i] = forward(transition_matrix, O, forward_messages[i-1])

    return forward_messages


def main():
    evidence1 = [1, 1]
    evidence2 = [1, 1, 0, 1, 1, 1]

    P_R_2 = forward_filtering(evidence1)
    P_R_5 = forward_filtering(evidence2)

    print(P_R_2[-1])
    """ Gives <0.883, 0.117>: 88.3% chance of rain"""

    for f in P_R_5:
        print("<{0:.3f}, {1:.3f}>".format(f[0,0], f[1,0])) #print the rounded forward messages on the form <0.xxx, 0.yyy>
    """ Gives the following output
    <0.5, 0.5>
    <0.818, 0.182>
    <0.883, 0.117>
    <0.307, 0.693>
    <0.767, 0.233>
    <0.874, 0.126>
    <0.893, 0.107>
    """

main()



