The install-over-a-running-binary test retries its own spawn on ETXTBSY (a sibling fork race, 1 in 80 parallel runs); install code unchanged.
