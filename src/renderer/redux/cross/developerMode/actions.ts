import * as types from "./types";

export const toggle = () => {
  return {
    type: types.TOGGLE,
  };
};

export const toggleTimer = () => {
  return {
    type: types.TOGGLE_TIMER,
  };
};
