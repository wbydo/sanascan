import * as types from "./types";

export const setActive = (isActive: boolean) => {
  return {
    error: false,
    payload: { isActive },
    type: types.SET_ACTIVE,
  };
};

export const setEstimatorActivity = (estimatorIsActive: boolean) => {
  return {
    error: false,
    payload: { estimatorIsActive },
    type: types.SET_ESTIMATOR_ACTIVITY,
  };
};

export const setTimerActivity = (timerIsActive: boolean) => {
  return {
    error: false,
    payload: { timerIsActive },
    type: types.SET_TIMER_ACTIVITY,
  };
};
