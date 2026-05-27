def get_device(device='raspberry_pi_zero_2w'):
    profiles={
      'raspberry_pi_zero_2w':{'mode':'lite','parallel':1},
      'raspberry_pi_5':{'mode':'standard','parallel':4}
    }
    return profiles.get(device,profiles['raspberry_pi_zero_2w'])
