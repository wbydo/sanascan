import * as types from "./types";

export const toggleTimer = () => {
  return {
    type: types.TOGGLE_TIMER,
  };
};

export const toggleEstimator = () => {
  return {
    type: types.TOGGLE_ESTIMATOR,
  };
};
