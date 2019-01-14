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
