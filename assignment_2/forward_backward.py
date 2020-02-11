import numpy as np

def forward(T, O, f):
    """ Calculate next forward message from Transition model T, Sensor model O and previous f """

    f_next = O*T.getT()*f # Calculate next f
    f_next = f_next / np.sum(f_next) # Normalize vector
    return f_next

def backward(T, O, b):
    """ Calculate previous backward message from T, O and current b"""
    b_prev = T*O*b
    return b_prev


def forward_backward(evidence, prior):

    transition_matrix = np.matrix("0.7 0.3; 0.3 0.7")
    sensor_matrix = np.matrix("0.9 0.0; 0.0 0.2")

    # initialize local variables
    timesteps = len(evidence) + 1
    forward_messages = [np.matrix("0.0; 0.0") for i in range(timesteps)]
    backward_messages = [np.matrix("1.0; 1.0") for i in range(timesteps)]
    smoothed_estimates = [np.matrix('0.0; 0.0') for i in range(timesteps)]

    forward_messages[0] = prior
    backward_message = np.matrix("1.0; 1.0")

    eye = np.identity(2)
    for i in range(1, timesteps):
        # Forwad smoothing
        if evidence[i-1]:
            O = sensor_matrix
        else:
            O = eye - sensor_matrix
        forward_messages[i] = forward(transition_matrix, O, forward_messages[i-1])

    for i in range(timesteps - 1, 0, -1):
        # Backward smoothing
        smoothed_estimates[i] = np.multiply(forward_messages[i],backward_message)
        smoothed_estimates[i] = smoothed_estimates[i] / np.sum(smoothed_estimates[i]) # Normalize
        if evidence[i-1]:
            O = sensor_matrix
        else:
            O = eye - sensor_matrix
        backward_message = backward(transition_matrix, O, backward_message)
        backward_messages[i] = backward_message

    return smoothed_estimates, forward_messages, backward_messages


def main():
    evidence = [1, 1, 0, 1, 1]
    prior = np.matrix("0.5; 0.5")

    estimates, forwards, backwards = forward_backward(evidence, prior)
    print("Estimates:")
    for f in estimates:
        print("<{0:.3f}, {1:.3f}>".format(f[0,0], f[1,0])) #print the rounded forward messages on the form <0.xxx, 0.yyy>

    print("\nForward messages:")
    for f in forwards:
        print("<{0:.3f}, {1:.3f}>".format(f[0,0], f[1,0])) #print the rounded forward messages on the form <0.xxx, 0.yyy>

    print("\nBackward messages:")
    for f in backwards:
        print("<{0:.3f}, {1:.3f}>".format(f[0,0], f[1,0])) #print the rounded forward messages on the form <0.xxx, 0.yyy>


main()
