import * as types from "./types";

export const increment = () => {
  return {
    type: types.INCREMENT,
  };
};

export const setMode = (mode: "normal" | "proposed") => {
  return {
    payload: { mode },
    type: types.SET_MODE,
  };
};
