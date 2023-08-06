# Gym-style API

The domanin features a continuos state and a dicrete action space.

The environment initializes:
- cross-sectional dataset with variables X_a, X_s, Y and N observations;
- logit model fitted on the dataset, retrieving parameters \theta_0, \theta_1, \theta_2;

The agent: 
- sees all patients;
- predict risk of admission \rho, using initialized parameters
- sample an action (50 possible values between -2 and 2)
- if risk > 0.2:
  - replace Xa by g, where g(\rho, Xa) is obtained using the patient's risk and Xa value
- else:
  - do not intervene, X_a stays the same
- give reward equal to average risk of admission, using predicted Y, initial parameters and sampled values


# To install
- git clone https://github.com/claudia-viaro/gym-discrete.git
- cd gym-discrete

- !pip install gym-discrete
- import gym_discrete
- env =gym.make('discrete-v0')

# To change version
- change version to, e.g., 1.0.7 from setup.py file
- git clone https://github.com/claudia-viaro/gym-discrete.git
- cd gym-discrete
- python setup.py sdist bdist_wheel
- twine check dist/*
- twine upload --repository-url https://upload.pypi.org/legacy/ dist/*
