import * as types from "./types";

export const increment = () => {
  return {
    type: types.INCREMENT,
  };
};

export const reset = () => {
  return {
    type: types.RESET,
  };
};

export const setMode = (mode: "normal" | "proposal") => {
  return {
    payload: { mode },
    type: types.SET_MODE,
  };
};

export const setDirection = (direction: "column" | "row") => {
  return {
    payload: {direction},
    type: types.SET_DIRECTION,
  };
};
